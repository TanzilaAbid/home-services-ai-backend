"""
Run this script to (re)index all providers from Postgres into ChromaDB.

Usage (from inside the running api container):
    docker exec -it homeservices_api python -m app.services.index_providers

Run it again anytime provider data changes (new providers, updated bios, etc.)
"""
import os
import psycopg2
from app.services.chroma_client import get_provider_collection

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:admin123@postgres:5432/home_services"
)


def fetch_providers():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
        SELECT
            pp.id,
            u.full_name,
            sc.name AS category,
            pp.bio,
            pp.skill_tags,
            pp.pricing_tier,
            pp.hourly_rate,
            pp.rating_avg
        FROM provider_profiles pp
        JOIN users u ON pp.user_id = u.id
        JOIN service_categories sc ON pp.category_id = sc.id
        WHERE pp.is_available = TRUE
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def build_searchable_text(name, category, bio, skill_tags, pricing_tier):
    """
    Combines all the useful info into one text blob.
    This is what ChromaDB will use to find matches when a
    customer asks something like 'painter for 3 bedroom house'.
    """
    tags = ", ".join(skill_tags) if skill_tags else ""
    return (
        f"{name} is a {category}. "
        f"Skills: {tags}. "
        f"Pricing tier: {pricing_tier}. "
        f"Bio: {bio}"
    )


def index_all_providers():
    collection = get_provider_collection()
    providers = fetch_providers()

    if not providers:
        print("No providers found in database. Run seed.sql first.")
        return

    ids = []
    documents = []
    metadatas = []

    for row in providers:
        provider_id, name, category, bio, skill_tags, pricing_tier, hourly_rate, rating = row

        ids.append(str(provider_id))
        documents.append(build_searchable_text(name, category, bio, skill_tags, pricing_tier))
        metadatas.append({
            "name": name,
            "category": category,
            "pricing_tier": pricing_tier or "",
            "hourly_rate": float(hourly_rate) if hourly_rate else 0.0,
            "rating": float(rating) if rating else 0.0,
        })

    # upsert = insert new / update existing, safe to re-run anytime
    collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
    print(f"Indexed {len(ids)} providers into ChromaDB.")


if __name__ == "__main__":
    index_all_providers()
