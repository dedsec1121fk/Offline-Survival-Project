#!/usr/bin/env python3
"""Offline Survival Project local Command Center.

A zero-third-party-dependency local web interface for the bundled bilingual
survival database. It binds to localhost by default, performs no telemetry,
and stores user-created operational planning data locally under
~/.offline_survival_project/.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import mimetypes
import os
import platform
import random
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote, unquote, urlparse

PROJECT_ROOT = Path(__file__).resolve().parent
WEB_ROOT = PROJECT_ROOT / "web"
INDEX_FILE = WEB_ROOT / "index.html"
LIBRARY_ROOT = PROJECT_ROOT / "Offline Library"
STATE_DIR = Path.home() / ".offline_survival_project"
STATE_FILE = STATE_DIR / "user_state.json"
STATE_PREVIOUS_FILE = STATE_DIR / "user_state.previous.json"
SCHEMA_VERSION = 7
COMMAND_CENTER_VERSION = 7
MAX_POST_BYTES = 4_000_000
DEFAULT_PORT = 8765
KIWIX_PORT = 8766
LIBRARY_TEXT_SUFFIXES = frozenset({".txt", ".md", ".json", ".csv", ".log"})
LIBRARY_SEARCH_MAX_BYTES = 1_000_000

SCENARIOS: dict[str, dict[str, str]] = {
    "water": {"en": "safe drinking water boil water emergency", "el": "ασφαλές πόσιμο νερό βράσιμο νερού έκτακτη ανάγκη"},
    "power": {"en": "power outage electricity generator carbon monoxide food refrigerator", "el": "διακοπή ρεύματος γεννήτρια μονοξείδιο άνθρακα ψυγείο τρόφιμα"},
    "wildfire": {"en": "wildfire smoke evacuation fire", "el": "δασική πυρκαγιά καπνός εκκένωση φωτιά"},
    "flood": {"en": "flood flooded road water electricity evacuation", "el": "πλημμύρα πλημμυρισμένος δρόμος νερό ρεύμα εκκένωση"},
    "heat": {"en": "heat stroke extreme heat cooling dehydration", "el": "θερμοπληξία καύσωνας ψύξη αφυδάτωση"},
    "cold": {"en": "hypothermia cold exposure warming", "el": "υποθερμία έκθεση κρύο θέρμανση"},
    "injury": {"en": "bleeding wound injury first aid trauma", "el": "αιμορραγία τραύμα τραυματισμός πρώτες βοήθειες"},
    "food": {"en": "food safety power outage refrigerator freezer preservation", "el": "ασφάλεια τροφίμων διακοπή ρεύματος ψυγείο κατάψυξη διατήρηση"},
    "evacuation": {"en": "evacuation go bag documents route family reunification", "el": "εκκένωση σακίδιο ανάγκης έγγραφα διαδρομή οικογένεια επανένωση"},
    "communications": {"en": "emergency communications radio phone battery information", "el": "επικοινωνίες έκτακτης ανάγκης ραδιόφωνο τηλέφωνο μπαταρία πληροφορίες"},
    "shelter": {"en": "shelter emergency home safety sanitation", "el": "καταφύγιο έκτακτη ανάγκη σπίτι ασφάλεια υγιεινή"},
    "medicine": {"en": "medication continuity medicines storage chronic care", "el": "συνέχεια φαρμάκων αποθήκευση φαρμάκων χρόνια πάθηση"},
}

DEFAULT_STATE: dict[str, Any] = {
    "favorites": [],
    "notes": {},
    "checklist": {},
    "custom_checklist": [],
    "profile": {
        "adults": 1,
        "children": 0,
        "pets": 0,
        "days": 3,
        "water_liters": 0,
        "food_kcal": 0,
        "battery_wh": 0,
    },
    "inventory": [],
    "contacts": [],
    "incident_log": [],
    "risk_flags": [],
    "communications": {},
    "evacuation": {},
    "medical_card": {},
    "medications": [],
    "waypoints": [],
    "navigation": {},
    "documents": [],
    "maintenance": [],
    "roles": [],
    "drill_history": [],
    "continuity": {},
    "resource_plans": [],
    "checkins": [],
    "vehicles": [],
    "kits": [],
    "field_logs": [],
    "routes": [],
    "shelter_zones": [],
    "water_batches": [],
    "recovery_items": [],
    "skill_matrix": [],
    "decision_board": [],
    "food_lots": [],
    "sanitation_points": [],
    "power_loads": [],
    "comms_windows": [],
    "dependents": [],
    "expense_log": [],
    "knowledge_progress": [],
    "settings": {"low_power": False},
    "schema_version": SCHEMA_VERSION,
    "updated_at": "",
}

_KIWIX_PROCESS: subprocess.Popen[Any] | None = None
_KIWIX_LOCK = threading.Lock()
_INTEGRITY_LOCK = threading.Lock()
_INTEGRITY_CACHE: dict[str, Any] | None = None


def load_core() -> Any:
    path = PROJECT_ROOT / "Offline Survival.py"
    spec = importlib.util.spec_from_file_location("offline_survival_core", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load Offline Survival.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CORE = load_core()
DATABASE = CORE.OfflineDatabase()




def integrity_report_cached() -> dict[str, Any]:
    global _INTEGRITY_CACHE
    with _INTEGRITY_LOCK:
        if _INTEGRITY_CACHE is None:
            _INTEGRITY_CACHE = DATABASE.integrity_report()
        return _INTEGRITY_CACHE

def safe_json_read(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return default


def _clean_text(value: Any, limit: int) -> str:
    return str(value or "").strip()[:limit]


def _bounded_int(value: Any, default: int, minimum: int, maximum: int) -> int:
    try:
        return max(minimum, min(maximum, int(value)))
    except (TypeError, ValueError):
        return default


def _bounded_float(value: Any, default: float, minimum: float, maximum: float) -> float:
    try:
        number = float(value)
        if not math.isfinite(number):
            return default
        return max(minimum, min(maximum, number))
    except (TypeError, ValueError):
        return default


def _clean_date(value: Any) -> str:
    text = _clean_text(value, 10)
    if not text:
        return ""
    try:
        datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        return ""
    return text


def _clean_datetime(value: Any) -> str:
    text = _clean_text(value, 40)
    if not text:
        return ""
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return ""
    return text


def load_state() -> dict[str, Any]:
    saved = safe_json_read(STATE_FILE, {})
    if not isinstance(saved, dict):
        saved = {}
    # Run old and new state through one sanitizer so schema upgrades stay safe.
    try:
        return sanitize_state(saved)
    except ValueError:
        return sanitize_state({})


def sanitize_state(candidate: Any) -> dict[str, Any]:
    if not isinstance(candidate, dict):
        raise ValueError("State must be a JSON object")

    favorites = candidate.get("favorites", [])
    notes = candidate.get("notes", {})
    checklist = candidate.get("checklist", {})
    custom = candidate.get("custom_checklist", [])
    profile = candidate.get("profile", {})
    inventory = candidate.get("inventory", [])
    contacts = candidate.get("contacts", [])
    incident_log = candidate.get("incident_log", [])
    risk_flags = candidate.get("risk_flags", [])
    communications = candidate.get("communications", {})
    evacuation = candidate.get("evacuation", {})
    medical_card = candidate.get("medical_card", {})
    medications = candidate.get("medications", [])
    waypoints = candidate.get("waypoints", [])
    navigation = candidate.get("navigation", {})
    documents = candidate.get("documents", [])
    maintenance = candidate.get("maintenance", [])
    roles = candidate.get("roles", [])
    drill_history = candidate.get("drill_history", [])
    continuity = candidate.get("continuity", {})
    resource_plans = candidate.get("resource_plans", [])
    checkins = candidate.get("checkins", [])
    vehicles = candidate.get("vehicles", [])
    kits = candidate.get("kits", [])
    field_logs = candidate.get("field_logs", [])
    routes = candidate.get("routes", [])
    shelter_zones = candidate.get("shelter_zones", [])
    water_batches = candidate.get("water_batches", [])
    recovery_items = candidate.get("recovery_items", [])
    skill_matrix = candidate.get("skill_matrix", [])
    decision_board = candidate.get("decision_board", [])
    food_lots = candidate.get("food_lots", [])
    sanitation_points = candidate.get("sanitation_points", [])
    power_loads = candidate.get("power_loads", [])
    comms_windows = candidate.get("comms_windows", [])
    dependents = candidate.get("dependents", [])
    expense_log = candidate.get("expense_log", [])
    knowledge_progress = candidate.get("knowledge_progress", [])
    settings = candidate.get("settings", {})

    if not isinstance(favorites, list) or len(favorites) > 5000:
        raise ValueError("Invalid favorites")
    clean_favorites = [_clean_text(item, 180) for item in favorites if _clean_text(item, 180)]
    clean_favorites = list(dict.fromkeys(clean_favorites))

    if not isinstance(notes, dict) or len(notes) > 5000:
        raise ValueError("Invalid notes")
    clean_notes = {_clean_text(key, 180): str(value)[:12000] for key, value in notes.items() if _clean_text(key, 180) and str(value).strip()}

    if not isinstance(checklist, dict) or len(checklist) > 1000:
        raise ValueError("Invalid checklist")
    clean_checklist = {_clean_text(key, 180): bool(value) for key, value in checklist.items() if _clean_text(key, 180)}

    if not isinstance(custom, list) or len(custom) > 500:
        raise ValueError("Invalid custom checklist")
    clean_custom: list[dict[str, Any]] = []
    for item in custom:
        if not isinstance(item, dict):
            continue
        text = _clean_text(item.get("text"), 300)
        if text:
            clean_custom.append({"id": _clean_text(item.get("id"), 80) or f"custom-{len(clean_custom)+1}", "text": text, "done": bool(item.get("done", False))})

    if not isinstance(profile, dict):
        profile = {}
    clean_profile = {
        "adults": _bounded_int(profile.get("adults"), 1, 0, 50),
        "children": _bounded_int(profile.get("children"), 0, 0, 50),
        "pets": _bounded_int(profile.get("pets"), 0, 0, 50),
        "days": _bounded_int(profile.get("days"), 3, 1, 365),
        "water_liters": _bounded_float(profile.get("water_liters"), 0, 0, 1_000_000),
        "food_kcal": _bounded_float(profile.get("food_kcal"), 0, 0, 100_000_000),
        "battery_wh": _bounded_float(profile.get("battery_wh"), 0, 0, 10_000_000),
    }

    if not isinstance(inventory, list) or len(inventory) > 2000:
        raise ValueError("Invalid inventory")
    clean_inventory: list[dict[str, Any]] = []
    for item in inventory:
        if not isinstance(item, dict):
            continue
        name = _clean_text(item.get("name"), 160)
        if not name:
            continue
        clean_inventory.append({
            "id": _clean_text(item.get("id"), 80) or f"inventory-{len(clean_inventory)+1}",
            "name": name,
            "category": _clean_text(item.get("category"), 80),
            "qty": _bounded_float(item.get("qty"), 0, 0, 1_000_000_000),
            "unit": _clean_text(item.get("unit"), 40),
            "expiry": _clean_date(item.get("expiry")),
            "notes": _clean_text(item.get("notes"), 500),
        })

    if not isinstance(contacts, list) or len(contacts) > 250:
        raise ValueError("Invalid contacts")
    clean_contacts: list[dict[str, Any]] = []
    for item in contacts:
        if not isinstance(item, dict):
            continue
        name = _clean_text(item.get("name"), 120)
        if not name:
            continue
        clean_contacts.append({
            "id": _clean_text(item.get("id"), 80) or f"contact-{len(clean_contacts)+1}",
            "name": name,
            "role": _clean_text(item.get("role"), 100),
            "phone": _clean_text(item.get("phone"), 80),
            "meeting": _clean_text(item.get("meeting"), 240),
            "notes": _clean_text(item.get("notes"), 500),
        })

    if not isinstance(incident_log, list) or len(incident_log) > 2000:
        raise ValueError("Invalid incident log")
    clean_log: list[dict[str, Any]] = []
    for item in incident_log:
        if not isinstance(item, dict):
            continue
        event = _clean_text(item.get("event"), 500)
        action = _clean_text(item.get("action"), 1000)
        if not event and not action:
            continue
        clean_log.append({
            "id": _clean_text(item.get("id"), 80) or f"log-{len(clean_log)+1}",
            "time": _clean_datetime(item.get("time")),
            "event": event,
            "action": action,
            "status": _clean_text(item.get("status"), 80),
        })

    if not isinstance(risk_flags, list) or len(risk_flags) > 100:
        raise ValueError("Invalid risk flags")
    known_risks = {"wildfire", "flood", "earthquake", "outage", "heat", "cold", "evacuation", "isolation"}
    clean_risks = list(dict.fromkeys(x for x in (_clean_text(v, 80) for v in risk_flags) if x in known_risks))

    def clean_small_dict(value: Any, limit: int = 40) -> dict[str, str]:
        if not isinstance(value, dict) or len(value) > limit:
            return {}
        return {_clean_text(k, 80): _clean_text(v, 1000) for k, v in value.items() if _clean_text(k, 80) and _clean_text(v, 1000)}

    clean_medical = clean_small_dict(medical_card, 40)

    if not isinstance(medications, list) or len(medications) > 500:
        raise ValueError("Invalid medications")
    clean_medications: list[dict[str, Any]] = []
    for item in medications:
        if not isinstance(item, dict):
            continue
        name = _clean_text(item.get("name"), 160)
        if not name:
            continue
        clean_medications.append({
            "id": _clean_text(item.get("id"), 80) or f"med-{len(clean_medications)+1}",
            "name": name,
            "purpose": _clean_text(item.get("purpose"), 240),
            "instructions": _clean_text(item.get("instructions"), 500),
            "on_hand": _bounded_float(item.get("on_hand"), 0, 0, 10_000_000),
            "unit": _clean_text(item.get("unit"), 40),
            "refill": _clean_date(item.get("refill")),
            "notes": _clean_text(item.get("notes"), 500),
        })

    if not isinstance(waypoints, list) or len(waypoints) > 1000:
        raise ValueError("Invalid waypoints")
    clean_waypoints: list[dict[str, Any]] = []
    for item in waypoints:
        if not isinstance(item, dict):
            continue
        name = _clean_text(item.get("name"), 160)
        if not name:
            continue
        lat = _bounded_float(item.get("lat"), 0, -90, 90)
        lon = _bounded_float(item.get("lon"), 0, -180, 180)
        clean_waypoints.append({
            "id": _clean_text(item.get("id"), 80) or f"waypoint-{len(clean_waypoints)+1}",
            "name": name,
            "type": _clean_text(item.get("type"), 80),
            "lat": lat,
            "lon": lon,
            "notes": _clean_text(item.get("notes"), 800),
        })
    clean_navigation: dict[str, Any] = {}
    if isinstance(navigation, dict) and "origin_lat" in navigation and "origin_lon" in navigation:
        try:
            nav_lat = float(navigation.get("origin_lat"))
            nav_lon = float(navigation.get("origin_lon"))
        except (TypeError, ValueError):
            nav_lat = nav_lon = math.nan
        if math.isfinite(nav_lat) and math.isfinite(nav_lon) and -90 <= nav_lat <= 90 and -180 <= nav_lon <= 180:
            clean_navigation = {"origin_lat": round(nav_lat, 7), "origin_lon": round(nav_lon, 7)}

    if not isinstance(documents, list) or len(documents) > 1000:
        raise ValueError("Invalid document register")
    clean_documents: list[dict[str, Any]] = []
    for item in documents:
        if not isinstance(item, dict):
            continue
        name = _clean_text(item.get("name"), 180)
        if not name:
            continue
        clean_documents.append({
            "id": _clean_text(item.get("id"), 80) or f"doc-{len(clean_documents)+1}",
            "name": name,
            "copy_type": _clean_text(item.get("copy_type"), 100),
            "location": _clean_text(item.get("location"), 300),
            "review": _clean_date(item.get("review")),
            "notes": _clean_text(item.get("notes"), 600),
        })

    if not isinstance(maintenance, list) or len(maintenance) > 1000:
        raise ValueError("Invalid maintenance schedule")
    clean_maintenance: list[dict[str, Any]] = []
    for item in maintenance:
        if not isinstance(item, dict):
            continue
        task = _clean_text(item.get("task"), 220)
        if not task:
            continue
        clean_maintenance.append({
            "id": _clean_text(item.get("id"), 80) or f"maint-{len(clean_maintenance)+1}",
            "task": task,
            "interval_days": _bounded_int(item.get("interval_days"), 30, 1, 3650),
            "last_done": _clean_date(item.get("last_done")),
            "notes": _clean_text(item.get("notes"), 600),
        })

    if not isinstance(roles, list) or len(roles) > 250:
        raise ValueError("Invalid household roles")
    clean_roles: list[dict[str, Any]] = []
    for item in roles:
        if not isinstance(item, dict):
            continue
        name = _clean_text(item.get("name"), 140)
        if not name:
            continue
        clean_roles.append({
            "id": _clean_text(item.get("id"), 80) or f"role-{len(clean_roles)+1}",
            "name": name,
            "primary": _clean_text(item.get("primary"), 180),
            "backup": _clean_text(item.get("backup"), 180),
            "skills": _clean_text(item.get("skills"), 500),
        })

    if not isinstance(drill_history, list) or len(drill_history) > 500:
        raise ValueError("Invalid drill history")
    clean_drills: list[dict[str, Any]] = []
    for item in drill_history:
        if not isinstance(item, dict):
            continue
        scenario = _clean_text(item.get("scenario"), 100)
        if not scenario:
            continue
        clean_drills.append({
            "id": _clean_text(item.get("id"), 80) or f"drill-{len(clean_drills)+1}",
            "scenario": scenario,
            "time": _clean_datetime(item.get("time")),
            "completed": _bounded_int(item.get("completed"), 0, 0, 50),
            "total": _bounded_int(item.get("total"), 0, 0, 50),
            "score": _bounded_int(item.get("score"), 0, 0, 100),
            "debrief": _clean_text(item.get("debrief"), 2000),
        })

    clean_continuity = clean_small_dict(continuity, 50)

    if not isinstance(resource_plans, list) or len(resource_plans) > 500:
        raise ValueError("Invalid resource plans")
    clean_resource_plans: list[dict[str, Any]] = []
    for item in resource_plans:
        if not isinstance(item, dict):
            continue
        name = _clean_text(item.get("name"), 160)
        if not name:
            continue
        clean_resource_plans.append({
            "id": _clean_text(item.get("id"), 80) or f"resource-{len(clean_resource_plans)+1}",
            "name": name,
            "stock": _bounded_float(item.get("stock"), 0, 0, 1_000_000_000),
            "unit": _clean_text(item.get("unit"), 40),
            "daily_use": _bounded_float(item.get("daily_use"), 0, 0, 1_000_000_000),
            "reserve": _bounded_float(item.get("reserve"), 0, 0, 1_000_000_000),
            "notes": _clean_text(item.get("notes"), 700),
        })

    if not isinstance(checkins, list) or len(checkins) > 500:
        raise ValueError("Invalid check-ins")
    clean_checkins: list[dict[str, Any]] = []
    for item in checkins:
        if not isinstance(item, dict):
            continue
        name = _clean_text(item.get("name"), 140)
        if not name:
            continue
        clean_checkins.append({
            "id": _clean_text(item.get("id"), 80) or f"checkin-{len(clean_checkins)+1}",
            "name": name,
            "status": _clean_text(item.get("status"), 80) if _clean_text(item.get("status"), 80) in {"ok", "away", "unknown", "needs-help"} else "unknown",
            "location": _clean_text(item.get("location"), 240),
            "time": _clean_datetime(item.get("time")),
            "next": _clean_datetime(item.get("next")),
            "notes": _clean_text(item.get("notes"), 700),
        })

    if not isinstance(vehicles, list) or len(vehicles) > 100:
        raise ValueError("Invalid vehicles")
    clean_vehicles: list[dict[str, Any]] = []
    for item in vehicles:
        if not isinstance(item, dict):
            continue
        name = _clean_text(item.get("name"), 160)
        if not name:
            continue
        clean_vehicles.append({
            "id": _clean_text(item.get("id"), 80) or f"vehicle-{len(clean_vehicles)+1}",
            "name": name,
            "fuel_l": _bounded_float(item.get("fuel_l"), 0, 0, 10_000),
            "consumption_l100km": _bounded_float(item.get("consumption_l100km"), 0, 0, 1000),
            "battery_pct": _bounded_float(item.get("battery_pct"), 0, 0, 100),
            "odometer_km": _bounded_float(item.get("odometer_km"), 0, 0, 100_000_000),
            "last_check": _clean_date(item.get("last_check")),
            "notes": _clean_text(item.get("notes"), 700),
        })

    if not isinstance(kits, list) or len(kits) > 100:
        raise ValueError("Invalid kits")
    clean_kits: list[dict[str, Any]] = []
    for item in kits:
        if not isinstance(item, dict):
            continue
        name = _clean_text(item.get("name"), 160)
        if not name:
            continue
        raw_items = item.get("items", [])
        if not isinstance(raw_items, list) or len(raw_items) > 250:
            raw_items = []
        clean_items: list[dict[str, Any]] = []
        for kit_item in raw_items:
            if not isinstance(kit_item, dict):
                continue
            item_name = _clean_text(kit_item.get("name"), 160)
            if not item_name:
                continue
            clean_items.append({
                "id": _clean_text(kit_item.get("id"), 80) or f"kit-item-{len(clean_items)+1}",
                "name": item_name,
                "qty": _bounded_float(kit_item.get("qty"), 1, 0, 1_000_000),
                "weight_g": _bounded_float(kit_item.get("weight_g"), 0, 0, 10_000_000),
                "packed": bool(kit_item.get("packed", False)),
                "critical": bool(kit_item.get("critical", False)),
                "notes": _clean_text(kit_item.get("notes"), 400),
            })
        clean_kits.append({
            "id": _clean_text(item.get("id"), 80) or f"kit-{len(clean_kits)+1}",
            "name": name,
            "owner": _clean_text(item.get("owner"), 140),
            "max_weight_kg": _bounded_float(item.get("max_weight_kg"), 0, 0, 1000),
            "notes": _clean_text(item.get("notes"), 700),
            "items": clean_items,
        })

    if not isinstance(field_logs, list) or len(field_logs) > 2000:
        raise ValueError("Invalid field logs")
    clean_field_logs: list[dict[str, Any]] = []
    for item in field_logs:
        if not isinstance(item, dict):
            continue
        label = _clean_text(item.get("label"), 160)
        notes_text = _clean_text(item.get("notes"), 1200)
        if not label and not notes_text:
            continue
        clean_field_logs.append({
            "id": _clean_text(item.get("id"), 80) or f"field-{len(clean_field_logs)+1}",
            "time": _clean_datetime(item.get("time")),
            "label": label,
            "value": _clean_text(item.get("value"), 160),
            "unit": _clean_text(item.get("unit"), 40),
            "notes": notes_text,
        })

    if not isinstance(routes, list) or len(routes) > 20:
        raise ValueError("Invalid routes")
    clean_routes: list[dict[str, Any]] = []
    route_point_budget = 25_000
    for item in routes:
        if route_point_budget <= 0:
            break
        if not isinstance(item, dict):
            continue
        name = _clean_text(item.get("name"), 160)
        points = item.get("points", [])
        if not name or not isinstance(points, list):
            continue
        points = points[: min(5000, route_point_budget)]
        clean_points: list[list[float]] = []
        for point in points:
            if not isinstance(point, (list, tuple)) or len(point) < 2:
                continue
            try:
                lat = float(point[0]); lon = float(point[1])
            except (TypeError, ValueError):
                continue
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                clean_points.append([round(lat, 7), round(lon, 7)])
        if len(clean_points) < 2:
            continue
        route_point_budget -= len(clean_points)
        clean_routes.append({
            "id": _clean_text(item.get("id"), 80) or f"route-{len(clean_routes)+1}",
            "name": name,
            "source": _clean_text(item.get("source"), 120),
            "notes": _clean_text(item.get("notes"), 700),
            "points": clean_points,
        })

    if not isinstance(shelter_zones, list) or len(shelter_zones) > 200:
        raise ValueError("Invalid shelter zones")
    clean_shelter_zones: list[dict[str, Any]] = []
    for item in shelter_zones:
        if not isinstance(item, dict):
            continue
        name = _clean_text(item.get("name"), 160)
        if not name:
            continue
        status = _clean_text(item.get("status"), 40)
        if status not in {"safe", "check", "avoid", "unknown"}:
            status = "unknown"
        clean_shelter_zones.append({
            "id": _clean_text(item.get("id"), 80) or f"zone-{len(clean_shelter_zones)+1}",
            "name": name,
            "status": status,
            "occupants": _bounded_int(item.get("occupants"), 0, 0, 10000),
            "utilities": _clean_text(item.get("utilities"), 240),
            "last_check": _clean_datetime(item.get("last_check")),
            "notes": _clean_text(item.get("notes"), 1200),
        })

    if not isinstance(water_batches, list) or len(water_batches) > 1000:
        raise ValueError("Invalid water batches")
    clean_water_batches: list[dict[str, Any]] = []
    for item in water_batches:
        if not isinstance(item, dict):
            continue
        source = _clean_text(item.get("source"), 180)
        if not source:
            continue
        status = _clean_text(item.get("status"), 40)
        if status not in {"untreated", "processing", "ready", "discarded"}:
            status = "untreated"
        clean_water_batches.append({
            "id": _clean_text(item.get("id"), 80) or f"water-{len(clean_water_batches)+1}",
            "time": _clean_datetime(item.get("time")),
            "source": source,
            "volume_l": _bounded_float(item.get("volume_l"), 0, 0, 1_000_000),
            "method": _clean_text(item.get("method"), 180),
            "status": status,
            "container": _clean_text(item.get("container"), 160),
            "notes": _clean_text(item.get("notes"), 1200),
        })

    if not isinstance(recovery_items, list) or len(recovery_items) > 2000:
        raise ValueError("Invalid recovery items")
    clean_recovery_items: list[dict[str, Any]] = []
    for item in recovery_items:
        if not isinstance(item, dict):
            continue
        area = _clean_text(item.get("area"), 180)
        if not area:
            continue
        severity = _clean_text(item.get("severity"), 40)
        if severity not in {"minor", "moderate", "major", "critical", "unknown"}:
            severity = "unknown"
        status = _clean_text(item.get("status"), 40)
        if status not in {"open", "isolated", "assigned", "resolved", "deferred"}:
            status = "open"
        clean_recovery_items.append({
            "id": _clean_text(item.get("id"), 80) or f"recovery-{len(clean_recovery_items)+1}",
            "time": _clean_datetime(item.get("time")),
            "area": area,
            "severity": severity,
            "status": status,
            "owner": _clean_text(item.get("owner"), 140),
            "action": _clean_text(item.get("action"), 700),
            "notes": _clean_text(item.get("notes"), 1600),
        })

    if not isinstance(skill_matrix, list) or len(skill_matrix) > 1000:
        raise ValueError("Invalid skill matrix")
    clean_skill_matrix: list[dict[str, Any]] = []
    for item in skill_matrix:
        if not isinstance(item, dict):
            continue
        person = _clean_text(item.get("person"), 140)
        skill = _clean_text(item.get("skill"), 180)
        if not person or not skill:
            continue
        level = _clean_text(item.get("level"), 40)
        if level not in {"new", "practiced", "confident", "trainer"}:
            level = "new"
        clean_skill_matrix.append({
            "id": _clean_text(item.get("id"), 80) or f"skill-{len(clean_skill_matrix)+1}",
            "person": person,
            "skill": skill,
            "level": level,
            "last_practiced": _clean_date(item.get("last_practiced")),
            "next_practice": _clean_date(item.get("next_practice")),
            "notes": _clean_text(item.get("notes"), 1000),
        })

    if not isinstance(decision_board, list) or len(decision_board) > 1500:
        raise ValueError("Invalid decision board")
    clean_decision_board: list[dict[str, Any]] = []
    for item in decision_board:
        if not isinstance(item, dict):
            continue
        issue = _clean_text(item.get("issue"), 240)
        decision = _clean_text(item.get("decision"), 700)
        if not issue or not decision:
            continue
        status = _clean_text(item.get("status"), 40)
        if status not in {"active", "review", "closed", "superseded"}:
            status = "active"
        clean_decision_board.append({
            "id": _clean_text(item.get("id"), 80) or f"decision-{len(clean_decision_board)+1}",
            "time": _clean_datetime(item.get("time")),
            "issue": issue,
            "decision": decision,
            "reason": _clean_text(item.get("reason"), 1200),
            "owner": _clean_text(item.get("owner"), 140),
            "next_review": _clean_datetime(item.get("next_review")),
            "status": status,
        })

    if not isinstance(food_lots, list) or len(food_lots) > 2000:
        raise ValueError("Invalid food lots")
    clean_food_lots: list[dict[str, Any]] = []
    for item in food_lots:
        if not isinstance(item, dict):
            continue
        name = _clean_text(item.get("name"), 180)
        if not name:
            continue
        status = _clean_text(item.get("status"), 40)
        if status not in {"sealed", "open", "use-first", "isolated", "discarded"}:
            status = "sealed"
        clean_food_lots.append({
            "id": _clean_text(item.get("id"), 80) or f"food-{len(clean_food_lots)+1}",
            "name": name,
            "category": _clean_text(item.get("category"), 120),
            "qty": _bounded_float(item.get("qty"), 0, 0, 100_000_000),
            "unit": _clean_text(item.get("unit"), 40),
            "kcal_total": _bounded_float(item.get("kcal_total"), 0, 0, 10_000_000_000),
            "opened_date": _clean_date(item.get("opened_date")),
            "best_before": _clean_date(item.get("best_before")),
            "location": _clean_text(item.get("location"), 180),
            "status": status,
            "notes": _clean_text(item.get("notes"), 1200),
        })

    if not isinstance(sanitation_points, list) or len(sanitation_points) > 1000:
        raise ValueError("Invalid sanitation points")
    clean_sanitation_points: list[dict[str, Any]] = []
    for item in sanitation_points:
        if not isinstance(item, dict):
            continue
        name = _clean_text(item.get("name"), 180)
        if not name:
            continue
        kind = _clean_text(item.get("kind"), 40)
        if kind not in {"toilet", "handwash", "waste", "laundry", "bathing", "other"}:
            kind = "other"
        status = _clean_text(item.get("status"), 40)
        if status not in {"ready", "limited", "service", "unusable"}:
            status = "ready"
        clean_sanitation_points.append({
            "id": _clean_text(item.get("id"), 80) or f"sanitation-{len(clean_sanitation_points)+1}",
            "name": name,
            "kind": kind,
            "status": status,
            "capacity": _bounded_float(item.get("capacity"), 0, 0, 100_000_000),
            "unit": _clean_text(item.get("unit"), 40),
            "owner": _clean_text(item.get("owner"), 140),
            "last_service": _clean_datetime(item.get("last_service")),
            "next_service": _clean_datetime(item.get("next_service")),
            "notes": _clean_text(item.get("notes"), 1200),
        })

    if not isinstance(power_loads, list) or len(power_loads) > 1000:
        raise ValueError("Invalid power loads")
    clean_power_loads: list[dict[str, Any]] = []
    for item in power_loads:
        if not isinstance(item, dict):
            continue
        name = _clean_text(item.get("name"), 180)
        if not name:
            continue
        priority = _clean_text(item.get("priority"), 40)
        if priority not in {"critical", "important", "optional"}:
            priority = "important"
        clean_power_loads.append({
            "id": _clean_text(item.get("id"), 80) or f"load-{len(clean_power_loads)+1}",
            "name": name,
            "watts": _bounded_float(item.get("watts"), 0, 0, 10_000_000),
            "hours_per_day": _bounded_float(item.get("hours_per_day"), 0, 0, 24),
            "priority": priority,
            "source": _clean_text(item.get("source"), 120),
            "enabled": bool(item.get("enabled", True)),
            "notes": _clean_text(item.get("notes"), 1000),
        })

    if not isinstance(comms_windows, list) or len(comms_windows) > 1000:
        raise ValueError("Invalid communications windows")
    clean_comms_windows: list[dict[str, Any]] = []
    for item in comms_windows:
        if not isinstance(item, dict):
            continue
        name = _clean_text(item.get("name"), 180)
        if not name:
            continue
        status = _clean_text(item.get("status"), 40)
        if status not in {"active", "paused", "missed"}:
            status = "active"
        clean_comms_windows.append({
            "id": _clean_text(item.get("id"), 80) or f"comms-{len(clean_comms_windows)+1}",
            "name": name,
            "method": _clean_text(item.get("method"), 120),
            "channel": _clean_text(item.get("channel"), 120),
            "participants": _clean_text(item.get("participants"), 300),
            "time_local": _clean_text(item.get("time_local"), 80),
            "frequency": _clean_text(item.get("frequency"), 120),
            "backup": _clean_text(item.get("backup"), 240),
            "status": status,
            "notes": _clean_text(item.get("notes"), 1000),
        })

    if not isinstance(dependents, list) or len(dependents) > 500:
        raise ValueError("Invalid dependents")
    clean_dependents: list[dict[str, Any]] = []
    for item in dependents:
        if not isinstance(item, dict):
            continue
        name = _clean_text(item.get("name"), 180)
        if not name:
            continue
        kind = _clean_text(item.get("kind"), 40)
        if kind not in {"child", "older-adult", "disability", "pet", "service-animal", "other"}:
            kind = "other"
        clean_dependents.append({
            "id": _clean_text(item.get("id"), 80) or f"dependent-{len(clean_dependents)+1}",
            "name": name,
            "kind": kind,
            "needs": _clean_text(item.get("needs"), 1600),
            "mobility": _clean_text(item.get("mobility"), 700),
            "communication": _clean_text(item.get("communication"), 700),
            "caregiver": _clean_text(item.get("caregiver"), 140),
            "backup": _clean_text(item.get("backup"), 140),
            "supplies": _clean_text(item.get("supplies"), 1200),
            "notes": _clean_text(item.get("notes"), 1200),
        })

    if not isinstance(expense_log, list) or len(expense_log) > 5000:
        raise ValueError("Invalid expense log")
    clean_expense_log: list[dict[str, Any]] = []
    for item in expense_log:
        if not isinstance(item, dict):
            continue
        description = _clean_text(item.get("description"), 240)
        if not description:
            continue
        status = _clean_text(item.get("status"), 40)
        if status not in {"recorded", "claim-ready", "submitted", "reimbursed", "not-covered"}:
            status = "recorded"
        clean_expense_log.append({
            "id": _clean_text(item.get("id"), 80) or f"expense-{len(clean_expense_log)+1}",
            "time": _clean_datetime(item.get("time")),
            "category": _clean_text(item.get("category"), 120),
            "description": description,
            "amount": _bounded_float(item.get("amount"), 0, 0, 1_000_000_000),
            "currency": _clean_text(item.get("currency"), 12),
            "payment": _clean_text(item.get("payment"), 80),
            "claim_ref": _clean_text(item.get("claim_ref"), 160),
            "status": status,
            "notes": _clean_text(item.get("notes"), 1600),
        })

    if not isinstance(knowledge_progress, list) or len(knowledge_progress) > 1000:
        raise ValueError("Invalid knowledge progress")
    clean_knowledge_progress: list[dict[str, Any]] = []
    seen_knowledge: set[str] = set()
    for item in knowledge_progress:
        if not isinstance(item, dict):
            continue
        path = _clean_text(item.get("path"), 500)
        if not path or path in seen_knowledge:
            continue
        status = _clean_text(item.get("status"), 24)
        if status not in {"reviewed", "review-later"}:
            status = "reviewed"
        seen_knowledge.add(path)
        clean_knowledge_progress.append({
            "path": path,
            "status": status,
            "last_review": _clean_date(item.get("last_review")),
            "notes": _clean_text(item.get("notes"), 800),
        })

    clean_settings = {"low_power": bool(settings.get("low_power", False))} if isinstance(settings, dict) else {"low_power": False}
    updated_at = _clean_datetime(candidate.get("updated_at"))

    return {
        "favorites": clean_favorites,
        "notes": clean_notes,
        "checklist": clean_checklist,
        "custom_checklist": clean_custom,
        "profile": clean_profile,
        "inventory": clean_inventory,
        "contacts": clean_contacts,
        "incident_log": clean_log,
        "risk_flags": clean_risks,
        "communications": clean_small_dict(communications),
        "evacuation": clean_small_dict(evacuation),
        "medical_card": clean_medical,
        "medications": clean_medications,
        "waypoints": clean_waypoints,
        "navigation": clean_navigation,
        "documents": clean_documents,
        "maintenance": clean_maintenance,
        "roles": clean_roles,
        "drill_history": clean_drills,
        "continuity": clean_continuity,
        "resource_plans": clean_resource_plans,
        "checkins": clean_checkins,
        "vehicles": clean_vehicles,
        "kits": clean_kits,
        "field_logs": clean_field_logs,
        "routes": clean_routes,
        "shelter_zones": clean_shelter_zones,
        "water_batches": clean_water_batches,
        "recovery_items": clean_recovery_items,
        "skill_matrix": clean_skill_matrix,
        "decision_board": clean_decision_board,
        "food_lots": clean_food_lots,
        "sanitation_points": clean_sanitation_points,
        "power_loads": clean_power_loads,
        "comms_windows": clean_comms_windows,
        "dependents": clean_dependents,
        "expense_log": clean_expense_log,
        "knowledge_progress": clean_knowledge_progress,
        "settings": clean_settings,
        "schema_version": SCHEMA_VERSION,
        "updated_at": updated_at,
    }


def save_state(candidate: Any) -> dict[str, Any]:
    state = sanitize_state(candidate)
    state["schema_version"] = SCHEMA_VERSION
    state["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    temp = STATE_FILE.with_suffix(".tmp")
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if STATE_FILE.is_file():
        try:
            shutil.copy2(STATE_FILE, STATE_PREVIOUS_FILE)
        except OSError:
            pass
    temp.replace(STATE_FILE)
    return state


def restore_previous_state() -> dict[str, Any]:
    if not STATE_PREVIOUS_FILE.is_file():
        raise ValueError("No previous state backup is available")
    return save_state(safe_json_read(STATE_PREVIOUS_FILE, {}))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def directory_size(path: Path) -> int:
    total = 0
    if not path.exists():
        return 0
    for item in path.rglob("*"):
        try:
            if item.is_file():
                total += item.stat().st_size
        except OSError:
            pass
    return total


def human_size(value: int) -> str:
    size = float(value)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} B"
        size /= 1024
    return f"{size:.1f} TB"


def compact_item(item: dict[str, Any]) -> dict[str, Any]:
    record = item["record"]
    return {
        "id": record.get("id", ""),
        "title": record.get("title", ""),
        "category": record.get("category", ""),
        "subcategory": record.get("subcategory", ""),
        "summary": record.get("summary", ""),
        "urgency": record.get("urgency", ""),
        "priority": record.get("priority", ""),
        "tags": record.get("tags", []),
        "path": item.get("relative_path", ""),
    }


def full_item(item: dict[str, Any]) -> dict[str, Any]:
    output = dict(item["record"])
    output["_path"] = item.get("relative_path", "")
    return output


def get_language(query: dict[str, list[str]]) -> str:
    language = query.get("lang", ["en"])[0]
    return language if language in CORE.LANGUAGES else "en"


def load_language(language: str) -> list[dict[str, Any]]:
    return DATABASE.load(language)


def find_exact_record(language: str, record_id: str) -> dict[str, Any] | None:
    matches = DATABASE.find_by_id(language, record_id)
    for item in matches:
        if str(item["record"].get("id", "")) == record_id:
            return item
    return None


def library_files() -> list[dict[str, Any]]:
    if not LIBRARY_ROOT.is_dir():
        return []
    result: list[dict[str, Any]] = []
    for path in sorted(LIBRARY_ROOT.rglob("*"), key=lambda p: str(p).casefold()):
        if path.is_symlink() or not path.is_file():
            continue
        try:
            stat = path.stat()
        except OSError:
            continue
        rel = path.relative_to(LIBRARY_ROOT).as_posix()
        suffix = path.suffix.casefold()
        result.append({
            "path": rel,
            "name": path.name,
            "extension": suffix,
            "size": stat.st_size,
            "size_human": human_size(stat.st_size),
            "kind": "Kiwix ZIM" if suffix == ".zim" else "Offline map" if suffix == ".pmtiles" else "Document",
            "readable": suffix in LIBRARY_TEXT_SUFFIXES,
            "kiwix": suffix == ".zim",
        })
    return result


def safe_library_path(raw: str) -> Path:
    candidate = (LIBRARY_ROOT / unquote(raw)).resolve()
    root = LIBRARY_ROOT.resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError("Invalid library path")
    return candidate


def read_text_prefix(path: Path, max_bytes: int) -> tuple[str, bool]:
    """Read a bounded UTF-8 prefix for the built-in viewer/search index."""
    with path.open("rb") as stream:
        raw = stream.read(max_bytes + 1)
    truncated = len(raw) > max_bytes
    if truncated:
        raw = raw[:max_bytes]
    return raw.decode("utf-8", errors="replace"), truncated


def search_library_text(phrase: str, limit: int = 60, prefix: str = "") -> list[dict[str, Any]]:
    """Search safe text-readable Library files without indexing or network access."""
    query = " ".join(str(phrase).split())[:160]
    if len(query) < 2:
        return []
    q_lower = query.lower()
    terms = [part for part in q_lower.split() if len(part) >= 2][:12]
    safe_prefix = str(prefix or "").replace("\\", "/").strip("/")[:220]
    if ".." in safe_prefix.split("/"):
        return []
    results: list[dict[str, Any]] = []
    for item in library_files():
        if safe_prefix and not str(item.get("path", "")).startswith(safe_prefix + "/"):
            continue
        if not item.get("readable"):
            continue
        try:
            path = safe_library_path(str(item["path"]))
            text, truncated = read_text_prefix(path, LIBRARY_SEARCH_MAX_BYTES)
        except (OSError, ValueError):
            continue
        normalized = " ".join(text.split())
        hay = normalized.lower()
        pos = hay.find(q_lower)
        exact = pos >= 0
        if not exact:
            if not terms or not all(term in hay for term in terms):
                continue
            positions = [hay.find(term) for term in terms if hay.find(term) >= 0]
            pos = min(positions) if positions else 0
        start = max(0, pos - 110)
        end = min(len(normalized), pos + max(len(query), 1) + 220)
        snippet = normalized[start:end]
        if start:
            snippet = "…" + snippet
        if end < len(normalized) or truncated:
            snippet += "…"
        results.append({
            "path": item["path"],
            "name": item["name"],
            "kind": item["kind"],
            "size_human": item["size_human"],
            "snippet": snippet,
            "exact_phrase": exact,
            "search_truncated": truncated,
        })
    results.sort(key=lambda row: (not row["exact_phrase"], str(row["name"]).casefold()))
    return results[:max(1, min(250, limit))]


def kiwix_executable() -> str | None:
    return shutil.which("kiwix-serve")


def start_kiwix(path: Path) -> dict[str, Any]:
    global _KIWIX_PROCESS
    executable = kiwix_executable()
    if not executable:
        return {
            "ok": False,
            "error": "kiwix-serve is not installed. Open the ZIM with the Kiwix app, or install Kiwix tools on this device.",
        }
    if path.suffix.casefold() != ".zim" or not path.is_file():
        return {"ok": False, "error": "The selected file is not a valid local ZIM file."}

    with _KIWIX_LOCK:
        if _KIWIX_PROCESS is not None and _KIWIX_PROCESS.poll() is None:
            return {"ok": True, "url": f"http://127.0.0.1:{KIWIX_PORT}", "already_running": True}
        try:
            _KIWIX_PROCESS = subprocess.Popen(
                [executable, "--port", str(KIWIX_PORT), str(path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError as error:
            return {"ok": False, "error": str(error)}
    return {"ok": True, "url": f"http://127.0.0.1:{KIWIX_PORT}", "already_running": False}


class Handler(BaseHTTPRequestHandler):
    server_version = "OfflineSurvivalCommandCenter/7.0"

    def log_message(self, format: str, *args: Any) -> None:
        # Local request log only; nothing leaves the device.
        if getattr(self.server, "quiet", False):
            return
        super().log_message(format, *args)

    def send_json(self, payload: Any, status: int = 200) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Permissions-Policy", "geolocation=(self), camera=(), microphone=(), payment=(), usb=()")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(data)

    def send_file(self, path: Path, cache: bool = False, untrusted: bool = False) -> None:
        if not path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        try:
            size = path.stat().st_size
            stream = path.open("rb")
        except OSError:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(size))
        self.send_header("Cache-Control", "public, max-age=3600" if cache else "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Permissions-Policy", "geolocation=(self), camera=(), microphone=(), payment=(), usb=()")
        if untrusted:
            self.send_header("Content-Disposition", f"attachment; filename*=UTF-8''{quote(path.name)}")
            self.send_header("Content-Security-Policy", "default-src 'none'; sandbox; frame-ancestors 'none'")
        else:
            self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers()
        with stream:
            while True:
                chunk = stream.read(1024 * 1024)
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    return

    def read_json_body(self) -> Any:
        raw_length = self.headers.get("Content-Length", "0")
        try:
            length = int(raw_length)
        except ValueError as error:
            raise ValueError("Invalid Content-Length") from error
        if length < 0 or length > MAX_POST_BYTES:
            raise ValueError("Request body too large")
        raw = self.rfile.read(length)
        if not raw:
            return {}
        try:
            return json.loads(raw.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as error:
            raise ValueError("Invalid JSON body") from error

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        try:
            if not self.host_header_allowed():
                self.send_json({"error": "Host header rejected"}, HTTPStatus.MISDIRECTED_REQUEST)
                return
            if path == "/":
                self.send_file(INDEX_FILE)
                return
            if path == "/reader.html":
                self.send_file(PROJECT_ROOT / "Offline Survival Reader.html")
                return
            static_assets = {
                "/styles.css": WEB_ROOT / "styles.css",
                "/app.js": WEB_ROOT / "app.js",
                "/v5.js": WEB_ROOT / "v5.js",
                "/v6.js": WEB_ROOT / "v6.js",
                "/v7.js": WEB_ROOT / "v7.js",
                "/phone-test.html": WEB_ROOT / "phone-test.html",
                "/phone-test.js": WEB_ROOT / "phone-test.js",
                "/manifest.webmanifest": WEB_ROOT / "manifest.webmanifest",
                "/sw.js": WEB_ROOT / "sw.js",
            }
            if path in static_assets:
                self.send_file(static_assets[path], cache=path != "/sw.js")
                return
            if path == "/api/meta":
                self.api_meta()
                return
            if path == "/api/search":
                self.api_search(query)
                return
            if path == "/api/categories":
                self.api_categories(query)
                return
            if path == "/api/category":
                self.api_category(query)
                return
            if path == "/api/record":
                self.api_record(query)
                return
            if path == "/api/essentials":
                self.api_essentials(query)
                return
            if path == "/api/food":
                self.api_food(query)
                return
            if path == "/api/random":
                self.api_random(query)
                return
            if path == "/api/scenario":
                self.api_scenario(query)
                return
            if path == "/api/state":
                self.send_json(load_state())
                return
            if path == "/api/library":
                self.send_json({"files": library_files(), "root": str(LIBRARY_ROOT), "kiwix_available": bool(kiwix_executable())})
                return
            if path == "/api/library/search":
                self.api_library_search(query)
                return
            if path == "/api/library/text":
                self.api_library_text(query)
                return
            if path == "/api/library/hash":
                self.api_library_hash(query)
                return
            if path == "/api/diagnostics":
                self.api_diagnostics()
                return
            if path == "/api/state/previous":
                self.send_json({"available": STATE_PREVIOUS_FILE.is_file()})
                return
            if path.startswith("/library/"):
                self.api_library_file(path[len("/library/"):])
                return
            self.send_error(HTTPStatus.NOT_FOUND)
        except FileNotFoundError as error:
            self.send_json({"error": f"Database folder missing: {error}"}, 500)
        except (RuntimeError, ValueError, OSError) as error:
            self.send_json({"error": str(error)}, 400)
        except Exception as error:
            self.send_json({"error": f"Unexpected local server error: {error}"}, 500)


    def host_header_allowed(self) -> bool:
        allowed = getattr(self.server, "allowed_hosts", None)
        if allowed is None:
            return True
        host = self.headers.get("Host", "").strip().casefold()
        return host in allowed

    def same_origin_request(self) -> bool:
        """Reject cross-origin browser writes while allowing non-browser local clients."""
        origin = self.headers.get("Origin")
        if not origin:
            return True
        try:
            parsed = urlparse(origin)
        except ValueError:
            return False
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            return False
        host = self.headers.get("Host", "").strip().casefold()
        return bool(host) and parsed.netloc.casefold() == host

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        try:
            if not self.host_header_allowed():
                self.send_json({"error": "Host header rejected"}, HTTPStatus.MISDIRECTED_REQUEST)
                return
            if not self.same_origin_request():
                self.send_json({"error": "Cross-origin state-changing request rejected"}, HTTPStatus.FORBIDDEN)
                return
            if parsed.path == "/api/state":
                body = self.read_json_body()
                self.send_json(save_state(body))
                return
            if parsed.path == "/api/state/restore-previous":
                self.send_json(restore_previous_state())
                return
            if parsed.path == "/api/kiwix/start":
                body = self.read_json_body()
                raw_path = str(body.get("path", "")) if isinstance(body, dict) else ""
                path = safe_library_path(raw_path)
                self.send_json(start_kiwix(path))
                return
            self.send_error(HTTPStatus.NOT_FOUND)
        except (ValueError, OSError) as error:
            self.send_json({"error": str(error)}, 400)
        except Exception as error:
            self.send_json({"error": f"Unexpected local server error: {error}"}, 500)

    def api_meta(self) -> None:
        report = integrity_report_cached()
        usage = shutil.disk_usage(PROJECT_ROOT)
        files = library_files()
        project_size = directory_size(PROJECT_ROOT)
        library_size = sum(item["size"] for item in files)
        essentials_count = sum(1 for item in load_language("en") if str(item["record"].get("id", "")).startswith("verified-essential-"))
        food_count = sum(1 for item in load_language("en") if str(item["record"].get("id", "")).startswith("verified-food-"))
        self.send_json({
            "app": "Offline Survival Project",
            "mode": "Ultimate Operations Command Center",
            "command_center_version": COMMAND_CENTER_VERSION,
            "state_schema_version": SCHEMA_VERSION,
            "report": report,
            "verified_essentials": essentials_count,
            "verified_food_guides": food_count,
            "state": load_state(),
            "system": {
                "platform": platform.platform(),
                "python": platform.python_version(),
                "project_size": project_size,
                "project_size_human": human_size(project_size),
                "disk_free": usage.free,
                "disk_free_human": human_size(usage.free),
                "library_files": len(files),
                "library_size": library_size,
                "library_size_human": human_size(library_size),
                "kiwix_available": bool(kiwix_executable()),
            },
            "scenarios": list(SCENARIOS),
        })

    def api_search(self, query: dict[str, list[str]]) -> None:
        language = get_language(query)
        phrase = query.get("q", [""])[0].strip()
        try:
            limit = max(1, min(200, int(query.get("limit", ["80"])[0])))
        except ValueError:
            limit = 80
        results = DATABASE.search(language, phrase) if phrase else []
        self.send_json({"query": phrase, "count": len(results), "results": [compact_item(item) for item in results[:limit]]})

    def api_categories(self, query: dict[str, list[str]]) -> None:
        language = get_language(query)
        uncategorized = "Uncategorized" if language == "en" else "Χωρίς κατηγορία"
        categories = DATABASE.categories(language, uncategorized)
        rows = [{"name": name, "count": len(items)} for name, items in categories.items()]
        self.send_json({"count": len(rows), "categories": rows})

    def api_category(self, query: dict[str, list[str]]) -> None:
        language = get_language(query)
        name = query.get("name", [""])[0]
        uncategorized = "Uncategorized" if language == "en" else "Χωρίς κατηγορία"
        categories = DATABASE.categories(language, uncategorized)
        items = categories.get(name, [])
        self.send_json({"name": name, "count": len(items), "results": [compact_item(item) for item in items]})

    def api_record(self, query: dict[str, list[str]]) -> None:
        language = get_language(query)
        record_id = query.get("id", [""])[0].strip()
        item = find_exact_record(language, record_id)
        if item is None:
            self.send_json({"error": "Record not found"}, 404)
            return
        self.send_json(full_item(item))

    def api_essentials(self, query: dict[str, list[str]]) -> None:
        language = get_language(query)
        rows = [item for item in load_language(language) if str(item["record"].get("id", "")).startswith("verified-essential-")]
        self.send_json({"count": len(rows), "results": [compact_item(item) for item in rows]})

    def api_food(self, query: dict[str, list[str]]) -> None:
        language = get_language(query)
        rows = [item for item in load_language(language) if str(item["record"].get("id", "")).startswith("verified-food-")]
        self.send_json({"count": len(rows), "results": [compact_item(item) for item in rows]})

    def api_random(self, query: dict[str, list[str]]) -> None:
        language = get_language(query)
        rows = load_language(language)
        if not rows:
            self.send_json({"error": "Database is empty"}, 404)
            return
        self.send_json(full_item(random.choice(rows)))

    def api_scenario(self, query: dict[str, list[str]]) -> None:
        language = get_language(query)
        key = query.get("key", [""])[0]
        scenario = SCENARIOS.get(key)
        if scenario is None:
            self.send_json({"error": "Unknown scenario"}, 404)
            return
        phrase = scenario[language]
        results = DATABASE.search(language, phrase)
        # Search terms may be broad; reward curated emergency essentials.
        results.sort(key=lambda item: (not str(item["record"].get("id", "")).startswith("verified-essential-"), CORE.normalize(item["record"].get("title", ""))))
        self.send_json({"key": key, "query": phrase, "count": len(results), "results": [compact_item(item) for item in results[:60]]})

    def api_library_search(self, query: dict[str, list[str]]) -> None:
        phrase = query.get("q", [""])[0].strip()
        try:
            limit = max(1, min(250, int(query.get("limit", ["60"])[0])))
        except ValueError:
            limit = 60
        prefix = query.get("prefix", [""])[0].strip().replace("\\", "/")[:220]
        if ".." in prefix.split("/"):
            raise ValueError("Invalid Library search prefix")
        rows = search_library_text(phrase, limit=limit, prefix=prefix)
        self.send_json({"query": phrase[:160], "prefix": prefix, "count": len(rows), "results": rows})

    def api_library_text(self, query: dict[str, list[str]]) -> None:
        raw = query.get("path", [""])[0]
        path = safe_library_path(raw)
        if path.suffix.casefold() not in LIBRARY_TEXT_SUFFIXES:
            raise ValueError("This library file is not text-readable in the built-in viewer")
        if not path.is_file():
            self.send_json({"error": "Library file not found"}, 404)
            return
        text = path.read_text(encoding="utf-8", errors="replace")
        if len(text) > 2_000_000:
            text = text[:2_000_000] + "\n\n[Viewer truncated this file at 2 MB.]"
        self.send_json({"path": raw, "text": text})

    def api_library_hash(self, query: dict[str, list[str]]) -> None:
        raw = query.get("path", [""])[0]
        path = safe_library_path(raw)
        if not path.is_file():
            self.send_json({"error": "Library file not found"}, 404)
            return
        self.send_json({"path": raw, "sha256": sha256_file(path), "size": path.stat().st_size})

    def api_diagnostics(self) -> None:
        checks: list[dict[str, Any]] = []
        def add(name: str, ok: bool, detail: str = "") -> None:
            checks.append({"name": name, "ok": bool(ok), "detail": detail})
        add("web_index", INDEX_FILE.is_file(), str(INDEX_FILE))
        add("web_styles", (WEB_ROOT / "styles.css").is_file(), str(WEB_ROOT / "styles.css"))
        add("web_script", (WEB_ROOT / "app.js").is_file(), str(WEB_ROOT / "app.js"))
        add("web_v5_script", (WEB_ROOT / "v5.js").is_file(), str(WEB_ROOT / "v5.js"))
        add("web_v6_script", (WEB_ROOT / "v6.js").is_file(), str(WEB_ROOT / "v6.js"))
        add("web_v7_script", (WEB_ROOT / "v7.js").is_file(), str(WEB_ROOT / "v7.js"))
        add("phone_browser_diagnostics", (WEB_ROOT / "phone-test.html").is_file() and (WEB_ROOT / "phone-test.js").is_file(), str(WEB_ROOT / "phone-test.html"))
        add("standalone_reader", (PROJECT_ROOT / "Offline Survival Reader.html").is_file(), str(PROJECT_ROOT / "Offline Survival Reader.html"))
        for code in ("en", "el"):
            root = DATABASE.language_root(code)
            add(f"database_{code}", root.is_dir(), str(root))
        try:
            STATE_DIR.mkdir(parents=True, exist_ok=True)
            probe = STATE_DIR / ".write-test"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink(missing_ok=True)
            add("state_writable", True, str(STATE_DIR))
        except OSError as error:
            add("state_writable", False, str(error))
        add("library_root", LIBRARY_ROOT.is_dir(), str(LIBRARY_ROOT))
        try:
            report = integrity_report_cached()
            add("database_integrity", bool(report.get("ok")), "validator report")
        except Exception as error:
            add("database_integrity", False, str(error))
        self.send_json({"ok": all(x["ok"] for x in checks), "checks": checks, "version": COMMAND_CENTER_VERSION, "schema": SCHEMA_VERSION})

    def api_library_file(self, raw: str) -> None:
        path = safe_library_path(raw)
        self.send_file(path, cache=False, untrusted=True)


def open_browser_later(url: str) -> None:
    """Delegate URL opening to the OS-installed/default browser.

    On Android/Termux this intentionally uses Android URL intents rather than
    selecting, embedding, or automating any browser engine. Desktop fallbacks
    also use the operating system's default URL opener.
    """
    time.sleep(0.6)
    candidates: list[list[str]] = []
    opener = shutil.which("termux-open-url")
    if opener:
        candidates.append([opener, url])
    am = shutil.which("am")
    if not am and Path("/system/bin/am").is_file():
        am = "/system/bin/am"
    if am:
        candidates.append([am, "start", "-a", "android.intent.action.VIEW", "-d", url])
    xdg = shutil.which("xdg-open")
    if xdg:
        candidates.append([xdg, url])
    mac_open = shutil.which("open")
    if mac_open:
        candidates.append([mac_open, url])

    for command in candidates:
        try:
            subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return
        except OSError:
            continue
    print(f"Could not invoke the system browser automatically. Open this URL in the installed browser: {url}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Offline Survival local Command Center.")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address. Default is localhost only.")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"HTTP port. Default: {DEFAULT_PORT}")
    parser.add_argument("--no-browser", action="store_true", help="Do not ask the operating system to open its installed/default browser.")
    parser.add_argument("--phone-test", action="store_true", help="Open on-device diagnostics in the installed/default phone browser.")
    parser.add_argument("--reader", action="store_true", help="Open the standalone bilingual Knowledge Reader in the installed/default browser.")
    parser.add_argument("--quiet", action="store_true", help="Suppress local request logging.")
    args = parser.parse_args()

    if not INDEX_FILE.is_file():
        print(f"Missing web interface: {INDEX_FILE}", file=sys.stderr)
        return 2
    if not (1 <= args.port <= 65535):
        print("Port must be between 1 and 65535.", file=sys.stderr)
        return 2

    try:
        server = ThreadingHTTPServer((args.host, args.port), Handler)
    except OSError as error:
        print(f"Could not start local Command Center: {error}", file=sys.stderr)
        return 2
    server.quiet = bool(args.quiet)  # type: ignore[attr-defined]
    if args.host in {"127.0.0.1", "localhost", "::1"}:
        port_text = str(args.port)
        server.allowed_hosts = {  # type: ignore[attr-defined]
            "127.0.0.1", f"127.0.0.1:{port_text}",
            "localhost", f"localhost:{port_text}",
            "[::1]", f"[::1]:{port_text}",
        }
    elif args.host not in {"0.0.0.0", "::"}:
        port_text = str(args.port)
        server.allowed_hosts = {args.host.casefold(), f"{args.host.casefold()}:{port_text}"}  # type: ignore[attr-defined]
    else:
        # Wildcard/LAN mode is an explicit advanced choice; hostname policy is left to the surrounding network/host.
        server.allowed_hosts = None  # type: ignore[attr-defined]

    display_host = "127.0.0.1" if args.host in {"0.0.0.0", "::"} else args.host
    base_url = f"http://{display_host}:{args.port}/"
    suffix = "phone-test.html" if args.phone_test else ("reader.html" if args.reader else "")
    url = base_url + suffix
    print("=" * 72)
    print("Offline Survival Project — Local Command Center")
    print("=" * 72)
    print(f"Open: {url}")
    if args.phone_test:
        print("Phone diagnostics: run inside the browser Android actually opens. No browser engine is selected or automated by this project.")
    print("Offline by design. No cloud account, telemetry, Docker, or database server required.")
    if args.host not in {"127.0.0.1", "localhost", "::1"}:
        print("WARNING: You chose a non-localhost bind address. Other devices on the network may be able to connect.")
    print("Press Ctrl+C to stop.")

    if not args.no_browser:
        threading.Thread(target=open_browser_later, args=(url,), daemon=True).start()

    try:
        server.serve_forever(poll_interval=0.3)
    except KeyboardInterrupt:
        print("\nStopping Command Center...")
    finally:
        server.server_close()
        global _KIWIX_PROCESS
        with _KIWIX_LOCK:
            if _KIWIX_PROCESS is not None and _KIWIX_PROCESS.poll() is None:
                _KIWIX_PROCESS.terminate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
