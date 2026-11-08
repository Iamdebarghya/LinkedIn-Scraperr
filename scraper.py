"""Public profile discovery using Google results via SerpAPI.

This tool does not log in to LinkedIn, access private profiles, or bypass access controls.
Set SERPAPI_API_KEY in the environment before running.
"""
from __future__ import annotations
import argparse, csv, os, sys, time
from urllib.parse import urlencode
import requests

API_URL = "https://serpapi.com/search.json"

def search_public_profiles(role: str, location: str, company: str = "", limit: int = 20):
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing SERPAPI_API_KEY environment variable.")
    query = f'site:linkedin.com/in/ "{role}" "{location}"'
    if company:
        query += f' "{company}"'
    params = {"engine": "google", "q": query, "api_key": api_key, "num": min(max(limit, 1), 100)}
    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    leads = []
    for item in payload.get("organic_results", []):
        url = item.get("link", "")
        if "linkedin.com/in/" not in url:
            continue
        leads.append({
            "name_or_title": item.get("title", ""),
            "snippet": item.get("snippet", ""),
            "profile_url": url.split("?")[0],
            "source": "Google public search result",
        })
    return leads

def export_csv(rows, path):
    fields = ["name_or_title", "snippet", "profile_url", "source"]
    with open(path, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

def main():
    parser = argparse.ArgumentParser(description="Discover publicly indexed LinkedIn profile URLs.")
    parser.add_argument("--role", required=True)
    parser.add_argument("--location", required=True)
    parser.add_argument("--company", default="")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--output", default="public_leads.csv")
    args = parser.parse_args()
    try:
        rows = search_public_profiles(args.role, args.location, args.company, args.limit)
        export_csv(rows, args.output)
        print(f"Saved {len(rows)} public search results to {args.output}")
    except (requests.RequestException, RuntimeError) as exc:
        print(f"Search failed: {exc}", file=sys.stderr)
        raise SystemExit(1)

if __name__ == "__main__":
    main()
