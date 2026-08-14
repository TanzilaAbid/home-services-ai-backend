# API Contract — Home Services Marketplace
### Between: Tanzila (AI Backend - FastAPI) & Javaria (Frontend/Express)

Base URL (local dev): `http://localhost:8000`

---

## 1. AI Chatbot Endpoint

**POST** `/api/chat`

Customer poochta hai jaise: *"I need a painter for my 3-bedroom house next Tuesday under $300"*

### Request Body
```json
{
  "message": "I need a painter for my 3-bedroom house next Tuesday under $300",
  "user_id": "uuid-optional",
  "session_id": "string-for-conversation-history"
}
```

### Response Body
```json
{
  "reply": "I found 3 painters available for your budget...",
  "intent": {
    "category": "painter",
    "location": "customer's saved address or null",
    "budget_max": 300,
    "date_requested": "2026-08-18"
  },
  "matched_providers": [
    {
      "provider_id": "uuid",
      "name": "Ali Painters",
      "rating": 4.7,
      "hourly_rate": 25.0,
      "pricing_tier": "standard",
      "skill_tags": ["interior painting", "wall repair"]
    }
  ]
}
```

---

## 2. Price Estimator Endpoint

**POST** `/api/price-estimate`

### Request Body
```json
{
  "service_type": "painter",
  "room_sqft": 250,
  "wall_condition": "average",
  "num_rooms": 3
}
```

### Response Body
```json
{
  "price_min": 180,
  "price_max": 320,
  "estimated_hours": 6,
  "currency": "USD"
}
```

---

## 3. Provider Search (supporting endpoint for frontend filters)

**GET** `/api/providers?category=painter&max_price=300&min_rating=4`

### Response Body
```json
{
  "providers": [
    {
      "provider_id": "uuid",
      "name": "Ali Painters",
      "category": "painter",
      "rating": 4.7,
      "hourly_rate": 25.0,
      "is_available": true
    }
  ],
  "count": 1
}
```

---

## Notes for Integration (Javaria)
- All endpoints return JSON, `Content-Type: application/json`
- CORS already enabled on FastAPI for local dev (`allow_origins=["*"]`)
- Error format (standard for all endpoints):
```json
{
  "error": "Description of what went wrong",
  "status_code": 400
}
```
- Auth: chatbot/price-estimate don't require login; provider search may later take a JWT header if we add personalization

## Open Questions (discuss with Javaria before finalizing)
- [ ] Does booking creation happen via Tanzila's API or Javaria's Node/Express API? (Recommended: Express, since bookings CRUD is Javaria's Task 2.2)
- [ ] Should chat responses include a `quick_replies` array for the chat widget buttons?
- [ ] Pagination needed for `/api/providers` if results grow large?
