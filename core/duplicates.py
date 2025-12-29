from core.utils import clear_console, prompt_continue, get_app_base_dir
from core.logger import log
from collections import defaultdict
from itertools import combinations
from rapidfuzz import fuzz
from pathlib import Path
import shutil


def delete_game_paths(game_paths: list[Path], logs: bool, trueDeletion: bool) -> None:
    if not trueDeletion:
        base = get_app_base_dir()
        delete_dir = base / "DELETE"
        delete_dir.mkdir(exist_ok=True)

    for game_path in game_paths:
        is_dir = game_path.is_dir()
        
        if trueDeletion:
            if is_dir:
                shutil.rmtree(game_path)
            else:
                game_path.unlink()
        else:
            target = delete_dir / game_path.name
            
            counter = 1
            while target.exists():
                target = delete_dir / f"{game_path.stem}_{counter}{game_path.suffix}"
                counter += 1

            shutil.move(str(game_path), str(target))

        if logs: 
            action = "Deleted" if trueDeletion else "Moved"
            dest = "" if trueDeletion else " to 'DELETE' folder"

            log(f"[DELETE]: {action} {'folder' if is_dir else 'file'} {game_path}{dest}.")

    action = "Deleted" if trueDeletion else "Moved"
    dest = "" if trueDeletion else " to 'DELETE' folder"
    print(f"{action} {len(game_paths)} games{dest}")


def confirm_delete(game_paths: list[Path], force: bool, trueDeletion: bool) -> bool:
    action = "moved to the 'DELETE' folder" if not trueDeletion else "deleted permanently"
    if not force:
        print(f"\nThese game paths will be {action}:")
        for p in game_paths:
            print(str(p))

    while True:
        answer = "yes" if force else input("\nDo you confirm? (yes/no) ").lower().strip()
        if answer in ['yes', 'no']:
            break

    return answer == 'yes'


def build_similarity_graph(games_data: dict[int, dict], threshold: float) -> dict[int, list[int]]:
    graph = defaultdict(list)
    game_items = list(games_data.items())

    for (id1, data1), (id2, data2) in combinations(game_items, 2):
        n1 = data1["normalized_name"]
        n2 = data2["normalized_name"]

        if threshold == 100:
            if n1 == n2:
                graph[id1].append(id2)
                graph[id2].append(id1)
            continue

        score = fuzz.token_sort_ratio(n1, n2)

        if score >= threshold:
            graph[id1].append(id2)
            graph[id2].append(id1)

    return graph

def dfs_clusters(graph: dict[int, list[int]], node: int, visited: set, cluster: list):
    visited.add(node)
    cluster.append(node)
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_clusters(graph, neighbor, visited, cluster)


def get_clusters(games_data: dict[int, dict], threshold: float) -> list[list[int]]:
    graph = build_similarity_graph(games_data, threshold)

    visited = set()
    clusters = []
    
    for node in graph:
        if node not in visited:
            cluster = []
            dfs_clusters(graph, node, visited, cluster)
            if len(cluster) > 1: clusters.append(cluster)

    return clusters
    

def detect_duplicates(games_data: dict[int, dict], force: bool, logs: bool, threshold: str, trueDeletion: bool) -> None:
    threshold_map = {"identical": 100, "similar": 76}

    print(f"Building {threshold} games...", end="", flush=True)
    clusters = get_clusters(games_data, threshold_map[threshold])
    print("DONE")

    if logs:
        for cluster in clusters:
            for id in cluster:
                log(f"[CLUSTER]: {games_data[id]['original_name']} -- {games_data[id]['normalized_name']}")
            log("")

    for cluster in clusters:
        clear_console()
        sorted_cluster = sorted(cluster, key=lambda x: games_data[x]["original_name"])

        print(f"Found {len(sorted_cluster)} games with the '{threshold}' option\n")
        for i, id in enumerate(sorted_cluster, start=1):
            print(f"{i}) {games_data[id]['original_name']} -> {games_data[id]['metadata']['console']}")
        
        while True:
            choice = input(
                "\nFrom which console numbers you wish to eliminate the game? Separate it with commas.\n"
                "(Leave it blank to skip or type 'quit' to exit): "
                ).strip().lower()
            if not choice or choice == 'quit': break

            try: 
                indices = [int(i.strip()) - 1 for i in choice.split(",")]
                game_paths = [games_data[sorted_cluster[idx]]['path'] for idx in indices]
            except (ValueError, IndexError):
                print(f"[WARNING]: Incorrect input of console numbers. Try again")
                continue
            break

        if not choice: continue
        elif choice == 'quit': break

        if confirm_delete(game_paths, force, trueDeletion): 
            delete_game_paths(game_paths, logs, trueDeletion)
        else:
            print("Skipping...")
            
        if not prompt_continue(): break
    
    print("\nDeletion finalized.")