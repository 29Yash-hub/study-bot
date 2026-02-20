from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import chat_with_bot
app = FastAPI()


class ChatRequest(BaseModel):
    user_id: str
    message: str


@app.post("/chat")
def chat(request: ChatRequest):
    reply = get_response(request.user_id, request.message)

    return {"response": reply}
