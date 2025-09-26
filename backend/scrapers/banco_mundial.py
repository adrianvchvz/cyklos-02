import requests
from datetime import datetime
from utils.date import parse_date

def scrape_banco_mundial():
    current_date = datetime.now().strftime("%Y-%m-%d")
    url = "https://search.worldbank.org/api/v2/procnotices"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {
        "format": "json",
        "fl": (
            "market_approach_name,market_approach_region_name,procurement_major_sector_name,"
            "id,procurement_group_desc,submission_deadline_date,bid_description,project_ctry_name,"
            "project_name,notice_type,notice_status,notice_lang_name,submission_date,noticedate,project_id"
        ),
        "srt": "submission_deadline_date",
        "order": "desc",
        "apilang": "en",
        "rows": 20,
        "srce": "both",
        "notice_type_exact": (
            "Invitation for Bids^Invitation for Prequalification^Request for Expression of Interest"
        ),
        "deadline_strdate": current_date,
    }
    
    resp = requests.get(url, params=params, timeout=30, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    opportunities = []
    for item in data.get("procnotices", []):
        opportunities.append({
            "title": item.get("project_name"),
            "description": item.get("bid_description"),
            "published_date": parse_date(item.get("noticedate")),
            "deadline_date": parse_date(item.get("submission_deadline_date")),
            "opportunity_url": f"https://projects.worldbank.org/en/projects-operations/procurement-detail/{item.get('id')}",
            "project_url": f"https://projects.worldbank.org/en/projects-operations/project-detail/{item.get('project_id')}",
            "source": "Banco Mundial – Project Procurement",
        })
    return opportunities
