from core.helpers.filesystem import get_app_base_dir
from pathlib import Path
import shutil

def delete_game_paths(game_paths: list[Path], safe_deletion: bool) -> None:
    if safe_deletion:
        base = get_app_base_dir()
        delete_dir = base / "DELETE"
        delete_dir.mkdir(exist_ok=True)

    for game_path in game_paths:
        is_dir = game_path.is_dir()
        
        if safe_deletion:
            target = delete_dir / game_path.name
            
            counter = 1
            while target.exists():
                target = delete_dir / f"{game_path.stem}_{counter}{game_path.suffix}"
                counter += 1

            shutil.move(str(game_path), str(target))

        else:
            if is_dir:
                shutil.rmtree(game_path)
            else:
                game_path.unlink()
