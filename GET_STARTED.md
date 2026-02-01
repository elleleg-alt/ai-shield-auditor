# 🚀 Get Started with AI Shield Auditor

**Quick guide to get your AI Shield Auditor up and running in minutes!**

---

## 🎯 Choose Your Path

### Path 1: "Just Show Me" (Fastest - 2 minutes)

Perfect for trying it out quickly.

```bash
# 1. Setup
./scripts/setup-local.sh

# 2. Run
source .venv/bin/activate
streamlit run app.py

# 3. Visit http://localhost:8501
```

---

### Path 2: "Production Ready" (Recommended - 5 minutes)

Get all the production features.

```bash
# 1. Setup
./scripts/setup-local.sh

# 2. Configure (optional - for LLM mode)
cp .env.example .env
nano .env  # Add your API keys

# 3. Run production version
source .venv/bin/activate
streamlit run app_enhanced.py

# 4. Visit http://localhost:8501
```

---

### Path 3: "Docker All The Way" (5 minutes)

Containerized deployment.

```bash
# Quick start
docker-compose up -d

# OR interactive deployment
./scripts/deploy-docker.sh
# Choose option 1 or 5

# Visit http://localhost:8501
```

---

### Path 4: "Deploy to Cloud" (10 minutes)

Free deployment on Streamlit Cloud.

```bash
# 1. Initialize git (if not already)
git init
git add .
git commit -m "Initial commit"

# 2. Push to GitHub
git remote add origin <your-github-repo-url>
git push origin main

# 3. Deploy
./scripts/deploy-streamlit-cloud.sh

# 4. Follow instructions to deploy on share.streamlit.io
```

---

## 📝 What to Do Once Running

### Step 1: Configure Environment (in sidebar)

1. Select your **Platform** (OpenAI, Anthropic, Azure, etc.)
2. Enable **Agent Mode** if you use autonomous agents
3. Select **Connectors** you use (Slack, Google Drive, etc.)
4. Specify **Vector Store** if using RAG
5. Identify **Sensitive Data Types** you handle
6. Click **"Detect & Lock Environment"**

### Step 2: Answer Questions

Go through each tab and answer the security questions honestly:
- Identity & Access
- Data Governance
- RAG Privacy
- Integrations
- Model Safety
- Compliance
- Deployment

### Step 3: Generate Report

1. Click **"Run Audit"**
2. Review your security score and findings
3. Export as **PDF** or **JSON**
4. Implement recommendations

---

## 🔑 LLM Mode (Optional)

Want AI-enhanced analysis? Add to `.env`:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
```

Then restart the app. You'll get smarter findings and recommendations!

---

## 🆘 Troubleshooting

### "Module not found" errors

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Port 8501 already in use

```bash
# Find and kill the process
lsof -ti:8501 | xargs kill -9

# OR use a different port
streamlit run app.py --server.port 8502
```

### Docker issues

```bash
# Clean rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Can't access at localhost:8501

Check firewall settings, or try `http://127.0.0.1:8501`

---

## 📚 Learn More

- **Full Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Production Checklist**: [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md)
- **All Improvements**: [IMPROVEMENTS_SUMMARY.md](IMPROVEMENTS_SUMMARY.md)
- **Detailed README**: [README.md](README.md)

---

## 🎓 Pro Tips

1. **Start Simple**: Use basic `app.py` first, switch to `app_enhanced.py` for production
2. **Answer Honestly**: Unknown is better than guessing
3. **Export Reports**: Save JSON for version tracking
4. **Iterate**: Re-run audits as you improve
5. **Deploy Early**: Use Streamlit Cloud for easy sharing

---

## ✅ Quick Verification

Run this to verify everything is set up correctly:

```bash
./scripts/verify-setup.sh
```

---

## 🎉 You're Ready!

Pick a path above and start auditing your AI systems in minutes.

**Questions?** Check the docs in the repository or open an issue.

**Happy Auditing! 🛡️**
