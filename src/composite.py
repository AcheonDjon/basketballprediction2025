import pandas as pd

def compute_composite_score(df):
    """
    Compute a composite score based on key performance metrics.
    """
    df["shooting_efficiency"] = (df["FGM_2"] + df["FGM_3"] + df["FTM"]) / (
        df["FGA_2"] + df["FGA_3"] + df["FTA"] + 1  # Avoid division by zero
    )
    df["rebound_score"] = df["DREB"] + df["OREB"]
    df["assist_turnover_ratio"] = df["AST"] / (df["TOV"] + 1)
    df["defensive_impact"] = df["STL"] + df["BLK"] - df["F_personal"]
    
    # Normalize each component
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
    df = compute_composite_score(df)
    team_avg_scores = df.groupby(["team", "region"])["composite_score"].mean().reset_index()
    team_avg_scores["rank"] = team_avg_scores.groupby("region")["composite_score"].rank(ascending=False)
    return team_avg_scores.sort_values(["region", "rank"])

if __name__ == "__main__":
    file_path = "data/merged_team_games.csv"  # Update this with the actual path
    df = pd.read_csv(file_path, sep="\t")
    ranked_teams = rank_teams_by_region(df)
    ranked_teams.to_csv("ranked_teams_by_region.csv", index=False)
    print("Ranking completed! Saved to ranked_teams_by_region.csv")
