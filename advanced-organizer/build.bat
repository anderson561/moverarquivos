@echo off
echo Gerando executavel do Organizador Avancado...
python -m PyInstaller --onefile --name "OrganizadorArquivos" --add-data "src;src" src\organizer.py
echo Build concluido! O executavel esta na pasta 'dist'.
pause
