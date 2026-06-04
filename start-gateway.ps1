# @AI_GENERATED
# Spawn kiro-gateway in a detached console window with logs printed live to that window.
# Use Start-Process so the new process does NOT inherit the Kiro hook runner's
# stdout/stderr handles (otherwise the hook would block the hook queue).

$ErrorActionPreference = 'Stop'
$gatewayDir = 'd:\ontitaner\ai-practice\sub_module\kiro-gateway'

Write-Host '[start-gateway] spawning kiro-gateway on port 8000 (logs in its own window) ...'
Start-Process -FilePath 'cmd.exe' `
    -ArgumentList '/c', "title kiro-gateway && set PYTHONIOENCODING=utf-8 && python $gatewayDir\main.py" `
    -WorkingDirectory $gatewayDir | Out-Null

Write-Host '[start-gateway] process spawned, logs print live in the kiro-gateway console window'
exit 0
# @AI_GENERATED: end
