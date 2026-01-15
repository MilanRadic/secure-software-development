# PowerShell script to start the Flask authorization server

Write-Host "Starting Authorization Server..." -ForegroundColor Green

# Navigate to auth directory
Set-Location $PSScriptRoot

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Check if activation was successful
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to activate virtual environment. Creating it..." -ForegroundColor Red
    python -m venv venv
    & .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
}

# Start the Flask server
Write-Host "Starting Flask server on http://127.0.0.1:5005..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
python app.py
