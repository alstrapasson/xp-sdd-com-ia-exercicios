<#
.SYNOPSIS
    Executa a verificacao de ambiente do pre-work (Windows).

.DESCRIPTION
    Localiza um Python 3.11+ utilizavel e roda verificar_ambiente.py.
    Uso: clique com o botao direito > "Executar com o PowerShell",
    ou no terminal:  .\verificar-ambiente.ps1
#>

$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Target = Join-Path $ScriptDir 'verificar_ambiente.py'

if (-not (Test-Path $Target)) {
    Write-Host "ERRO: verificar_ambiente.py nao encontrado em $ScriptDir" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

# `py` (Python launcher) e mais confiavel que `python` no Windows, porque `python` pode
# apontar para o atalho da Microsoft Store, que abre a loja em vez de executar.
$Candidates = @(
    @{ Cmd = 'py';     Args = @('-3') },
    @{ Cmd = 'python'; Args = @() },
    @{ Cmd = 'python3'; Args = @() }
)

$Python = $null
foreach ($c in $Candidates) {
    if (Get-Command $c.Cmd -ErrorAction SilentlyContinue) {
        try {
            $v = & $c.Cmd @($c.Args + '--version') 2>&1
            if ($v -match '(\d+)\.(\d+)') {
                if ([int]$Matches[1] -gt 3 -or ([int]$Matches[1] -eq 3 -and [int]$Matches[2] -ge 11)) {
                    $Python = $c
                    break
                }
            }
        } catch { }
    }
}

if (-not $Python) {
    Write-Host ""
    Write-Host "ERRO: nenhum Python 3.11 ou superior encontrado." -ForegroundColor Red
    Write-Host "Instale em https://www.python.org/downloads/ marcando 'Add python.exe to PATH',"
    Write-Host "feche e reabra o terminal, e rode este script novamente."
    Write-Host ""
    Read-Host "Pressione Enter para sair"
    exit 1
}

& $Python.Cmd @($Python.Args + $Target + $args)
$code = $LASTEXITCODE

Write-Host ""
if ($code -eq 0) {
    Write-Host "Ambiente pronto. Envie o arquivo JSON gerado ao instrutor." -ForegroundColor Green
} else {
    Write-Host "Ha bloqueios pendentes. Siga as instrucoes acima e rode novamente." -ForegroundColor Yellow
}

# Mantem a janela aberta quando o script e executado por duplo clique.
if ($Host.Name -eq 'ConsoleHost' -and -not $env:WT_SESSION) {
    Read-Host "Pressione Enter para sair"
}
exit $code
