@echo off
echo Criando ambiente virtual...
python -m venv venv

echo Ativando ambiente...
call venv\Scripts\activate

echo Instalando dependências...
pip install --upgrade pip
pip install -r requirements.txt

echo Ambiente pronto! Para ativar novamente, use:
echo call venv\Scripts\activate
pause
