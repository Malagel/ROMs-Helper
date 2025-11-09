import random
from pathlib import Path

def write_dummy_file(base_path: Path, number: int) -> None:
    size_mb = random.randint(1, 50)
    extensions = ["iso", "bin", "txt", "nsp", "txt", "chd"]
    path = base_path / f"file_{number:03d}.{random.choice(extensions)}"

    with path.open("wb") as f:
        f.truncate(size_mb * (1024 ** 2))


def create_structure(base_path: str, structure: dict) -> None:
    for name, content in structure.items():
        current = Path(base_path) / name
        current.mkdir()

        if isinstance(content, dict):
            for k, v in content.items():

                if k == "files" and isinstance(v, int):
                    for i in range(1, v + 1):
                        write_dummy_file(current, i)
                else:
                    create_structure(current, {k: v})