# Secure Software Development - Application

This project is set up for the Secure Software Development course.

## Prerequisites

Based on the pre-installation guide, you need:

- ✅ **Python 3.12+** (Currently: Python 3.14.2)
- **Git** and a **GitHub account**
- **PortSwigger account** (free account at https://portswigger.net/)
- **Postman** (desktop app and account at https://www.postman.com/downloads/)
- **WSL** (for Windows users - https://learn.microsoft.com/en-us/windows/wsl/install)

## Python Environment Setup

### Virtual Environment

A virtual environment has been created in the `venv` folder.

**To activate the virtual environment:**
- **Windows PowerShell:** `.\venv\Scripts\Activate.ps1`
- **Windows CMD:** `venv\Scripts\activate.bat`
- **Linux/Mac/WSL:** `source venv/bin/activate`

**To deactivate:**
```bash
deactivate
```

### Installed Python Packages

The following packages are installed in the virtual environment:

- **locust** - Load testing tool
- **bandit** - Security linter for Python code
- **pip-audit** - Security vulnerability scanner for Python dependencies

### Installing Dependencies

If you need to reinstall dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running Bandit (Security Linter)
```bash
bandit -r .  # Scan current directory recursively
```

### Running pip-audit (Dependency Vulnerability Scanner)
```bash
pip-audit  # Scan installed packages for vulnerabilities
```

### Running Locust (Load Testing)
```bash
locust  # Start Locust web interface
```

## Project Structure

```
.
├── venv/              # Virtual environment (do not commit)
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Project Structure

```
.
├── venv/              # Virtual environment (do not commit)
├── src/               # Source code directory
├── tests/             # Test files
├── exercises/         # Course exercises and assignments
├── requirements.txt   # Python dependencies
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

## Git Setup

The repository has been initialized. To connect to GitHub:

1. Create a new repository on GitHub (don't initialize with README)
2. Add the remote:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   ```
3. Make your first commit:
   ```bash
   git add .
   git commit -m "Initial setup: Python environment and project structure"
   ```
4. Push to GitHub:
   ```bash
   git branch -M main
   git push -u origin main
   ```

## Usage

### Activating the Virtual Environment

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac/WSL:**
```bash
source venv/bin/activate
```

### Running Security Tools

**Bandit (Security Linter):**
```bash
bandit -r src/  # Scan source code
bandit -r .     # Scan entire project
```

**pip-audit (Dependency Scanner):**
```bash
pip-audit        # Check for vulnerabilities
pip-audit --fix  # Attempt to fix vulnerabilities
```

**Locust (Load Testing):**
```bash
locust  # Start Locust web interface (default: http://localhost:8089)
```

## Notes

- ✅ All prerequisites are set up
- ✅ Python virtual environment is ready
- ✅ All required packages are installed
- ✅ Git repository is initialized
- Always activate the virtual environment before working on the project
- The `venv` folder is already in `.gitignore`
