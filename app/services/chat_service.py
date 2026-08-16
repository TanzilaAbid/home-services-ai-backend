from app.services.gemini_client import call_gemini, extract_intent
from app.services.chroma_client import get_provider_collection
 
 
def search_matching_providers(intent: dict, n_results: int = 3) -> list:
    """
    Uses the extracted intent to do a semantic search in ChromaDB
    for the best matching providers.
    """
    collection = get_provider_collection()
 
    # Build a search query out of whatever info we have
    query_parts = []
    if intent.get("category"):
        query_parts.append(intent["category"])
    if intent.get("location"):
        query_parts.append(intent["location"])
    query_text = " ".join(query_parts) if query_parts else "home service provider"
 
    where_filter = None
    if intent.get("category"):
        # normalize case since categories in DB are capitalized (e.g. "Painter")
        # but Gemini may return lowercase (e.g. "painter")
        where_filter = {"category": intent["category"].strip().capitalize()}
 
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where=where_filter,
    )
 
    matched = []
    if results and results.get("ids") and results["ids"][0]:
        for i, provider_id in enumerate(results["ids"][0]):
            metadata = results["metadatas"][0][i]
            matched.append({
                "provider_id": provider_id,
                "name": metadata.get("name"),
                "category": metadata.get("category"),
                "hourly_rate": metadata.get("hourly_rate"),
                "pricing_tier": metadata.get("pricing_tier"),
                "rating": metadata.get("rating"),
            })
    return matched
 
 
def build_quick_replies(matched_providers: list, intent: dict) -> list:
    """
    Suggests 2-4 short quick-reply options for the chat widget buttons,
    based on whether providers were found.
    """
    if matched_providers:
        replies = ["Book Now", "See More Providers", "Adjust Budget"]
    else:
        replies = ["Increase Budget", "Try Different Category", "Talk to Support"]
    return replies
 
 
def generate_reply(user_message: str, matched_providers: list) -> str:
    """
    Asks Gemini to write a friendly, natural reply summarizing the matches.
    """
    if not matched_providers:
        provider_summary = "No matching providers were found."
    else:
        lines = []
        for p in matched_providers:
            lines.append(
                f"- {p['name']} ({p['category']}), rating {p['rating']}, "
                f"${p['hourly_rate']}/hr, tier: {p['pricing_tier']}"
            )
        provider_summary = "\n".join(lines)
 
    prompt = f"""
You are a friendly assistant for a home services marketplace (painters, plumbers, electricians).
The customer said: "{user_message}"
 
Here are the matching providers found in our database:
{provider_summary}
 
Write a short, warm, helpful reply (2-4 sentences) recommending these providers to the customer.
If no providers were found, politely say so and suggest they broaden their search.
Do not invent providers that aren't listed above.
"""
    return call_gemini(prompt)
 
 
def handle_chat_message(user_message: str) -> dict:
    """
    Full pipeline: extract intent -> search ChromaDB -> generate reply.
    This is what the /api/chat endpoint will call.
    """
    intent = extract_intent(user_message)
    matched_providers = search_matching_providers(intent)
    reply = generate_reply(user_message, matched_providers)
    quick_replies = build_quick_replies(matched_providers, intent)
 
    return {
        "reply": reply,
        "intent": intent,
        "matched_providers": matched_providers,
        "quick_replies": quick_replies,
    }
 