import requests

def scrape_bid_beo():
    url = "https://beo-procurement.iadb.org/en/views/activeOpportunities/view?page=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, timeout=30, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    opportunities = []
    for item in data.get("response", []):
        opportunities.append({
            "title": item.get("field_title_of_consultancy_value"),
            "description": item.get("sector_name"),
            "published_date": item.get("field_publication_date_value"),
            "deadline_date": item.get("field_deadline_date_value"),
            "opportunity_url": f"https://www.iadb.org/document.cfm?id={item.get('field_document_id_value')}",
            "project_url": f"https://www.iadb.org/en/project/{item.get('field_operation_number_value')}",
            "source": "BID – Bank-Executed Operations (BEO)"
        })
    return opportunities