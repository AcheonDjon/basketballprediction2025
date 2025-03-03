import pandas as pd

# Load the dataset (replace 'games.csv' with the path to your dataset)
df = pd.read_csv('data/merged_team_games.csv')

# List of columns representing stats
stat_columns = [
    'FGA_2', 'FGM_2', 'FGA_3', 'FGM_3', 'FTA', 'FTM', 'AST', 'BLK', 'STL', 
    'TOV', 'TOV_team', 'DREB', 'OREB', 'F_tech', 'F_personal', 'team_score', 
    'opponent_team_score', 'largest_lead', 'OT_length_min_tot', 'rest_days', 
    'attendance', 'tz_dif_H_E', 'prev_game_dist', 'travel_dist'
]

# Initialize a dictionary to store the total stats for each team
team_stats = {}

# Iterate through each game and update the stats for the team
for index, row in df.iterrows():
    team = row['team']
    
    # Initialize the team's stats if not already in the dictionary
    if team not in team_stats:
        team_stats[team] = {stat: 0 for stat in stat_columns}
        team_stats[team]['games_played'] = 0  # To track the number of games
    
    # Update stats for the team
    for stat in stat_columns:
        team_stats[team][stat] += row[stat]
    
    # Count the games for each team
    team_stats[team]['games_played'] += 1

# Now calculate the average for each stat for each team
team_averages = {}

for team, stats in team_stats.items():
    team_averages[team] = {}
    games_played = stats['games_played']
    
    # Calculate the averages for each stat
    for stat, total in stats.items():
        if stat != 'games_played':  # Skip the 'games_played' field
            team_averages[team][stat] = total / games_played

# Convert the averages into a DataFrame
averages_df = pd.DataFrame(team_averages).T

# Save the DataFrame to a CSV file
averages_df.to_csv('average_stats.csv', index=True)

print("Averages have been saved to 'team_averages.csv'")
