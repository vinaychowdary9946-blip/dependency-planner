# Local API guide

Start `python server.py`, then send JSON to `http://127.0.0.1:8000/api`. The API is a development interface on loopback, not an internet-facing service.

Example (Python, Windows/Linux/macOS):

```python
import json
from urllib.request import Request, urlopen
payload = {'action': 'plan', 'tasks': [{'id': 'design', 'duration': 2}, {'id': 'api', 'duration': 5, 'deps': ['design']}]}
request = Request("http://127.0.0.1:8000/api", data=json.dumps(payload).encode(), headers={"Content-Type":"application/json"})
with urlopen(request) as response:
    print(json.load(response))
```

Success: HTTP 200 with a JSON result. Invalid domain commands: HTTP 400 with `{"error":"..."}`. Unknown routes: 404. Foreign browser origins: 403. Request bodies are limited to 100,000 bytes. SQL uses bound parameters. No arbitrary Python, shell command, or user-supplied handler execution is supported.

## Actions
- `plan`: `tasks`, an array of `{id, duration, deps}`. `deps` defaults to an empty list. Returns `duration`, deterministic `order`, and task start, finish, slack and critical flags.
- `impact`: `tasks`, `changed` task ID. Returns changed task plus all descendants.

Use one consistent duration unit. Time estimates are numeric inputs, not calendar dates.
