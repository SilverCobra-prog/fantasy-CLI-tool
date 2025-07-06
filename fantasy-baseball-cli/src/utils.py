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

def format_player_stats(player_dict):
    """Nicely format player stats from the statsapi.get('people', ...)['people'][0] dict."""
    lines = []
    lines.append(f"{player_dict['fullName']} ({player_dict['primaryPosition']['name']})")
    lines.append("")

    for stat_group in player_dict.get('stats', []):
        group_name = stat_group['group']['displayName'].capitalize()
        type_name = stat_group['type']['displayName'].capitalize()
        lines.append(f"{type_name} {group_name}")
        for split in stat_group.get('splits', []):
            stat = split.get('stat', {})
            for k, v in stat.items():
                if isinstance(v, dict):
                    continue
                lines.append(f"    {k}: {v}")
            lines.append("")  #
    return "\n".join(lines)

def fetch_player_stats(player_id, season=None, type="season"):
    """
    Fetch player statistics for a specific season or career.
    Returns a formatted string for career, or a formatted dict for a specific season.
    """
    try:
        if season:
            stats = statsapi.get(
                'people',
                {
                    'personIds': player_id,
                    'season': season,
                    'hydrate': f'stats(group=[hitting,pitching,fielding],type=season,season={season})'
                }
            )['people'][0]
            return format_player_stats(stats)
        else:
            return statsapi.player_stats(player_id, type=type)
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

def handle_api_error(response):
    """Handle errors from the API response."""
    if response.status_code != 200:
        print(f"API Error: {response.status_code} - {response.text}")
        return False
    return True