from langchain_core.tools import tool
from langchain.agents import create_agent

from agents.common import llm
from intent import AGENT_SYSTEM_PROMPTS


@tool
def lookup_invoice(order_id: str) -> str:
    """Look up invoice and payment details for a given order ID."""
    return f"Invoice for order {order_id}: amount $49.99, status PAID, billed on 2026-06-01."


@tool
def check_subscription_status(email: str) -> str:
    """Check the subscription/plan status for a customer's account email."""
    return f"Account {email} is on the Premium plan, active until 2026-12-31."


@tool
def process_refund(order_id: str, reason: str) -> str:
    """Process a refund for an order given a reason. Returns confirmation and ETA."""
    return f"Refund for order {order_id} has been initiated (reason: {reason}). Funds arrive in 5-7 business days."


BILLING_TOOLS = [lookup_invoice, check_subscription_status, process_refund]

billing_agent = create_agent(llm, BILLING_TOOLS, system_prompt=AGENT_SYSTEM_PROMPTS["billing"])
