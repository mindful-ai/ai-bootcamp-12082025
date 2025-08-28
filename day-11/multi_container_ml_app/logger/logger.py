from fastapi import FastAPI, Request

app = FastAPI(title="Logger Service", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/log")
async def log(request: Request):
    data = await request.json()
    print("[LOGGER] ", data)
    return {"logged": True}
