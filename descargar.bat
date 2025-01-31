@echo off
start notepad input_links.txt
timeout /t 4 /nobreak >nul
python script-yt-dlp-line.py
pause
