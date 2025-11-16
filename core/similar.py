from pathlib import Path
from difflib import SequenceMatcher
import shutil
from core.utils import normalize, log, clear_console, prompt_continue


def tokenize(name: str) -> set[str]:
    return {w for w in normalize(name).split() if len(w) >= 3}


def similar(a: str, b:str, threshold: float) -> bool:
    return SequenceMatcher(None, a, b).ratio() >= threshold


def delete_game_paths(game_paths: list[Path], logs: bool) -> None:
    for game_path in game_paths:
        if game_path.is_dir():
            shutil.rmtree(game_path)
        else:
            game_path.unlink()
        
        if logs: log(f"[DELETE]: Deleted {'folder' if game_path.is_dir() else 'file'} {game_path}.")

    print(f"\nDeleted {len(game_paths)} games")



def get_game_paths(path: Path, game_console_pairs: list[tuple[str, str]]) -> list[Path]:
    paths = []
    for game, console in game_console_pairs:
        console_path = path / console

        for file in console_path.rglob("*"):
            if file.stem == game:
                paths.append(file)

    return paths

def confirm_delete(game_paths: list[Path], force: bool) -> bool:
    if not force:
        print("\nThese game paths will be deleted permanently:")
        for p in game_paths:
            print(p)
    answer = "yes" if force else input("\nDo you confirm? (yes/no) ").lower().strip()
    return answer == "yes"


def build_edges(games: list[str], logs: bool, threshold: float) -> dict[str, set[str]]:
    edges = {g: set() for g in games}
    tokens = {g: tokenize(g) for g in games}
    normalized = {g: normalize(g, lower=True) for g in games}

    for i in range(len(games)):
        for j in range(i + 1, len(games)):
            a = games[i]
            b = games[j]

            if threshold == 1.0:
                if a.lower() == b.lower():
                    edges[a].add(b)
                    edges[b].add(a)
                continue

            if tokens[a].isdisjoint(tokens[b]): continue

            if similar(normalized[a], normalized[b], threshold):
                edges[a].add(b)
                edges[b].add(a)


    if logs: 
        for game, similars in edges.items():
            log(f"[EDGES]: {game} = {similars}")

    return edges


def dfs_edges(node: str, edges: dict[str, set[str]], visited: set[str], games_and_consoles: dict[str, list[str]], cluster: list[tuple[str, str]]):
    visited.add(node)
    for console in games_and_consoles[node]:
        cluster.append((node, console))

    for neighbor in edges[node]:
        if neighbor not in visited:
            dfs_edges(neighbor, edges, visited, games_and_consoles, cluster)


def get_similar_games(games_and_consoles: dict[str, list[str]], logs: bool, threshold: float) -> list[list[tuple[str, str]]]:
    edges = build_edges(list(games_and_consoles.keys()), logs, threshold)
    similar_games = list() 

    visited = set()
    for node in edges:
        if node in visited: continue

        cluster = list()
        dfs_edges(node, edges, visited, games_and_consoles, cluster)

        if len(cluster) > 1:
            if logs: 
                for game, console in cluster:
                    log(f"[CLUSTER]: {game} -> {console}")
                log("--next--")
                    
            similar_games.append(cluster)
    
    return similar_games


def delete_similar(path: Path, games_and_consoles: dict[str, list[str]], force: bool, logs: bool, threshold: str) -> None:
    threshold_map = {"exact": 1.0, "close": 0.75, "fuzzy": 0.65}

    print("Building similar games...")
    clusters = get_similar_games(games_and_consoles, logs, threshold_map[threshold])

    for c in clusters:
        clear_console()
        cluster = sorted(c)

        print(f"Found {len(cluster)} games with the '{threshold}' option\n")
        for i, (game, console) in enumerate(cluster, start=1):
            print(f"{i}) {game} -> {console}")
        
        while True:
            choice = input(
                "\nFrom which console numbers you wish to eliminate the game? "
                "(comma-separated, 'skip' if unsure): "
                ).strip().lower()
        
            try: 
                indices = [int(i.strip()) - 1 for i in choice.split(",")]
                games_to_delete = [cluster[idx] for idx in indices]
                game_paths = get_game_paths(path, games_to_delete)
            except (ValueError, IndexError) as e:
                print(f"[WARNING]: Incorrect input of console numbers. {e}\n")
                continue
            break
        
        if confirm_delete(game_paths, force): delete_game_paths(game_paths, logs)
        if not prompt_continue(): break
    
    print("Deletion finalized. Press enter to exit")
    input()







        



        



            





