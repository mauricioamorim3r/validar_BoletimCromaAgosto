@echo off
echo ========================================
echo   BRAVA ENERGIA - BUILD SYSTEM
echo   Sistema de Validacao de Boletins
echo   Campo Atalaia
echo ========================================
echo.
echo Executando build completo...
echo.

python build.py

if errorlevel 1 (
    echo.
    echo ❌ Build falhou!
    echo Verifique os erros acima.
    pause
    exit /b 1
) else (
    echo.
    echo ✅ Build concluido com sucesso!
    echo.
    echo 📦 Distribuicao: dist/
    echo 📚 Documentacao: dist/README.md
    echo 🚀 Executar: dist/start_production.bat
    echo.
    pause
)
