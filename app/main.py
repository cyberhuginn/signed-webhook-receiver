from fastapi import FastAPI, HTTPException
from app.schemas import WebhookRequest
from app.security import verify_signature

app = FastAPI()


@app.post("/api/v1/webhook")
async def webhook(payload: WebhookRequest):
    if not verify_signature(
            payload.data,
            payload.sign
    ):
        raise HTTPException(
            status_code=404,
            detail="Not Found"
        )

    data = payload.data

    print("VALID DATA:", data)

    return {
        "status": "ok"
    }
