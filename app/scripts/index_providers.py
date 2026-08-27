"""
One-time (or repeatable) script: pulls provider profiles from PostgreSQL
and indexes them into the ChromaDB 'providers' collection so the chatbot
can semantically search for them.

Run this from Railway's Console tab on the 'comfortable-generosity' service,
or locally with the right DATABASE_URL / CHROMA_HOST / CHROMA_PORT set.

Usage:
    python -m app.scripts.index_providers
"""
import os
import psycopg2
import psycopg2.extras
import chromadb

DATABASE_URL = os.getenv("DATABASE_URL")
CHROMA_HOST = os.getenv("CHROMA_HOST", "chroma.railway.internal")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))

QUERY = """
SELECT
    pp.id AS provider_id,
    u.full_name,
    u.city,
    sc.name AS category,
    pp.bio,
    pp.skill_tags,
    pp.pricing_tier,
    pp.hourly_rate,
    pp.rating_avg,
    pp.is_available
FROM provider_profiles pp
JOIN users u ON u.id = pp.user_id
JOIN service_categories sc ON sc.id = pp.category_id
WHERE pp.is_available = TRUE;
"""


def build_document_text(row: dict) -> str:
    skills = ", ".join(row.get("skill_tags") or [])
    return (
        f"Category: {row.get('category')}. "
        f"Bio: {row.get('bio')}. "
        f"Skills: {skills}. "
        f"Pricing tier: {row.get('pricing_tier')}. "
        f"Hourly rate: {row.get('hourly_rate')} PKR. "
        f"City: {row.get('city')}."
    )


def run():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set")

    # 1. Pull providers from Postgres
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(QUERY)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        print("No available providers found in Postgres. Nothing to index.")
        return

    # 2. Connect to ChromaDB and prepare the batch
    client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    collection = client.get_or_create_collection(name="providers")

    ids = [str(row["provider_id"]) for row in rows]
    documents = [build_document_text(row) for row in rows]
    metadatas = [
        {
            "provider_id": str(row["provider_id"]),
            "name": row["full_name"] or "",
            "category": row["category"] or "",
            "city": row["city"] or "",
            "pricing_tier": row["pricing_tier"] or "",
            "hourly_rate": float(row["hourly_rate"] or 0),
            "rating": float(row["rating_avg"] or 0),
            "is_available": bool(row["is_available"]),
        }
        for row in rows
    ]

    # 3. Upsert into Chroma
    collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
    print(f"Indexed {len(ids)} providers into ChromaDB collection 'providers'.")


if __name__ == "__main__":
    run()
