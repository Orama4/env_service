from fastapi import FastAPI
from app.api.routes import router
from app.models.loader import load_models
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="YOLO Detection API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Replace "*" with specific methods if needed
    allow_headers=["*"],  # Replace "*" with specific headers if needed
)


@app.on_event("startup")
async def startup_event():
    await load_models()

app.include_router(router)
