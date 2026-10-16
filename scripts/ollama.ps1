# Atalho para o Ollama quando o terminal do Cursor nao carrega o PATH do usuario.
# Uso: .\scripts\ollama.ps1 list
#      .\scripts\ollama.ps1 run llama3.2 "Ola"

$ErrorActionPreference = "Stop"

$exe = Join-Path $env:LOCALAPPDATA "Programs\Ollama\ollama.exe"
if (-not (Test-Path $exe)) {
    Write-Error "ollama.exe nao encontrado em: $exe`nReinstale com: winget install Ollama.Ollama"
}

if ($args.Count -eq 0) {
    & $exe --help
} else {
    & $exe @args
}
