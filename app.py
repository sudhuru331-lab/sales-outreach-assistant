import streamlit as st
from dotenv import load_dotenv
from anthropic import Anthropic
import re
import random

load_dotenv()
client = Anthropic()

st.set_page_config(page_title="Sales Outreach Assistant", page_icon="✉️", layout="wide")

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #0B1220;
    color: #E7EAF0;
}

.app-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
}
.app-badge {
    width: 38px; height: 38px; border-radius: 9px;
    background: #F2A93B;
    display: flex; align-items: center; justify-content: center;
    font-family: 'IBM Plex Mono', monospace; font-weight: 700;
    color: #412402; font-size: 15px;
}
.app-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 22px; font-weight: 600; color: #E7EAF0; margin: 0;
}
.app-subtitle {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; letter-spacing: 1.5px; color: #8FA0BF; margin: 0;
}

.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; letter-spacing: 1.5px; color: #8FA0BF;
    margin: 18px 0 8px 0; text-transform: uppercase;
}

div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {
    background-color: #131B2E !important;
    color: #E7EAF0 !important;
    border: 1px solid #2A3550 !important;
    border-radius: 8px !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: #131B2E !important;
    border: 1px solid #2A3550 !important;
    border-radius: 8px !important;
    color: #E7EAF0 !important;
}

.stButton button {
    background-color: #F2A93B !important;
    color: #412402 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 10px 22px !important;
}
.stButton button:hover {
    background-color: #D98A1F !important;
    color: #FAEEDA !important;
}

.route-card {
    background: #1B2438;
    border: 1px solid #2A3550;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 16px;
}
.route-header {
    background: #182033;
    padding: 8px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #2A3550;
}
.route-id {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; color: #F2A93B; letter-spacing: 0.5px;
}
.route-tag {
    font-size: 10px; background: #412402; color: #FAC775;
    padding: 3px 10px; border-radius: 20px;
    font-family: 'IBM Plex Mono', monospace;
}
.route-body { padding: 16px; }
.route-subject {
    font-weight: 600; font-size: 15px; margin-bottom: 10px; color: #E7EAF0;
}
.route-text {
    font-size: 13.5px; color: #C3CCDE; line-height: 1.65; white-space: pre-wrap;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="app-header">
    <div class="app-badge">SO</div>
    <div>
        <p class="app-title">Sales Outreach Assistant</p>
        <p class="app-subtitle">DISPATCH CONSOLE</p>
    </div>
</div>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

# ---------- Lead intake ----------
st.markdown('<p class="section-label">Lead manifest</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    lead_name = st.text_input("Lead's Name", placeholder="e.g. Jamie Chen")
    lead_company = st.text_input("Lead's Company", placeholder="e.g. Acme Logistics")
with col2:
    lead_title = st.text_input("Lead's Job Title", placeholder="e.g. VP of Operations")
    tone = st.selectbox("Email Tone", ["Friendly & casual", "Professional & direct", "Consultative & insight-led"])

context_notes = st.text_area(
    "Anything you know about them or their company",
    placeholder="e.g. They recently raised a Series B, use manual freight tracking, posted about scaling challenges on LinkedIn"
)

num_variants = st.slider("How many variants to generate?", 1, 3, 2)

generate = st.button("Generate Email", type="primary")

def parse_variants(text):
    blocks = re.split(r"VARIANT\s+\d+", text)
    blocks = [b.strip() for b in blocks if b.strip()]
    parsed = []
    for b in blocks:
        subj_match = re.search(r"Subject:\s*(.+)", b)
        subject = subj_match.group(1).strip() if subj_match else "No subject"
        body = re.sub(r"Subject:\s*.+", "", b, count=1).strip()
        parsed.append({"subject": subject, "body": body})
    return parsed

def render_variants(variants, key_prefix):
    for i, v in enumerate(variants, start=1):
        route_id = f"RTE-{random.randint(1000,9999)}-{chr(64+i)}"
        st.markdown(f"""
        <div class="route-card">
            <div class="route-header">
                <span class="route-id">{route_id}</span>
                <span class="route-tag">VARIANT {i}</span>
            </div>
            <div class="route-body">
                <div class="route-subject">{v['subject']}</div>
                <div class="route-text">{v['body']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.text_area(f"Copy variant {i}", value=f"Subject: {v['subject']}\n\n{v['body']}", height=160, key=f"{key_prefix}_{i}")

if generate:
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
- End with a clear, low-friction call to action
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

        variants = parse_variants(result_text)

        st.session_state.history.insert(0, {
            "lead": f"{lead_name} ({lead_company})",
            "variants": variants
        })

        st.markdown('<p class="section-label">Generated emails</p>', unsafe_allow_html=True)
        render_variants(variants, "current")

if len(st.session_state.history) > 1:
    st.markdown('<p class="section-label">Previous generations (this session)</p>', unsafe_allow_html=True)
    for idx, entry in enumerate(st.session_state.history[1:], start=1):
        with st.expander(entry["lead"]):
            render_variants(entry["variants"], f"hist{idx}")