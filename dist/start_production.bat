@echo off
echo ========================================
echo   BRAVA ENERGIA - PRODUCAO
echo   Sistema de Validacao de Boletins
echo   Campo Atalaia
echo ========================================
echo.
echo Iniciando servidor de producao...
echo Acesse: http://localhost:8080
echo.
echo CTRL+C para parar
echo ========================================
echo.

set FLASK_ENV=production
python -c "import config_production as config; import app; app.app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)"

pause
