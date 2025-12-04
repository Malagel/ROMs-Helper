from core.utils import log, clear_console, prompt_continue
from collections import defaultdict
from itertools import combinations
from rapidfuzz import fuzz
from pathlib import Path
import shutil


def delete_game_paths(game_paths: list[Path], logs: bool) -> None:
    for game_path in game_paths:
        is_dir = game_path.is_dir()

        if is_dir:
            shutil.rmtree(game_path)
        else:
            game_path.unlink()
        
        if logs: log(f"[DELETE]: Deleted {'folder' if is_dir else 'file'} {game_path}.")

    print(f"\nDeleted {len(game_paths)} games")


def confirm_delete(game_paths: list[Path], force: bool) -> bool:
    if not force:
        print("\nThese game paths will be deleted permanently:")
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
    

def delete_similar(games_data: dict[int, dict], force: bool, logs: bool, threshold: str) -> None:
    threshold_map = {"identical": 100, "similar": 76}

    print("Building similar games...")
    clusters = get_clusters(games_data, threshold_map[threshold])

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
                "(Press 'enter' to go next or 'quit' to exit): "
                ).strip().lower()
            if not choice or choice == 'quit': break

            try: 
                indices = [int(i.strip()) - 1 for i in choice.split(",")]
                game_paths = [games_data[sorted_cluster[idx]]['path'] for idx in indices]
            except (ValueError, IndexError) as e:
                print(f"[WARNING]: Incorrect input of console numbers. {e}")
                continue
            break

        if not choice: continue
        elif choice == 'quit': break

        if confirm_delete(game_paths, force): 
            delete_game_paths(game_paths, logs)
        else:
            print("Skipping...")
            
        if not prompt_continue(): break
    
    print("Deletion finalized.")