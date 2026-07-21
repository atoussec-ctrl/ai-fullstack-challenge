<#
.SYNOPSIS
    Sobe a stack MindSight AI (backend Flask + frontend Vite) no Windows,
    liberando portas presas, validando saude dos servicos e testando a API.

.DESCRIPTION
    1. Verifica pre-requisitos (venv do backend, node_modules do frontend, .env)
    2. Verifica se as portas do backend/frontend estao ocupadas por processos
       "presos" de execucoes anteriores e finaliza esses processos
    3. Sobe o backend Flask e o frontend Vite em background
    4. Aguarda os health checks responderem (com timeout)
    5. Executa smoke tests na API (health, livros, fluxo de chat completo)
    6. Abre a aplicacao no navegador padrao

.PARAMETER BackendPort
    Porta do backend Flask (default: 5000)

.PARAMETER FrontendPort
    Porta do frontend Vite (default: 3002)

.PARAMETER SkipSeed
    Pula o seed do catalogo de livros

.PARAMETER NoBrowser
    Nao abre o navegador automaticamente ao final

.EXAMPLE
    ./start-stack.ps1

.EXAMPLE
    ./start-stack.ps1 -NoBrowser -SkipSeed
#>

[CmdletBinding()]
param(
    [int]$BackendPort = 5000,
    [int]$FrontendPort = 3002,
    [switch]$SkipSeed,
    [switch]$NoBrowser
)

$ErrorActionPreference = 'Stop'
$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Join-Path $RootDir 'backend'
$FrontendDir = Join-Path $RootDir 'frontend'
$VenvPython = Join-Path $BackendDir '.venv\Scripts\python.exe'
$PidsFile = Join-Path $RootDir '.stack-pids.json'
$LogDir = Join-Path $RootDir '.stack-logs'

function Write-Step  ($msg) { Write-Host "`n==> $msg" -ForegroundColor Cyan }
function Write-Ok    ($msg) { Write-Host "    OK: $msg" -ForegroundColor Green }
function Write-Warn2 ($msg) { Write-Host "    AVISO: $msg" -ForegroundColor Yellow }
function Write-Err2  ($msg) { Write-Host "    ERRO: $msg" -ForegroundColor Red }

function Get-ProcessesOnPort {
    param([int]$Port)
    $conns = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if (-not $conns) { return @() }
    $procIds = $conns.OwningProcess | Sort-Object -Unique
    foreach ($procId in $procIds) {
        Get-Process -Id $procId -ErrorAction SilentlyContinue
    }
}

function Stop-ProcessesOnPort {
    param([int]$Port, [string]$Label)
    $procs = Get-ProcessesOnPort -Port $Port
    if (-not $procs) {
        Write-Ok "Porta $Port ($Label) livre."
        return
    }
    foreach ($proc in $procs) {
        Write-Warn2 "Porta $Port ($Label) ocupada por PID $($proc.Id) [$($proc.ProcessName)] - finalizando processo preso..."
        try {
            Stop-Process -Id $proc.Id -Force -Confirm:$false -ErrorAction Stop
            Write-Ok "PID $($proc.Id) finalizado."
        } catch {
            Write-Err2 "Nao foi possivel finalizar PID $($proc.Id): $($_.Exception.Message)"
        }
    }
    Start-Sleep -Milliseconds 800
    if (Get-ProcessesOnPort -Port $Port) {
        throw "Porta $Port ($Label) continua ocupada apos tentativa de liberacao. Libere manualmente e rode novamente."
    }
}

function Wait-ForHttp {
    param([string]$Url, [int]$TimeoutSec = 40)
    $sw = [Diagnostics.Stopwatch]::StartNew()
    while ($sw.Elapsed.TotalSeconds -lt $TimeoutSec) {
        try {
            $resp = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 3
            if ($resp.StatusCode -ge 200 -and $resp.StatusCode -lt 400) { return $true }
        } catch {
            # ainda subindo - ignora e tenta de novo
        }
        Start-Sleep -Seconds 1
    }
    return $false
}

