from fastapi import FastAPI
from fastapi._compat import RequiredParam
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

app = FastAPI(
    title="Chat API",
    description="A simple chat API",
    version="1.0.222"
)


@app.get("/",summary="Root endpoint",tags=["root"])
async def root():
    return {"message": "Hello, World!"}

@app.post("/chat",summary="Chat endpoint",tags=["chat"],description="Chat with the API")
async def chat(request: ChatRequest):
    return {"message": f"nb! {request.message}"}

@app.post("/fool/{id}",summary="Fool endpoint",tags=["fool"],description="Fool with the API")
async def fool(request: int,id: int):
    return {"message": f"fool! {request} {id}"}