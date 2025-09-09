import os

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from models import WhatsappRequestBody
from services import MessageSubmissionService

load_dotenv()

app = FastAPI()
security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != os.getenv("UVICORN_API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    return {"status": "ok"}


@app.post("/messages-upsert")
async def messages_upsert(
    body: WhatsappRequestBody, token: str = Depends(verify_token)
):
    print(body.model_dump())
    MessageSubmissionService().kickoff_interaction(body)
    return body.model_dump()


if __name__ == "__main__":
    host = os.getenv("UVICORN_HOST", "0.0.0.0")
    port = int(os.getenv("UVICORN_PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
