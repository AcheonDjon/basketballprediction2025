import pandas as pd

df = pd.read_csv('./data/merged_team_games.csv', sep='\t')

df['ORtg'] = (df['team_score'] / df['Possessions']) * 100
df['DRtg'] = (df['opponent_team_score'] / df['Possessions']) * 100
df['NRtg'] = df['ORtg'] - df['DRtg']

df['WinPct'] = df['numwins'] / df['games_played']
df['WinPct'] = (df['WinPct'] - 0.5) * 20


df = df[['team', 'opponent_team', 'FGA%', 'PEM', 'REBF', 'NRtg', 'WinPct', 'Point_Differential']].copy()
df.to_csv('./data/SHAP/RaptorMerged.csv', sep='\t', index=False)
