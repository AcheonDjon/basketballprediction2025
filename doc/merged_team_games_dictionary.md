# Merged Team Games Data Dictionary

## Game Identification and Basic Information
| Column Name | Description | Data Type | Example | Notes |
|------------|-------------|------------|---------|--------|
| game_id | Unique identifier for each game | string | game_2022_2011 | Format: game_YEAR_NUMBER |
| game_date | Date when the game was played | date | 2021-12-30 | YYYY-MM-DD format |
| team | Team identifier | string | georgia_lady_bulldogs | Underscore-separated team name |
| region | Geographic region of the team | string | North | Regional classification |

## Shooting Statistics
| Column Name | Description | Data Type | Example | Formula/Notes |
|------------|-------------|------------|---------|---------------|
| FGA_2 | Two-Point Field Goal Attempts | integer | 61 | Shots inside 3-point line |
| FGM_2 | Two-Point Field Goals Made | integer | 27 | Successful 2-point shots |
| FGA_3 | Three-Point Field Goal Attempts | integer | 11 | Shots beyond 3-point arc |
| FGM_3 | Three-Point Field Goals Made | integer | 5 | Successful 3-point shots |
| FTA | Free Throw Attempts | integer | 6 | Free throw attempts |
| FTM | Free Throws Made | integer | 3 | Successful free throws |

## Game Play Statistics
| Column Name | Description | Data Type | Example | Formula/Notes |
|------------|-------------|------------|---------|---------------|
| AST | Assists | integer | 14 | Direct passes leading to baskets |
| BLK | Blocks | integer | 7 | Shots blocked by defenders |
| STL | Steals | integer | 7 | Possessions gained from opponent |
| TOV | Individual Turnovers | integer | 18 | Individual possession losses |
| TOV_team | Team Turnovers | integer | 0 | Team-attributed turnovers |
| DREB | Defensive Rebounds | integer | 25 | Rebounds from opponent misses |
| OREB | Offensive Rebounds | integer | 11 | Rebounds from own team misses |

## Fouls and Scoring
| Column Name | Description | Data Type | Example | Formula/Notes |
|------------|-------------|------------|---------|---------------|
| F_tech | Technical Fouls | integer | 0 | Number of technical fouls |
| F_personal | Personal Fouls | integer | 18 | Number of personal fouls |
| team_score | Final Team Score | integer | 62 | Total team points |
| opponent_team_score | Final Opponent Score | integer | 68 | Total opponent points |
| largest_lead | Largest Lead | float | 1.0 | Maximum point difference |

## Game Conditions and Logistics
| Column Name | Description | Data Type | Example | Formula/Notes |
|------------|-------------|------------|---------|---------------|
| notD1_incomplete | Non-Division 1/Incomplete Flag | boolean | False | Game status indicator |
| OT_length_min_tot | Overtime Length | float | null | Total overtime minutes |
| rest_days | Days of Rest | float | 9.0 | Days since last game |
| attendance | Game Attendance | float | 3241.0 | Number of spectators |
| tz_dif_H_E | Time Zone Difference | float | 0.0 | Time zone differential |
| prev_game_dist | Previous Game Distance | float | 0.0 | Distance from last game |
| home_away | Home/Away Indicator | string | home | Location descriptor |
| home_away_NS | Home/Away Numeric | integer | 1 | Home=1, Away=-1, Neutral=0 |
| travel_dist | Travel Distance | float | 0.0 | Distance to game venue |

## Key Metrics and Calculations

### Efficiency Metrics
1. Shooting Percentages:
   ```python
   Two_Point_Percentage = FGM_2 / FGA_2
   Three_Point_Percentage = FGM_3 / FGA_3
   Free_Throw_Percentage = FTM / FTA
   ```

2. Advanced Statistics:
   ```python
   Effective_Field_Goal_Percentage = (FGM_2 + 1.5 * FGM_3) / (FGA_2 + FGA_3)
   True_Shooting_Percentage = team_score / (2 * (FGA_2 + FGA_3 + 0.44 * FTA))
   Offensive_Rebound_Rate = OREB / (OREB + opponent_DREB)
   ```

3. Game Impact Metrics:
   ```python
   Point_Differential = team_score - opponent_team_score
   Estimated_Possessions = FGA_2 + FGA_3 - OREB + TOV + (0.44 * FTA)
   ```

## Data Quality Notes
1. Numeric Precision:
   - Integer values for most game statistics
   - Float values for calculated metrics and distances
   - Boolean for status flags

2. Missing Values:
   - Represented as empty strings or null values
   - Common in OT_length_min_tot for regular-time games
   - May appear in attendance data

3. Regional Classifications:
   - Teams are categorized by geographic region
   - Used for regional analysis and comparisons

## Usage Considerations
1. Time-based Analysis:
   - Use game_date for temporal trends
   - Consider rest_days for fatigue analysis
   - Account for time zone differences (tz_dif_H_E)

2. Location Analysis:
   - Use home_away_NS for numeric calculations
   - Consider travel_dist for away game impact
   - Factor in regional differences

3. Performance Metrics:
   - Combine shooting stats for efficiency analysis
   - Consider context (home/away, rest days)
   - Account for opponent strength

4. Data Integrity:
   - Check notD1_incomplete flag for data completeness
   - Verify attendance data availability
   - Consider regional variations in scheduling