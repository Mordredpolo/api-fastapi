@echo off
:loop
echo Envoi du ping...
curl --silent --max-time 10 https://api-fastapi-4sn5.onrender.com/ping > nul
timeout /t 240 > nul
goto loop
