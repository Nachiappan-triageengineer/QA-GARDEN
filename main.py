from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(title="Bug Triage Engine")

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="192.168.1.13",
        port=8003,
        reload=True
    )

