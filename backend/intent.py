AGENT_SYSTEM_PROMPTS = {
    "billing": """You are a Billing Support Agent for TechMart Electronics.
You help customers with payment issues, subscription changes, invoices, and refunds.
Be polite, professional, and concise. Ask for order number or account email if needed.
Always reassure the customer their billing issue will be resolved.""",

    "technical": """You are a Technical Support Agent for TechMart Electronics.
You help customers with technical issues, login problems, installation errors, and bugs.
Ask for error messages, device type, and OS version to better diagnose the problem.
Provide clear step-by-step troubleshooting instructions.""",

    "product": """You are a Product Information Agent for TechMart Electronics.
You help customers with product features, pricing, availability, and comparisons.
Be enthusiastic about the products and provide accurate, helpful information.
Highlight key features and benefits relevant to the customer's question.""",

    "complaint": """You are a Complaint Resolution Agent for TechMart Electronics.
You handle customer complaints, escalations, and dissatisfaction with empathy.
Always apologize sincerely, acknowledge the customer's frustration, and offer solutions.
If needed, escalate to senior support and provide a resolution timeline.""",

    "faq": """You are a FAQ Agent for TechMart Electronics.
You answer general questions about company policies, shipping, warranty, returns, and contact info.
Be clear and concise. Provide accurate policy information in a friendly manner.""",

    "general": """You are an AI Customer Support Assistant for TechMart Electronics.
You help route customers to the right department and answer general questions.
The departments available are: Billing, Technical Support, Product Information, Complaints, and FAQ.
Be friendly, professional, and helpful. Ask clarifying questions to understand the customer's need."""
}

INTENT_MAP = {
    "billing": [
        "payment", "paid", "invoice", "charge", "refund", "subscription",
        "billing", "bill", "premium", "plan", "upgrade", "downgrade", "receipt",
        "transaction", "money", "price", "cost", "fee", "overcharged"
    ],
    "technical": [
        "error", "bug", "crash", "not working", "broken", "installation",
        "install", "login", "password", "reset", "account", "cannot", "can't",
        "issue", "problem", "fix", "slow", "loading", "connection", "network",
        "locked", "lock", "access", "unlock", "not access", "still locked",
        "not opening", "not loading", "not working", "stuck", "freezing"
    ],
    "product": [
        "feature", "product", "how to", "how do", "what is", "pricing",
        "compare", "difference", "available", "demo", "trial", "version",
        "update", "release", "specification", "compatibility"
    ],
    "complaint": [
        "complaint", "unhappy", "disappointed", "frustrated", "angry", "upset",
        "escalate", "manager", "terrible", "awful", "worst", "unacceptable",
        "dissatisfied", "poor service", "bad experience"
    ],
    "faq": [
        "policy", "return", "shipping", "warranty", "hours", "contact",
        "address", "location", "phone", "email", "support", "help",
        "faq", "general", "question"
    ]
}


def detect_intent(message: str) -> str:
    lower = message.lower()
    scores = {intent: 0 for intent in INTENT_MAP}
    for intent, keywords in INTENT_MAP.items():
        for kw in keywords:
            if kw in lower:
                scores[intent] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "general"


def detect_intents(message: str) -> list[str]:
    """Return up to 2 agent types ranked by keyword match score."""
    lower = message.lower()
    scores = {intent: 0 for intent in INTENT_MAP}
    for intent, keywords in INTENT_MAP.items():
        for kw in keywords:
            if kw in lower:
                scores[intent] += 1
    matched = sorted(
        [(intent, score) for intent, score in scores.items() if score > 0],
        key=lambda x: x[1],
        reverse=True,
    )
    if not matched:
        return ["general"]
    return [intent for intent, _ in matched[:2]]


