import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from database import engine
import models
from routers.auth_router import router as auth_router
from routers.chat_router import router as chat_router
from rag.rag_pipeline import load_vector_store

load_dotenv()

# Create all tables on startup
models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the RAG vector store in the background so the server can bind
    # its port immediately instead of blocking on model download/embedding
    asyncio.create_task(asyncio.to_thread(load_vector_store))
    yield


app = FastAPI(
    title="Multi-Agent AI Customer Support API",
    description="REST API for the Multi-Agent AI Customer Support System",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(chat_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "Multi-Agent AI Support API"}
