from fastapi import FastAPI

app = FastAPI(
    title="Cognitext AI API",
    description="Backend API for the Cognitext AI Intelligent Document Intelligence Platform.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Cognitext AI API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "cognitext-api",
    }