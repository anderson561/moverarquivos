@echo off
echo [AVISO] Rodando MOVIMENTACAO REAL de arquivos!
set /p TARGET_PATH="Digite o caminho da pasta a ser organizada (Pressione Enter para o Desktop padrao): "
echo Pressione qualquer tecla para iniciar a execucao real ou feche a janela para cancelar.
pause
if "%TARGET_PATH%"=="" (
    "dist\OrganizadorArquivos.exe" --real
) else (
    "dist\OrganizadorArquivos.exe" --path "%TARGET_PATH%" --real
)
pause
