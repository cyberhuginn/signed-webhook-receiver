from pydantic import BaseModel


class WebhookRequest(BaseModel):
    sign: str
    data: dict
