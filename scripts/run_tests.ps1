# Executa a suíte pytest do Aegis AI Lab (Etapa 5)
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Error "Crie o ambiente virtual antes: python -m venv .venv"
}

.\.venv\Scripts\python.exe -m pip install -q -r requirements.txt
.\.venv\Scripts\python.exe -m pytest
