from core.helpers.text import normalize, extract_sequel_numbers
from core.helpers.exceptions import ClusterTooLargeError
from collections import defaultdict
from itertools import combinations
from rapidfuzz import fuzz

from core.helpers.constants import( 
    MAX_THRESHOLD,
    SEQUEL_PENALTIES,
    MAX_CLUSTER_SIZE
    )

def build_similarity_graph(games_data: dict[int, dict], threshold: float) -> dict[int, list[int]]:
    graph = defaultdict(list)
    game_items = list(games_data.items())

    for (id1, data1), (id2, data2) in combinations(game_items, 2):
        if threshold == MAX_THRESHOLD:
            n1 = normalize(data1["strict_name"], full_clean=False)
            n2 = normalize(data2["strict_name"], full_clean=False) 

            if n1 == n2:
                graph[id1].append(id2)
                graph[id2].append(id1)
            continue

        n1 = data1["fuzzy_name"]
        n2 = data2["fuzzy_name"]
        nums1 = extract_sequel_numbers(n1)
        nums2 = extract_sequel_numbers(n2)
        
        score = fuzz.token_sort_ratio(n1, n2)

        if (nums1 and not nums2) or (nums2 and not nums1):
            score *= SEQUEL_PENALTIES["missing_vs_present"]
        elif nums1 and nums2 and nums1 != nums2:
            score *= SEQUEL_PENALTIES["different_numbers"]  

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


def get_clusters(games_data: dict[int, dict], threshold: float) -> list[list[int]]:
    graph = build_similarity_graph(games_data, threshold)

    visited = set()
    clusters = []
    
    for node in graph:
        if node not in visited:
            cluster = []
            dfs_clusters(graph, node, visited, cluster)
            if len(cluster) > 1: clusters.append(cluster)

    return sorted(clusters, key=lambda x: games_data[x[0]]["original_name"])

