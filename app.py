import streamlit as st
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

st.set_page_config(page_title="Sales Outreach Assistant", page_icon="✉️")

st.title("✉️ Sales Outreach Assistant")
st.write("Generate personalized cold outreach emails in seconds.")

# Keep a running history for this session
if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Lead Details")

lead_name = st.text_input("Lead's Name", placeholder="e.g. Jamie Chen")
lead_title = st.text_input("Lead's Job Title", placeholder="e.g. VP of Operations")
lead_company = st.text_input("Lead's Company", placeholder="e.g. Acme Logistics")
context_notes = st.text_area(
    "Anything you know about them or their company",
    placeholder="e.g. They recently raised a Series B, use manual freight tracking, posted about scaling challenges on LinkedIn"
)

tone = st.selectbox(
    "Email Tone",
    ["Friendly & casual", "Professional & direct", "Consultative & insight-led"]
)

num_variants = st.slider("How many variants to generate?", 1, 3, 2)

if st.button("Generate Email", type="primary"):
    if not lead_name or not lead_company:
        st.warning("Please fill in at least the lead's name and company.")
    else:
        with st.spinner("Writing your email(s)..."):
            prompt = f"""Write {num_variants} short, personalized cold outreach email(s) for a sales development rep. Each variant should take a genuinely different angle or hook, not just reworded sentences.

Lead name: {lead_name}
Lead title: {lead_title}
Lead company: {lead_company}
Context/notes: {context_notes if context_notes else "None provided"}
Tone: {tone}

Requirements for EACH variant:
- Include a short, specific subject line (not generic like "Quick question")
- Keep the body under 120 words
- No filler like "I hope this email finds you well"
- Reference the context naturally if provided
- - End with a clear, low-friction call to action
- Do NOT reference real, named companies, case studies, or statistics as social proof (e.g. do not say things like "Flexport did X"). If you want to use a proof point, keep it generic and unattributed (e.g. "companies at similar stage have cut X by Y%") rather than inventing a specific real company's story.

Format your response EXACTLY like this for each variant, with nothing else before or after:

VARIANT 1
Subject: [subject line]
[email body]

VARIANT 2
Subject: [subject line]
[email body]

(continue numbering if more variants)"""

            response = client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}]
            )

            result_text = response.content[0].text

        # Save to session history
        st.session_state.history.insert(0, {
            "lead": f"{lead_name} ({lead_company})",
            "output": result_text
        })

        st.subheader("Generated Emails")
        st.write(result_text)
        st.text_area("Copy from here:", value=result_text, height=300)

# --- Show past generations ---
if len(st.session_state.history) > 1:
    st.divider()
    st.subheader("Previous Generations (this session)")
    for i, entry in enumerate(st.session_state.history[1:], start=1):
        with st.expander(f"{entry['lead']}"):
            st.write(entry["output"])