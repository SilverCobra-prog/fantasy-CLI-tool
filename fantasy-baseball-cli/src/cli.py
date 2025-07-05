import argparse
from .utils import fetch_player_stats
import statsapi

def create_cli_parser():
    """Create and return the argument parser for the CLI tool."""
    parser = argparse.ArgumentParser(
        description="Retrieve MLB statistics.",
        add_help=True
    )
    parser.add_argument(
        '--player-name',
        type=str,
        required=True,
        help='The name of the player to retrieve statistics for (e.g., "Mike Trout").'
    )
    return parser

def main():
    """Parse CLI arguments and print MLB statistics."""
    parser = create_cli_parser()
    args = parser.parse_args()

    try:
        players = statsapi.lookup_player(args.player_name)
        if not players:
            print(f"No player found with name '{args.player_name}'.")
            return
        player_id = players[0]['id']
        stats = fetch_player_stats(player_id)
        print(stats)
    except Exception as e:
        print(f"Error retrieving stats: {e}")

if __name__ == "__main__":
    main()