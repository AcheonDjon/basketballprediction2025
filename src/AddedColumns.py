import pandas as pd

df = pd.read_csv("data/merged_team_games.csv", sep="\t")

df["Win"] = (df["team_score"] > df["opponent_team_score"]).astype(int)
df['Point_Differential'] = df["team_score"] - df["opponent_team_score"]
df['Possessions'] = 0.5 * (df['FGA_2'] + df['FGA_3'] + df['opponent_FGA2'] + df['opponent_FGA3']) + 0.4 * (df['FTA'] + df['opponent_FTA']) - df['OREB'] - df['opponent_OREB'] + df['TOV'] + df['opponent_TOV']
df['AST%'] = df['AST'] / (df['AST'] + df['TOV'])
df['BLK%'] = df['BLK'] / (df['opponent_FGA2'] + df['opponent_FGA3'])
df['TOV%'] = df['TOV'] / df['Possessions']
df['TOV_team%'] = df['TOV_team'] / df['Possessions']
df['STL%'] = df['STL'] / df['Possessions']
df['games_played'] = df['games_played'] = df['team'].map(df['team'].value_counts())
df['numwins'] = df['Win'].eq(1).groupby(df['team']).transform('sum')

df.to_csv("data/merged_team_games.csv", sep="\t", index=False)