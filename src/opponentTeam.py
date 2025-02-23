import pandas as pd

# Load the data from the CSV file
df = pd.read_csv('./data/merged_team_games.csv', sep='\t')

# Sort the dataframe by 'game_id'
df = df.sort_values(by='game_id')

# Create a new column 'opponent_team' by shifting the 'team' column
df['opponent_team'] = df.groupby('game_id')['team'].shift(1)

# Fill the NaN values in the 'opponent_team' column
df['opponent_team'] = df['opponent_team'].fillna(df.groupby('game_id')['team'].shift(-1))

# Save the updated dataframe to a new CSV file
df.to_csv('./data/merged_team_games.csv', index=False)