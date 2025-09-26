def classify_opportunity(opportunity, conn):
    cur = conn.cursor()
    text = ((opportunity.get("title") or "") + " " + (opportunity.get("description") or "")).lower()

    cur.execute("""
        SELECT k.word, k.pillar_id, p.name_pillar
        FROM keywords k
        JOIN pillars p ON k.pillar_id = p.id_pillar
    """)

    for word, pillar_id, pillar_name in cur.fetchall():
        if word.lower() in text:
            return pillar_id, pillar_name

    return None, None
