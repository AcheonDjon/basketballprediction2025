# Basketball Team Win Probability Calculator
## Combining SHARP Scores and Elo Ratings

This document explains how our basketball team win probability calculator works, with a step-by-step explanation and a real example using data from the provided datasets.

## How It Works

Our calculator uses two popular rating systems to predict the outcome of basketball games:

1. **SHARP Scores** - A basketball-specific rating system that evaluates team strength
2. **Elo Ratings** - A rating system originally developed for chess but adapted for many sports

By combining these two rating systems, we get a more robust prediction than using either system alone.

## The Algorithm

The probability calculation follows these steps:

1. **Extract ratings** for both teams from the datasets
2. **Calculate differences** in both SHARP scores and Elo ratings
3. **Combine these differences** using a weighting parameter
4. **Convert to a probability** using a logistic function

### The Formula

```
P(team1 wins) = 1 / (1 + 10^(-combined_diff/400))
```

Where:
- `combined_diff = (sharp_weight × SHARP_diff) + ((1 - sharp_weight) × Elo_diff)`
- `SHARP_diff = team1_sharp - team2_sharp`
- `Elo_diff = team1_elo - team2_elo`
- `sharp_weight` is a parameter between 0 and 1 that determines the influence of each rating system (default = 0.5)

## Real Example: South Carolina Gamecocks vs UCF Knights

Let's walk through a complete calculation using real data from our datasets.

### Step 1: Extract Ratings

From our tab-delimited data files:

**South Carolina Gamecocks:**
- SHARP score: 22.77 (from SHAPRanking.csv)
- Elo rating: 3010.23 (from regionGroupEloRanking.csv)

**UCF Knights:**
- SHARP score: 17.65 (from SHAPRanking.csv)
- Elo rating: 2687.22 (from regionGroupEloRanking.csv)

### Step 2: Calculate Differences

**SHARP difference:**
```
SHARP_diff = 22.77 - 17.65 = 5.12
```

**Elo difference:**
```
Elo_diff = 3010.23 - 2687.22 = 323.01
```

### Step 3: Combine the Differences

Using the default weight of 0.5 (equal influence for both systems):

```
combined_diff = (0.5 × 5.12) + (0.5 × 323.01)
combined_diff = 2.56 + 161.505
combined_diff = 164.065
```

### Step 4: Convert to Win Probability

```
P(South Carolina wins) = 1 / (1 + 10^(-164.065/400))
P(South Carolina wins) = 1 / (1 + 10^(-0.41016))
P(South Carolina wins) = 1 / (1 + 0.38883)
P(South Carolina wins) = 1 / 1.38883
P(South Carolina wins) = 0.7199
```

**Result:** South Carolina Gamecocks have a 71.99% chance of winning against UCF Knights.

### Visualizing the Result

```
South Carolina Gamecocks: 71.99%
UCF Knights: 28.01%
```

## Understanding the Weighting Parameter

The `sharp_weight` parameter lets you adjust how much each rating system influences the final prediction:

- `sharp_weight = 1.0`: Only SHARP scores are used
- `sharp_weight = 0.0`: Only Elo ratings are used
- `sharp_weight = 0.5`: Equal weighting (default)

### Example with Different Weights

Let's recalculate the same matchup with different weights:

**SHARP scores only (sharp_weight = 1.0):**
```
combined_diff = 1.0 × 5.12 + 0.0 × 323.01 = 5.12
P(South Carolina wins) = 1 / (1 + 10^(-5.12/400)) = 0.5088 (50.88%)
```

**Elo ratings only (sharp_weight = 0.0):**
```
combined_diff = 0.0 × 5.12 + 1.0 × 323.01 = 323.01
P(South Carolina wins) = 1 / (1 + 10^(-323.01/400)) = 0.8431 (84.31%)
```

This shows how the two rating systems can give different predictions, and combining them provides a balanced approach.

## Python Implementation

```python
def probability_from_ratings(team1_sharp, team2_sharp, team1_elo, team2_elo, sharp_weight=0.5):
    """
    Calculate the probability of team1 winning against team2 based on their SHARP scores and Elo ratings.
    
    Args:
        team1_sharp (float): SHARP score of the first team
        team2_sharp (float): SHARP score of the second team
        team1_elo (float): Elo rating of the first team
        team2_elo (float): Elo rating of the second team
        sharp_weight (float, optional): Weight given to SHARP scores vs Elo ratings.
                                     0 means only use Elo, 1 means only use SHARP.
                                     Defaults to 0.5 (equal weighting).
    
    Returns:
        float: Probability of team1 winning against team2 (between 0 and 1)
    """
    import math
    
    # Calculate the difference in SHARP scores
    sharp_diff = team1_sharp - team2_sharp
    
    # Calculate the difference in Elo ratings
    elo_diff = team1_elo - team2_elo
    
    # Combine the differences using the specified weight
    combined_diff = sharp_weight * sharp_diff + (1 - sharp_weight) * elo_diff
    
    # Convert combined difference to win probability using logistic function
    probability = 1.0 / (1.0 + math.pow(10, -combined_diff / 400))
    
    return probability
```

## Using the Complete Calculator

To use the full calculator with team names from our datasets:

```python
# Get win probabilities for a matchup
result = get_match_probabilities("south_carolina_gamecocks", "ucf_knights")
team1_prob, team2_prob = result

print(f"South Carolina Gamecocks win probability: {team1_prob:.2%}")
print(f"UCF Knights win probability: {team2_prob:.2%}")
```

**Output:**
```
South Carolina Gamecocks win probability: 71.99%
UCF Knights win probability: 28.01%
```