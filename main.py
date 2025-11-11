from dotenv import load_dotenv
load_dotenv()
import getpass
import os
from fastapi import FastAPI
from agent import get_agent_response
from pydantic import BaseModel

class ChatRequest(BaseModel):
    userchat: str

# if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
#     os.environ["HUGGINGFACEHUB_API_TOKEN"] = getpass.getpass("Enter your token: ")
app = FastAPI()

@app.get("/")
def server_root():
    return {"message": "Hello, FastAPI is running!"}

@app.post("/chatagent")
def chat_agent(request: ChatRequest):
    response = get_agent_response(user_input=request.userchat)
    return {"response": response}