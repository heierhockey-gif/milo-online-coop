@echo off
title Milo the Electrician - Online Co-op
cd /d "%~dp0"
echo.
echo ============================================
echo       MILO THE ELECTRICIAN - CO-OP
echo ============================================
echo.
echo This starts a LOCAL test server. For worldwide internet play,
echo deploy this folder to Render using the included render.yaml.
echo.
where py >nul 2>nul
if %errorlevel%==0 (
  py -m pip install --user -r requirements.txt
  if errorlevel 1 goto failed
  py start_milo_server.py
  goto done
)
where python >nul 2>nul
if %errorlevel%==0 (
  python -m pip install --user -r requirements.txt
  if errorlevel 1 goto failed
  python start_milo_server.py
  goto done
)
echo Python was not found. Install it from https://www.python.org/downloads/
start "" "https://www.python.org/downloads/"
goto done
:failed
echo Could not install the server packages. Check your internet connection.
:done
echo.
echo Press any key to close.
pause >nul
