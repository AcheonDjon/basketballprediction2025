import pandas as pd

df = pd.read_csv("data/merged_team_games.csv", sep=",")

df["Win"] = (df["team_score"] > df["opponent_team_score"]).astype(int)
df['Point_Differential'] = df["team_score"] - df["opponent_team_score"]
df.to_csv("data/merged_team_games.csv", sep="\t", index=False)