# Redundancy audit

## Ask a harder question than “do we have a backup?”
A backup is useful only if it survives a different failure. Audit each critical capability by writing the primary method, the backup method, and the dependencies shared by both.

## Common coupling
Look for two phones that depend on the same charger, two routes that use the same bridge, two payment methods that need the same network, two lights that use the same depleted battery type, or two people whose availability overlaps only during normal working hours. Shared dependencies are not automatically bad, but they should be visible.

## Independence test
For each pair, imagine the primary failure source is still present. Can the backup be reached, powered, understood, and operated by someone else? Does it require credentials or instructions stored only in the failed system? Can it be used without creating a new safety problem?

## Strengthen selectively
Do not duplicate everything. Prioritize capabilities whose loss would quickly affect safety, communication, shelter, essential care, or the ability to leave. Sometimes the best redundancy is procedural: a printed contact list, a second meeting point, cross-training another household member, or a clearly documented manual fallback.

## Record the result
Label each capability as independent enough, partially coupled, or single-point dependent. Link unresolved gaps to a concrete action instead of adding vague “buy backup” notes.
