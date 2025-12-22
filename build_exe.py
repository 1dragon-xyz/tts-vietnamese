import PyInstaller.__main__
import os
import shutil
import subprocess
import sys

# --- Configuration ---
APP_NAME = "VietnameseTTS"
MAIN_SCRIPT = os.path.join("desktop-app", "main.py")
VERSION_FILE = "VERSION"
VERSION_PY_PATH = os.path.join("desktop-app", "_version.py")
VERSION_RC_FILE = "file_version_info.txt"

def read_version():
    if not os.path.exists(VERSION_FILE):
        return "1.0.0.0"
    with open(VERSION_FILE, "r") as f:
        return f.read().strip()

def create_version_py(version):
    """Generates _version.py for the app to display its own version."""
    with open(VERSION_PY_PATH, "w") as f:
        f.write(f'__version__ = "{version}"\n')

def create_version_rc(version):
    """Generates a Windows version resource file."""
    # Windows versions must be tuple-like: 1,0,0,0
    # Clean version string just in case
    clean_ver = version.replace("v", "")
    parts = clean_ver.split(".")
    while len(parts) < 4:
        parts.append("0")
    win_ver_str = ", ".join(parts[:4])
    
    content = f"""
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({win_ver_str}),
    prodvers=({win_ver_str}),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Anh Nguyen'),
        StringStruct(u'FileDescription', u'Vietnamese Text to Speech Desktop Application'),
        StringStruct(u'FileVersion', u'{clean_ver}'),
        StringStruct(u'InternalName', u'{APP_NAME}'),
        StringStruct(u'LegalCopyright', u'Copyright (c) 2024 Anh Nguyen'),
        StringStruct(u'OriginalFilename', u'{APP_NAME}.exe'),
        StringStruct(u'ProductName', u'{APP_NAME}'),
        StringStruct(u'ProductVersion', u'{clean_ver}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    with open(VERSION_RC_FILE, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    # 1. Setup Versioning
    version = read_version()
    print(f"preparing build for version: {version}")
    
    create_version_py(version)
    create_version_rc(version)

    # 2. Clean previous builds
    # Force kill any existing process
    try:
        subprocess.run(["taskkill", "/F", "/IM", f"{APP_NAME}.exe"], capture_output=True)
    except:
        pass

    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")

    print(f"Building {APP_NAME}...")

    # 3. Run PyInstaller
    args = [
        MAIN_SCRIPT,
        f'--name={APP_NAME}',
        '--onefile',
        '--windowed',
        '--clean',
        '--noconfirm',
        f'--version-file={VERSION_RC_FILE}', # Embed version info
    ]
    
    PyInstaller.__main__.run(args)

    # 4. Rename output with version
    dist_file = os.path.join("dist", f"{APP_NAME}.exe")
    final_name = os.path.join("dist", f"{APP_NAME}_v{version}.exe")
    
    if os.path.exists(dist_file):
        os.rename(dist_file, final_name)
        print(f"\nBuild Complete! Output: {final_name}")
    else:
        print("\nError: Build failed, output file not found.")

    # 5. Cleanup temporary files
    if os.path.exists(VERSION_PY_PATH):
        os.remove(VERSION_PY_PATH)
    if os.path.exists(VERSION_RC_FILE):
        os.remove(VERSION_RC_FILE)

if __name__ == "__main__":
    main()
