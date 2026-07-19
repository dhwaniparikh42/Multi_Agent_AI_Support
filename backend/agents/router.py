from intent import detect_intents
from agents.common import run_agent
from agents.billing import billing_agent
from agents.technical import technical_agent
from agents.product import product_agent
from agents.complaint import complaint_agent
from agents.faq import faq_agent
from agents.general import general_agent
from rag.rag_pipeline import retrieve_context

AGENTS = {
    "billing": billing_agent,
    "technical": technical_agent,
    "product": product_agent,
    "complaint": complaint_agent,
    "faq": faq_agent,
    "general": general_agent,
}

AGENT_LABELS = {
    "billing": "Billing Support",
    "technical": "Technical Support",
    "product": "Product Information",
    "complaint": "Complaint Resolution",
    "faq": "FAQ",
    "general": "General Support",
}


def _build_augmented_message(message: str) -> str:
    """
    RAG Steps 5-7:
    Retrieve relevant chunks from the knowledge base and prepend them
    to the user message so the LLM answers from real company documents.
    """
    context = retrieve_context(message, k=3)
    if not context:
        return message
    return (
        "Use the following information from TechMart's knowledge base to help answer "
        "the customer's question. Only use this information if it is relevant.\n\n"
        f"KNOWLEDGE BASE CONTEXT:\n{context}\n\n"
        f"CUSTOMER QUESTION:\n{message}"
    )


def get_agent_response(message: str, conversation_history: list = None) -> tuple[str, str]:
    agent_types = detect_intents(message)

    # RAG: augment the message with retrieved document context before calling agents
    augmented_message = _build_augmented_message(message)

    if len(agent_types) == 1:
        agent_type = agent_types[0]
        try:
            reply = run_agent(AGENTS[agent_type], augmented_message, conversation_history)
        except Exception as e:
            reply = (
                "I'm sorry, I'm having trouble connecting to the AI service right now. "
                f"Please try again in a moment.\n\nError: {str(e)}"
            )
        return agent_type, reply

    # Multiple agents matched — run each and combine their responses
    parts = []
    for agent_type in agent_types:
        try:
            reply = run_agent(AGENTS[agent_type], augmented_message, conversation_history)
            parts.append(f"**{AGENT_LABELS[agent_type]}:**\n{reply}")
        except Exception as e:
            parts.append(
                f"**{AGENT_LABELS[agent_type]}:** I'm having trouble responding right now. "
                f"Error: {str(e)}"
            )

    combined_reply = "\n\n".join(parts)
    primary_type = ",".join(agent_types)
    return primary_type, combined_reply
