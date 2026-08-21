Home Services Marketplace — AI Backend

FastAPI-based backend for a home services marketplace platform. Handles the AI chatbot (RAG-powered provider matching), instant price estimation, and core data storage for users, providers, bookings, and reviews.

Team split: This repo covers the AI backend (chatbot + price estimator + database). Frontend and booking/CRUD logic live in a separate repo (see Integration).

Features
🤖 AI Chatbot — Understands natural-language requests (e.g. "I need a painter for my 3-bedroom house next Tuesday under $300"), extracts intent, and returns matched providers.
🔎 RAG-powered provider search — Provider bios, skills, and pricing are embedded and indexed in ChromaDB for semantic matching.
💰 Instant Price Estimator — Rule-based algorithm that returns a price range and estimated job duration from service type, room size, and condition.
🗄️ PostgreSQL schema — Users, provider profiles, service categories, bookings, and reviews, with foreign keys and indexes for fast lookups.
📄 Auto-generated API docs — Swagger/OpenAPI via FastAPI at /docs.
Tech Stack
Layer	Technology
API framework	FastAPI
Database	PostgreSQL 16
Vector store	ChromaDB
AI provider	Google Gemini 2.5 Flash / Groq Llama 3.3
ORM	SQLAlchemy
Containerization	Docker & Docker Compose
Project Structure
home-services-ai-backend/
├── app/
│   ├── main.py                # FastAPI app entrypoint, CORS, router registration
│   ├── database.py            # SQLAlchemy engine/session setup
│   ├── models/                # ORM models
│   ├── routers/
│   │   ├── chatbot.py         # POST /api/chat
│   │   └── pricing.py         # POST /api/price-estimate
│   └── services/
│       ├── gemini_client.py       # LLM calls + intent extraction
│       ├── chroma_client.py       # ChromaDB collection access
│       ├── chat_service.py        # RAG search over providers
│       ├── index_providers.py     # Embeds & indexes provider data into ChromaDB
│       └── pricing_service.py     # Price estimator algorithm
├── db/
│   ├── schema.sql              # Table definitions, relationships, indexes
│   └── seed.sql                # Sample/dummy data for local testing
├── docker-compose.yml           # Postgres + ChromaDB + API services
├── Dockerfile
├── requirements.txt
├── API_CONTRACT.md              # Endpoint contract shared with frontend team
└── .env.example                 # Environment variable template
Getting Started
Prerequisites
Docker and Docker Compose
An API key for Gemini or Groq (whichever you plan to use)
1. Clone and configure environment
bash
git clone https://github.com/TanzilaAbid/home-services-ai-backend.git
cd home-services-ai-backend
cp .env.example .env

Open .env and fill in your own GEMINI_API_KEY or GROQ_API_KEY. Never commit .env — it's already excluded via .gitignore.

2. Start the services
bash
docker compose up --build

This starts three containers:

PostgreSQL → localhost:5432 (tables auto-created from db/schema.sql)
ChromaDB → localhost:8001
FastAPI → localhost:8000
3. Verify everything is running
Check	URL
API health	http://localhost:8000
Swagger UI (interactive API docs)	http://localhost:8000/docs
ChromaDB heartbeat	http://localhost:8001/api/v1/heartbeat

To inspect the database directly:

bash
docker exec -it homeservices_pg psql -U admin -d home_services -c "\dt"
```
Yeh 5 tables dikhani chahiye: `users`, `provider_profiles`, `service_categories`, `bookings`, `reviews`

---

## Agla Step (Day 2)
- Sample/dummy data database mein daalna
- ChromaDB setup finalize karna
- Javaria ke saath API contract decide karna (kaunse endpoints, kya JSON format)

## Troubleshooting
- **Port already in use**: `docker-compose.yml` mein ports change kar lo (e.g. `5433:5432`)
- **Docker permission error (Linux)**: `sudo docker compose up --build` try karo
- **Container build slow first time**: normal hai, pehli baar images download hoti hain
