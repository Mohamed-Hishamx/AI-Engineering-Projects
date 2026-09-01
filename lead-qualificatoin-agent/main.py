from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_tavily import TavilySearch
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

app = FastAPI()

# --- Data model for incoming webhook ---
class Lead(BaseModel):
    name: str
    company: str

# --- Build the agent (runs fresh for each request) ---
def build_agent():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",   # Free, fast model on Groq
        temperature=0,
    )

    tools = [TavilySearch(max_results=3)]

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a B2B sales lead qualification expert.

Given a lead's name and company, search the web to learn about:
- What the company does and its size
- Recent news or funding
- Whether they seem like a good sales prospect

Then score the lead from 1-10 based on:
- 1-3: Poor fit (tiny company, no budget signals, wrong industry)
- 4-6: Medium fit (possible prospect, needs more research)
- 7-10: Strong fit (growing company, clear budget, right industry)

Always end with:
SCORE: X/10
REASON: (2-3 sentence explanation)
"""),
        ("human", "Qualify this lead — Name: {name}, Company: {company}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- Webhook endpoint ---
@app.post("/qualify")
async def qualify_lead(lead: Lead):
    print(f"\n{'='*50}")
    print(f"Qualifying lead: {lead.name} @ {lead.company}")
    print(f"{'='*50}\n")

    agent_executor = build_agent()

    result = agent_executor.invoke({
        "name": lead.name,
        "company": lead.company,
    })

    print(f"\n{'='*50}")
    print("FINAL RESULT:")
    print(result["output"])
    print(f"{'='*50}\n")

    return {
        "lead": lead.name,
        "company": lead.company,
        "result": result["output"]
    }

# --- Health check ---
@app.get("/")
def root():
    return {"status": "Lead qualifier agent is running"}