import os
from typing import Optional
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

API_KEY = "ak_c22i31zmctud6feoqenewi7i"
EMAIL = os.environ.get("EMAIL", "your-email@example.com")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analytics")
async def analytics(request: Request, x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    body = await request.json()
    events = body.get("events", [])

    users = set()
    totals = {}
    revenue = 0.0
    for e in events:
        user = e.get("user")
        amount = e.get("amount", 0) or 0
        users.add(user)
        if amount > 0:
            revenue += amount
            totals[user] = totals.get(user, 0) + amount

    top_user = max(totals, key=totals.get) if totals else None

    return {
        "email": EMAIL,
        "total_events": len(events),
        "unique_users": len(users),
        "revenue": revenue,
        "top_user": top_user,
    }
