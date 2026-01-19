def detect_intent(text: str) -> str:
    t = text.lower().strip()
    if "balance" in t:
        return "balance_inquiry"
    if "transfer" in t or "send" in t:
        return "fund_transfer"
    return "unknown"


def extract_entities(text: str):
    words = text.split()
    amounts = [w for w in words if w.replace(',', '').isdigit()]
    recipients = []
    for i, word in enumerate(words):
        if word.lower() in ["to", "for"] and i + 1 < len(words):
            recipients.append(words[i + 1])
    return amounts, recipients
