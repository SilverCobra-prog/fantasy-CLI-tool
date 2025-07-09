# Fantasy Baseball CLI

A command-line interface tool for retrieving player statistics using the MLB StatsAPI.

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

To use the Fantasy Baseball CLI, run the following command in your terminal:

```
python src/main.py [flags]
```

## Commands

- `--player <player_name> [--season <year> | --career]`: Retrieve statistics for a specific player for a specific season (use `--season <year>`) or for their career (use `--career`). If neither is specified, current season stats are returned by default.
- `--compare <player_name> <player_name> [--season <year> | --career]`: Compare two specific players for a given season or for their career. If neither is specified, current season stats are compared by default.
- `--team <team_name>`: Retrieve statistics for all players on a specific team.
- `--fantasy-score <player_name> --season <year>`: Show fantasy statistics for a specific player for a specific season.
- `--fantasy-add <player_name>`: Add a player to your fantasy team.
- `--fantasy-remove <player_name>`: Remove a player from your fantasy team.
- `--fantasy-list`: List all players currently on your fantasy team.
- `--fantasy-team-stats`: Show combined statistics for your fantasy team.
- `--help`: Show help information about the available commands.

## Examples

1. Retrieve statistics for a specific player:

```
python src/main.py --player "Mike Trout"
```

2. Retrieve statistics for a specific team:

```
python src/main.py --team "Los Angeles Angels"
```

## Contributing

Feel free to submit issues or pull requests for improvements and bug fixes.

## License

This project is licensed under the MIT License.