import pandas as pd

df = pd.read_csv("data/merged_team_games.csv", sep="\t")

df["Win"] = (df["team_score"] > df["opponent_team_score"]).astype(int)
df['Point_Differential'] = df["team_score"] - df["opponent_team_score"]
df['Possessions'] = df['team_score'] + 0.5 * df['FGA%'] - df['OREB'] + df['TOV'] + 0.4 * df['FTA']
df['AST%'] = df['AST'] / (df['AST'] + df['TOV'])
df['BLK%'] = df['BLK'] / df['FGA%']
df['TOV%'] = df['TOV'] / df['Possessions']
df['TOV_team%'] = df['TOV_team'] / df['Possessions']
df['STL%'] = df['STL'] / df['Possessions']
df['games_played'] = df['games_played'] = df['team'].map(df['team'].value_counts())

df.to_csv("data/merged_team_games.csv", sep="\t", index=False)