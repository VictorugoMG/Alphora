from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.stocks import router as stocks_router

app = FastAPI(
    title="Alphora API",
    description="Stock market prediction API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stocks_router)


@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}
