from langchain_core.tools import tool
from langchain.agents import create_agent

from agents.common import llm
from intent import AGENT_SYSTEM_PROMPTS


@tool
def check_system_status(service: str) -> str:
    """Check whether a given service or feature is currently experiencing an outage."""
    return f"{service} is currently operational. No known incidents reported."


@tool
def get_password_reset_link(email: str) -> str:
    """Generate a password reset link/instructions for the given account email."""
    return f"A password reset link has been sent to {email}. It expires in 30 minutes."


@tool
def lookup_error_code(error_code: str) -> str:
    """Look up the meaning and troubleshooting steps for a known error code."""
    return (
        f"Error {error_code}: usually caused by an outdated app version or corrupted cache. "
        "Try updating the app, then clearing the cache and restarting."
    )


TECHNICAL_TOOLS = [check_system_status, get_password_reset_link, lookup_error_code]

technical_agent = create_agent(llm, TECHNICAL_TOOLS, system_prompt=AGENT_SYSTEM_PROMPTS["technical"])
