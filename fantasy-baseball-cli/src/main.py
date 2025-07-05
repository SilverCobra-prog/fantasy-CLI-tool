import argparse
import sys
from cli import fetch_player_stats

def main():
    parser = argparse.ArgumentParser(description="Retrieve MLB player statistics.")
    parser.add_argument('player_name', type=str, help='Name of the player to retrieve statistics for')
    args = parser.parse_args()

    if not args.player_name:
        print("Player name is required.")
        sys.exit(1)

    stats = fetch_player_stats(args.player_name)
    if stats:
        print(stats)
    else:
        print(f"No statistics found for player: {args.player_name}")

if __name__ == "__main__":
    main()