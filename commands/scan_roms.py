from pathlib import Path
from core.options import Options
from core.logger import log
from core.errors import AppError
from core.scan_roms.collector import collect_roms_data

def scan_roms(path: Path, opts: Options) -> dict[str, dict]:
    if opts.logs: log(f"\n▶ Fetching and organizing data from {path}")
    print(f"• Getting your ROMs data from {path}... ", end="", flush=True)

    try:
        data = collect_roms_data(path, opts.valid_subfolders)
    except PermissionError as e:
        raise AppError(f"No permission to read directory: {path}") from e

    print("DONE")
    
    return data