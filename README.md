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

Expected tables: users, provider_profiles, service_categories, bookings, reviews

API Endpoints

Full request/response schemas are documented in API_CONTRACT.md. Summary:

Method	Endpoint	Description
POST	/api/chat	Natural-language chatbot — extracts intent and returns matched providers
POST	/api/price-estimate	Returns estimated price range and job duration
GET	/api/providers	Filterable provider search (category, price, rating)

All responses are JSON. Errors follow a standard shape:

json
{ "error": "Description of what went wrong", "status_code": 400 }
Database Schema

Five core tables, related via foreign keys:

users — customers, providers, and admins (differentiated by role)
service_categories — e.g. Painter, Plumber, Electrician
provider_profiles — bio, skill tags, pricing tier, hourly rate, rating
bookings — links a customer, provider, and category with status tracking
reviews — ratings and comments tied to completed bookings

See db/schema.sql for full definitions and indexes.

Integration with Frontend
CORS is enabled for local development (allow_origins=["*"])
No auth required for /api/chat or /api/price-estimate
See API_CONTRACT.md for open integration questions and the full request/response contract
Roadmap
 Docker + PostgreSQL + ChromaDB setup
 Database schema with relationships and indexes
 RAG chatbot foundation (intent parsing + vector search)
 Price estimator algorithm
 Full RAG pipeline testing with real queries
 Deployment to Render/Railway
 End-to-end testing with frontend
Troubleshooting
Port already in use — change the host port in docker-compose.yml (e.g. 5433:5432)
Docker permission error (Linux) — try sudo docker compose up --build
Slow first build — normal, Docker images are being downloaded for the first time