import pandas as pd
import math

def get_match_probabilities(team1_name, team2_name, SHAP_weight=0.5):
    """
    Calculate the win probabilities for two teams based on their SHAP scores and Elo ratings.
    
    Args:
        team1_name (str): Name of the first team
        team2_name (str): Name of the second team
        SHAP_weight (float, optional): Weight given to SHAP scores vs Elo ratings.
                                     0 means only use Elo, 1 means only use SHAP.
                                     Defaults to 0.5 (equal weighting).
    
    Returns:
        tuple: (team1_win_probability, team2_win_probability)
    """
    # Load the tab-delimited files
    try:
        SHAP_df = pd.read_csv("output/SHAPRanking.csv", delimiter='\t', header=0)
        elo_df = pd.read_csv("output/regionGroupEloRanking.csv", delimiter='\t', header=0)
    except Exception as e:
        print(f"Error loading CSV files: {e}")
        return None
    
    # Get team name columns - using exact names from the files
    SHAP_team_col = 'Team'  # First column in SHAPRanking.csv
    elo_team_col = 'team'    # First column in regionGroupEloRanking.csv
    
    # Standardize team names for lookup (convert to lowercase)
    SHAP_df[SHAP_team_col] = SHAP_df[SHAP_team_col].str.strip().str.lower()
    elo_df[elo_team_col] = elo_df[elo_team_col].str.strip().str.lower()
    
    team1_name_lower = team1_name.strip().lower()
    team2_name_lower = team2_name.strip().lower()
    
    # Find the teams in both datasets
    team1_SHAP_data = SHAP_df[SHAP_df[SHAP_team_col] == team1_name_lower]
    team2_SHAP_data = SHAP_df[SHAP_df[SHAP_team_col] == team2_name_lower]
    team1_elo_data = elo_df[elo_df[elo_team_col] == team1_name_lower]
    team2_elo_data = elo_df[elo_df[elo_team_col] == team2_name_lower]
    
    # Check if teams are found in both datasets
    if team1_SHAP_data.empty or team2_SHAP_data.empty or team1_elo_data.empty or team2_elo_data.empty:
        if team1_SHAP_data.empty or team1_elo_data.empty:
            print(f"Team '{team1_name}' not found in one or both datasets.")
        if team2_SHAP_data.empty or team2_elo_data.empty:
            print(f"Team '{team2_name}' not found in one or both datasets.")
        return None
    
    # Get the SHAP scores and Elo ratings using exact column names from files
    SHAP_score_col = 'Avg RaptorScore'  # From SHAPRanking.csv
    elo_rating_col = 'elo'               # From regionGroupEloRanking.csv
    
    team1_SHAP = float(team1_SHAP_data[SHAP_score_col].values[0])
    team2_SHAP = float(team2_SHAP_data[SHAP_score_col].values[0])
    team1_elo = float(team1_elo_data[elo_rating_col].values[0])
    team2_elo = float(team2_elo_data[elo_rating_col].values[0])
    
    # Calculate the probability using the combined ratings
    team1_win_prob = probability_from_ratings(team1_SHAP, team2_SHAP, team1_elo, team2_elo, SHAP_weight)
    team2_win_prob = 1.0 - team1_win_prob
    
    return team1_win_prob, team2_win_prob

def probability_from_ratings(team1_SHAP, team2_SHAP, team1_elo, team2_elo, SHAP_weight=0.5):
    """
    Calculate the probability of team1 winning against team2 based on their SHAP scores and Elo ratings.
    
    Args:
        team1_SHAP (float): SHAP score of the first team
        team2_SHAP (float): SHAP score of the second team
        team1_elo (float): Elo rating of the first team
        team2_elo (float): Elo rating of the second team
        SHAP_weight (float, optional): Weight given to SHAP scores vs Elo ratings.
                                     0 means only use Elo, 1 means only use SHAP.
                                     Defaults to 0.5 (equal weighting).
    
    Returns:
        float: Probability of team1 winning against team2 (between 0 and 1)
    """
    # Calculate the difference in SHAP scores
    SHAP_diff = team1_SHAP - team2_SHAP
    
    # Calculate the difference in Elo ratings
    elo_diff = team1_elo - team2_elo
    
    # Combine the differences using the specified weight
    combined_diff = SHAP_weight * SHAP_diff + (1 - SHAP_weight) * elo_diff
    
    # Convert combined difference to win probability using logistic function
    probability = 1.0 / (1.0 + math.pow(10, -combined_diff / 400))
    
    return probability

# Example usage
if __name__ == "__main__":
    # Example team names from the datasets
    team1 = "south_carolina_gamecocks"
    team2 = "ucf_knights"
    
    result = get_match_probabilities(team1, team2)
    
    if result:
        team1_prob, team2_prob = result
        print(f"Matchup: {team1} vs {team2}")
        print(f"{team1} win probability: {team1_prob:.2%}")
        print(f"{team2} win probability: {team2_prob:.2%}")