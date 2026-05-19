from fastapi import FastAPI

from api.routes.extract import router as extract_router
from api.routes.chat import router as chat_router

app = FastAPI(title="mini-chat-cli", version="0.1.0")

app.include_router(extract_router)
app.include_router(chat_router)


@app.get("/health")
def health():
    return {"status": "ok"}
