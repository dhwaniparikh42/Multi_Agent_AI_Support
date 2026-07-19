import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7,
)


def to_langchain_history(conversation_history: list = None) -> list:
    if not conversation_history:
        return []
    messages = []
    for msg in conversation_history[-6:]:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
    return messages


def run_agent(agent, message: str, conversation_history: list = None) -> str:
    history = to_langchain_history(conversation_history)
    result = agent.invoke({"messages": history + [HumanMessage(content=message)]})
    return result["messages"][-1].content
