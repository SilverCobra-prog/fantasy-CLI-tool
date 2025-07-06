import argparse
from .utils import fetch_player_stats, lookup_player_id, compare_players

def create_cli_parser():
    """Create and return the argument parser for the CLI tool."""
    parser = argparse.ArgumentParser(
        description="Retrieve or compare MLB player statistics.",
        add_help=True
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--player-name',
        type=str,
        help='Get stats of a player by name (e.g., --player-name "Mike Trout").'
    )
    group.add_argument(
        '--compare',
        nargs=2,
        metavar=('PLAYER1', 'PLAYER2'),
        help='Compare two players by name (e.g., --compare "Mike Trout" "Shohei Ohtani").'
    )
    return parser

def main():
    """Parse CLI arguments and print MLB statistics or compare two players."""
    parser = create_cli_parser()
    args = parser.parse_args()

    try:
        if args.player_name:
            player_id = lookup_player_id(args.player_name)
            if player_id:
                stats = fetch_player_stats(player_id)
                print(stats)
        elif args.compare:
            player_id_1 = lookup_player_id(args.compare[0])
            player_id_2 = lookup_player_id(args.compare[1])
            if player_id_1 and player_id_2:
                comparison = compare_players(player_id_1, player_id_2)
                print(comparison)
    except Exception as e:
        print(f"Error retrieving stats: {e}")

if __name__ == "__main__":
    main()