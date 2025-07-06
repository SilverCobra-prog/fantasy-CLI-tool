import requests

def lookup_player_id(name):
    """Get a player's name from their MLB player ID."""
    url = "https://statsapi.mlb.com/api/v1/people/search"
    params = {"names": [name]} 
    res = requests.get(url, params=params)
    data = res.json()
    if "people" in data and data["people"]:
        return data["people"][0]["id"]
    return None


def lookup_player_name(id):
    """Get a player's MLB player ID from their name."""
    url = "https://statsapi.mlb.com/api/v1/people/search"
    params = {"personIds": [id]} 
    res = requests.get(url, params=params)
    data = res.json()
    if "people" in data and data["people"]:
        return data["people"][0]["fullName"]
    return None

def format_player_stats(player_dict):
    """Nicely format player stats."""
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
            url = f"https://statsapi.mlb.com/api/v1/people/{player_id}"
            params = {
                "hydrate": f"stats(group=[hitting,pitching,fielding],type=season,season={season})",
                "season": season
            }
            res = requests.get(url, params=params)
            if res.status_code != 200:
                print(f"API Error: {res.status_code} - {res.text}")
                return None
            data = res.json()
            if "people" in data and data["people"]:
                return format_player_stats(data["people"][0])
            else:
                print("No player data found.")
                return None
        else:
            url = f"https://statsapi.mlb.com/api/v1/people/{player_id}"
            params = {
                "hydrate": "stats(group=[hitting,pitching,fielding],type=career)"
            }
            res = requests.get(url, params=params)
            if res.status_code != 200:
                print(f"API Error: {res.status_code} - {res.text}")
                return None
            data = res.json()
            if "people" in data and data["people"]:
                return format_player_stats(data["people"][0])
            else:
                print("No player data found.")
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