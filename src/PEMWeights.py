import pandas as pd
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
import numpy as np

# Load the data
df = pd.read_csv('./data/merged_team_games.csv', sep='\t')

#Possessions Calculation
df['Possessions'] = df['team_score'] + 0.5 * df['FGA%'] - df['OREB'] + df['TOV'] + 0.4 * df['FTA']
# Calculate percentages
df['AST%'] = df['AST'] / (df['AST'] + df['TOV'])
df['BLK%'] = df['BLK'] / df['FGA%']
df['TOV%'] = df['TOV'] / df['Possessions']
df['TOV_team%'] = df['TOV_team'] / df['Possessions']
df['STL%'] = df['STL'] / df['Possessions']

# Define independent variables (predictors)
X = df[['AST%', 'BLK%', 'TOV%', 'TOV_team%', 'STL%']]

# Define dependent variable (target)
y = df['Point_Differential']

# Standardize the predictors
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Define the range of alpha values to test
alphas = np.logspace(-4, 0, 50)

# Initialize and fit LassoCV
lasso_cv = LassoCV(alphas=alphas, cv=10, random_state=0)
lasso_cv.fit(X_scaled, y)

# Get the optimal alpha
optimal_alpha = lasso_cv.alpha_
print(f"Optimal Alpha: {optimal_alpha}")

# Get the coefficients with the optimal alpha
optimal_coefficients = lasso_cv.coef_
print(f"Optimal Coefficients: {optimal_coefficients}")

# Print the coefficients for each predictor
coeff_names = ['AST%', 'BLK%', 'TOV%', 'TOV_team%', 'STL%']
for coeff_name, coeff_value in zip(coeff_names, optimal_coefficients):
    print(f"{coeff_name} Coefficient: {coeff_value}")
