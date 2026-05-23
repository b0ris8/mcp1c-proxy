mkdir  C:\Python314\venvs\mcp1c
python -m venv C:\Python314\venvs\mcp1c
$env:PYTHONPATH="C:\mcp1c-proxy\src"
C:\Python314\venvs\mcp1c\Scripts\Activate.ps1
 cd C:\mcp1c-proxy
 python -m pip install --upgrade pip
 pip install -r C:\mcp1c-proxy\requirements.txt
 Remove-Item -Recurse -Force .\build -ErrorAction SilentlyContinue; Remove-Item -Recurse -Force .\dist -ErrorAction SilentlyContinue
 
 
python -m PyInstaller C:\mcp1c-proxy\mcp1c.spec --clean