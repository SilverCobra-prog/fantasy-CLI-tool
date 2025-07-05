import argparse
from .utils import fetch_player_stats

def create_cli_parser():
    """Create and return the argument parser for the CLI tool."""
    parser = argparse.ArgumentParser(
        description="Retrieve MLB statistics.",
        add_help=True
    )
    parser.add_argument(
        '--player-id',
        type=int,
        required=True,
        help='The ID of the player to retrieve statistics for.'
    )
    return parser

def main():
    """Parse CLI arguments and print MLB statistics."""
    parser = create_cli_parser()
    args = parser.parse_args()

    try:
        stats = fetch_player_stats(args.player_id)
        print(stats)
    except Exception as e:
        print(f"Error retrieving stats: {e}")

if __name__ == "__main__":
    main()