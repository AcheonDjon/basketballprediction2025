import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the dataset
df = pd.read_csv("data/merged_team_games.csv", sep="\t")

#Weights determined from /src/FGA%Weights.py and /src/PEMWeights.py
Weights = {
    'FGM_2': 14.675530004335037, 
    'FGA_2': -4.469675995921854, 
    'FGM_3': 1.5251372075060012, 
    'FGA_3': 0.5059892999597321, 
    'FTM': 3.638516298137418, 
    'FTA': 0.8520139945087526, 
    'TOV': -4.170418710132634, 
    'TOV_team': 0.429464666889546,
    'AST%': 6.200483124713528,
    'BLK%': -1.7694952254330552,
    'TOV%': -7.517894302735887,
    'TOV_team%': -0.09121828073442506
    }

#Replacing original columns with a new FGA% Column
df["FGA%"] = (Weights['FGM_2']*df["FGM_2"] + 
              Weights['FGM_3'] * df["FGM_3"] + 
              Weights['FTM']*df["FTM"]) / (Weights['FGA_2']*df["FGA_2"] + 
                                           Weights['FGA_3']*df["FGA_3"]+
                                           Weights['FTA']*df["FTA"]+
                                           Weights['TOV']*df["TOV"]+
                                           Weights['TOV_team']*df["TOV_team"])

# Calculate possessions using a common formula in basketball statistics
df['Possessions'] = df['team_score'] + 0.5 * df['FGA%'] - df['OREB'] + df['TOV'] + 0.4 * df['FTA']

# Calculate Ratings
df['ORtg'] = (df['team_score'] / df['Possessions']) * 100
df['DRtg'] = (df['opponent_team_score'] / df['Possessions']) * 100
df['NRtg'] = df['ORtg'] - df['DRtg']

# Calculate effiency component percentages
df['AST%'] = df['AST'] / (df['AST'] + df['TOV'])
df['BLK%'] = df['BLK'] / df['FGA%']  # Assuming FGA% reflects opponent's field goal attempts
df['TOV%'] = df['TOV'] / df['Possessions']
df['TOV_team%'] = df['TOV_team'] / df['Possessions']

# Normalize the percentages (min-max scaling)
df['AST%_Norm'] = (df['AST%'] - df['AST%'].min()) / (df['AST%'].max() - df['AST%'].min())
df['BLK%_Norm'] = (df['BLK%'] - df['BLK%'].min()) / (df['BLK%'].max() - df['BLK%'].min())
df['TOV%_Norm'] = (df['TOV%'] - df['TOV%'].min()) / (df['TOV%'].max() - df['TOV%'].min())
df['TOV_team%_Norm'] = (df['TOV_team%'] - df['TOV_team%'].min()) / (df['TOV_team%'].max() - df['TOV_team%'].min())

df['PEM'] = (Weights['AST%'] * df['AST%_Norm'] +
             Weights['BLK%'] * df['BLK%_Norm'] +
             Weights['TOV%'] * df['TOV%_Norm'] +
             Weights['TOV_team%'] * df['TOV_team%_Norm'])


#Removes the Accounted Columns
df.drop(columns=['AST%', 'BLK%', 'TOV%', 'TOV_team%', 'AST%_Norm', 'BLK%_Norm', 'TOV%_Norm', 'TOV_team%_Norm', 'Possessions'], inplace=True)
df.drop(columns=['FGM_2', 'FGA_2', 'FGM_3', 'FGA_3', 'FTM', 'FTA', 'TOV', 'TOV_team', 'ORtg', 'DRtg'], inplace=True)
df.to_csv("data/RaptorMerged.csv", sep="\t", index=False)