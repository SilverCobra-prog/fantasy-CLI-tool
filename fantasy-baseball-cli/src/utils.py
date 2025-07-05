import statsapi

def fetch_player_stats(player_id):
    """Fetch player statistics from the MLB StatsAPI."""
    try:
        # statsapi.player_stats returns a string summary, not a dict
        player_stats = statsapi.player_stats(player_id)
        return player_stats
    except Exception as e:
        print(f"Error fetching stats for player ID {player_id}: {e}")
        return None

def format_stats(stats):
    """Format the player statistics for display."""
    if not stats:
        return "No statistics available."
    # statsapi.player_stats returns a string, so just return it
    return stats


def handle_api_error(response):
    """Handle errors from the API response."""
    if response.status_code != 200:
        print(f"API Error: {response.status_code} - {response.text}")
        return False
    return True