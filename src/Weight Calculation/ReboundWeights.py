import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv('./data/merged_team_games.csv', sep='\t')

# Define the features (defensive and offensive rebound scores)
X = df[['DREB', 'OREB']]

# Define the target variable (point differential)
y = df['Point_Differential']

# Fit the linear regression model
model = LinearRegression()
model.fit(X, y)

# Get the coefficients (weights) from the linear regression model
coeffs = model.coef_

# Use the coefficients as weights to combine the defensive and offensive rebound scores
df['rebound_score'] = (coeffs[0] * df['DREB'] + coeffs[1] * df['OREB'])/(coeffs[0] + coeffs[1])
df.to_csv("data/merged_team_games.csv", sep="\t", index=False)