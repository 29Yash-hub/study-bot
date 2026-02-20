import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# MongoDB Connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client["studybot"]
collection = db["chat_history"]

# LLM Setup (Groq)
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-8b-8192"
)

# 🔹 Get Chat History from MongoDB
def get_chat_history(user_id):
    chats = collection.find({"user_id": user_id}).sort("timestamp", 1)
    history = []

    for chat in chats:
        history.append({
            "role": chat["role"],
            "content": chat["message"]
        })

    return history


# 🔹 Save Message to MongoDB
def save_message(user_id, role, message):
    collection.insert_one({
        "user_id": user_id,
        "role": role,
        "message": message,
        "timestamp": datetime.utcnow()
    })


# 🔹 Main Chat Function
def chat_with_bot(user_id, message):
    # Get previous history
    history = get_chat_history(user_id)

    # Add current user message
    messages = history + [
        {"role": "user", "content": message}
    ]

    # Get LLM response
    response = llm.invoke(messages)

    # Save both user & assistant messages
    save_message(user_id, "user", message)
    save_message(user_id, "assistant", response.content)

    return response.content