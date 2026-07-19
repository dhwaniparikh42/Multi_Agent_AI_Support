from langchain_core.tools import tool
from langchain.agents import create_agent

from agents.common import llm
from intent import AGENT_SYSTEM_PROMPTS

POLICIES = {
    "return": "Items can be returned within 30 days of delivery in original condition for a full refund.",
    "shipping": "Standard shipping takes 3-5 business days; express shipping takes 1-2 business days.",
    "warranty": "All products come with a 1-year manufacturer warranty covering defects.",
    "contact": "Support is available at support@techmart.example or 1-800-555-0100, Mon-Fri 9am-6pm.",
}


@tool
def get_policy(policy_name: str) -> str:
    """Look up a company policy by name: return, shipping, warranty, or contact."""
    key = policy_name.strip().lower()
    return POLICIES.get(key, "That policy wasn't found. Available topics: return, shipping, warranty, contact.")


@tool
def search_faq(query: str) -> str:
    """Search general FAQ knowledge base entries by keyword."""
    return f"Top FAQ match for '{query}': Please check our Help Center for step-by-step guides on this topic."


FAQ_TOOLS = [get_policy, search_faq]

faq_agent = create_agent(llm, FAQ_TOOLS, system_prompt=AGENT_SYSTEM_PROMPTS["faq"])
