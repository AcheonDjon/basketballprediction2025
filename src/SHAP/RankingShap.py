import pandas as pd

# Load your DataFrames
df = pd.read_csv('./data/SHAP/RaptorMerged.csv', sep='\t')
df2 = pd.read_csv('./data/team_region_groups.csv', sep='\t')

# Get the unique team names from df2
unique_teams = df2['team'].unique()

# Initialize an empty list to store the results
results = []

# Loop through each team
for team_name in unique_teams:
    # Find all rows where the team name matches in df
    team_games = df[df['team'] == team_name]

    # Check if the team was found
    if not team_games.empty:
        # Calculate the mean RaptorScore
        average_raptor_score = team_games['Raptor_Score'].mean()
        region = df2.loc[df2['team'] == team_name, 'region'].iloc[0]
        results.append({'Team': team_name, 'Region': region, 'Avg RaptorScore': average_raptor_score})
    else:
        print(f"Team {team_name} not found in the RaptorMerged data.")

# Convert the results to a DataFrame
df_results = pd.DataFrame(results)

# Sort the df_results by region and then by average RaptorScore
df_results = df_results.sort_values(by=['Region', 'Avg RaptorScore'], ascending=[True, False])

# Add a ranking column
df_results['Rank'] = df_results.groupby('Region')['Avg RaptorScore'].rank(method='dense', ascending=False).astype(int)

df_results.to_csv('./output/SHAPRanking.csv', sep='\t', index=False)