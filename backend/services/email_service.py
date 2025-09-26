import os, smtplib, ssl
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
DEST_EMAIL = os.getenv("DEST_EMAIL")

def send_email(new_opportunities):
    if not new_opportunities:
        return

    subject = f"📢 {len(new_opportunities)} nuevas convocatorias encontradas"
    body_html = """<html><body style="font-family: Arial; background:#f9f9f9; padding:20px;">
                   <h2 style="color:#2c3e50;">📢 Nuevas convocatorias encontradas</h2>"""

    for c in new_opportunities:
        body_html += f"""
        <div style="background:#fff; border-radius:12px; padding:15px; margin-bottom:20px;
             box-shadow:0 2px 6px rgba(0,0,0,0.1);">
          <h3 style="margin:0; color:#e74c3c;">🚨 {c.get('title')}</h3>
          <p style="margin:6px 0;">
             🏛️ <b>Fuente:</b> {c.get('source')}<br>
             📌 <b>Pilar:</b> {c.get('pillar_name')}<br>
             📅 <b>Publicación:</b> {c.get('published_date') or 'N/D'}<br>
             ⏳ <b>Límite:</b> {c.get('deadline_date') or 'N/D'}
          </p>
          <p>{c.get('description') or 'N/D'}</p>
          <p>
            {f'<a href="{c.get("opportunity_url")}" style="margin-right:10px;">📄Convocatoria</a>' if c.get("opportunity_url") else ''}
            {f'<a href="{c.get("project_url")}" style="margin-right:10px;">📁Proyecto</a>' if c.get("project_url") else ''}
          </p>
        </div>
        """

    body_html += "</body></html>"

    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = DEST_EMAIL
    msg["Subject"] = subject
    msg.set_content("Nuevas convocatorias disponibles")
    msg.add_alternative(body_html, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

    print(f"Se enviaron {len(new_opportunities)} convocatorias nuevas por correo.")