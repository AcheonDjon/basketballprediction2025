# Basketball Game Statistics Data Dictionary

## Game Identification and Basic Information
| Column Name | Description | Example | Notes |
|------------|-------------|---------|--------|
| game_id | Unique identifier for each game | game_2022_2011 | Format: game_YEAR_NUMBER |
| game_date | Date when the game was played | 2021-12-30 | YYYY-MM-DD format |
| team | Team identifier | georgia_lady_bulldogs | Underscore-separated team name |

## Shooting StatisticsÂ
| Column Name | Description | Example | Details |
|------------|-------------|---------|---------|
| FGA_2 | Two-Point Field Goal Attempts | 61 | Shots attempted inside the 3-point line |
| FGM_2 | Two-Point Field Goals Made | 27 | Successful shots made inside the 3-point line |
| FGA_3 | Three-Point Field Goal Attempts | 11 | Shots attempted beyond the 3-point arc |
| FGM_3 | Three-Point Field Goals Made | 5 | Successful shots made beyond the 3-point arc |
| FTA | Free Throw Attempts | 6 | Number of free throw attempts |
| FTM | Free Throws Made | 3 | Number of successful free throws |

## Game Play Statistics
| Column Name | Description | Example | Details |
|------------|-------------|---------|---------|
| AST | Assists | 14 | Passes that directly lead to made baskets |
| BLK | Blocks | 7 | Shots blocked/deflected by defenders |
| STL | Steals | 7 | Possessions gained by taking ball from opponent |
| TOV | Individual Turnovers | 18 | Times losing possession through individual errors |
| TOV_team | Team Turnovers | 0 | Turnovers attributed to the entire team |
| DREB | Defensive Rebounds | 25 | Rebounds secured after opponent's missed shots |
| OREB | Offensive Rebounds | 11 | Rebounds secured after own team's missed shots |

## Fouls and Scoring
| Column Name | Description | Example | Details |
|------------|-------------|---------|---------|
| F_tech | Technical Fouls | 0 | Number of technical fouls called |
| F_personal | Personal Fouls | 18 | Number of personal fouls committed |
| team_score | Final Team Score | 62 | Total points scored by the team |
| opponent_team_score | Final Opponent Score | 68 | Total points scored by the opposing team |
| largest_lead | Largest Lead | 1 | Biggest point difference during the game |

## Game Conditions and Logistics
| Column Name | Description | Example | Details |
|------------|-------------|---------|---------|
| notD1_incomplete | Non-Division 1/Incomplete Flag | FALSE | Indicates if game was non-D1 or incomplete |
| OT_length_min_tot | Overtime Length | NA | Total minutes of overtime played |
| rest_days | Days of Rest | 9 | Days since team's previous game |
| attendance | Game Attendance | 3241 | Number of spectators at the game |
| tz_dif_H_E | Time Zone Difference | 0 | Time zone difference from home stadium |
| prev_game_dist | Previous Game Distance | 0 | Distance from previous game location |
| home_away | Home/Away Indicator | home | Whether team played at home or away |
| home_away_NS | Home/Away Numeric | 1 | Home=1, Away=-1, Neutral=0 |
| travel_dist | Travel Distance | 0 | Distance traveled to game venue |

## Derived Statistics
These columns can be used to calculate important basketball metrics:

1. Shooting Percentages:
   - 2PT%: `FGM_2 / FGA_2`
   - 3PT%: `FGM_3 / FGA_3`
   - FT%: `FTM / FTA`

2. Advanced Metrics:
   - Effective Field Goal% (eFG%): `(FGM_2 + 1.5 * FGM_3) / (FGA_2 + FGA_3)`
   - True Shooting% (TS%): `Points / (2 * (FGA_2 + FGA_3 + 0.44 * FTA))`
   - Offensive Rebound%: `OREB / (OREB + opponent_DREB)`

3. Game Impact Metrics:
   - Point Differential: `team_score - opponent_team_score`
   - Possession Estimate: `FGA_2 + FGA_3 - OREB + TOV + (0.44 * FTA)`

## Usage Notes
1. All numeric values are integers unless specified otherwise
2. Distance measurements are typically in miles/kilometers
3. Time-related fields use standard date/time formats
4. Missing values are represented as NA
5. Boolean flags use TRUE/FALSE values