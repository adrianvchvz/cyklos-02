import psycopg
import os
from utils.classification import classify_opportunity
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")


def get_conn():
    return psycopg.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )


def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            CREATE TABLE IF NOT EXISTS sources (
                id_source SERIAL PRIMARY KEY,
                name_source TEXT,
                url TEXT,   
                relevance TEXT,
                level INTEGER
            );

            CREATE TABLE IF NOT EXISTS pillars (
                id_pillar SERIAL PRIMARY KEY,
                name_pillar TEXT
            );

            CREATE TABLE IF NOT EXISTS keywords (
                id_keyword SERIAL PRIMARY KEY,
                word TEXT,
                language TEXT,
                pillar_id INTEGER REFERENCES pillars(id_pillar)
            );

            CREATE TABLE IF NOT EXISTS opportunities (
                id_opportunity SERIAL PRIMARY KEY,
                title TEXT,
                description TEXT,
                published_date DATE,
                deadline_date DATE,
                opportunity_url TEXT UNIQUE,
                project_url TEXT UNIQUE,
                source_id INTEGER REFERENCES sources(id_source),
                pillar_id INTEGER REFERENCES pillars(id_pillar)
            );
            """
            )
            conn.commit()
        print("BD inicializada")


def seed_db():
    with get_conn() as conn:
        with conn.cursor() as cur:

            sources = [
                (
                    "Banco Mundial – Project Procurement",
                    "https://projects.worldbank.org/en/projects-operations/opportunities",
                    "Muy Alta",
                    1,
                ),
                (
                    "BID – Project Procurement",
                    "https://projectprocurement.iadb.org/",
                    "Muy Alta",
                    1,
                ),
                (
                    "BID – Bank-Executed Operations (BEO)",
                    "https://beo-procurement.iadb.org/",
                    "Alta",
                    1,
                ),
                (
                    "MINAM",
                    "https://www.minam.gob.pe/convocatorias/",
                    "Alta",
                    2,
                ),
                (
                    "Profonanpe",
                    "https://profonanpe.org.pe/lista-convocatorias/",
                    "Alta",
                    2,
                ),
            ]

            for s in sources:
                cur.execute("SELECT 1 FROM sources WHERE name_source = %s", (s[0],))
                if not cur.fetchone():
                    cur.execute(
                        """
                        INSERT INTO sources (name_source, url, relevance, level)
                        VALUES (%s, %s, %s, %s)
                        """,
                        s,
                    )

            pilares_keywords = {
                "Economía Circular": [
                    ("economía circular", "es"),
                    ("valorización de residuos", "es"),
                    ("simbiosis industrial", "es"),
                    ("ecodiseño", "es"),
                    ("producción más limpia", "es"),
                    ("gestión de RCD", "es"),
                    ("logística inversa", "es"),
                    ("circular economy", "en"),
                    ("waste valorization", "en"),
                    ("industrial symbiosis", "en"),
                    ("ecodesign", "en"),
                    ("cleaner production", "en"),
                    ("C&D waste management", "en"),
                    ("reverse logistics", "en"),
                ],
                "Cambio Climático": [
                    ("cambio climático", "es"),
                    ("adaptación", "es"),
                    ("mitigación", "es"),
                    ("vulnerabilidad", "es"),
                    ("NDCs", "es"),
                    ("finanzas climáticas", "es"),
                    ("resiliencia", "es"),
                    ("transición energética", "es"),
                    ("descarbonización", "es"),
                    ("climate change", "en"),
                    ("adaptation", "en"),
                    ("mitigation", "en"),
                    ("vulnerability", "en"),
                    ("NDCs", "en"),
                    ("climate finance", "en"),
                    ("resilience", "en"),
                    ("energy transition", "en"),
                    ("decarbonization", "en"),
                ],
                "Gestión Ambiental": [
                    ("evaluación de impacto ambiental", "es"),
                    ("EIA", "es"),
                    ("debida diligencia ambiental", "es"),
                    ("cumplimiento normativo", "es"),
                    ("gestión de pasivos ambientales", "es"),
                    ("monitoreo ambiental", "es"),
                    ("environmental impact assessment", "en"),
                    ("EIA", "en"),
                    ("environmental due diligence", "en"),
                    ("regulatory compliance", "en"),
                    ("environmental liability management", "en"),
                    ("environmental monitoring", "en"),
                ],
                "Soluciones basadas en la Naturaleza": [
                    ("soluciones basadas en la naturaleza", "es"),
                    ("infraestructura natural", "es"),
                    ("servicios ecosistémicos", "es"),
                    ("capital natural", "es"),
                    ("pago por servicios ambientales", "es"),
                    ("nature-based solutions", "en"),
                    ("natural infrastructure", "en"),
                    ("ecosystem services", "en"),
                    ("natural capital", "en"),
                    ("payment for ecosystem services", "en"),
                ],
                "Plásticos y Contaminación": [
                    ("plásticos de un solo uso", "es"),
                    ("contaminación marina", "es"),
                    ("gestión de plásticos", "es"),
                    ("economía circular del plástico", "es"),
                    ("microplásticos", "es"),
                    ("single-use plastics", "en"),
                    ("marine pollution", "en"),
                    ("plastic waste management", "en"),
                    ("circular economy for plastics", "en"),
                    ("microplastics", "en"),
                ],
                "Huellas Ambientales": [
                    ("huella de carbono", "es"),
                    ("huella hídrica", "es"),
                    ("huella ambiental", "es"),
                    ("análisis de ciclo de vida", "es"),
                    ("inventario de GEI", "es"),
                    ("carbon footprint", "en"),
                    ("water footprint", "en"),
                    ("environmental footprint", "en"),
                    ("life cycle assessment", "en"),
                    ("GHG inventory", "en"),
                ],
                "Reporte y Estrategia de Sostenibilidad": [
                    ("reporte de sostenibilidad", "es"),
                    ("GRI", "es"),
                    ("SASB", "es"),
                    ("TCFD", "es"),
                    ("estrategia ASG", "es"),
                    ("ESG", "es"),
                    ("materialidad", "es"),
                    ("debida diligencia en derechos humanos", "es"),
                    ("sustainability reporting", "en"),
                    ("GRI", "en"),
                    ("SASB", "en"),
                    ("TCFD", "en"),
                    ("ESG strategy", "en"),
                    ("materiality", "en"),
                    ("human rights due diligence", "en"),
                ],
                "Fortalecimiento de Capacidades": [
                    ("fortalecimiento de capacidades", "es"),
                    ("capacitación", "es"),
                    ("asistencia técnica", "es"),
                    ("diseño de talleres", "es"),
                    ("manuales de formación", "es"),
                    ("capacity building", "en"),
                    ("training", "en"),
                    ("technical assistance", "en"),
                    ("workshop design", "en"),
                    ("training manuals", "en"),
                ],
            }

            for pillar, kws in pilares_keywords.items():
                cur.execute(
                    "SELECT id_pillar FROM pillars WHERE name_pillar = %s", (pillar,)
                )
                row = cur.fetchone()
                if row:
                    pillar_id = row[0]
                else:
                    cur.execute(
                        "INSERT INTO pillars (name_pillar) VALUES (%s) RETURNING id_pillar",
                        (pillar,),
                    )
                    pillar_id = cur.fetchone()[0]

                for word, lang in kws:
                    cur.execute(
                        "SELECT 1 FROM keywords WHERE word = %s AND pillar_id = %s",
                        (word, pillar_id),
                    )
                    if not cur.fetchone():
                        cur.execute(
                            "INSERT INTO keywords (word, language, pillar_id) VALUES (%s, %s, %s)",
                            (word, lang, pillar_id),
                        )

            conn.commit()
        print("Datos iniciales insertados correctamente")


def insert_opportunities(opportunities):
    new_opportunities = []

    with get_conn() as conn:
        with conn.cursor() as cur:
            for opportunity in opportunities:
                # Obtener id de fuente
                cur.execute(
                    "SELECT id_source FROM sources WHERE name_source = %s",
                    (opportunity["source"],),
                )
                source_row = cur.fetchone()
                if not source_row:
                    continue
                source_id = source_row[0]

                # Clasificar
                pillar_id, pillar_name = classify_opportunity(opportunity, conn)
                if not pillar_id:
                    continue

                # Insertar oportunidad con manejo de duplicados en SQL
                cur.execute(
                    """
                    INSERT INTO opportunities
                    (title, description, published_date, deadline_date, opportunity_url, project_url, source_id, pillar_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (opportunity_url) DO NOTHING
                    RETURNING id_opportunity
                    """,
                    (
                        opportunity.get("title"),
                        opportunity.get("description"),
                        opportunity.get("published_date"),
                        opportunity.get("deadline_date"),
                        opportunity.get("opportunity_url"),
                        opportunity.get("project_url"),
                        source_id,
                        pillar_id,
                    ),
                )

                inserted = cur.fetchone()
                if inserted: 
                    opportunity["pillar_name"] = pillar_name
                    new_opportunities.append(opportunity)

            conn.commit()

    return new_opportunities




