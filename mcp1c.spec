# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_all, collect_submodules

project_root = SPECPATH
src_root = os.path.join(project_root, "src")

pathex = [project_root, src_root]
datas = []
binaries = []
hiddenimports = []

hiddenimports += collect_submodules("py_server")
hiddenimports += [
    "py_server.main",
    "py_server.entry",
    "py_server.config",
    "py_server.http_server",
    "py_server.stdio_server",
    "py_server.mcp_server",
    "py_server.onec_client",
]

for pkg in ["fastapi", "starlette", "uvicorn", "pydantic", "mcp"]:
    d, b, h = collect_all(pkg)
    datas += d
    binaries += b
    hiddenimports += h

datas += [(os.path.join(src_root, "py_server"), "py_server")]

a = Analysis(
    [os.path.join(src_root, "py_server", "entry.py")],
    pathex=pathex,
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    excludes=["mcp.cli", "typer"],
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="mcp1c-proxy",
    console=True,
    icon=os.path.join(src_root, "py_server", "mcp1c.ico") if sys.platform == "win32" else None,
)
