<#
.SYNOPSIS
    Para os servicos da stack MindSight AI iniciados por start-stack.ps1.

.DESCRIPTION
    Finaliza os processos registrados em .stack-pids.json e, como garantia,
    tambem finaliza qualquer processo ainda escutando nas portas do
    backend/frontend informadas.
#>

[CmdletBinding()]
param(
    [int]$BackendPort = 5000,
    [int]$FrontendPort = 3002
)

$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PidsFile = Join-Path $RootDir '.stack-pids.json'

function Write-Ok    ($msg) { Write-Host "OK: $msg" -ForegroundColor Green }
function Write-Warn2 ($msg) { Write-Host "AVISO: $msg" -ForegroundColor Yellow }

function Stop-ByPid {
    param([int]$ProcId, [string]$Label)
    $proc = Get-Process -Id $ProcId -ErrorAction SilentlyContinue
    if ($proc) {
        Stop-Process -Id $ProcId -Force -Confirm:$false -ErrorAction SilentlyContinue
        Write-Ok "$Label (PID $ProcId) finalizado."
    }
}

function Stop-ByPort {
    param([int]$Port, [string]$Label)
    $conns = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if (-not $conns) { return }
    foreach ($procId in ($conns.OwningProcess | Sort-Object -Unique)) {
        Stop-Process -Id $procId -Force -Confirm:$false -ErrorAction SilentlyContinue
        Write-Ok "$Label na porta $Port (PID $procId) finalizado."
    }
}

if (Test-Path $PidsFile) {
    $pids = Get-Content $PidsFile | ConvertFrom-Json
    Stop-ByPid -ProcId $pids.backend -Label 'Backend'
    Stop-ByPid -ProcId $pids.frontend -Label 'Frontend'
    Remove-Item $PidsFile -Force
} else {
    Write-Warn2 "Arquivo .stack-pids.json nao encontrado, finalizando por porta."
}

# Garantia extra: mata qualquer coisa ainda presa nas portas
Stop-ByPort -Port $BackendPort -Label 'Processo'
Stop-ByPort -Port $FrontendPort -Label 'Processo'

Write-Ok "Stack finalizada."
