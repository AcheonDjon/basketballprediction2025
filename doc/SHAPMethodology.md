# Composite-Score Ranking Methodology

Based on the prompt to rank teams by quality, we decided to employ a composite-score ranking system rather than a traditional Elo system. While the Elo system focuses on wins, our approach requires a more holistic view by incorporating four key fields: **eFG%** (efficiency of field goals attempted), **PEM** (Player Efficiency Metric), **REBF** (Rebound and Foul), and **NRtg** (Net Rating).

In our methodology, we use **XGBoost**, a gradient-boosting machine learning algorithm effective in predicting score outcomes, and **SHAP** for interpretability. SHAP is used to extract feature importances relative to the point differential between the team and the opponent—recognizing that a simple win–loss metric does not capture the nuances of close or challenging games.

---

## 1. Point Differential Calculation

We begin by computing the point differential as a basic measure of game outcome:

```python
df['Point_Differential'] = df["team_score"] - df["opponent_team_score"]
```

# <<<<<<< HEAD

SHAP generates insightful charts (e.g., for eFG% weight calculation) that inform our weighting process.

---

> > > > > > > 0799bca0ce71c45ac8f07054050db33a582ebba6

## 2. Metric Calculations

### A. Effective Field Goal Percentage (eFG%)

The eFG% metric, adjusted using the absolute value of SHAP values and normalized to a percentage, is calculated as a weighted ratio of made shots to attempted shots:

```python
df["eFG%"] = (
    numerator_weights['FGM_2'] * df["FGM_2"] +
    numerator_weights['FGM_3'] * df["FGM_3"] +
    numerator_weights['FTM'] * df["FTM"]
) / (
    denom_weights['FGA_2'] * df["FGA_2"] +
    denom_weights['FGA_3'] * df["FGA_3"] +
    denom_weights['FTA'] * df["FTA"]
)
```

---

### B. Player Efficiency Metric (PEM)

PEM groups individual player performances into a single metric. First, we derive several estimations:

```python
df['Possessions'] = df['team_score'] + 0.5 * (df['FGA_2'] + df['FGA_3']) + df['OREB'] + df['TOV'] + 0.4 * df['FTA']
df['AST%'] = df['AST'] / (df['AST'] + df['TOV'])
df['BLK%'] = df['BLK'] / (df['opponent_FGA2'] + df['opponent_FGA3'])
df['TOV%'] = df['TOV'] / df['Possessions']
df['TOV_team%'] = df['TOV_team'] / df['Possessions']
df['STL%'] = df['STL'] / df['Possessions']
```

Using SHAP-derived weights, we calculate PEM by adding positive contributions and subtracting negative ones (such as turnovers):

```python
df["PEM"] = (
    numerator_weights['AST%'] * df["AST%"] +
    numerator_weights['BLK%'] * df["BLK%"] +
    numerator_weights['TOV%'] * df["TOV%"] -
    numerator_weights['TOV_team%'] * df["TOV_team%"] -
    numerator_weights['STL%'] * df["STL%"]
)
```

---

### C. Rebound and Foul (REBF)

The REBF metric captures both rebound performance and foul impact, normalized by possessions:

```python
df["REBF"] = (
    numerator_weights['DREB'] * (df["DREB"] / df["Possessions"]) +
    numerator_weights['OREB'] * (df["OREB"] / df["Possessions"]) -
    (numerator_weights['F_tech'] + numerator_weights['F_personal']) * ((df['F_tech'] + df['F_personal']) / df['Possessions'])
)
```

---

### D. Net Rating (NRtg)

Net Rating, a common measure of overall team performance, is calculated by first determining offensive and defensive ratings:

```python
df['ORtg'] = (df['team_score'] / df['Possessions']) * 100
df['DRtg'] = (df['opponent_team_score'] / df['Possessions']) * 100
df['NRtg'] = df['ORtg'] - df['DRtg']
```

---

## 3. Final Composite Score (Raptor Score)

After calculating the four metrics that cover shooting efficiency, player performance, rebounding/fouls, and overall game performance, we run a regression using XGBoost. In the final model, win percentage replaces point differential as the dependent variable to ensure that our weights align with the ultimate goal—winning games.

The final Raptor Score is computed as follows:

```python
df["Raptor_Score"] = (
    numerator_weights['eFG%'] * df["eFG%"] +
    numerator_weights['PEM'] * df["PEM"] +
    numerator_weights['REBF'] * df["REBF"] +
    numerator_weights['NRtg'] * df["NRtg"]
)
```

These scores are calculated for every game. The final team ranking is obtained by averaging each team's Raptor Scores across all games and then ranking them based on these averages.

---

## Conclusion

This composite scoring system provides a holistic measure of basketball team quality by integrating multiple facets of the game. By leveraging XGBoost for weight optimization and SHAP for model interpretability, our approach captures nuances that a traditional win–loss system or a simple Elo rating cannot. The resulting Raptor Score offers a comprehensive ranking that reflects both individual and team performance metrics.

---
