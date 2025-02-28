import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv('./data/merged_team_games.csv', sep='\t')
print(df.columns)
# Define the features (defensive and offensive rebound scores)
X = df[['F_tech', 'F_personal']]

# Define the target variable (point differential)
y = df['Point_Differential']

# Fit the linear regression model
model = LinearRegression()
model.fit(X, y)

# Get the coefficients (weights) from the linear regression model
coeffs = model.coef_

# Use the coefficients as weights to combine the defensive and offensive rebound scores
df['Foul'] = (coeffs[0] * df['F_tech'] + coeffs[1] * df['F_personal']) / df['Possessions']
df.drop(columns=['Foul Metric'], inplace=True)
df.to_csv("data/merged_team_games.csv", sep="\t", index=False)