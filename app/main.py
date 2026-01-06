from fastapi import FastAPI
from app.api import chat, score

app = FastAPI(title="Match Score Bot Server")

app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(score.router, prefix="/score", tags=["Score"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
