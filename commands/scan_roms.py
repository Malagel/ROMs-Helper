from pathlib import Path
from core.options import Options
from core.logger import log
from core.scan_roms.collector import collect_roms_data

def scan_roms(path: Path, opts: Options) -> dict[str, dict]:
    if opts.logs: log(f"\n▶ Fetching and organizing data from {path}")
    print(f"• Getting your ROMs data from {path}... ", end="", flush=True)

    try:
        data = collect_roms_data(path, opts.valid_subfolders)
    except Exception as e:
        print(f"\n[ERROR]: Failed to fetch the data from your folder. {e}")
        if opts.logs:
            log(f"[ERROR]: Fetching data failed. \n{repr(e)}")
        raise

    print("DONE")
    
    return data