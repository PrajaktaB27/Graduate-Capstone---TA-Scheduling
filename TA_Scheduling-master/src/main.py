from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.api import api_router


# API Routes
app = FastAPI(title="TA Backend")
app.include_router(api_router, prefix="/api/v1")
#app.include_router(auth_router, prefix="/auth_api")

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
