\# ✉️ Sales Outreach Assistant



An AI-powered tool that generates personalized cold outreach emails for sales development reps. Built to speed up prospecting research and drafting while keeping messaging authentic and specific to each lead.



\*\*\[Try it live →](YOUR\_APP\_URL\_HERE)\*\*



\## What it does



\- Takes basic lead info (name, title, company, and any known context like funding news or pain points)

\- Generates multiple distinct email variants — each with a different angle/hook, not just reworded copies

\- Produces subject lines alongside email bodies

\- Keeps a session history so you can compare past generations



\## Why I built it



As someone job searching for SDR/Customer Success roles, I wanted to understand both sides of AI-assisted sales tooling — how it can speed up rep workflows, and where it needs guardrails (e.g. preventing the model from inventing fake company case studies as "social proof," which I caught and fixed during testing).



\## Tech stack



\- \*\*Python\*\*

\- \*\*Streamlit\*\* — web interface

\- \*\*Anthropic Claude API\*\* — email generation

\- \*\*python-dotenv\*\* — environment variable management



\## Running it locally



1\. Clone this repo

2\. Install dependencies: `pip install -r requirements.txt`

3\. Add your Anthropic API key to a `.env` file: `ANTHROPIC\_API\_KEY=your\_key\_here`

4\. Run: `streamlit run app.py`

