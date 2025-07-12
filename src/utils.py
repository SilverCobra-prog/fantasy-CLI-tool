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
            lines.append("")  
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
    
def lookup_team_id(team_name):
    """
    Lookup a team's MLB ID by its name (case-insensitive, supports partial matches).
    """
    teams_url = "https://statsapi.mlb.com/api/v1/teams"
    teams_res = requests.get(teams_url)
    if teams_res.status_code != 200:
        print(f"API Error: {teams_res.status_code} - {teams_res.text}")
        return None
    teams_data = teams_res.json()
    team_name_lower = team_name.lower()
    for team in teams_data.get("teams", []):
        if (team_name_lower == team["name"].lower() or
            team_name_lower == team.get("teamName", "").lower() or
            team_name_lower == team.get("locationName", "").lower() or
            team_name_lower in team["name"].lower() or
            team_name_lower in team.get("teamName", "").lower()):
            return team["id"]
    print(f"Team '{team_name}' not found.")
    return None

def format_team_stats(stats):
    """
    Nicely format team stats from the /api/v1/teams/{teamId}/stats endpoint.
    """
    if not stats:
        return "No stats available."

    lines = []
    for stat_group in stats:
        group_name = stat_group.get('group', {}).get('displayName', '').capitalize()
        type_name = stat_group.get('type', {}).get('displayName', '').capitalize()
        lines.append(f"{type_name} {group_name}")
        for split in stat_group.get('splits', []):
            stat = split.get('stat', {})
            for k, v in stat.items():
                if isinstance(v, dict):
                    continue
                lines.append(f"    {k}: {v}")
            lines.append("")
    return "\n".join(lines)


def fetch_team_stats(team_name, season=None, group="hitting,pitching,fielding", stats_type="season"):
    """
    Fetch team stats using /api/v1/teams/{teamId}/stats endpoint.
    Defaults to season 2025 if not specified.
    """
    if not season:
        season = "2025"
    team_id = lookup_team_id(team_name)
    if not team_id:
        return f"Team '{team_name}' not found."
    stats_url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/stats"
    params = {
        "stats": stats_type,
        "group": group,
        "season": season
    }
    stats_res = requests.get(stats_url, params=params)
    if stats_res.status_code != 200:
        return f"API Error: {stats_res.status_code} - {stats_res.text}"
    stats_data = dict(stats_res.json())
    return print(format_team_stats(stats_data.get("stats", [])))

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


def calculate_fantasy_score(players_stats):
    """
    Calculate the total fantasy score for a player or list of stat dicts using a custom scoring system.
    Accepts a single dict or a list of dicts.
    Returns the total fantasy score (float).
    """
    scoring = {
        # Batting
        "runs": 1,                # R
        "totalBases": 1,          # TB
        "rbi": 1,                 # RBI
        "baseOnBalls": 1,         # BB
        "strikeOuts": -1,         # K 
        "stolenBases": 1,         # SB
        # Pitching
        "inningsPitched": 3,      # IP
        "hits": -1,               # H
        "earnedRuns": -2,         # ER
        "holds": 2,               # HD
        "pitchingBaseOnBalls": -1,# BB 
        "pitchingStrikeOuts": 1,  # K 
        "wins": 2,                # W
        "losses": -2,             # L
        "saves": 2                # SV
    }

    if isinstance(players_stats, dict):
        stats_list = [players_stats]
    else:
        stats_list = players_stats

    total = 0.0
    for stats in stats_list:
        # Batting
        total += scoring["runs"] * float(stats.get("runs", 0))
        total += scoring["totalBases"] * float(stats.get("totalBases", 0))
        total += scoring["rbi"] * float(stats.get("rbi", 0))
        total += scoring["baseOnBalls"] * float(stats.get("baseOnBalls", 0))
        total += scoring["strikeOuts"] * float(stats.get("strikeOuts", 0))
        total += scoring["stolenBases"] * float(stats.get("stolenBases", 0))
        # Pitching
        total += scoring["inningsPitched"] * float(stats.get("inningsPitched", 0))
        total += scoring["hits"] * float(stats.get("hits", 0))
        total += scoring["earnedRuns"] * float(stats.get("earnedRuns", 0))
        total += scoring["holds"] * float(stats.get("holds", 0))
        # For pitching walks and strikeouts, try to distinguish if possible
        # If not, use baseOnBalls and strikeOuts for both
        total += scoring["pitchingBaseOnBalls"] * float(stats.get("baseOnBalls", 0))
        total += scoring["pitchingStrikeOuts"] * float(stats.get("strikeOuts", 0))
        total += scoring["wins"] * float(stats.get("wins", 0))
        total += scoring["losses"] * float(stats.get("losses", 0))
        total += scoring["saves"] * float(stats.get("saves", 0))
    return total

def fetch_team_roster(team_id, season):
    """
    Fetch the roster for a specific team and season using the MLB StatsAPI.
    Returns a list of player dictionaries or None if not found.
    """
    url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/roster"
    params = {"season": season}
    try:
        res = requests.get(url, params=params)
        if res.status_code != 200:
            print(f"API Error: {res.status_code} - {res.text}")
            return None
        data = res.json()
        return data.get("roster", [])
    except Exception as e:
        print(f"Error fetching roster for team {team_id} in season {season}: {e}")
        return None