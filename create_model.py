import argparse
import json
import os
import sys
import requests
import valohai

URL = os.getenv("VALOHAI_URL", "https://app.valohai.com/api/v0/models/")


def main():
    
    api_token = os.getenv("VALOHAI_API_TOKEN")

    if not api_token:
        print("❌ Missing API token. Set VALOHAI_API_TOKEN env var.", file=sys.stderr)
        sys.exit(2)

    # Normalize descriptions: the string "null" (any case) → None
    descriptions = valohai.parameters("descriptions").value

    # Normalize associated projects: comma-separated → list (skip empties)
    associated_projects = valohai.parameters("associated_projects").value
    print(associated_projects)

    payload = {
        "owner": valohai.parameters("owner").value,
        "name": valohai.parameters("name").value,
        "slug": valohai.parameters("slug").value,
        "descriptions": descriptions,
        "access_mode": valohai.parameters("access_mode").value,
        "associated_projects": associated_projects,
    }

    headers = {
        "Authorization": f"Token {api_token}",
        "Content-Type": "application/json",
    }

    resp = requests.post(URL, headers=headers, data=json.dumps(payload))
    if resp.status_code in (200, 201):
        print("✅ Model created:")
        print(json.dumps(resp.json(), indent=2))
    else:
        print(f"❌ Error {resp.status_code}:\n{resp.text}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
