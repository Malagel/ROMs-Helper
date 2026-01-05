from core.utils import clear_console, prompt_continue, get_app_base_dir, normalize
from core.logger import log
from collections import defaultdict
from itertools import combinations
from rapidfuzz import fuzz
from pathlib import Path
import shutil
import time

MAX_CLUSTER_SIZE = 100

class ClusterTooLargeError(Exception):
    pass


def delete_game_paths(game_paths: list[Path], logs: bool, trueDeletion: bool) -> None:
    if not trueDeletion:
        base = get_app_base_dir()
        delete_dir = base / "DELETE"
        delete_dir.mkdir(exist_ok=True)

    action = "Deleted" if trueDeletion else "Moved"
    dest = "." if trueDeletion else " to 'DELETE' folder"

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

        if logs: log(f"[DETECT DUPLICATES]: {action} {'folder' if is_dir else 'file'} {game_path}{dest}")

    len_game_paths = len(game_paths)
    game_s = 'game' if len_game_paths == 1 else 'games'
    print(f"\n• {action} {len_game_paths} {game_s}{dest}")


def confirm_delete(game_paths: list[Path], force: bool, trueDeletion: bool) -> bool:
    if force: return True
    sentence = 'This game path' if len(game_paths) == 1 else 'These game paths'
    action = "moved to the 'DELETE' folder" if not trueDeletion else "deleted permanently"
    print(f"\n{sentence} will be {action}:")

    for p in game_paths:
        print(f"▶ {p}")

    while True:
        print("\nDo you confirm? [y/N]")
        answer = input("> ").lower().strip()
        if answer in ['y', 'n']:
            break
        print("[ERROR]: Invalid answer, try again.")
    
    return answer == 'y'


def build_similarity_graph(games_data: dict[int, dict], threshold: float) -> dict[int, list[int]]:
    graph = defaultdict(list)
    game_items = list(games_data.items())

    for (id1, data1), (id2, data2) in combinations(game_items, 2):
        n1 = data1["normalized_name"]
        n2 = data2["normalized_name"]

        if threshold == 100:
            n1 = normalize(data1["original_name"])
            n2 = normalize(data2["original_name"]) 

            if n1 == n2:
                graph[id1].append(id2)
                graph[id2].append(id1)
            continue

        score = fuzz.token_sort_ratio(n1, n2)

        if score >= threshold:
            graph[id1].append(id2)
            graph[id2].append(id1)

    return graph


def dfs_clusters(graph: dict[int, list[int]], node: int, visited: set, cluster: list[int]):
    visited.add(node)
    cluster.append(node)

    if len(cluster) > MAX_CLUSTER_SIZE: 
        raise ClusterTooLargeError

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_clusters(graph, neighbor, visited, cluster)


def get_clusters(games_data: dict[int, dict], threshold: float, logs: bool) -> list[list[int]]:
    if logs: log(f"[DETECT DUPLICATES]: Building similarity graph with threshold {threshold}. This can be customized with --dd-custom-threshold.")
    graph = build_similarity_graph(games_data, threshold)
    if logs: log(f"[DETECT DUPLICATES]: Graph done.")

    visited = set()
    clusters = []
    
    if logs: log(f"[DETECT DUPLICATES]: Building clusters by searching inside the graph.")

    for node in graph:
        if node not in visited:
            cluster = []
            dfs_clusters(graph, node, visited, cluster)
            if len(cluster) > 1: clusters.append(cluster)

    return clusters
    

def detect_duplicates(games_data: dict[int, dict], force: bool, logs: bool, threshold: float, trueDeletion: bool) -> None:
    print(f"• Building games with the threshold as {'default' if threshold == 76.0 else threshold}...", end="", flush=True)

    try:
        clusters = get_clusters(games_data, threshold, logs)
    except ClusterTooLargeError:
        msg ="\n[ERROR]: With the current threshold, the number of detected games exceeds 100.\n" \
             "Similarity was detected across too many entries of games, making it unfeasible for displaying.\n" \
             "Please try again with a higher threshold value."
        print(msg)
        if logs: log(msg)

        print("\n• Duplicates detection finalized.")
        return

    print("DONE")

    if logs:
        log("[DETECT DUPLICATES]: Showing clusters...")
        for cluster in clusters:
            for id in cluster:
                log(f"> {games_data[id]['original_name']} -- {games_data[id]['normalized_name']}")
            log("[DETECT DUPLICATES]: Next cluster.")

    for cluster in clusters:
        clear_console()
        sorted_cluster = sorted(cluster, key=lambda x: games_data[x]["original_name"])

        print(f"Found {len(sorted_cluster)} games with the threshold as {'default' if threshold == 76.0 else threshold}:\n")
        for i, id in enumerate(sorted_cluster, start=1):
            print(f"[{i}] {games_data[id]['original_name']}  →  {games_data[id]['metadata']['console']}")
        
        while True:
            print(
                f"\nSelect the games you wish to {'eliminate' if trueDeletion else 'move to a folder'}" 
                ", separated with spaces (e.g.: 1 3 5).\n"
                "(Leave it blank to skip or type 'quit' to exit): "
                )
            choice = input("> ").strip().lower()
            if not choice or choice == 'quit': break

            try: 
                indices = [int(i.strip()) - 1 for i in choice.split() if i.isdigit() and int(i) > 0]
                if not indices: 
                    raise ValueError
                
                game_paths = [games_data[sorted_cluster[idx]]['path'] for idx in indices]

            except (ValueError, IndexError):
                print(f"[ERROR]: The value is invalid, try again")
                continue

            if confirm_delete(game_paths, force, trueDeletion): 
                delete_game_paths(game_paths, logs, trueDeletion)
                break
            else:
                print("\n• Retrying...")

        if not choice: continue
        elif choice == 'quit': break

        if not prompt_continue(): break
    
    print("\n• Duplicates detection finalized.")