#!/bin/bash
# Deploy to Streamlit Cloud
# This script helps prepare your app for Streamlit Cloud deployment

set -e

echo "🚀 Preparing for Streamlit Cloud Deployment"
echo "==========================================="

# Check if git repository exists
if [ ! -d .git ]; then
    echo "❌ Error: Not a git repository"
    echo "Initialize git first: git init"
    exit 1
fi

# Check for uncommitted changes
if [[ -n $(git status -s) ]]; then
    echo "⚠️  You have uncommitted changes:"
    git status -s
    read -p "Commit changes now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter commit message: " commit_msg
        git add .
        git commit -m "$commit_msg"
    fi
fi

# Check if remote exists
if ! git remote | grep -q origin; then
    echo "❌ No git remote found"
    echo "Add a remote: git remote add origin <your-repo-url>"
    exit 1
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main || git push origin master

echo ""
echo "✅ Code pushed successfully!"
echo ""
echo "Next steps:"
echo "1. Go to https://share.streamlit.io"
echo "2. Sign in with GitHub"
echo "3. Click 'New app'"
echo "4. Select your repository"
echo "5. Set main file path: app.py (or app_enhanced.py for production features)"
echo "6. Add secrets (if using LLM mode):"
echo "   OPENAI_API_KEY = \"sk-...\""
echo "   ANTHROPIC_API_KEY = \"sk-ant-...\""
echo "   LLM_PROVIDER = \"openai\""
echo "7. Deploy!"
echo ""
echo "📚 Documentation: https://docs.streamlit.io/streamlit-community-cloud"
