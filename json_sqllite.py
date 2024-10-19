import json
import sqlite3
import os

# Function to safely convert string to float, using default value if empty or invalid
def safe_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

# Define the path to the JSON file
json_file_path = os.path.join(os.getcwd(), 'Valorant', 'players_scored.json')

# Read the JSON file
with open(json_file_path, 'r') as file:
    players_data = json.load(file)

# Connect to the SQLite database
conn = sqlite3.connect('players.db')
cursor = conn.cursor()

# Function to insert a player and their agents into the database
def insert_player(player):
    # Insert player data into Players table
    cursor.execute('''
        INSERT INTO Players (
            player_name, player_link, player_team_initials, player_country_initials,
            rounds_played, rating, average_combat_score, kills_deaths,
            kill_assist_trade_survive_percentage, average_damage_per_round,
            kills_per_round, assists_per_round, first_kills_per_round,
            first_deaths_per_round, headshot_percentage, clutch_success_percentage,
            max_kills_in_single_map, kills, deaths, role,
            rating_score, agent_flexibility, experience, total_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        player['player_name'], player['player_link'], player['player_team_initials'], player['player_country_initials'],
        int(player['rounds_played']), safe_float(player['rating']), safe_float(player['average_combat_score']), safe_float(player['kills_deaths']),
        safe_float(player['kill_assist_trade_survive_percentage'].strip('%')) / 100, safe_float(player['average_damage_per_round']),
        safe_float(player['kills_per_round']), safe_float(player['assists_per_round']), safe_float(player['first_kills_per_round']),
        safe_float(player['first_deaths_per_round']), safe_float(player['headshot_percentage'].strip('%')) / 100,
        safe_float(player['clutch_success_percentage'].strip('%')) / 100, int(player['max_kills_in_single_map']),
        int(player['kills']), int(player['deaths']), player['role'],
        safe_float(player.get('rating_score', 0.0)),
        safe_float(player.get('agent_flexibility', 0.0)),
        safe_float(player.get('experience', 0.0)),
        safe_float(player.get('total_score', 0.0))
    ))

    # Get the last inserted player_id
    player_id = cursor.lastrowid

    # Check if 'agents' key exists before processing
    if 'agents' in player:
        # Insert agent data into Agents table
        for agent in player['agents']:
            for agent_name, stats in agent.items():
                cursor.execute('''
                    INSERT INTO Agents (
                        player_id, agent_name, games_played, use_rate, rounds, rating,
                        average_combat_score, kill_death_ratio, average_damage_per_round,
                        kast, kills_per_round, assists_per_round, first_kills_per_round,
                        first_deaths_per_round, kills, deaths, assists, first_kills, first_deaths
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    player_id, agent_name, stats['games_played'], safe_float(stats['use_rate'].strip('%')) / 100, int(stats['rnd']),
                    safe_float(stats['rating']), safe_float(stats['acs']), safe_float(stats['kd']), safe_float(stats['adr']),
                    safe_float(stats['kast'].strip('%')) / 100, safe_float(stats['kpr']), safe_float(stats['apr']),
                    safe_float(stats['fkpr']), safe_float(stats['fdpr']), int(stats['k']), int(stats['d']),
                    int(stats['a']), int(stats['fk']), int(stats['fd'])
                ))

# Iterate through each player in the JSON and insert into the database
for player in players_data['players']:
    insert_player(player)

# Commit changes and close the connection
conn.commit()
conn.close()