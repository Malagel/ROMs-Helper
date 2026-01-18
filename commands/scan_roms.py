from pathlib import Path
from core.options import Options
from core.logger import log
from core.scan_roms.collector import collect_roms_data

def scan_roms(path: Path, opts: Options) -> dict[str, dict]:
    if opts.logs: log(f"\n▶ Fetching and organizing data from {path}")
    print(f"• Getting your ROMs data from {path}... ", end="", flush=True)

    data = collect_roms_data(path, opts.valid_subfolders)

    print("DONE")
    
    return data