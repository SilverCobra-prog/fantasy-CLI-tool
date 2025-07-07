import requests

def lookup_team_id(team_name):
    """
    Lookup a team's MLB ID by its name (case-insensitive, supports partial matches).
    Returns the team ID or None if not found.
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

def fetch_team_stats(team_name, season=None, group="hitting,pitching", stats_type="season"):
    """
    Fetch team stats using /api/v1/teams/{teamId}/stats endpoint.
    Defaults to season 2025 if not specified.
    """
    if not season:
        season = "2025"
    team_id = lookup_team_id(team_name)
    if not team_id:
        print(f"Team '{team_name}' not found.")
        return None
    stats_url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/stats"
    params = {
        "stats": stats_type,
        "group": group,
        "season": season
    }
    # Print the endpoint and params for debugging
    print(f"Requesting: {stats_url} with params {params}")
    stats_res = requests.get(stats_url, params=params)
    if stats_res.status_code != 200:
        print(f"API Error: {stats_res.status_code} - {stats_res.text}")
        return None
    stats_data = stats_res.json()
    return stats_data.get("stats", [])

print(fetch_team_stats("San Francisco Giants"))