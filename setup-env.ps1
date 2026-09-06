# Run from any directory: powershell -ExecutionPolicy Bypass -File .\setup-env.ps1
param([string]$Python = "python")
$ErrorActionPreference = "Stop"
$venvPath = Join-Path $PSScriptRoot ".venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"

if (-not (Test-Path -LiteralPath $venvPython)) {
    & $Python -c "import sys; assert sys.version_info[:2] == (3, 11), 'Python 3.11 is required'"
    if ($LASTEXITCODE -ne 0) { throw "Select Python 3.11 with -Python <path-to-python.exe>." }
    & $Python -m venv $venvPath
    if ($LASTEXITCODE -ne 0) { throw "Virtual environment creation failed." }
}
& $venvPython -c "import sys; assert sys.version_info[:2] == (3, 11), 'Existing .venv must use Python 3.11'"
if ($LASTEXITCODE -ne 0) { throw "The existing .venv uses an unsupported Python version." }
& $venvPython -m pip install -r (Join-Path $PSScriptRoot "requirements.txt")
if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed." }
& $venvPython -m pip check
if ($LASTEXITCODE -ne 0) { throw "Dependency verification failed." }
& $venvPython -m ipykernel install --sys-prefix --name jepx-data-analytics --display-name "Python (.venv - jepx-data-analytics)"
if ($LASTEXITCODE -ne 0) { throw "Notebook kernel registration failed." }
Write-Host "Ready: $venvPython"
