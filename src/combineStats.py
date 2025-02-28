import pandas as pd

def combine_stats(df):
    
    # Calculate shooting efficiency, incorporating field goals and free throws
    df["shooting_efficiency"] = (df["FGM_2"] + df["FGM_3"] + df["FTM"]) / (
        df["FGA_2"] + df["FGA_3"] + df["FTA"] + 1  # Avoid division by zero
    )
    
    # Aggregate total rebounds as a performance indicator
    df["rebound_score"] = df["DREB"] + df["OREB"]
    
    # Compute assist-to-turnover ratio, adding 1 to turnovers to prevent division by zero
    df["assist_turnover_ratio"] = df["AST"] / (df["TOV"] + 1)
    
    # Defensive impact metric combines steals, blocks, and penalizes personal fouls
    df["defensive_impact"] = df["STL"] + df["BLK"] - df["F_personal"]

    df.drop(columns=['FGM_2', 'FGM_3', 'FTM', 'FGA_2', 'FGA_3', 'FTA', 'DREB', 'OREB', 'AST', 'TOV', 'STL', 'BLK', 'F_personal'], inplace=True)

    return df


# Load dataset
df = pd.read_csv("data/merged_team_games.csv")  # Adjust file path if necessary

df = combine_stats(df)

df.to_csv("data/working_elo/merged_team_games_with_combined_stats.csv", index=False, sep='\t')