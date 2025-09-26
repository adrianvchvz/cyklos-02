from datetime import datetime

# Lista de formatos comunes
FORMATS = [
    "%Y-%m-%d",       # 2025-09-26
    "%d/%m/%Y",       # 26/09/2025
    "%d-%b-%Y",       # 26-Sep-2025
    "%d-%m-%Y",       # 26-09-2025
    "%b %d, %Y",      # Sep 26, 2025
    "%Y/%m/%d",       # 2025/09/26
]

def parse_date(date_str):
    """Normaliza una fecha a objeto date o None si no se puede parsear."""
    if not date_str:
        return None

    for fmt in FORMATS:
        try:
            return datetime.strptime(date_str.strip(), fmt).date()
        except ValueError:
            continue

    # casos ISO8601 o con Z al final
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00")).date()
    except Exception:
        return None
