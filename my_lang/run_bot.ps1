# Script PowerShell para executar o chatbot my_lang no Windows
# Execute com: .\run_bot.ps1

# Definir o diretório do projeto
$projectDir = $PSScriptRoot

# Mudar para o diretório do projeto
Set-Location $projectDir

Write-Host "Iniciando o chatbot em $projectDir..." -ForegroundColor Green

# Verificar se o ambiente virtual existe
if (Test-Path -Path ".venv") {
    Write-Host "Ativando ambiente virtual..." -ForegroundColor Yellow
    # Ativa o ambiente virtual
    .\.venv\Scripts\Activate.ps1
} else {
    Write-Host "Ambiente virtual não encontrado. Será usado Python global." -ForegroundColor Yellow
}

# Verificar se as dependências estão instaladas
Write-Host "Verificando dependências..." -ForegroundColor Yellow
$pipResult = pip show langmem
if ($LASTEXITCODE -ne 0) {
    Write-Host "Instalando dependências..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Executar o aplicativo
try {
    Write-Host "Iniciando o chatbot..." -ForegroundColor Green
    python -m src.app
}
catch {
    Write-Host "Erro ao executar o chatbot:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
} 