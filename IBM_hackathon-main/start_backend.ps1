# Start backend server
Write-Host "Starting AI Learning Intelligence Platform backend..."
Set-Location backend
python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
