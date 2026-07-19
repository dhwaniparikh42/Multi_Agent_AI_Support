from langchain.agents import create_agent

from agents.common import llm
from intent import AGENT_SYSTEM_PROMPTS

general_agent = create_agent(llm, [], system_prompt=AGENT_SYSTEM_PROMPTS["general"])
