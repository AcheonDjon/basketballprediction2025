import pandas as pd

def compute_composite_score(df):
    """
    Compute a composite score based on key performance metrics.
    """
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
    
    # Normalize each component to contribute fairly to the composite score
    df["composite_score"] = (
        0.4 * df["shooting_efficiency"] +
        0.2 * df["rebound_score"] / df["rebound_score"].max() +
        0.2 * df["assist_turnover_ratio"] / df["assist_turnover_ratio"].max() +
        0.2 * df["defensive_impact"] / df["defensive_impact"].max()
    )
    return df

def rank_teams_by_region(df):
    """
    Rank teams by region based on composite scores.
    """
    # Compute composite scores for all players/teams in the dataset
    df = compute_composite_score(df)
    
    # Compute average composite score per team per region
    team_avg_scores = df.groupby(["team", "region"])["composite_score"].mean().reset_index()
    
    # Rank teams within each region based on their average composite score
    team_avg_scores["rank"] = team_avg_scores.groupby("region")["composite_score"].rank(ascending=False)
    
    # Return sorted ranking based on region and rank
    return team_avg_scores.sort_values(["region", "rank"])

if __name__ == "__main__":
    file_path = "data/merged_team_games.csv"  # Update this with the actual path
    
    # Load dataset from file
    df = pd.read_csv(file_path, sep="\t")
    
    # Compute rankings
    ranked_teams = rank_teams_by_region(df)
    
    # Save ranked results to a new CSV file
    ranked_teams.to_csv("output/ranked_teams_by_region.csv", index=False)
    
    # Notify user of completion
    print("Ranking completed! Saved to ranked_teams_by_region.csv")
