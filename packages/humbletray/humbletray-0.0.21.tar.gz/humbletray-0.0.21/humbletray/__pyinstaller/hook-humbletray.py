from pathlib import Path
from PyInstaller.utils.hooks import get_package_paths

# ok great, we're getting the templates directly from the horses mouth
templates = Path(get_package_paths("justpy.templates")[1])
leaf = Path(get_package_paths("humbletray")[1]) / "leaf.png"

datas = [(str(leaf), "."), (templates, "justpy/templates")]

hiddenimports = [
    "pystray._win32",
    "schedule",
    "uvicorn.lifespan.on",
    "uvicorn.protocols.websockets.auto",
    "uvicorn.protocols.http.auto",
    "uvicorn.logging",
    "uvicorn.loops.auto",
    "uvicorn.protocols",
]