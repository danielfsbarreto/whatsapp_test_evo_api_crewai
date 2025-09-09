from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class RequestBody(BaseModel):
    class Config:
        extra = "allow"


@app.post("/messages-upsert")
async def messages_upsert(body: RequestBody):
    print(body.model_dump())
    return body.model_dump()


@app.post("/send-message")
async def send_message(body: RequestBody):
    print(body.model_dump())
    return body.model_dump()
