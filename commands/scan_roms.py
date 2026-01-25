from pathlib import Path
from core.options import Options
from core.logger import log
from core.errors import AppError
from core.scan_roms.collector import collect_roms_data

def scan_roms(opts: Options) -> dict[str, dict]:
    if opts.logs: log(f"\n▶ Fetching and organizing data from {opts.path}")
    print(f"• Getting your ROMs data from {opts.path}... ", end="", flush=True)

    try:
        data = collect_roms_data(opts.path, opts.valid_subfolders)
    except PermissionError as e:
        raise AppError(f"No permission to read directory: {opts.path}") from e

    print("DONE")
    
    return data