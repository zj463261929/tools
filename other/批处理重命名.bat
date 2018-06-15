@echo off
setlocal enabledelayedexpansion
set /p name=rename:
for /f "delims=" %%a in ('dir /b *.jpg') do (
set /a num+=1
ren "%%a" "!name!!num!.jpg"
)
echo chuliwanbi
pause>nul
