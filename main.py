from dotenv import load_dotenv
from fastapi import FastAPI

from models import WhatsappRequestBody
from services import MessageSubmissionService

load_dotenv()

app = FastAPI()


@app.post("/messages-upsert")
async def messages_upsert(body: WhatsappRequestBody):
    print(body.model_dump())
    MessageSubmissionService().kickoff_interaction(body)
    return body.model_dump()
