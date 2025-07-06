import argparse
from .utils import fetch_player_stats, lookup_player_id
from .commands import compare_players

def create_cli_parser():
    """Create and return the argument parser for the CLI tool."""
    parser = argparse.ArgumentParser(
        description="Retrieve or compare MLB player statistics.",
        add_help=True
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--player',
        type=str,
        help='Get stats of a player by name (e.g., --player "Mike Trout").'
    )
    group.add_argument(
        '--compare',
        nargs=2,
        metavar=('PLAYER1', 'PLAYER2'),
        help='Compare two players by name (e.g., --compare "Mike Trout" "Shohei Ohtani").'
    )
    stat_group = parser.add_mutually_exclusive_group(required=False)
    stat_group.add_argument(
        '--season',
        type=str,
        help='Optionally specify a season/year for stats (e.g., --season 2021).'
    )
    stat_group.add_argument(
        '--career',
        action='store_true',
        help='Show career stats instead of season stats.'
    )
    return parser

def main():
    """Parse CLI arguments and print MLB statistics or compare two players."""
    parser = create_cli_parser()
    args = parser.parse_args()

    try:
        if args.player:
            player_id = lookup_player_id(args.player)
            if player_id:
                if args.career:
                    stats = fetch_player_stats(player_id, type="career")
                else:
                    stats = fetch_player_stats(player_id, season=args.season)
                print(stats)
        elif args.compare:
            player_id_1 = lookup_player_id(args.compare[0])
            player_id_2 = lookup_player_id(args.compare[1])
            if player_id_1 and player_id_2:
                comparison = compare_players(
                    player_id_1,
                    player_id_2,
                    season=args.season,
                    career=args.career
                )
                print(comparison)    
    except Exception as e:
        print(f"Error retrieving stats: {e}")

if __name__ == "__main__":
    main()