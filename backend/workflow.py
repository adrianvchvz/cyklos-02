from db.database import init_db, seed_db, insert_opportunities
from scrapers.banco_mundial import scrape_banco_mundial
from scrapers.bid_beo import scrape_bid_beo
from scrapers.minam import scrape_minam
from scrapers.profonanpe import scrape_profonanpe
from services.email_service import send_email
from services.telegram_service import send_telegram

def run_workflow():
    
    #Inicializar base de datos
    init_db()
    seed_db()

    #Scrapear convocatorias
    all_opportunities = []
    all_opportunities += scrape_banco_mundial()
    all_opportunities += scrape_bid_beo()
    all_opportunities += scrape_minam()
    all_opportunities += scrape_profonanpe()

    #Insertar convocatorias en la base de datos
    new_opportunities = insert_opportunities(all_opportunities)

    #Notificar convocatorias
    send_email(new_opportunities)
    send_telegram(new_opportunities)

    return len(new_opportunities), len(all_opportunities)