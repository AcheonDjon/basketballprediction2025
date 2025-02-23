import pandas as pd
from collections import defaultdict

# Elo calculation function
def calc_expected_score(rating_team, rating_opponent):
    return 1 / (1 + 10 ** ((rating_opponent - rating_team) / 400))

def calc_elo_change(rating, expected_score, actual_score, k=32):
    return k * (actual_score - expected_score)

# Load dataset
df = pd.read_csv("data/merged_team_games.csv")  # Adjust file path if necessary

df = df.sort_values(by='game_id')

# Initialize Elo ratings
initial_elo = 1500
elo_dict = defaultdict(lambda: initial_elo)

# Store Elo history
elo_history = []

# Parameters
max_passes = 100    # Maximum number of iterations for convergence (increased)
threshold = 0.1     # Convergence threshold for Elo changes
k = 32              # K-factor

for pass_num in range(max_passes):
    max_change = 0  # Track the largest Elo change in this pass

    # Iterate over each game
    for index, row in df.iterrows():
        team = row['team']
        opponent = row['opponent_team']
        win = row['Win']  # 1 if the team won, 0 if they lost

        # Get current Elo ratings
        rating_team = elo_dict[team]
        rating_opponent = elo_dict[opponent]

        # Calculate Elo change
        expected_team = calc_expected_score(rating_team, rating_opponent)
        expected_opponent = calc_expected_score(rating_opponent, rating_team)
        # Actual scores
        actual_team = win
        actual_opponent = 1 - win  # Assuming win is 1 if team wins, 0 if loses

        # Calculate Elo changes separately
        elo_change_team = k * (actual_team - expected_team)
        elo_change_opponent = k * (actual_opponent - expected_opponent)

        # Update Elo ratings
        elo_dict[team] += elo_change_team
        elo_dict[opponent] += elo_change_opponent


        # Record the maximum Elo change
      
        max_change = max(max_change, abs(elo_change_team), abs(elo_change_opponent))


        # Store Elo history
        elo_history.append({
            'pass_num': pass_num + 1,
            'game_id': row['game_id'],
            'team': team,
            'opponent_team': opponent,
            'win': win,
            'elo_before': rating_team,
            'elo_after': elo_dict[team],
            'opponent_elo_before': rating_opponent,
            'opponent_elo_after': elo_dict[opponent],
            'elo_change_team': elo_change_team,
            'elo_change_opponent': elo_change_opponent 
        })

# Create a DataFrame from the Elo history
elo_history_df = pd.DataFrame(elo_history)

# Elo History CSV If Wanted
#elo_history_df.to_csv("data/working_elo/elo_history.csv", index=False)

# Add final Elo ratings to the original DataFrame
final_elos = pd.DataFrame(list(elo_dict.items()), columns=['team', 'final_elo'])
df = df.merge(final_elos, on='team', how='left')

# Save the updated dataset with final Elo ratings
df.to_csv("data/working_elo/merged_team_games_with_elo.csv", index=False, sep='\t')

