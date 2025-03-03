import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
import shap
import numpy as np
import optuna  # Bayesian Optimization Library

# Step 1: Load and Preprocess the Data
df = pd.read_csv("./data/merged_team_games.csv", sep="\t")

# Example: Drop columns that are identifiers or not useful
important = ['FGM_2', 'FGA_2', 'FGM_3', 'FGA_3', 'FTM', 'FTA', 'Point_Differential']
target = "Point_Differential"
features = [col for col in important if col != target]

X = df[features]
y = df[target]

# Step 2: Split Data into Training and Testing Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train_optuna, X_val_optuna, y_train_optuna, y_val_optuna = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Step 3: Define Bayesian Optimization Objective Function
def objective(trial):
    """Objective function for Optuna to optimize XGBoost hyperparameters."""
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 50, 500),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'gamma': trial.suggest_float('gamma', 0, 5),
        'reg_alpha': trial.suggest_float('reg_alpha', 0, 1),
        'reg_lambda': trial.suggest_float('reg_lambda', 0, 1),
        'random_state': 42,
        'eval_metric': 'rmse',
        'early_stopping_rounds': 10
    }

    model = xgb.XGBRegressor(**params)
    model.fit(X_train_optuna, y_train_optuna, eval_set=[(X_val_optuna, y_val_optuna)], verbose=False,)
    
    # Evaluate using Mean Squared Error
    predictions = model.predict(X_val_optuna)
    mse = np.mean((y_val_optuna - predictions) ** 2)
    
    return mse  # Minimize MSE

# Step 4: Run Bayesian Optimization
study = optuna.create_study(direction='minimize')  # Minimize MSE
study.optimize(objective, n_trials=50)  # Run 50 trials

# Step 5: Train the Best Model from Bayesian Optimization
best_params = study.best_params
best_model = xgb.XGBRegressor(**best_params)
best_model.fit(X_train, y_train)


# Step 6: Initialize the SHAP Explainer and Calculate SHAP Values
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

print("Numerator Weights:", numerator_weights)
print("Denominator Weights:", denom_weights)

# Step 7: Compute eFG% using SHAP-Derived Weights
df["eFG%"] = (
    numerator_weights['FGM_2'] * df["FGM_2"] + 
    numerator_weights['FGM_3'] * df["FGM_3"] + 
    numerator_weights['FTM'] * df["FTM"]/
    (denom_weights['FGA_2'] * df["FGA_2"] +
    denom_weights['FGA_3'] * df["FGA_3"] +
    denom_weights['FTA'] * df["FTA"] )
)

# Step 8: Save Processed Data
df = df[['team', 'opponent_team', 'eFG%', 'PEM', 'REBF', 'NRtg', 'WinPct', 'Point_Differential']].copy()
df.to_csv('./data/SHAP/RaptorMerged.csv', sep='\t', index=False)

# Step 9: Visualize SHAP Values
shap.summary_plot(shap_values, X_test)
shap.dependence_plot("FGM_2", shap_values.values, X_test)