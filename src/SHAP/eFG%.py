import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
import shap
import numpy as np

# Step 1: Load and Preprocess the Data
df = pd.read_csv("./data/merged_team_games.csv", sep="\t")

# Example: Drop columns that are identifiers or not useful
important = ['FGM_2', 'FGA_2', 'FGM_3', 'FGA_3', 'FTM', 'FTA', 'Point_Differential']
# Define the target and feature set
target = "Point_Differential"
# Assume you want to keep all remaining numeric columns as features
features = [col for col in important if col != target]

X = df[features]
y = df[target]

# Step 2: Split Data into Training and Testing Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
param_grid = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 4, 5]
}

# Step 3: Train a Tree-Based Model (e.g., XGBoost)
model = xgb.XGBRegressor(random_state=42)

# Get the best parameters
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_

best_model = xgb.XGBRegressor(random_state=42, **best_params)
best_model.fit(X_train, y_train)

# Step 4: Initialize the SHAP Explainer and Calculate SHAP Values
# For tree-based models, TreeExplainer is efficient.
explainer = shap.Explainer(best_model, X_train)
shap_values = explainer(X_test)

feature_names = X_train.columns
shap_importances = np.abs(shap_values.values).mean(axis=0)
shap_dict = dict(zip(feature_names, shap_importances))
# Define feature groups for numerator and denominator
numerator_features = ['FGM_2', 'FGM_3', 'FTM']
denom_features = ['FGA_2', 'FGA_3', 'FTA']

# Normalize SHAP importances so that weights sum to 1 in each group
num_total = sum(shap_dict[feat] for feat in numerator_features)
numerator_weights = {feat: shap_dict[feat] / num_total for feat in numerator_features}

denom_total = sum(shap_dict[feat] for feat in denom_features)
denom_weights = {feat: shap_dict[feat] / denom_total for feat in denom_features}

print(numerator_weights)
print(denom_weights)

df["eFG%"] = (
    numerator_weights['FGM_2'] * df["FGM_2"] + 
    numerator_weights['FGM_3'] * df["FGM_3"] + 
    numerator_weights['FTM'] * df["FTM"]
) / (
    denom_weights['FGA_2'] * df["FGA_2"] + 
    denom_weights['FGA_3'] * df["FGA_3"] +
    denom_weights['FTA'] * df["FTA"] 
)


df = df[['team', 'opponent_team', 'eFG%', 'PEM', 'REBF', 'NRtg', 'WinPct', 'Point_Differential']].copy()
df.to_csv('./data/SHAP/RaptorMerged.csv', sep='\t', index=False)




# Step 5: Visualize the SHAP Values
# Summary plot: shows overall feature importance and effect direction
shap.summary_plot(shap_values, X_test)

# Optional: Dependence plot for a specific feature (e.g., 'FGM_2')
shap.dependence_plot("FGM_2", shap_values.values, X_test)
