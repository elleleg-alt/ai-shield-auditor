#!/bin/bash
# Local development setup script

set -e

echo "🛠️  AI Shield Auditor - Local Setup"
echo "===================================="

# Check Python version
echo "🐍 Checking Python version..."
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
REQUIRED_VERSION="3.11"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo "❌ Python 3.11+ required (found: $PYTHON_VERSION)"
    echo "Install from: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ -d .venv ]; then
    read -p "Virtual environment exists. Recreate? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf .venv
        python3 -m venv .venv
    fi
else
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p reports
mkdir -p logs

# Setup environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your API keys"
    echo ""
    read -p "Open .env in editor now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} .env
    fi
else
    echo "✅ .env file already exists"
fi

# Check if all required files exist
echo ""
echo "🔍 Checking project structure..."
REQUIRED_FILES=(
    "app.py"
    "core/schema.py"
    "core/utils.py"
    "core/report.py"
    "core/detectors.py"
    "templates/questions.yml"
    "templates/providers.yml"
)

ALL_GOOD=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing: $file"
        ALL_GOOD=false
    fi
done

if [ "$ALL_GOOD" = true ]; then
    echo "✅ All required files present"
else
    echo "⚠️  Some files are missing. Project may not work correctly."
fi

# Test imports
echo ""
echo "🧪 Testing imports..."
python3 -c "import streamlit; import pandas; import pydantic; print('✅ Core imports successful')" || {
    echo "❌ Import test failed"
    exit 1
}

# Summary
echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your API keys (if not done already)"
echo "2. Run: source .venv/bin/activate"
echo "3. Run: streamlit run app.py"
echo "4. Open: http://localhost:8501"
echo ""
echo "For production features, use:"
echo "  streamlit run app_enhanced.py"
echo ""
echo "For deployment options, see:"
echo "  - DEPLOYMENT.md"
echo "  - scripts/deploy-docker.sh"
echo "  - scripts/deploy-streamlit-cloud.sh"
