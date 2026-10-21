# LINE auto-reply bot for small businesses

Small shops in Thailand get most of their customer questions on LINE: *"what time do you open?"*, *"how much is a latte?"*, *"do you deliver?"*. When the owner is busy, those messages sit unanswered. This bot replies instantly, in Thai or English, using only the business's real information.

## How it decides what to say

```
customer message
   │
   ├─ 1. Keyword match (English + Thai)  ──►  instant, free, exact answer
   │
   ├─ 2. No match → Claude, given ONLY the business's data  ──►  natural reply
   │
   └─ 3. Claude unsure, or asked a fact it doesn't have  ──►  hand off to a human
```

- **Keywords first.** Common questions about hours, menu, delivery and location (`เปิด`, `ราคา`, `ส่ง`…) are answered straight from `business_data.json`. That costs nothing and is always correct.
- **AI fallback, with no guessing.** Anything else goes to Claude with a strict prompt: answer only from the business data, reply in the customer's language, and keep it short. If it would have to guess a price or policy, it replies `HANDOFF` instead.
- **Human handoff.** The customer is told the team will follow up, instead of getting a made-up answer. Custom orders get a clear "I'll check with the owner" rather than a polite dead end.

## Make it any business's bot

Everything specific to the business is in `business_data.json`. Swap in a real shop's hours, menu and delivery zone, add the way their customers phrase questions to `KEYWORD_MAP` in `reply_logic.py`, and it's their bot.

## Tech

`Python` · `Flask` · `LINE Messaging API (line-bot-sdk v3)` · `Claude API`

## Run it

```bash
pip install -r requirements.txt
export LINE_CHANNEL_SECRET=...        # from the LINE Developers Console
export LINE_CHANNEL_ACCESS_TOKEN=...
export ANTHROPIC_API_KEY=...
python app.py
```

Expose it with `ngrok http 5000` and set `https://<your-ngrok-url>/callback` as the webhook in the LINE Developers Console. To keep it running all the time, deploy to Railway or Render with the same three environment variables.
