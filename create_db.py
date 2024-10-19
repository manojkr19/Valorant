import sqlite3

# Connect to the SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('players.db')
cursor = conn.cursor()

# Create the Players table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT,
    player_link TEXT,
    player_team_initials TEXT,
    player_country_initials TEXT,
    rounds_played INTEGER,
    rating REAL,
    average_combat_score REAL,
    kills_deaths REAL,
    kill_assist_trade_survive_percentage REAL,
    average_damage_per_round REAL,
    kills_per_round REAL,
    assists_per_round REAL,
    first_kills_per_round REAL,
    first_deaths_per_round REAL,
    headshot_percentage REAL,
    clutch_success_percentage REAL,
    max_kills_in_single_map INTEGER,
    kills INTEGER,
    deaths INTEGER,
    role TEXT,
    rating_score REAL,
    agent_flexibility REAL,
    experience REAL,
    total_score REAL
)
''')

# Create the Agents table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Agents (
    agent_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    agent_name TEXT,
    games_played INTEGER,
    use_rate REAL,
    rounds INTEGER,
    rating REAL,
    average_combat_score REAL,
    kill_death_ratio REAL,
    average_damage_per_round REAL,
    kast REAL,
    kills_per_round REAL,
    assists_per_round REAL,
    first_kills_per_round REAL,
    first_deaths_per_round REAL,
    kills INTEGER,
    deaths INTEGER,
    assists INTEGER,
    first_kills INTEGER,
    first_deaths INTEGER,
    FOREIGN KEY (player_id) REFERENCES Players (player_id)
)
''')

# Commit changes and close the connection to the database
conn.commit()
conn.close()