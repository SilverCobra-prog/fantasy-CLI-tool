"""Database functions for managing fantasy teams in the Fantasy Baseball CLI."""

import sqlite3
from src.commands import get_player_fantasy_points

FANTASY_DB_PATH = "fantasy_team.db"


def init_fantasy_db(db_path=FANTASY_DB_PATH):
    """
    Initialize the fantasy team database.
    Creates the fantasy_team table if it does not exist.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS fantasy_team (
            user TEXT,
            player_id INTEGER,
            player_name TEXT,
            PRIMARY KEY (user, player_id)
        )
    """
    )
    conn.commit()
    conn.close()


def add_player_to_team(user, player_id, player_name, db_path=FANTASY_DB_PATH):
    """
    Add a player to a user's fantasy team.
    If the player is already on the team, do nothing.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        """
        INSERT OR IGNORE INTO fantasy_team (user, player_id, player_name)
        VALUES (?, ?, ?)
    """,
        (user, player_id, player_name),
    )
    conn.commit()
    conn.close()


def remove_player_from_team(user, player_id, db_path=FANTASY_DB_PATH):
    """
    Remove a player from a user's fantasy team.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        """
        DELETE FROM fantasy_team WHERE user=? AND player_id=?
    """,
        (user, player_id),
    )
    conn.commit()
    conn.close()


def list_fantasy_team(user, db_path=FANTASY_DB_PATH):
    """
    List all players on a user's fantasy team.
    Returns a list of (player_id, player_name) tuples.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        """
        SELECT player_id, player_name FROM fantasy_team WHERE user=?
    """,
        (user,),
    )
    players = c.fetchall()
    conn.close()
    return players


def print_team_fantasy_scores(user, db_path=FANTASY_DB_PATH):
    """
    Print the fantasy scores for all players on a user's fantasy team and the total score.
    """
    team = list_fantasy_team(user, db_path=db_path)
    if not team:
        print(f"No players found for user '{user}'.")
        return

    total_score = 0
    print(f"Fantasy Team: {user}:\n{'-'*40}")
    for player_id, player_name in team:
        try:
            score = get_player_fantasy_points(player_id)
        except sqlite3.Error as e:
            print(
                f"Database error fetching score for {player_name} (ID {player_id}): {e}"
            )
            continue
        total_score += score
    print("-" * 40)
    print(f"Season Fantasy Score: {total_score}")
