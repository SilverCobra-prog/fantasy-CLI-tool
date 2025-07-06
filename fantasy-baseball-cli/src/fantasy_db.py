import sqlite3

FANTASY_DB_PATH = "fantasy_team.db"

def init_fantasy_db(db_path=FANTASY_DB_PATH):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS fantasy_team (
            user TEXT,
            player_id INTEGER,
            player_name TEXT,
            PRIMARY KEY (user, player_id)
        )
    """)
    conn.commit()
    conn.close()

def add_player_to_team(user, player_id, player_name, db_path=FANTASY_DB_PATH):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        INSERT OR IGNORE INTO fantasy_team (user, player_id, player_name)
        VALUES (?, ?, ?)
    """, (user, player_id, player_name))
    conn.commit()
    conn.close()

def remove_player_from_team(user, player_id, db_path=FANTASY_DB_PATH):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        DELETE FROM fantasy_team WHERE user=? AND player_id=?
    """, (user, player_id))
    conn.commit()
    conn.close()

def list_fantasy_team(user, db_path=FANTASY_DB_PATH):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        SELECT player_id, player_name FROM fantasy_team WHERE user=?
    """, (user,))
    players = c.fetchall()
    conn.close()
    return players

# Example usage:
if __name__ == "__main__":
    init_fantasy_db()
    user = "sumukh"
    # Add a player
    add_player_to_team(user, 545361, "Mike Trout")
    add_player_to_team(user, 111188, "Barry Bonds")
    # List team
    print(f"{user}'s fantasy team:")
    for pid, pname in list_fantasy_team(user):
        print(f"{pname} (ID: {pid})")
    # Remove a player
    remove_player_from_team(user, 545361)
    print(f"\nAfter removal, {user}'s fantasy team:")
    for pid, pname in list_fantasy_team(user):
        print(f"{pname} (ID: {pid})")