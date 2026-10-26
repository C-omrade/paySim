from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv(".paySim_fast_env")
from app.api.routes import health, analytics, transactions

app = FastAPI(
    title="Payment Monitoring API",
    description="Real-time payment transaction monitoring",
    version="1.0.0",
)

app.include_router(health.router)
app.include_router(analytics.router)
app.include_router(transactions.router)

@app.get("/")
def root():
    return {
        "message": "Payment Monitoring API is running"
    }