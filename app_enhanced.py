"""
Enhanced AI Shield Security Auditor with production features
- Error handling and logging
- Security validation
- Health monitoring
- Performance optimization
"""

import os
import json
import datetime
import importlib
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import core modules
from core.utils import load_yaml
from core.detectors import detect_environment
from core.schema import AuditReport, UserEnvironment
from core.report import generate_pdf
from core.logging_config import setup_logging, get_logger
from core.security import SecurityValidator, RateLimiter, redact_sensitive_info
from core.health import get_health_status, check_dependencies, check_llm_providers

# Setup logging
log_level = os.getenv("LOG_LEVEL", "INFO")
setup_logging(log_level)
logger = get_logger(__name__)

# Initialize security components
validator = SecurityValidator()
rate_limiter = RateLimiter(max_requests=50, window_seconds=60)

# --- Page config ---
st.set_page_config(
    page_title="AI Shield Auditor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for better UI ---
st.markdown("""
<style>
    .stAlert {
        border-radius: 10px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .success-box {
        background-color: #10b981;
        padding: 15px;
        border-radius: 8px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("🛡️ AI Shield Security Auditor")
st.caption("Self-guided audit for LLM/chatbot security, privacy, and governance")

# --- Error handling wrapper ---
def safe_execute(func, error_message="An error occurred"):
    """Wrapper for safe execution with error handling"""
    try:
        return func()
    except Exception as e:
        logger.error(f"{error_message}: {str(e)}", exc_info=True)
        st.error(f"{error_message}. Please check the logs or contact support.")
        return None

# --- Load templates with error handling ---
try:
    QUESTIONS = load_yaml("templates/questions.yml")
    PROVIDERS = load_yaml("templates/providers.yml")
    SECTIONS = list(QUESTIONS["sections"].keys())
    logger.info("Templates loaded successfully", sections=len(SECTIONS))
except Exception as e:
    logger.error("Failed to load templates", error=str(e))
    st.error("⚠️ Failed to load configuration templates. Please check the installation.")
    st.stop()

# --- Session State ---
if "env" not in st.session_state:
    st.session_state.env = None
if "answers" not in st.session_state:
    st.session_state.answers = {s: {} for s in SECTIONS}
if "results" not in st.session_state:
    st.session_state.results = None
if "audit_count" not in st.session_state:
    st.session_state.audit_count = 0

# --- Sidebar: Environment & Settings ---
with st.sidebar:
    st.header("⚙️ Setup")

    # Add version and health status
    with st.expander("ℹ️ System Info"):
        health = get_health_status()
        st.json(health)

        deps = check_dependencies()
        st.write("**Dependencies:**")
        for dep, status in deps.items():
            st.write(f"{'✅' if status else '❌'} {dep}")

        llm_status = check_llm_providers()
        st.write("**LLM Providers:**")
        st.write(f"Active: {llm_status['active_provider']}")
        st.write(f"OpenAI: {'✅' if llm_status['openai'] else '❌'}")
        st.write(f"Anthropic: {'✅' if llm_status['anthropic'] else '❌'}")

    st.markdown("---")

    # Environment configuration
    platform = st.selectbox(
        "Platform",
        ["OpenAI", "Azure", "Anthropic", "Google", "Custom"],
        index=0,
        help="Select your LLM platform"
    )

    agent_mode = st.radio(
        "Agent Mode enabled?",
        ["Yes", "No"],
        index=1,
        help="Are you using autonomous agents?"
    ) == "Yes"

    connectors = st.multiselect(
        "Connectors",
        ["Slack", "Google Drive", "Jira", "SharePoint", "Custom API"],
        help="Select all integrations used"
    )

    vector_store = st.text_input(
        "Vector Store",
        placeholder="e.g., Pinecone, FAISS, Chroma",
        help="Vector database for RAG (if applicable)"
    )

    sensitive_data_types = st.multiselect(
        "Sensitive Data Types",
        ["PII", "PHI", "PCI", "Secrets", "Proprietary"],
        help="Types of sensitive data in your system"
    )

    if st.button("🔒 Detect & Lock Environment", use_container_width=True):
        def detect_env():
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

            logger.info(
                "Environment locked",
                platform=env_dict["platform"],
                agent_mode=env_dict["agent_mode"],
                connectors=len(connectors)
            )

            st.success(
                f"✅ Environment locked:\n\n"
                f"**Platform:** {env_dict['platform']}\n\n"
                f"**Agent Mode:** {env_dict['agent_mode']}\n\n"
                f"**Connectors:** {', '.join(connectors) or 'None'}"
            )

        safe_execute(detect_env, "Failed to detect environment")

    # Show current environment
    if st.session_state.env:
        st.markdown("---")
        st.markdown("**Current Environment:**")
        st.info(
            f"🖥️ {st.session_state.env.platform}\n\n"
            f"{'🤖 Agent Mode' if st.session_state.env.agent_mode else '📝 Standard Mode'}"
        )

# --- Main: Audit Wizard ---
st.markdown("---")

# Progress indicator
if st.session_state.env:
    answered = sum(len(answers) for answers in st.session_state.answers.values())
    total = sum(len(QUESTIONS["sections"][s]["questions"]) for s in SECTIONS)
    progress = answered / total if total > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Questions Answered", f"{answered}/{total}")
    with col2:
        st.metric("Progress", f"{int(progress * 100)}%")
    with col3:
        st.metric("Audits Run", st.session_state.audit_count)

    st.progress(progress)

st.markdown("---")

# Audit questions in tabs
tabs = st.tabs([f"{i+1}. {s}" for i, s in enumerate(SECTIONS)])

for i, section in enumerate(SECTIONS):
    with tabs[i]:
        st.subheader(f"📋 {section}")

        # Load questions
        qlist = QUESTIONS["sections"][section]["questions"]

        # Inject questions into audit class module
        module_name = section.lower().replace(" & ", "_").replace(" ", "_")

        try:
            mod = importlib.import_module(f"audits.{module_name}")
            setattr(mod, "template_questions", qlist)
            class_name = "".join([w.capitalize() for w in module_name.split("_")]) + "Audit"
            audit_cls = getattr(mod, class_name)()
        except Exception as e:
            logger.error(f"Failed to load audit module: {module_name}", error=str(e))
            st.error(f"⚠️ Failed to load {section} audit module")
            continue

        # Render questions in a cleaner layout
        st.markdown(f"**Answer {len(qlist)} questions honestly:**")

        for idx, q in enumerate(qlist):
            # Clean question text
            question_text = q.replace(" (Yes/No/Unknown)", "")

            val = st.radio(
                question_text,
                ["Unknown", "Yes", "No"],
                key=f"{section}-{idx}",
                horizontal=True
            )
            st.session_state.answers[section][q] = val

            if idx < len(qlist) - 1:
                st.markdown("---")

        st.info("💡 Tip: Answer honestly. 'Unknown' responses are acceptable and will generate targeted recommendations.")

# --- Run Audit ---
st.markdown("---")
st.markdown("### 📊 Generate Report")

col1, col2, col3, col4 = st.columns(4)

with col1:
    run = st.button("▶️ Run Audit", use_container_width=True, type="primary")

with col2:
    export_json = st.button("💾 Export JSON", use_container_width=True)

with col3:
    export_pdf = st.button("📄 Export PDF", use_container_width=True)

with col4:
    clear = st.button("🔄 Reset", use_container_width=True)

if clear:
    st.session_state.answers = {s: {} for s in SECTIONS}
    st.session_state.results = None
    st.rerun()

if run:
    if not st.session_state.env:
        st.error("⚠️ Please detect & lock your environment in the sidebar first.")
        st.stop()

    # Rate limiting check (using session as identifier)
    session_id = st.runtime.scriptrunner.script_run_context.get_script_run_ctx().session_id

    if not rate_limiter.is_allowed(session_id):
        st.error("⚠️ Rate limit exceeded. Please wait before running another audit.")
        logger.warning("Rate limit exceeded", session_id=redact_sensitive_info(session_id))
        st.stop()

    with st.spinner("🔍 Running comprehensive security audit..."):
        def run_audit():
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

            st.session_state.results = report
            st.session_state.audit_count += 1

            logger.info(
                "Audit completed",
                overall_score=report.overall_score(),
                overall_risk=report.overall_risk(),
                categories=len(results)
            )

            # Display results
            st.success("✅ Audit completed successfully!")

            # Overall metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Overall Score", f"{report.overall_score()}/10")
            with col2:
                risk_color = {"Low": "🟢", "Moderate": "🟡", "High": "🔴"}
                st.metric("Risk Level", f"{risk_color.get(report.overall_risk(), '⚪')} {report.overall_risk()}")
            with col3:
                total_findings = sum(len(r.findings) for r in results)
                st.metric("Total Findings", total_findings)

            # Detailed results table
            st.markdown("### 📈 Detailed Results")
            df = pd.DataFrame([{
                "Category": r.category,
                "Score": f"{r.score}/10",
                "Risk": r.risk_level,
                "Findings": len(r.findings),
                "Recommendations": len(r.recommendations)
            } for r in results])

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            # Expandable findings
            st.markdown("### 🔍 Findings & Recommendations")
            for result in results:
                with st.expander(f"{result.category} - {result.risk_level} Risk"):
                    if result.findings:
                        st.markdown("**Findings:**")
                        for finding in result.findings:
                            severity_emoji = {
                                "High": "🔴",
                                "Medium": "🟡",
                                "Low": "🟢"
                            }
                            st.markdown(
                                f"{severity_emoji.get(finding.severity, '⚪')} "
                                f"**{finding.severity}:** {finding.text}"
                            )

                    if result.recommendations:
                        st.markdown("**Recommendations:**")
                        for rec in result.recommendations:
                            st.markdown(f"✅ {rec.text} *(Effort: {rec.effort})*")

        safe_execute(run_audit, "Failed to run audit")

if export_json:
    if not st.session_state.results:
        st.error("⚠️ Run the audit first.")
    else:
        def export_json_report():
            payload = st.session_state.results.model_dump()
            payload["summary"]["overall_score"] = st.session_state.results.overall_score()
            payload["summary"]["overall_risk"] = st.session_state.results.overall_risk()
            js = json.dumps(payload, indent=2)

            st.download_button(
                "📥 Download JSON Report",
                js,
                file_name=f"ai_shield_audit_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

            logger.info("JSON report exported")

        safe_execute(export_json_report, "Failed to export JSON")

if export_pdf:
    if not st.session_state.results:
        st.error("⚠️ Run the audit first.")
    else:
        def export_pdf_report():
            payload = st.session_state.results
            payload.summary["overall_score"] = str(payload.overall_score())
            payload.summary["overall_risk"] = payload.overall_risk()

            path = f"reports/audit_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf_path = generate_pdf(payload, path)

            with open(pdf_path, "rb") as f:
                st.download_button(
                    "📥 Download PDF Report",
                    f,
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf",
                    use_container_width=True
                )

            logger.info("PDF report exported", path=pdf_path)

        safe_execute(export_pdf_report, "Failed to export PDF")

# --- Footer ---
st.markdown("---")
st.caption(
    "🛡️ AI Shield Auditor v1.0 | "
    "Checklist-first design | "
    "Optional LLM enhancements | "
    "[Documentation](https://github.com/your-repo) | "
    "[Report Issues](https://github.com/your-repo/issues)"
)
