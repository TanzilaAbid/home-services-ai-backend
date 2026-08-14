from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chatbot, pricing

app = FastAPI(
    title="Home Services Marketplace - AI Backend",
    description="AI Chatbot, Price Estimator & Data Services (Tanzila's microservice)",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "service": "AI Backend running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(chatbot.router, prefix="/api", tags=["chatbot"])
app.include_router(pricing.router, prefix="/api", tags=["pricing"])
