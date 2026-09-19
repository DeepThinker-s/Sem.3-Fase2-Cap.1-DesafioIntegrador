param(
    [string]$PythonExecutable
)

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = if ($PythonExecutable) {
    $PythonExecutable
} else {
    Join-Path $ProjectRoot '.venv\Scripts\python.exe'
}

if (-not (Test-Path -LiteralPath $Python)) {
    throw 'Ambiente .venv ausente. Execute: python -m venv .venv e instale requirements.txt.'
}

function Invoke-PythonStep {
    param([string[]]$Arguments)
    & $Python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Falha na etapa: python $($Arguments -join ' ')"
    }
}

Push-Location $ProjectRoot
try {
    Invoke-PythonStep @('-m', 'pytest')
    Invoke-PythonStep @('src\extrair_diagnosticos.py')
    Invoke-PythonStep @('src\treinar_classificador.py')
    Invoke-PythonStep @(
        '-m', 'nbconvert', '--to', 'notebook', '--execute', '--inplace',
        '--ExecutePreprocessor.timeout=180',
        'notebooks\cardioai_classificacao_risco.ipynb'
    )
}
finally {
    Pop-Location
}
