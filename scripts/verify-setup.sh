#!/bin/bash
# Verify that all improvements are in place

set -e

echo "🔍 AI Shield Auditor - Setup Verification"
echo "=========================================="
echo ""

ERRORS=0
WARNINGS=0

# Check function
check_file() {
    if [ -f "$1" ]; then
        echo "✅ $1"
    else
        echo "❌ MISSING: $1"
        ((ERRORS++))
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo "✅ $1/"
    else
        echo "❌ MISSING: $1/"
        ((ERRORS++))
    fi
}

check_optional() {
    if [ -f "$1" ]; then
        echo "✅ $1"
    else
        echo "⚠️  OPTIONAL: $1"
        ((WARNINGS++))
    fi
}

# Core files
echo "📁 Core Application Files:"
check_file "app.py"
check_file "app_enhanced.py"
check_file "requirements.txt"
check_file ".env.example"
echo ""

# Core modules
echo "📦 Core Modules:"
check_file "core/schema.py"
check_file "core/utils.py"
check_file "core/report.py"
check_file "core/detectors.py"
check_file "core/scoring.py"
check_file "core/logging_config.py"
check_file "core/security.py"
check_file "core/health.py"
echo ""

# Audit modules
echo "🔍 Audit Modules:"
check_file "audits/identity.py"
check_file "audits/data_governance.py"
check_file "audits/rag_privacy.py"
check_file "audits/integration_security.py"
check_file "audits/model_safety.py"
check_file "audits/compliance.py"
check_file "audits/deployment.py"
echo ""

# Templates
echo "📋 Templates:"
check_file "templates/questions.yml"
check_file "templates/providers.yml"
echo ""

# Deployment files
echo "🐳 Deployment Configuration:"
check_file "Dockerfile"
check_file "docker-compose.yml"
check_file ".dockerignore"
check_file ".streamlit/config.toml"
check_file ".gitignore"
echo ""

# Scripts
echo "🔧 Deployment Scripts:"
check_file "scripts/setup-local.sh"
check_file "scripts/deploy-docker.sh"
check_file "scripts/deploy-streamlit-cloud.sh"
check_file "scripts/verify-setup.sh"
echo ""

# CI/CD
echo "⚙️  CI/CD:"
check_file ".github/workflows/deploy.yml"
echo ""

# Documentation
echo "📚 Documentation:"
check_file "README.md"
check_file "DEPLOYMENT.md"
check_file "PRODUCTION_CHECKLIST.md"
check_file "IMPROVEMENTS_SUMMARY.md"
check_optional "QUICKSTART.md"
echo ""

# Optional files
echo "🔐 Environment:"
check_optional ".env"
echo ""

# Directories
echo "📂 Required Directories:"
check_dir "core"
check_dir "audits"
check_dir "templates"
check_dir "scripts"
check_dir ".streamlit"
check_dir ".github/workflows"
echo ""

# Check Python
echo "🐍 Python Environment:"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo "✅ Python $PYTHON_VERSION installed"

    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)" 2>/dev/null; then
        echo "✅ Python version is 3.11+"
    else
        echo "⚠️  Python 3.11+ recommended (found: $PYTHON_VERSION)"
        ((WARNINGS++))
    fi
else
    echo "❌ Python3 not found"
    ((ERRORS++))
fi
echo ""

# Check Docker
echo "🐳 Docker (Optional):"
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | awk '{print $3}' | tr -d ',')
    echo "✅ Docker $DOCKER_VERSION installed"
else
    echo "⚠️  Docker not installed (optional)"
    ((WARNINGS++))
fi
echo ""

# Check git
echo "📦 Git:"
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | awk '{print $3}')
    echo "✅ Git $GIT_VERSION installed"

    if [ -d .git ]; then
        echo "✅ Git repository initialized"
    else
        echo "⚠️  Not a git repository (run: git init)"
        ((WARNINGS++))
    fi
else
    echo "⚠️  Git not installed"
    ((WARNINGS++))
fi
echo ""

# Test Python imports (if venv exists)
if [ -d .venv ]; then
    echo "🧪 Testing Python Imports:"
    source .venv/bin/activate 2>/dev/null || true

    if python3 -c "import streamlit" 2>/dev/null; then
        echo "✅ streamlit"
    else
        echo "❌ streamlit not installed"
        ((ERRORS++))
    fi

    if python3 -c "import pandas" 2>/dev/null; then
        echo "✅ pandas"
    else
        echo "❌ pandas not installed"
        ((ERRORS++))
    fi

    if python3 -c "import pydantic" 2>/dev/null; then
        echo "✅ pydantic"
    else
        echo "❌ pydantic not installed"
        ((ERRORS++))
    fi

    echo ""
else
    echo "⚠️  Virtual environment not found (.venv)"
    echo "   Run: ./scripts/setup-local.sh"
    ((WARNINGS++))
    echo ""
fi

# Summary
echo "========================================"
echo "📊 Verification Summary:"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "✅ All checks passed! Your setup is complete."
    echo ""
    echo "Next steps:"
    echo "1. Configure environment: cp .env.example .env (if not done)"
    echo "2. Edit .env with your API keys (optional)"
    echo "3. Run application: streamlit run app_enhanced.py"
    echo "4. Visit: http://localhost:8501"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo "✅ Core setup complete with $WARNINGS warning(s)"
    echo ""
    echo "Warnings can typically be ignored for basic functionality."
    echo ""
    echo "Next steps:"
    echo "1. Review warnings above (if important to you)"
    echo "2. Configure environment: cp .env.example .env"
    echo "3. Run application: streamlit run app_enhanced.py"
    exit 0
else
    echo "❌ Setup incomplete: $ERRORS error(s), $WARNINGS warning(s)"
    echo ""
    echo "Please fix the errors above before continuing."
    echo ""
    echo "Common fixes:"
    echo "- Missing files: Check that all files were created"
    echo "- Python not found: Install Python 3.11+"
    echo "- Missing modules: Run ./scripts/setup-local.sh"
    exit 1
fi
