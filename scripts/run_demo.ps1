# Demo de portfólio (Etapa 11) — pytest + segurança + campanhas
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Error "Crie o venv e instale requirements antes da demo."
}

.\.venv\Scripts\python.exe scripts\demo_etapa11.py --full
