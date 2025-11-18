Param()

$ErrorActionPreference = "Stop"

# Descobre a raiz do projeto (pasta acima de scripts)
$ProjectRoot = (Resolve-Path "$PSScriptRoot\..").Path
$WebappRoot  = Join-Path $ProjectRoot "AMLDO_W\AMLDO"

Write-Host ""
Write-Host "AMLDO WebApp ANTIGA (Original)" -ForegroundColor Green
Write-Host "Diretório: $WebappRoot" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $WebappRoot)) {
    Write-Host "Diretório da webapp antiga não encontrado: $WebappRoot" -ForegroundColor Red
    return
}

Set-Location $WebappRoot

# Verificar .env
if (-not (Test-Path ".env")) {
    Write-Host ".env não encontrado em $WebappRoot" -ForegroundColor Yellow
    Write-Host 'Crie um arquivo ".env" com as configurações necessárias da webapp antiga.' -ForegroundColor Yellow
    return
}

Write-Host "Configuração (.env) OK." -ForegroundColor Green
Write-Host ""

# Ativar venv do projeto principal, se existir
$venvActivate = Join-Path $ProjectRoot "venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    Write-Host "Ativando virtual environment compartilhado..." -ForegroundColor Cyan
    & $venvActivate
    Write-Host "venv ativado." -ForegroundColor Green
} else {
    Write-Host "Virtual environment não encontrado em '$venvActivate'." -ForegroundColor Yellow
    Write-Host "Crie com: python -m venv venv (na raiz do projeto AMLDO)" -ForegroundColor Yellow
}

# Verificar dependências
if (Test-Path "requirements.txt") {
    Write-Host "Verificando/instalando dependências da webapp antiga..." -ForegroundColor Cyan
    python -m pip install -r "requirements.txt"
}

Write-Host ""
Write-Host "Iniciando WebApp ANTIGA na porta 8001..." -ForegroundColor Green
Write-Host "URL: http://localhost:8001" -ForegroundColor Cyan
Write-Host ""

Set-Location (Join-Path $WebappRoot "webapp")
python -m uvicorn main:app --reload --port 8001 --host 0.0.0.0

