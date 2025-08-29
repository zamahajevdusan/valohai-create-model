import argparse
import json
import os
import sys
import requests
import valohai
import urllib

VALOHAI_URL = os.getenv("VALOHAI_URL", "https://app.valohai.com/")
MODEL_API = "api/v0/models/"
MODEL_API_URL = urllib.parse.urljoin(VALOHAI_URL, MODEL_API)


def main():
    
    api_token = os.getenv("VALOHAI_API_TOKEN")

    if not api_token:
        print("❌ Missing API token. Set VALOHAI_API_TOKEN env var.", file=sys.stderr)
        sys.exit(2)

    # Normalize descriptions: the string "null" (any case) → None
    descriptions = [{
        "category": "overview",
        "title": "",
        "body": ""
    }]

    # Normalize associated projects: comma-separated → list (skip empties)
    associated_projects = valohai.parameters("associated_projects").value

    payload = {
        "owner": valohai.parameters("owner").value,
        "name": valohai.parameters("model_name").value,
        "slug": valohai.parameters("slug").value,
        "descriptions": descriptions,
        "access_mode": valohai.parameters("access_mode").value,
        "associated_projects": associated_projects,
    }

    headers = {
        "Authorization": f"Token {api_token}",
        "Content-Type": "application/json",
    }
    payload = json.dumps(payload)
    print(payload)
    resp = requests.post(MODEL_API_URL, headers=headers, data=payload, timeout=60)
    if resp.status_code in (200, 201):
        print("✅ Model created:")
        print(json.dumps(resp.json(), indent=2))
        print()
        print(json.dumps({
            "model_url": f"model://{valohai.parameters('model_name').value}"
        }, indent=4))
    else:
        print(f"❌ Error {resp.status_code}:\n{resp.text}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
