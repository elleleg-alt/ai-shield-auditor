# 🛡️ AI Shield Auditor

> **Production-ready security auditing platform for LLM/AI applications**

A comprehensive, self-guided security auditor for AI/LLM systems. Evaluates security posture across identity, data governance, RAG privacy, integrations, model safety, compliance, and deployment.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.39.0-red.svg)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## ✨ Features

- 🎯 **Guided Security Audit** - Step-by-step questionnaire across 7 security domains
- 📊 **Comprehensive Reporting** - PDF and JSON export with actionable recommendations
- 🔐 **Production-Ready** - Security hardened, rate limited, with structured logging
- 🐳 **Deploy Anywhere** - Docker, Cloud Run, ECS, Streamlit Cloud, and more
- 🤖 **LLM-Enhanced** - Optional AI-powered analysis (OpenAI, Anthropic)
- 📈 **Real-time Scoring** - Instant security posture assessment
- 🔍 **7 Security Domains** - Identity, Data Governance, RAG Privacy, Integrations, Model Safety, Compliance, Deployment

---

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Clone repository
git clone <your-repo-url>
cd ai-shield-auditor

# Run setup script
chmod +x scripts/setup-local.sh
./scripts/setup-local.sh

# Activate environment
source .venv/bin/activate

# Run application
streamlit run app_enhanced.py
```

Visit `http://localhost:8501`

### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys (optional)

# Run application
streamlit run app.py
```

### Option 3: Docker

```bash
# Using docker-compose (easiest)
docker-compose up -d

# OR build and run manually
docker build -t ai-shield-auditor .
docker run -p 8501:8501 ai-shield-auditor
```

Visit `http://localhost:8501`

---

## 📋 What You Get

### Core Features
- ✅ **Interactive Audit Wizard** - User-friendly Streamlit interface
- ✅ **7 Security Categories** - Comprehensive coverage of AI security domains
- ✅ **Instant Scoring** - Real-time security posture assessment
- ✅ **PDF Reports** - Professional audit reports
- ✅ **JSON Export** - CI/CD integration ready
- ✅ **LLM Mode (Optional)** - AI-enhanced findings and recommendations

### Production Features (app_enhanced.py)
- ✅ **Error Handling** - Graceful error recovery
- ✅ **Structured Logging** - JSON logs for production
- ✅ **Rate Limiting** - DDoS protection
- ✅ **Input Validation** - Security hardened
- ✅ **Health Monitoring** - Built-in health checks
- ✅ **Security Headers** - Industry-standard HTTP headers

---

## 📁 Project Structure

```
ai-shield-auditor/
├── app.py                      # Original application
├── app_enhanced.py             # Production-ready version ⭐
├── Dockerfile                  # Container definition
├── docker-compose.yml          # Orchestration
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
│
├── core/                       # Core modules
│   ├── schema.py              # Data models
│   ├── scoring.py             # Scoring logic
│   ├── report.py              # PDF generation
│   ├── detectors.py           # Platform detection
│   ├── utils.py               # Utilities
│   ├── logging_config.py      # Logging setup ⭐
│   ├── security.py            # Security utilities ⭐
│   └── health.py              # Health checks ⭐
│
├── audits/                     # Audit modules
│   ├── identity.py            # Identity & Access
│   ├── data_governance.py     # Data Governance
│   ├── rag_privacy.py         # RAG Privacy
│   ├── integration_security.py # Integrations
│   ├── model_safety.py        # Model Safety
│   ├── compliance.py          # Compliance
│   └── deployment.py          # Deployment Security
│
├── templates/                  # Configuration
│   ├── questions.yml          # Audit questions
│   └── providers.yml          # Platform configs
│
├── scripts/                    # Deployment scripts ⭐
│   ├── setup-local.sh
│   ├── deploy-docker.sh
│   └── deploy-streamlit-cloud.sh
│
├── .github/workflows/          # CI/CD ⭐
│   └── deploy.yml
│
└── docs/                       # Documentation ⭐
    ├── DEPLOYMENT.md
    ├── PRODUCTION_CHECKLIST.md
    └── IMPROVEMENTS_SUMMARY.md
```

⭐ = New production-ready additions

---

## 🔧 Configuration

### Environment Variables

Create `.env` file (copy from `.env.example`):

```env
# LLM Provider (optional)
LLM_PROVIDER=openai          # Options: openai, anthropic, none
OPENAI_API_KEY=sk-...        # If using OpenAI
ANTHROPIC_API_KEY=sk-ant-... # If using Anthropic

# Application Settings
LOG_LEVEL=INFO               # Options: DEBUG, INFO, WARNING, ERROR
```

### Modes

**Checklist Mode (Default)**
- No API keys required
- Deterministic scoring
- Fast and free
- Ideal for getting started

