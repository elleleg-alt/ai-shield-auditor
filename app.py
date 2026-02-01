
import os
import json
import datetime
import importlib
import pandas as pd
import streamlit as st

from core.utils import load_yaml
from core.detectors import detect_environment
from core.schema import AuditReport, UserEnvironment
from core.report import generate_pdf

# --- Page config ---
st.set_page_config(page_title="AI Shield Auditor", page_icon="🛡️", layout="wide")

st.title("🛡️ AI Shield Security Auditor")
st.caption("Self-guided audit for LLM/chatbot security, privacy, and governance")

# --- Load templates ---
QUESTIONS = load_yaml("templates/questions.yml")
PROVIDERS = load_yaml("templates/providers.yml")

SECTIONS = list(QUESTIONS["sections"].keys())

# --- Session State ---
if "env" not in st.session_state:
    st.session_state.env = None
if "answers" not in st.session_state:
    st.session_state.answers = {s: {} for s in SECTIONS}
if "results" not in st.session_state:
    st.session_state.results = None

# --- Sidebar: Environment ---
with st.sidebar:
    st.header("Setup")
    platform = st.selectbox("Platform", ["OpenAI", "Azure", "Anthropic", "Google", "Custom"], index=0)
    agent_mode = st.radio("Agent Mode enabled?", ["Yes", "No"], index=1) == "Yes"
    connectors = st.multiselect("Connectors", ["Slack", "Google Drive", "Jira", "SharePoint", "Custom API"])
    vector_store = st.text_input("Vector Store (e.g., Pinecone, FAISS, Chroma)")
    sensitive_data_types = st.multiselect("Sensitive Data Types", ["PII", "PHI", "PCI", "Secrets", "Proprietary"])

    if st.button("Detect & Lock Environment"):
        env_dict = detect_environment({
            "platform": platform,
            "agent_mode": agent_mode,
            "connectors": connectors,
            "vector_store": vector_store
        })
        st.session_state.env = UserEnvironment(
            platform=env_dict["platform"],
            agent_mode=env_dict["agent_mode"],
            connectors=env_dict["connectors"],
            vector_store=env_dict["vector_store"],
            sensitive_data_types=sensitive_data_types
        )
        st.success(f"Environment locked: {env_dict['platform']} • Agent Mode={env_dict['agent_mode']} • Connectors={', '.join(connectors) or 'None'}")

# --- Main: Audit Wizard ---
tabs = st.tabs(SECTIONS)

for i, section in enumerate(SECTIONS):
    with tabs[i]:
        st.subheader(section)

        # Load questions
        qlist = QUESTIONS["sections"][section]["questions"]

        # Inject questions into audit class module before instantiation
        module_name = section.lower().replace(" & ", "_").replace(" ", "_")
        mod = importlib.import_module(f"audits.{module_name}")
        setattr(mod, "template_questions", qlist)
        # Find class in module by convention
        class_name = "".join([w.capitalize() for w in module_name.split("_")]) + "Audit"
        audit_cls = getattr(mod, class_name)()

        # Render questions
        cols = st.columns(2)
        for idx, q in enumerate(qlist):
            with cols[idx % 2]:
                val = st.selectbox(q, ["Unknown", "Yes", "No"], key=f"{section}-{idx}")
                st.session_state.answers[section][q] = val

        st.info("Tip: Answer honestly. Unknowns are fine; you'll get targeted recommendations.")

# --- Run Audit ---
st.markdown("---")
col1, col2, col3 = st.columns([1,1,1])

with col1:
    run = st.button("▶️ Run Audit")
with col2:
    export_json = st.button("💾 Export JSON")
with col3:
    export_pdf = st.button("📄 Export PDF")

if run:
    if not st.session_state.env:
        st.error("Please detect & lock your environment in the sidebar first.")
        st.stop()

    # Evaluate each section
    results = []
    for section in SECTIONS:
        module_name = section.lower().replace(" & ", "_").replace(" ", "_")
        mod = importlib.import_module(f"audits.{module_name}")
        class_name = "".join([w.capitalize() for w in module_name.split("_")]) + "Audit"
        audit_cls = getattr(mod, class_name)()

        answers = st.session_state.answers[section]
        res = audit_cls.evaluate(answers)
        results.append(res)

    # Build report
    report = AuditReport(
        user_environment=st.session_state.env,
        audit_categories=results,
        summary={
            "overall_score": "auto",
            "overall_risk": "auto",
            "report_generated": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    )

    # Display overview table
    df = pd.DataFrame([{
        "Category": r.category,
        "Score": r.score,
        "Risk": r.risk_level,
        "Findings": "; ".join([f.text for f in r.findings]) or "-",
        "Recommendations": "; ".join([r2.text for r2 in r.recommendations]) or "-"
    } for r in results])
    st.dataframe(df, use_container_width=True)

    st.session_state.results = report

if export_json:
    if not st.session_state.results:
        st.error("Run the audit first.")
    else:
        payload = st.session_state.results.model_dump()
        payload["summary"]["overall_score"] = st.session_state.results.overall_score()
        payload["summary"]["overall_risk"] = st.session_state.results.overall_risk()
        js = json.dumps(payload, indent=2)
        st.download_button("Download JSON", js, file_name="ai_shield_audit.json", mime="application/json")

if export_pdf:
    if not st.session_state.results:
        st.error("Run the audit first.")
    else:
        payload = st.session_state.results
        payload.summary["overall_score"] = str(payload.overall_score())
        payload.summary["overall_risk"] = payload.overall_risk()
        path = f"reports/audit_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = generate_pdf(payload, path)
        with open(pdf_path, "rb") as f:
            st.download_button("Download PDF", f, file_name=os.path.basename(pdf_path), mime="application/pdf")

st.markdown("---")
st.caption("Starter kit • Checklist-first design • Optional LLM enhancements can be added in core/scoring.py and prompts/")
