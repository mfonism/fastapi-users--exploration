from fastapi import FastAPI

app = FastAPI(title="Explore")


@app.get("/health")
def health():
    return {"status": "ok"}