**LLM Mode (Optional)**
- Requires API keys
- AI-enhanced analysis
- Smarter recommendations
- Better contextual insights

---

## 🎯 Security Domains

1. **Identity & Access Control**
   - MFA enforcement
   - API key management
   - IAM configuration
   - Key rotation policies

2. **Data Governance**
   - Data classification
   - Encryption (at rest/transit)
   - Data retention
   - PII/PHI handling

3. **RAG Privacy**
   - Document-level ACLs
   - Retrieval security
   - Multi-tenant isolation
   - Cache policies

4. **Integration Security**
   - OAuth scopes
   - API restrictions
   - Webhook verification
   - Third-party connectors

5. **Model Safety**
   - Prompt injection testing
   - Jailbreak prevention
   - Tool call restrictions
   - Safety filters

6. **Compliance**
   - GDPR/HIPAA/FERPA
   - Audit trails
   - Privacy impact assessments
   - Incident response

7. **Deployment Security**
   - Network isolation
   - Container security
   - CI/CD scanning
   - Version control

---

## 🚢 Deployment Options

| Platform | Difficulty | Cost | Best For |
|----------|-----------|------|----------|
| [Streamlit Cloud](DEPLOYMENT.md#streamlit-cloud) | ⭐ Easy | Free | Quick demos |
| [Docker Local](DEPLOYMENT.md#docker-deployment) | ⭐⭐ Medium | Free | Development |
| [Google Cloud Run](DEPLOYMENT.md#google-cloud-run) | ⭐⭐ Medium | ~$5/mo | Serverless |
| [Railway](DEPLOYMENT.md#railway) | ⭐⭐ Medium | Free tier | Modern apps |
| [Render](DEPLOYMENT.md#render) | ⭐⭐ Medium | $7/mo | Git-based |
| [AWS ECS](DEPLOYMENT.md#aws-ecsfargate) | ⭐⭐⭐ Hard | ~$30/mo | Enterprise |

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

## 📚 Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete deployment guide for all platforms
- **[PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md)** - Pre-deployment checklist
- **[IMPROVEMENTS_SUMMARY.md](IMPROVEMENTS_SUMMARY.md)** - What's new and improved
- **[QUICKSTART.md](QUICKSTART.md)** - Getting started guide

---

## 🔍 Usage Example

```bash
# 1. Start the application
streamlit run app_enhanced.py

# 2. In the sidebar, configure your environment:
#    - Select platform (OpenAI, Azure, Anthropic, etc.)
#    - Enable agent mode (if applicable)
#    - Select connectors (Slack, Google Drive, etc.)
#    - Specify vector store (if using RAG)
#    - Identify sensitive data types

# 3. Click "Detect & Lock Environment"

# 4. Answer questions in each category tab

# 5. Click "Run Audit" to generate report

# 6. Export as PDF or JSON
```

---

## 🐳 Docker Commands

```bash
# Build image
docker build -t ai-shield-auditor .

# Run container
docker run -p 8501:8501 \
  -e LLM_PROVIDER=openai \
  -e OPENAI_API_KEY=sk-... \
  ai-shield-auditor

# With docker-compose
docker-compose up -d          # Start
docker-compose logs -f        # View logs
docker-compose down           # Stop

# Health check
curl http://localhost:8501/_stcore/health
```

---

## 🧪 Testing

```bash
# Test imports
python -c "from core.schema import AuditReport; print('OK')"

# Test application startup
streamlit run app.py --server.headless=true &
sleep 5
curl -f http://localhost:8501/_stcore/health
```

---

## 📊 Sample Output

After running an audit, you'll receive:

- **Overall Security Score**: 0-10 rating
- **Risk Level**: Low/Moderate/High
- **Category Breakdown**: Scores for each domain
- **Findings**: Specific security issues identified
- **Recommendations**: Actionable remediation steps
- **PDF Report**: Professional documentation
- **JSON Export**: Machine-readable for CI/CD

---

## 🔐 Security

This application follows security best practices:

- ✅ Input validation and sanitization
- ✅ Rate limiting (50 requests/minute)
- ✅ Security headers (HSTS, CSP, X-Frame-Options)
- ✅ Non-root Docker container
- ✅ Secrets via environment variables
- ✅ Sensitive data redaction in logs
- ✅ HTTPS recommended for production

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests (if applicable)
5. Submit a pull request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🆘 Support

- **Documentation**: See `DEPLOYMENT.md` and other docs
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)

---

## 🗺️ Roadmap

- [ ] Automated security testing integration
- [ ] Multi-language support
- [ ] Custom audit templates
- [ ] API-first mode
- [ ] Team collaboration features
- [ ] Continuous monitoring
- [ ] Integration with SIEM tools

---

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- OWASP for LLM security guidelines
- AI security community for best practices

---

## ⭐ Star History

If you find this useful, please consider starring the repository!

---

**Built with ❤️ for the AI security community**
