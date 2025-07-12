from src.utils import fetch_player_stats, parse_stats, lookup_player_name, calculate_fantasy_score
import requests

def compare_players(player_id_1, player_id_2, season=None, career=False):
    """
    Compare two players' statistics and return a side-by-side formatted string.
    Optionally compare for a specific season or for career stats.
    """
    if career:
        stats1_str = fetch_player_stats(player_id_1, type="career")
        stats2_str = fetch_player_stats(player_id_2, type="career")
    else:
        stats1_str = fetch_player_stats(player_id_1, season=season)
        stats2_str = fetch_player_stats(player_id_2, season=season)

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

def get_player_fantasy_points(player_id, season=None):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}"
    season_used = season or '2025'
    params = {
        "hydrate": f"stats(group=[hitting,pitching,fielding],type=season,season={season_used})"
    }
    res = requests.get(url, params=params, timeout=120)
    if res.status_code == 200:
        data = res.json()
        if "people" in data and data["people"]:
            player = data["people"][0]
            stat_dicts = []
            for stat_group in player.get('stats', []):
                for split in stat_group.get('splits', []):
                    stat_dicts.append(split.get('stat', {}))
            score = calculate_fantasy_score(stat_dicts)
            print(f"Fantasy score for {player.get('fullName')} ({season_used}): {score}")
            return score
        else:
            print("No player data found.")
    else:
        print(f"API Error: {res.status_code} - {res.text}")
