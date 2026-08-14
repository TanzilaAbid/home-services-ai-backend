# Home Services Marketplace — AI Backend (Tanzila's Part)

## Day 1 Setup — Follow these steps on YOUR computer

### 1. Files ko extract karo
Is zip ko extract karo aur terminal/CMD us folder mein open karo:
```
cd tanzila-backend
```

### 2. .env file banao
```bash
cp .env.example .env
```
Phir `.env` file kholo aur agar chahen to password/keys badal lo. Abhi ke liye defaults chal jayenge.

### 3. Git init karo
```bash
git init
git add .
git commit -m "Day 1: Project skeleton, Docker setup, DB schema"
```
(`.env` ko git mein push nahi karna — woh already `.gitignore` mein hai)

### 4. Docker containers start karo
```bash
docker compose up --build
```
Yeh 3 cheezein start karega:
- **PostgreSQL** → port 5432 (schema.sql se tables automatically ban jayengi)
- **ChromaDB** → port 8001
- **FastAPI** → port 8000

### 5. Verify karo sab chal raha hai
Browser mein kholo:
- http://localhost:8000 → `{"status": "ok", ...}` dikhna chahiye
- http://localhost:8000/docs → FastAPI ka Swagger UI (auto-generated API docs)
- http://localhost:8001/api/v1/heartbeat → ChromaDB alive hai ya nahi

Postgres check karne ke liye (agar `psql` installed hai):
```bash
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
