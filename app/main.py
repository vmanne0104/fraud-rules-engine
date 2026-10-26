from fastapi import FastAPI
from pydantic import BaseModel, Field
from .engine import score_event, DEFAULT_RULES

app = FastAPI(title="Fraud Rules Engine", version="1.0.0")

class Event(BaseModel):
    account_id: str
    hours_since_sim_swap: float | None = Field(None, ge=0)
    account_age_days: int | None = Field(None, ge=0)
    order_amount: float | None = Field(None, ge=0)
    new_country: bool | None = None
    failed_otp: int | None = Field(None, ge=0)

@app.post("/v1/score")
def score(event: Event):
    data = event.model_dump(exclude_none=True)
    return {"account_id": event.account_id, **score_event(data)}

@app.get("/v1/rules")
def rules():
    return [r.__dict__ for r in DEFAULT_RULES]

@app.get("/healthz")
def health():
    return {"status": "ok"}
