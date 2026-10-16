# Recarrega PATH Machine + User na sessao atual do PowerShell (util apos instalar Ollama).
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
            [System.Environment]::GetEnvironmentVariable("Path", "User")
Write-Host "PATH recarregado. Teste: ollama --version"
