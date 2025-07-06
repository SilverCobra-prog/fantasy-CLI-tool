import statsapi
from .utils import fetch_player_stats, parse_stats, lookup_player_name

def compare_players(player_id_1, player_id_2):
    """Compare two players' statistics and return a side-by-side formatted string."""
    stats1_str = fetch_player_stats(player_id_1)
    stats2_str = fetch_player_stats(player_id_2)

    if not stats1_str or not stats2_str:
        return "Could not retrieve stats for one or both players."

    stats1 = parse_stats(stats1_str)
    stats2 = parse_stats(stats2_str)

    all_keys = sorted(set(stats1.keys()) | set(stats2.keys()))
    player1_name = lookup_player_name(player_id_1)
    player2_name = lookup_player_name(player_id_2)
    header = f"{'Stat':<20} | {player1_name} | {player2_name}"
    sep = "-" * len(header)
    rows = [header, sep]
    for key in all_keys:
        val1 = stats1.get(key, "-")
        val2 = stats2.get(key, "-")
        rows.append(f"{key:<20} | {val1:<{len(player1_name)}} | {val2:<{len(player2_name)}}")
    return "\n".join(rows)

def format_stats(stats):
    """Format the player statistics for display."""
    if not stats:
        return "No statistics available."
    return stats
