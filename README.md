# Public LinkedIn Profile Lead Finder

A small Python research utility that finds **publicly indexed** LinkedIn profile pages through the Google Search Results API (SerpAPI), then exports the result set to CSV for manual review.

## Why this project
Recruiting and sales teams often need a repeatable way to discover public professional profiles by role, geography and company. This project turns a search brief into a structured review file.

## Features
- Role, location and optional company query parameters
- Restricts results to public `linkedin.com/in/` URLs
- Captures search title and snippet with source attribution
- CSV export for manual qualification
- API key read from an environment variable, never hard-coded

## Tech stack
Python 3.10+, Requests, SerpAPI, CSV.

## Setup
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```
Set `SERPAPI_API_KEY` in your shell, then run:
```bash
python scraper.py --role "Data Analyst" --location "India" --company "Retail" --limit 20
```
Output: `public_leads.csv`.

## Data and compliance notes
This tool queries a third-party search API. It does not sign in to LinkedIn, scrape behind authentication, circumvent rate limits, or collect private profile data. Search snippets may be incomplete or stale. Review each result manually and follow applicable privacy, platform and outreach rules. API usage may incur charges under your SerpAPI plan.

## Limitations / next steps
- Search result ranking and coverage depend on Google and SerpAPI.
- No enrichment, email discovery, automated messaging or CRM sync is performed.
- Future work: add deduplication, configurable query templates and a review status field.

## Author
Debarghya Hajra | Data Analytics & Python Projects
