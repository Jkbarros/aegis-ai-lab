# Demo controlada para README — ambiente isolado, sem chaves reais
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "Criando venv e instalando dependencias..."
    python -m venv .venv
    .\.venv\Scripts\pip.exe install -r requirements.txt
}

if (-not (Test-Path ".\.env")) {
    Write-Host "Usando .env.demo como base (ambiente controlado)."
    Copy-Item .\.env.demo .\.env
}

.\.venv\Scripts\python.exe scripts\prepare_readme_demo.py --reset-reports --guided
