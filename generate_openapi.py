import json
from app import app

with open("openapi.json", "w") as f:
    json.dump(app.openapi(), f, indent=2)
print("✅ OpenAPI spec generated at openapi.json")
