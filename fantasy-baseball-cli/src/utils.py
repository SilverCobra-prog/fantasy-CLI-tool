import statsapi

def lookup_player_id(name):
    """Lookup a player ID by name using statsapi."""
    players = statsapi.lookup_player(name)
    if not players:
        print(f"No player found with name '{name}'.")
        return None
    if len(players) > 1:
        print(f"Multiple players found for '{name}', using the first match: {players[0]['fullName']}")
    return players[0]['id']

def lookup_player_name(id):
    """Lookup a player's full name by name using statsapi."""
    players = statsapi.lookup_player(id)
    if not players:
        print(f"No player found with id '{id}'.")
        return None
    if len(players) > 1:
        print(f"Multiple players found for '{id}', using the first match: {players[0]['fullName']}")
    return players[0]['fullName']

def fetch_player_stats(player_id):
    """Fetch player statistics from the MLB StatsAPI."""
    try:
        player_stats = statsapi.player_stats(player_id)
        return player_stats
    except Exception as e:
        print(f"Error fetching stats for player ID {player_id}: {e}")
        return None

def parse_stats(stats_str):
    """Parse all key-value pairs in the stats string into a dictionary."""
    lines = stats_str.splitlines()
    stats = {}
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            stats[key.strip()] = value.strip()
    return stats

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

def handle_api_error(response):
    """Handle errors from the API response."""
    if response.status_code != 200:
        print(f"API Error: {response.status_code} - {response.text}")
        return False
    return True