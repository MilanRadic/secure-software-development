# Setup Guide - Next Steps

## ✅ Completed

- Python 3.14.2 installed and verified
- Virtual environment created (`venv/`)
- Required packages installed (locust, bandit, pip-audit)
- Git repository initialized
- Project structure created
- Files staged for commit

## 🔧 Required: Configure Git

Before making your first commit, you need to configure Git with your name and email:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Or for this repository only (without `--global`):
```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

## 📝 Make Your First Commit

After configuring Git:

```bash
git commit -m "Initial setup: Python environment and project structure"
```

## 🔗 Connect to GitHub

1. **Create a new repository on GitHub:**
   - Go to https://github.com/new
   - Name it (e.g., "secure-software-development")
   - **Don't** initialize with README, .gitignore, or license
   - Click "Create repository"

2. **Add the remote and push:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

   Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name.

## 🚀 You're Ready!

Once Git is configured and connected to GitHub, you're all set to start working on your Secure Software Development course exercises!

### Quick Start Commands

**Activate virtual environment:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Run security tools:**
```bash
bandit -r src/      # Security linting
pip-audit           # Check dependencies
locust              # Load testing
```
