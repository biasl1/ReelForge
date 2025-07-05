#!/bin/bash
# ReelTune Development Setup Script
# Run this after cloning the repository

echo "🚀 Setting up ReelTune development environment..."

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: Run this script from the ReelTune project root directory"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv

# Check if virtual environment was created successfully
if [ ! -d ".venv" ]; then
    echo "❌ Error: Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment and install dependencies
echo "📋 Installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Clean up any generated files
echo "🧹 Cleaning up generated files..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.log" -delete 2>/dev/null || true

# Check if git is initialized
if [ -d ".git" ]; then
    echo "📝 Setting up git hooks..."
    # Create a pre-commit hook to prevent committing generated files
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Pre-commit hook to prevent committing generated files

echo "🔍 Checking for generated files..."

# Check for __pycache__ directories
if git diff --cached --name-only | grep -q "__pycache__"; then
    echo "❌ Error: Attempting to commit __pycache__ files"
    echo "Run: find . -name '__pycache__' -type d -exec rm -rf {} +"
    exit 1
fi

# Check for .pyc files
if git diff --cached --name-only | grep -q "\.pyc$"; then
    echo "❌ Error: Attempting to commit .pyc files"
    echo "Run: find . -name '*.pyc' -delete"
    exit 1
fi

# Check for log files
if git diff --cached --name-only | grep -q "\.log$"; then
    echo "❌ Error: Attempting to commit log files"
    echo "Remove log files before committing"
    exit 1
fi

# Check for project files
if git diff --cached --name-only | grep -q "\.rforge$"; then
    echo "❌ Error: Attempting to commit project files (.rforge)"
    echo "Project files should not be committed to the repository"
    exit 1
fi

echo "✅ Pre-commit checks passed"
EOF
    chmod +x .git/hooks/pre-commit
    echo "✅ Git pre-commit hook installed"
fi

echo ""
echo "🎉 Setup complete! To get started:"
echo ""
echo "1. Activate the virtual environment:"
echo "   source .venv/bin/activate"
echo ""
echo "2. Run the application:"
echo "   python main.py"
echo ""
echo "3. Or use VS Code tasks (Cmd+Shift+P → 'Tasks: Run Task'):"
echo "   - Run ReelTune"
echo "   - Run ReelTune (Debug)"
echo "   - Clean Generated Files"
echo ""
echo "🛡️  Git pre-commit hook installed to prevent committing generated files"
echo ""
