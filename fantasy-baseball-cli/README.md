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

- `--player <player_name>`: Retrieve statistics for a specific player.
- `--compare <player_name> <player_name>`: Compare two specific players.
- `--team <team_name>`: Retrieve statistics for all players on a specific team.
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