function Get-EnvValue {
    param([string]$Name, [string]$Default = '')
    $envPath = Join-Path $RootDir '.env'
    if (-not (Test-Path $envPath)) { return $Default }
    $line = Get-Content $envPath | Where-Object { $_ -match "^\s*$Name\s*=" } | Select-Object -Last 1
    if (-not $line) { return $Default }
    return ($line -split '=', 2)[1].Trim()
}

# ── 1. Pre-flight ──────────────────────────────────────────────────────────
Write-Step "Verificando pre-requisitos"

if (-not (Test-Path $VenvPython)) {
    Write-Err2 "venv do backend nao encontrada em $VenvPython"
    Write-Host "    Rode primeiro:"
    Write-Host "      cd backend; python3 -m venv .venv; .venv\Scripts\python.exe -m pip install -r requirements.txt"
    exit 1
}
Write-Ok "venv do backend encontrada."

if (-not (Test-Path (Join-Path $FrontendDir 'node_modules'))) {
    Write-Err2 "node_modules do frontend nao encontrado."
    Write-Host "    Rode primeiro: cd frontend; pnpm install"
    exit 1
}
Write-Ok "node_modules do frontend encontrado."

$envFile = Join-Path $RootDir '.env'
if (-not (Test-Path $envFile)) {
    Write-Warn2 ".env nao encontrado na raiz. Copiando de .env.example..."
    Copy-Item (Join-Path $RootDir '.env.example') $envFile
}
Write-Ok ".env presente."

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

# ── 2. Libera portas presas ─────────────────────────────────────────────────
Write-Step "Verificando conflitos de porta"
Stop-ProcessesOnPort -Port $BackendPort -Label 'backend'
Stop-ProcessesOnPort -Port $FrontendPort -Label 'frontend'

# ── 3. Seed do catalogo (idempotente) ───────────────────────────────────────
if (-not $SkipSeed) {
    Write-Step "Populando catalogo de livros (seed)"
    Push-Location $BackendDir
    try {
        & $VenvPython seed.py
    } finally {
        Pop-Location
    }
}

# ── 4. Sobe backend ──────────────────────────────────────────────────────────
Write-Step "Subindo backend Flask (porta $BackendPort)"
$backendOut = Join-Path $LogDir 'backend.out.log'
$backendErr = Join-Path $LogDir 'backend.err.log'
$backendProc = Start-Process -FilePath $VenvPython -ArgumentList 'run.py' `
    -WorkingDirectory $BackendDir `
    -RedirectStandardOutput $backendOut -RedirectStandardError $backendErr `
    -WindowStyle Hidden -PassThru
Write-Host "    PID backend: $($backendProc.Id)  (logs: $backendOut)"

# ── 5. Sobe frontend ─────────────────────────────────────────────────────────
Write-Step "Subindo frontend Vite (porta $FrontendPort)"
# pnpm no Windows resolve para pnpm.ps1 via Get-Command, mas Start-Process nao
# consegue executar scripts .ps1/.cmd diretamente como Win32 app. Usar cmd.exe
# como host evita o erro "%1 is not a valid Win32 application".
if (-not (Get-Command pnpm -ErrorAction SilentlyContinue)) { throw "pnpm nao encontrado no PATH. Rode: corepack enable" }
$frontendOut = Join-Path $LogDir 'frontend.out.log'
$frontendErr = Join-Path $LogDir 'frontend.err.log'
$frontendProc = Start-Process -FilePath 'cmd.exe' -ArgumentList '/c', 'pnpm', 'dev' `
    -WorkingDirectory $FrontendDir `
    -RedirectStandardOutput $frontendOut -RedirectStandardError $frontendErr `
    -WindowStyle Hidden -PassThru
Write-Host "    PID frontend: $($frontendProc.Id)  (logs: $frontendOut)"

