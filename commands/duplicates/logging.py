from core.logger import log

def log_found_clusters(clusters: list[list[int]], games_data: dict[int, dict]):
    log("Showing clusters built...")
    for cluster in clusters:
        for id in cluster:
            log(f"> Original: {games_data[id]['original_name']}, Normalized: {games_data[id]['fuzzy_name']}")
        log("----- Next Cluster -----")

