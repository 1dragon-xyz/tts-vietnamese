import PyInstaller.__main__
import os
import shutil
import subprocess

# Define the build parameters
APP_NAME = "VietnameseTTS"
MAIN_SCRIPT = os.path.join("desktop-app", "main.py")

# Force kill any existing process
try:
    subprocess.run(["taskkill", "/F", "/IM", f"{APP_NAME}.exe"], capture_output=True)
except:
    pass

# Clean previous builds
if os.path.exists("build"):
    shutil.rmtree("build")
if os.path.exists("dist"):
    shutil.rmtree("dist")

print(f"Building {APP_NAME}...")

PyInstaller.__main__.run([
    MAIN_SCRIPT,
    f'--name={APP_NAME}',
    '--onefile',            # Bundle everything into a single .exe
    '--windowed',           # No console window (GUI only)
    '--clean',              # Clean cache
    '--noconfirm',          # Overwrite output directory without asking
])

print(f"\nBuild Complete! Check the 'dist' folder for {APP_NAME}.exe")