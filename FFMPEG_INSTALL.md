# FFmpeg Installation Guide for Windows

## Option 1: Using Chocolatey (Recommended)

If you have Chocolatey package manager:
```powershell
choco install ffmpeg
```

## Option 2: Using Scoop

If you have Scoop package manager:
```powershell
scoop install ffmpeg
```

## Option 3: Manual Installation

1. Go to https://ffmpeg.org/download.html
2. Click on "Windows" 
3. Download the "release builds" from BtbN or gyan.dev
4. Extract the zip file to a folder (e.g., `C:\ffmpeg`)
5. Add the `bin` folder to your system PATH:
   - Open System Properties → Environment Variables
   - Edit the PATH variable
   - Add `C:\ffmpeg\bin` (or wherever you extracted it)
   - Restart your terminal

## Test Installation

After installation, test in PowerShell:
```powershell
ffmpeg -version
```

## Quick Install with Chocolatey

If you don't have Chocolatey, install it first:
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

Then install FFmpeg:
```powershell
choco install ffmpeg
```

## After Installing FFmpeg

Run the demo again:
```powershell
D:\Google-Hakathon\.venv\Scripts\python.exe demo.py
```

This should successfully create the merged video file!
