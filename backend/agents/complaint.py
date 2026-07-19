from langchain_core.tools import tool
from langchain.agents import create_agent
from agents.common import llm
from intent import AGENT_SYSTEM_PROMPTS


@tool
def create_escalation_ticket(summary: str, severity: str) -> str:
    """Create an escalation ticket for a customer complaint with a severity (low/medium/high)."""
    return f"Escalation ticket ESC-{hash(summary) % 10000:04d} created (severity: {severity}). A senior agent will follow up within 24 hours."


@tool
def get_escalation_status(ticket_id: str) -> str:
    """Check the status of an existing escalation ticket by ID."""
    return f"Ticket {ticket_id} is currently in progress and assigned to the senior support team."


COMPLAINT_TOOLS = [create_escalation_ticket, get_escalation_status]

complaint_agent = create_agent(llm, COMPLAINT_TOOLS, system_prompt=AGENT_SYSTEM_PROMPTS["complaint"])
