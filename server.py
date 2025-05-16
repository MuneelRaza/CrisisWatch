from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from agent.crisis_agent import crisis_agent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Crisis Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



agent = crisis_agent()


class ChatRequest(BaseModel):
    user_input: str


class ChatResponse(BaseModel):
    response: str


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    config = {"configurable": {"thread_id": "fastapi"}}

    try:
        response = agent.invoke(
            {
                "messages": [HumanMessage(content=req.user_input)]
            },
            config
        )
        bot_msg = response["messages"][-1].content
        return {"response": bot_msg}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}
