from langchain_core.tools import tool
from langchain.agents import create_agent

from agents.common import llm
from intent import AGENT_SYSTEM_PROMPTS


@tool
def search_product_catalog(query: str) -> str:
    """Search the product catalog by keyword and return matching products."""
    return f"Found products matching '{query}': ProBook X1 ($899), ProBook X2 ($1199), ProBook Lite ($599)."


@tool
def get_product_price(product_name: str) -> str:
    """Get the current price and availability for a named product."""
    return f"{product_name} is priced at $899 and is currently in stock."


@tool
def compare_products(product_a: str, product_b: str) -> str:
    """Compare two products by key specs (price, features, availability)."""
    return (
        f"{product_a} vs {product_b}: {product_a} offers a longer battery life and lower price, "
        f"while {product_b} offers a faster processor and larger display."
    )


PRODUCT_TOOLS = [search_product_catalog, get_product_price, compare_products]

product_agent = create_agent(llm, PRODUCT_TOOLS, system_prompt=AGENT_SYSTEM_PROMPTS["product"])
