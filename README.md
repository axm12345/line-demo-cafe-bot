# LINE Auto-Reply Bot — Starter

A demo bot for a fake cafe. Edit `business_data.json` to make it a real
client's bot.

## How it works

1. `app.py` — receives messages from LINE, sends replies. You probably won't
   need to touch this much.
2. `reply_logic.py` — decides WHAT to say. This is the part to actually
   read, understand, and extend.
3. `business_data.json` — the "knowledge" the bot has about the business.

## Local setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Get your LINE credentials:
   - Create a LINE Official Account (free) at https://manager.line.biz
   - In the LINE Developers Console (https://developers.line.biz), find your
     Channel Secret and generate a Channel Access Token
   - Enable "Use webhook" for the channel, and turn OFF the default
     auto-reply / greeting messages (so they don't conflict with your bot)

3. Get an Anthropic API key at https://console.anthropic.com

4. Set environment variables (don't commit these anywhere):
   ```
   export LINE_CHANNEL_SECRET="your_channel_secret"
   export LINE_CHANNEL_ACCESS_TOKEN="your_access_token"
   export ANTHROPIC_API_KEY="your_api_key"
   ```

5. Run it locally:
   ```
   python app.py
   ```

6. To test locally before deploying, use ngrok to expose your local server:
   ```
   ngrok http 5000
   ```
   Then set the ngrok URL + `/callback` (e.g.
   `https://abc123.ngrok.io/callback`) as your webhook URL in the LINE
   Developers Console.

## Deploying for real (so it's always on)

Push this folder to a GitHub repo, then deploy on Railway or Render:

- Both platforms auto-detect Flask apps
- Add the three environment variables in their dashboard (never commit
  actual keys to GitHub)
- Once deployed, take the public URL they give you, add `/callback` to the
  end, and set that as your webhook URL in the LINE Developers Console

## Testing before pitching a client

Message your own bot with a range of phrasing:
- Exact keyword matches: "what time do you open"
- Rephrased versions: "when can I come by"
- Something totally unrelated: "do you sell birthday cakes"
  (should trigger a graceful handoff, not a made-up answer)

## Customizing for a real client

1. Replace everything in `business_data.json` with their real info
2. Expand `KEYWORD_MAP` in `reply_logic.py` with however their actual
   customers tend to phrase questions (ask the owner what they get asked
   most)
3. Consider adding a notification step (e.g. sending yourself or the owner
   a message) whenever a HANDOFF happens, so a human actually follows up
