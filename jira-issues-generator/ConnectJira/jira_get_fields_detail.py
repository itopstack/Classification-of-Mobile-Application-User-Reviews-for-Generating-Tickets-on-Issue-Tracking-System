import requests
import json
import constant

response = requests.request(
   "GET",
   constant.url_fields,
   headers=constant.headers
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
