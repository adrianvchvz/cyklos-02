import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(new_opportunities):
    if not new_opportunities:
        return

    new_opportunities = list(reversed(new_opportunities))

    for c in new_opportunities:
        message = (
            f"🚨 <b>{c.get('title')}</b>\n\n"
            f"🏛️ <b>Fuente:</b> {c.get('source')}\n"
            f"📌 <b>Pilar:</b> {c.get('pillar_name')}\n"
            f"📅 <b>Publicada:</b> {c.get('published_date') or 'N/D'}\n"
            f"⏳ <b>Límite:</b> {c.get('deadline_date') or 'N/D'}\n\n"
            f"{c.get('description') or 'N/D'}\n\n"
            f"{'📄 ' + c.get('opportunity_url') if c.get('opportunity_url') else ''}\n"
            f"{'📁 ' + c.get('project_url') if c.get('project_url') else ''}"
        )

        response  = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
        )
        if response .status_code != 200:
            print(f"⚠️ Error al enviar a Telegram: {response .text}")

    print(f"Se enviaron {len(new_opportunities)} convocatorias nuevas por Telegram.")

