Param(
    [ValidateSet("start","stop")]
    [string]$Action = "start"
)

$ErrorActionPreference = "Stop"

# Descobre a raiz do projeto (pasta acima de scripts)
$ProjectRoot = (Resolve-Path "$PSScriptRoot\..").Path
$PidFile     = Join-Path $ProjectRoot "amldo_webapps.pids"

if ($Action -eq "stop") {
    if (-not (Test-Path $PidFile)) {
        Write-Host "Nenhum arquivo de PIDs encontrado. Nada para parar." -ForegroundColor Yellow
        return
    }

    Write-Host "Parando webapps a partir de PIDs salvos..." -ForegroundColor Yellow
    Get-Content $PidFile | ForEach-Object {
        $pidText = $_.Trim()
        if ($pidText) {
            $procId = [int]$pidText
            $proc = Get-Process -Id $procId -ErrorAction SilentlyContinue
            if ($proc) {
                Write-Host "Parando processo PID: $procId ($($proc.ProcessName))" -ForegroundColor Cyan
                Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
            }
        }
    }

    Remove-Item $PidFile -ErrorAction SilentlyContinue
    Write-Host "Webapps paradas." -ForegroundColor Green
    return
}

# Ação = start
if (Test-Path $PidFile) {
    Write-Host "Parece que as webapps já estão rodando (arquivo de PIDs existe)." -ForegroundColor Yellow
    Write-Host "Use: .\scripts\run_both_webapps.ps1 stop" -ForegroundColor Yellow
    return
}

# Limpa arquivo de PIDs (usar ASCII simples para evitar caracteres nulos)
"" | Out-File -FilePath $PidFile -Encoding ascii

Write-Host ""
Write-Host "Iniciando WebApp NOVA (porta 8000) e WebApp ANTIGA (porta 8001) em novas janelas..." -ForegroundColor Green
Write-Host ""

$runNew = Join-Path $ProjectRoot "scripts\run_webapp_new.ps1"
$runOld = Join-Path $ProjectRoot "scripts\run_webapp_old.ps1"

if (-not (Test-Path $runNew)) {
    Write-Host "Script não encontrado: $runNew" -ForegroundColor Red
    return
}
if (-not (Test-Path $runOld)) {
    Write-Host "Script não encontrado: $runOld" -ForegroundColor Red
    return
}

# Inicia webapp nova em nova janela do PowerShell
$cmdNew = "cd `"$ProjectRoot`"; & `"$runNew`""
$newProc = Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit","-Command",$cmdNew -PassThru
$newProc.Id.ToString() | Out-File -FilePath $PidFile -Append -Encoding ascii

# Inicia webapp antiga em nova janela do PowerShell
$cmdOld = "cd `"$ProjectRoot`"; & `"$runOld`""
$oldProc = Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit","-Command",$cmdOld -PassThru
$oldProc.Id.ToString() | Out-File -FilePath $PidFile -Append -Encoding ascii

Write-Host "WebApp NOVA:   http://localhost:8000" -ForegroundColor Cyan
Write-Host "WebApp ANTIGA: http://localhost:8001" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para parar ambas, use:" -ForegroundColor Yellow
Write-Host "  .\scripts\run_both_webapps.ps1 stop" -ForegroundColor Yellow