@{ backend = $backendProc.Id; frontend = $frontendProc.Id; startedAt = (Get-Date).ToString('o') } |
    ConvertTo-Json | Set-Content $PidsFile

# ── 6. Health checks ─────────────────────────────────────────────────────────
Write-Step "Aguardando backend responder em /api/v1/health"
if (-not (Wait-ForHttp -Url "http://localhost:$BackendPort/api/v1/health" -TimeoutSec 40)) {
    Write-Err2 "Backend nao respondeu a tempo. Veja $backendErr"
    exit 1
}
Write-Ok "Backend no ar."

Write-Step "Aguardando frontend responder em http://localhost:$FrontendPort"
if (-not (Wait-ForHttp -Url "http://localhost:$FrontendPort" -TimeoutSec 40)) {
    Write-Err2 "Frontend nao respondeu a tempo. Veja $frontendErr"
    exit 1
}
Write-Ok "Frontend no ar."

# O frontend sobe via wrapper cmd.exe (necessario para o shim pnpm.cmd), entao
# o PID real que escuta a porta e um processo filho (node), nao o cmd.exe
# registrado acima. Resolve o PID real pela porta para o stop-stack funcionar
# sem depender do fallback por porta.
$realFrontendPid = (Get-ProcessesOnPort -Port $FrontendPort | Select-Object -First 1).Id
if ($realFrontendPid) {
    @{ backend = $backendProc.Id; frontend = $realFrontendPid; startedAt = (Get-Date).ToString('o') } |
        ConvertTo-Json | Set-Content $PidsFile
}

# ── 7. Smoke tests da API ────────────────────────────────────────────────────
Write-Step "Testando endpoints da API"

$health = Invoke-RestMethod -Uri "http://localhost:$BackendPort/api/v1/health"
Write-Ok "Health check: status=$($health.status)"

$books = Invoke-RestMethod -Uri "http://localhost:$BackendPort/api/v1/books"
Write-Ok "$($books.Count) livro(s) no catalogo."

Write-Step "Testando fluxo de chat (sessao + mensagem)"
$gateway = Get-EnvValue -Name 'CHAT_GATEWAY' -Default 'local'
try {
    $session = Invoke-RestMethod -Method Post -Uri "http://localhost:$BackendPort/api/v1/chat/sessions" `
        -ContentType 'application/json' -Body (@{ title = 'Smoke test start-stack.ps1' } | ConvertTo-Json)

    $msg = Invoke-RestMethod -Method Post -Uri "http://localhost:$BackendPort/api/v1/chat/messages" `
        -ContentType 'application/json' `
        -Body (@{ session_id = $session.id; content = 'O que e uma lista em Python?'; thinking_mode = 'fast' } | ConvertTo-Json)

    $preview = $msg.assistant_message.content
    if ($preview.Length -gt 100) { $preview = $preview.Substring(0, 100) + '...' }
    Write-Ok "Gateway '$gateway' respondeu: $preview"
} catch {
    Write-Err2 "Falha no fluxo de chat (gateway '$gateway'): $($_.Exception.Message)"
    Write-Warn2 "Verifique as chaves de API no .env e os logs em $backendErr"
}

# ── 8. Abre a aplicacao ──────────────────────────────────────────────────────
if (-not $NoBrowser) {
    Write-Step "Abrindo aplicacao no navegador"
    Start-Process "http://localhost:$FrontendPort"
}

Write-Host "`n=================================================" -ForegroundColor Green
Write-Host " MindSight AI no ar" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host " Frontend : http://localhost:$FrontendPort"
Write-Host " Backend  : http://localhost:$BackendPort/api/v1"
Write-Host " Docs     : http://localhost:$BackendPort/docs"
Write-Host " Gateway  : $gateway"
Write-Host " Logs     : $LogDir"
Write-Host " Parar    : ./stop-stack.ps1"
Write-Host "=================================================`n"
