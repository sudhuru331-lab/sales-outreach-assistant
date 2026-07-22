# ✉️ Sales Outreach Assistant

An AI-powered console for sales development reps that generates personalized cold outreach emails, scores lead fit, and builds a follow-up cadence — all backed by persistent history and one-click company research.

**[Try it live →](https://sales-outreach-assistant-ymakjc84ty7tu2xu4juq79.streamlit.app)**

![Main view](screenshots/main-view.png)

## What it does

**Email generation**
- Takes lead info (name, title, company, and any known context — funding news, pain points, LinkedIn activity)
- Generates multiple distinct email variants, each with a genuinely different angle or hook rather than reworded copies
- Produces a specific subject line alongside each body
- One-click copy to clipboard on every generated email
- Download any batch of variants as a `.txt` file

![Generated emails](screenshots/generated-emails.png)

**Lead Qualifier + Follow-Up Sequence**
- Scores each lead as Hot / Warm / Cold based only on the info provided, with a short grounded rationale (no invented company facts)
- Automatically builds a 3-email follow-up cadence, with pacing and tone adjusted to the qualification tier — a Hot lead gets a faster, punchier sequence than a Cold one

![Qualifier result](screenshots/qualifier-result.png)

**Company research assistant**
- Pulls a concise company summary via live web search, given just a company name (and optionally a URL)
- Auto-fills the lead context field so you're not manually researching each prospect before drafting

**Persistent history & export**
- Every generation is saved to a local SQLite database, not just session memory — history survives a refresh or restart
- Export the full history to CSV, or clear it in one click

**Reliability**
- Wraps every Claude API call in retry-with-backoff logic, so a transient `529 overloaded` error from the API doesn't crash the app — it retries automatically and tells the user what's happening

## Why I built it

As someone job searching for SDR/Customer Success roles, I wanted to understand both sides of AI-assisted sales tooling: how it can speed up a rep's workflow, and where it needs guardrails. A concrete example I caught and fixed during testing — the model would sometimes invent fake company case studies as "social proof" in an email; the prompt now explicitly forbids naming real, unverified companies as evidence.

The lead qualification and follow-up sequencing features were added to move this beyond a single-shot email generator and closer to how a real SDR workflow actually operates: score the lead first, then tailor the cadence to that score.

## Tech stack

- **Python**
- **Streamlit** — web interface, styled with custom CSS for a dark "dispatch console" theme
- **Anthropic Claude API** — email generation, lead scoring, follow-up sequencing, and company research (via the web search tool)
- **SQLite** — persistent generation history
- **python-dotenv** — environment variable management

## Running it locally

1. Clone this repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your Anthropic API key to a `.env` file: `ANTHROPIC_API_KEY=your_key_here`
4. Run: `streamlit run app.py`
