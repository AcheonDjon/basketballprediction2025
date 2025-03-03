import pandas as pd
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler

# Load the data
df = pd.read_csv("./data/merged_team_games.csv", sep="\t")

# Print all the columns
print(df.columns)

# Define the features and target
X = df[['FGM_2', 'FGA_2', 'FGM_3', 'FGA_3', 'FTM', 'FTA', 'TOV', 'TOV_team']]
Y = df['Point_Differential']

# Apply Standard Scaling to the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Define the range of alpha values to test
alphas = [0.001, 0.01, 0.1, 1, 10]

# Initialize and fit LassoCV
lasso_cv = LassoCV(alphas=alphas, cv=10, random_state=0)
lasso_cv.fit(X_scaled, Y)

# Get the optimal alpha
optimal_alpha = lasso_cv.alpha_
print(f"Optimal Alpha: {optimal_alpha}")

# Get the coefficients with the optimal alpha
optimal_coefficients = lasso_cv.coef_
print(f"Optimal Coefficients: {optimal_coefficients}")

# Define the weights based on Lasso coefficients
weights = {
    'FGM_2': optimal_coefficients[0],
    'FGA_2': optimal_coefficients[1],
    'FGM_3': optimal_coefficients[2],
    'FGA_3': optimal_coefficients[3],
    'FTM': optimal_coefficients[4],
    'FTA': optimal_coefficients[5],
    'TOV': optimal_coefficients[6],
    'TOV_team': optimal_coefficients[7]
}

# Print the coefficients for each predictor
coeff_names = ['FGM_2', 'FGA_2', 'FGM_3', 'FGA_3', 'FTM', 'FTA', 'TOV', 'TOV_team']
for coeff_name, coeff_value in zip(coeff_names, optimal_coefficients):
    print(f"{coeff_name} Coefficient: {coeff_value}")

