import requests
from bs4 import BeautifulSoup

def scrape_minam():
    url = "https://www.minam.gob.pe/convocatorias/"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, timeout=30, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table", {"id": "tbl_grilla"})

    opportunities = []
    if table:
        for row in table.find("tbody").find_all("tr"):
            cells = row.find_all("td")
            if len(cells) >= 3:
                title = cells[0].get_text(strip=True)
                link = cells[0].find("a")["href"]
                description = cells[1].get_text(strip=True)

                opportunities.append({
                    "title": title,
                    "description": description,
                    "published_date": None,
                    "deadline_date": None,
                    "opportunity_url": link,
                    "project_url": None,
                    "source": "MINAM"
                })
    return opportunities
