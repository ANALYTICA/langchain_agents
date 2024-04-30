from typing import Union
from fastapi import FastAPI
from llama import load_model, get_retriever, raq_question
from agents import agent_initialize, question_agent, python_agent
from pydantic import BaseModel
import pickle
from parse import parse_order

db = {}
with open('db.pickle', 'wb') as handle:
    pickle.dump(db, handle, protocol=pickle.HIGHEST_PROTOCOL)

app = FastAPI()
model = load_model()
#retriever = get_retriever()
agent = agent_initialize(model)
python = python_agent(model)

@app.get("/")
def read_root():
    return {"This": "is a test"}

class Message(BaseModel):
    text: str

@app.put("/chat/tools")
async def respond(message: Message):
    try:
        results = question_agent(message.text, agent) 
    except: 
        results = {"message":"You broke the llm."}
    return results

@app.put("/chat/response")
async def respond(message: Message):
    #results = raq_question(message.text, model, retriever)
    #results = question_agent(message.text, agent)
    try:
        results = model.invoke(message.text) 
    except: 
        results = {"message":"You broke the llm."}
    return results

@app.put("/chat/order")
async def respond(message: Message):
    try:
        results = parse_order(model, message.text) 
    except: 
        results = {"message":"You broke the llm."}
    #results = parse_review(model, message.text)
    return results

@app.put("/chat/python")
async def respond(message: Message):
    results = python.run(message.text)
    return results