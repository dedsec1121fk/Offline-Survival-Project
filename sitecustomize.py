import builtins

# Startup fallback for older script revisions that reference PAGE_BREAK
# before defining it in module globals.
if not hasattr(builtins, "PAGE_BREAK"):
    builtins.PAGE_BREAK = "=" * 96
