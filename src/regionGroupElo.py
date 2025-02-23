import pandas as pd

df1 = pd.read_csv("data/merged_team_games_with_elo.csv", sep="\t")
df2 = pd.read_csv("data/team_region_groups.csv", sep= "\t")

for team2 in df2['team']:
    for index, team1 in enumerate(df1['team']):
        if team1 == team2:
            df2.loc[df2['team'] == team2, 'elo'] = df1.loc[index, 'final_elo']

df2 = df2.sort_values(by=['region', 'elo'], ascending=[True, False])
df2['rank'] = df2.groupby('region')['elo'].rank(method='min', ascending=False).astype(int)

df2.to_csv("output/regionGroupEloRanking.csv", sep="\t", index=False)

