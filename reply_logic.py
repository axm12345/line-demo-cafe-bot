"""
reply_logic.py

This is the part YOU should read closely and extend — it decides what the bot
actually says. Everything else in this project is plumbing to get messages
in and out of LINE; this file is the actual product.

Flow for every incoming message:
  1. Try to match it against known keywords (fast, free, always accurate).
  2. If nothing matches, fall back to an AI-generated reply that's grounded
     in the business's data (flexible, costs a fraction of a cent per call).
  3. If the AI itself isn't confident, hand off to a human instead of guessing.
"""

import json
import os
from anthropic import Anthropic

# Load the business's knowledge base once at startup.
with open("business_data.json", "r", encoding="utf-8") as f:
    BUSINESS_DATA = json.load(f)

# Keyword -> which entry in business_data.json to reply with.
# This is the part you'll customize the most per client. Add as many
# keywords as you can think of for how real customers phrase things.
KEYWORD_MAP = {
    "hours": [
        "open", "close", "hour", "time", "when are you",
        "เปิด", "ปิด", "กี่โมง", "เวลา",
    ],
    "menu": [
        "menu", "price", "cost", "how much", "coffee", "food",
        "เมนู", "ราคา", "เท่าไหร่", "เท่าไร",
    ],
    "delivery": [
        "deliver", "delivery", "grab", "line man", "send",
        "ส่ง", "เดลิเวอรี่", "แกร็บ",
    ],
    "location": [
        "where", "location", "address", "map",
        "ที่ไหน", "ที่อยู่", "แผนที่",
    ],
}

HANDOFF_MESSAGE = (
    "That's a great question — let me check with the team and get back to "
    "you shortly! 🙏"
)


def match_keywords(message: str) -> str | None:
    """
    Step 1: fast, free, 100% predictable matching.
    Returns the stored answer text if the message clearly matches a known
    topic, otherwise None (so we fall through to the AI).
    """
    message_lower = message.lower()

    for data_key, keywords in KEYWORD_MAP.items():
        if any(keyword in message_lower for keyword in keywords):
            return BUSINESS_DATA[data_key]["text"]

    return None


def ask_ai(message: str) -> str:
    """
    Step 2: fallback for anything that didn't match a keyword.
    We give the AI ONLY the business's real data as context and explicitly
    tell it not to invent anything — this is what stops it from making up
    a wrong price or a delivery zone that doesn't exist.
    """
    client = Anthropic()  # reads ANTHROPIC_API_KEY from environment

    context = "\n".join(
        f"{key}: {value['text']}"
        for key, value in BUSINESS_DATA.items()
        if isinstance(value, dict) and "text" in value
    )

    system_prompt = f"""You are a friendly customer service assistant for {BUSINESS_DATA['business_name']}, replying to customers on LINE.

Known information about the business (this is ALL you know — do not invent anything beyond this):
{context}

Rules:
- Reply in the same language the customer used (Thai, English, or a mix) — match them naturally.
- Keep replies short and warm, like a real person texting back — 1-3 sentences.
- For greetings, thanks, or general small talk (e.g. "hello", "thank you", "are you open rn"
  phrased casually), reply naturally and warmly — you don't need the business data for this.
- For any question about specific facts (prices, hours, delivery, location, policies), if the
  answer isn't clearly in the information above, do NOT guess or make something up.
  Instead, respond with exactly: HANDOFF
- For a custom order, special request, or menu suggestion (something not currently offered),
  do NOT just thank them and move on. Acknowledge it warmly, AND clearly tell them you'll check
  with the owner/chef and follow up with them directly — make it sound like a real next step is
  happening, not a polite dead end.
- Never invent prices, hours, or policies that aren't listed above.
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        system=system_prompt,
        messages=[{"role": "user", "content": message}],
    )

    reply_text = response.content[0].text.strip()

    if reply_text == "HANDOFF" or not reply_text:
        return HANDOFF_MESSAGE

    return reply_text


def generate_reply(message: str) -> str:
    """
    Main entry point — called by app.py for every incoming message.
    """
    rule_based_answer = match_keywords(message)
    if rule_based_answer:
        return rule_based_answer

    try:
        return ask_ai(message)
    except Exception as e:
        # TEMPORARY: print the real error so we can see what's failing.
        # Remove this print line once things are working.
        print(f"AI call failed: {e}")
        return HANDOFF_MESSAGE