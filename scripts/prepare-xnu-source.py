import os
import urllib.request
import json
import sys

URL = sys.argv[1] if len(sys.argv) > 1 else "https://api.github.com/repos/apple-oss-distributions/xnu/git/trees/main?recursive=1"
CACHE = pathlib.Path(".cache/xnu-tree.json")
CACHE.parent.mkdir(parents=True, exist_ok=True)

headers = {"User-Agent": "UniXNU"}
token = os.environ.get("GITHUB_TOKEN")
if token:
    headers["Authorization"] = f"Bearer {token}"

try:
    req = urllib.request.Request(URL, headers=headers)
    data = urllib.request.urlopen(req, timeout=30).read()
    CACHE.write_bytes(data)
except Exception as e:
    print(f"Warning: API fetch failed ({e}), attempting fallback...", file=sys.stderr)
    # Fallback if rate limited or offline
    if not CACHE.exists():
        print("Error: No cached XNU source tree available.", file=sys.stderr)
        sys.exit(1)
