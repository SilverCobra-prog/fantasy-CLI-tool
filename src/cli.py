import argparse
from .utils import fetch_player_stats, lookup_player_id, fetch_team_stats
from .commands import compare_players, get_player_fantasy_points
from .fantasy_db import init_fantasy_db, add_player_to_team, remove_player_from_team, list_fantasy_team, print_team_fantasy_scores

def create_cli_parser():
    """Create and return the argument parser for the CLI tool."""
    parser = argparse.ArgumentParser(
        description="Retrieve or compare MLB player statistics, or manage your fantasy team.",
        add_help=True
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--player',
        type=str,
        help='Get stats of a player by name (e.g., --player "Mike Trout").'
    )
    group.add_argument(
        '--team',
        type=str,
        help='Get stats of a player by name (e.g., --team "San Francisco Giants").'
    )
    group.add_argument(
        '--compare',
        nargs=2,
        metavar=('PLAYER1', 'PLAYER2'),
        help='Compare two players by name (e.g., --compare "Mike Trout" "Shohei Ohtani").'
    )
    group.add_argument(
        '--fantasy-add',
        nargs=2,
        metavar=('USER', 'PLAYER'),
        help='Add a player to a user\'s fantasy team (e.g., --fantasy-add my-team "Mike Trout").'
    )
    group.add_argument(
        '--fantasy-remove',
        nargs=2,
        metavar=('USER', 'PLAYER'),
        help='Remove a player from a user\'s fantasy team (e.g., --fantasy-remove my-team "Mike Trout").'
    )
    group.add_argument(
        '--fantasy-list',
        metavar='USER',
        help='List all players on a user\'s fantasy team (e.g., --fantasy-list my-team).'
    )
    group.add_argument(
        '--fantasy-score',
        type=str,
        metavar='PLAYER',
        help='Show the fantasy score for a player for a season (e.g., --fantasy-score "Mike Trout" --season 2021).'
    )
    group.add_argument(
        '--fantasy-team-score',
        type=str,
        metavar=('USER'),
        help='Show the fantasy score for all players in a fantasy team for a season (e.g., --fantasy-team-score my-team).'
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
    """Parse CLI arguments and print MLB statistics or manage fantasy teams."""
    parser = create_cli_parser()
    args = parser.parse_args()

    try:
        init_fantasy_db()
        if args.player:
            player_id = lookup_player_id(args.player)
            if player_id:
                if args.career:
                    stats = fetch_player_stats(player_id, type="career")
                else:
                    stats = fetch_player_stats(player_id, season=args.season)
                print(stats)
        elif args.team:
            fetch_team_stats(args.team, season=args.season)
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
        elif args.fantasy_score:
            player_id = lookup_player_id(args.fantasy_score)
            if player_id:
                get_player_fantasy_points(player_id, args.season)
            else:
                print(f"Player '{args.fantasy_score}' not found.")
        elif args.fantasy_add:
            user, player_name = args.fantasy_add
            player_id = lookup_player_id(player_name)
            if player_id:
                add_player_to_team(user, player_id, player_name)
                print(f"Added {player_name} (ID: {player_id}) to {user}'s fantasy team.")
            else:
                print(f"Player '{player_name}' not found.")
        elif args.fantasy_remove:
            user, player_name = args.fantasy_remove
            player_id = lookup_player_id(player_name)
            if player_id:
                remove_player_from_team(user, player_id)
                print(f"Removed {player_name} (ID: {player_id}) from {user}'s fantasy team.")
            else:
                print(f"Player '{player_name}' not found.")
        elif args.fantasy_list:
            user = args.fantasy_list
            team = list_fantasy_team(user)
            if team:
                print(f"{user}'s fantasy team:")
                for pid, pname in team:
                    print(f"{pname} (ID: {pid})")
            else:
                print(f"{user} has no players on their fantasy team.")
        elif args.fantasy_team_score:
            user = args.fantasy_team_score
            team = list_fantasy_team(user)
            if team:
                print_team_fantasy_scores(user)
            else:
                print(f"{user} has no players on their fantasy team.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()