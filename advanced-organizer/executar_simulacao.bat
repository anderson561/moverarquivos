@echo off
echo Rodando SIMULACAO do Organizador (Nenhum arquivo sera movido)...
set /p TARGET_PATH="Digite o caminho da pasta a ser organizada (Pressione Enter para o Desktop padrao): "
if "%TARGET_PATH%"=="" (
    "dist\OrganizadorArquivos.exe"
) else (
    "dist\OrganizadorArquivos.exe" --path "%TARGET_PATH%"
)
pause
