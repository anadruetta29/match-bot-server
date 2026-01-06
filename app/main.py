from fastapi import FastAPI

app = FastAPI(title="Match Score Bot API")

app.include_router(chat_router)

@app.get("/health")
def health():
    return {"status": "ok"}
