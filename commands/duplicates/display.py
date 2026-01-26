def sort_and_print_cluster(cluster: list[int], games_data: dict[int, dict], threshold_string: str) -> list[int]:
    sorted_cluster = sorted(cluster, key=lambda x: games_data[x]["original_name"])

    print(f"• Found {len(sorted_cluster)} games with the threshold as {threshold_string}:\n")
    for i, id in enumerate(sorted_cluster, start=1):
        print(f"[{i}] {games_data[id]['original_name']}  →  {games_data[id]['metadata']['console']}")

    return sorted_cluster