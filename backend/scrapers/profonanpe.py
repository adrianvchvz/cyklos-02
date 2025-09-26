import requests
from bs4 import BeautifulSoup
from utils.date import parse_date

def scrape_profonanpe():
    url = "https://profonanpe.org.pe/lista-convocatorias/"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, timeout=30, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    opportunities = []
    for section in soup.select("section.content-convocatorias"):
        h4s = section.select("h4.elementor-heading-title")
        date_tag = section.select_one("p:-soup-contains('Fecha de cierre')")
        tdr_link = section.select_one("a:-soup-contains('Descargar TdR')")
        apply_link = section.select_one("a:-soup-contains('Postular')")

        if not h4s or not date_tag:
            continue

        title = h4s[0].get_text(strip=True)
        description = h4s[1].get_text(strip=True) if len(h4s) > 1 else None

        # Extraer y normalizar fecha de cierre
        raw_deadline = date_tag.get_text(strip=True).replace("Fecha de cierre:", "").strip()
        deadline_date = parse_date(raw_deadline)

        opportunities.append({
            "title": title,
            "description": description,
            "published_date": None,  # Profonanpe no da fecha de publicación
            "deadline_date": deadline_date,
            "opportunity_url": tdr_link["href"] if tdr_link else None,
            "project_url": apply_link["href"] if apply_link else None,
            "source": "Profonanpe"
        })

    return opportunities

