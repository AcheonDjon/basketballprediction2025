# Composite Score Ranking Summary

## Overview

This script processes basketball team performance data to compute a composite score based on key metrics. The scores are then used to rank teams by region.

## Methodology

### Compute Composite Score:

- **Shooting Efficiency**: Calculates efficiency based on field goals and free throws made.
- **Rebound Score**: Sum of defensive and offensive rebounds.
- **Assist-to-Turnover Ratio**: Ensures turnovers are factored in with a safeguard against division by zero.
- **Defensive Impact**: A combination of steals, blocks, and penalties for personal fouls.
- **Normalization**: Each component is normalized before final computation.

### Rank Teams by Region:

- Compute the average composite score for each team in their respective regions.
- Rank teams within each region based on their scores.
- Sort results by region and rank.

## Execution

- Reads input data from `data/merged_team_games.csv`.
- Processes and ranks teams.
- Saves the ranked output to `ranked_teams_by_region.csv`.
- Outputs a completion message.

## Usage

Run the script in a Python environment with pandas installed. Ensure the input file exists at the specified path before execution.

## Dependencies

- `pandas` library for data manipulation.
- A properly formatted CSV file containing team performance data.

## Output

The final rankings are stored in `ranked_teams_by_region.csv`, providing a structured view of team performance by region.