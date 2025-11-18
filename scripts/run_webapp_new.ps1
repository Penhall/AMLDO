Param()

$ErrorActionPreference = "Stop"

# Descobre a raiz do projeto (pasta acima de scripts)
$ProjectRoot = (Resolve-Path "$PSScriptRoot\..").Path

Write-Host ""
Write-Host "AMLDO v0.3.0 - WebApp NOVA" -ForegroundColor Green
Write-Host "Diretório do projeto: $ProjectRoot" -ForegroundColor Cyan
Write-Host ""

Set-Location $ProjectRoot

# Verificar .env
if (-not (Test-Path ".env")) {
    Write-Host ".env não encontrado na raiz do projeto." -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Write-Host "Criando .env a partir de .env.example..." -ForegroundColor Cyan
        Copy-Item ".env.example" ".env" -Force
    }
    Write-Host "Edite o arquivo .env e configure GOOGLE_API_KEY antes de continuar." -ForegroundColor Red
    return
}

$envLines = Get-Content ".env"
$hasKey   = $envLines -match '^\s*GOOGLE_API_KEY='
$isDummy  = $envLines -match 'GOOGLE_API_KEY=sua_chave_aqui'

if (-not $hasKey -or $isDummy) {
    Write-Host "GOOGLE_API_KEY não configurada corretamente em .env." -ForegroundColor Red
    Write-Host 'Abra ".env" e configure: GOOGLE_API_KEY=SUa_CHAVE_REAL_AQUI' -ForegroundColor Yellow
    return
}

Write-Host "Configuração (.env / GOOGLE_API_KEY) OK." -ForegroundColor Green
Write-Host ""

# Ativar venv
$venvActivate = Join-Path $ProjectRoot "venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    Write-Host "Ativando virtual environment..." -ForegroundColor Cyan
    & $venvActivate
    Write-Host "venv ativado." -ForegroundColor Green
} else {
    Write-Host "Virtual environment não encontrado em '$venvActivate'." -ForegroundColor Yellow
    Write-Host "Crie com: python -m venv venv" -ForegroundColor Yellow
    return
}

Write-Host ""
Write-Host "Iniciando WebApp NOVA (v0.3.0)..." -ForegroundColor Green
Write-Host "API:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Chat: http://localhost:8000/consulta" -ForegroundColor Cyan
Write-Host ""

amldo-api

