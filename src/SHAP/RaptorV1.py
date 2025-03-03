import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
import shap
import numpy as np
import optuna

# Step 1: Load and Preprocess the Data
df = pd.read_csv("./data/SHAP/RaptorMerged.csv", sep="\t")

# Example: Drop columns that are identifiers or not useful
important = ['WinPct','eFG%', 'PEM', 'REBF', 'NRtg']

# Define the target and feature set
target = "WinPct"
# Assume you want to keep all remaining numeric columns as features
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
best_params = study.best_params


model = xgb.XGBRegressor( **best_params)
model.fit(X_train, y_train)

# Step 4: Initialize the SHAP Explainer and Calculate SHAP Values
# For tree-based models, TreeExplainer is efficient.
explainer = shap.Explainer(model, X_train)
shap_values = explainer(X_test)

feature_names = X_train.columns
shap_importances = np.abs(shap_values.values).mean(axis=0)
shap_dict = dict(zip(feature_names, shap_importances))


# Normalize SHAP importances so that weights sum to 1 in each group
num_total = sum(shap_dict[feat] for feat in feature_names)
numerator_weights = {feat: shap_dict[feat] / num_total for feat in feature_names}


print(numerator_weights)
df["Raptor_Score"] = (
    numerator_weights['eFG%'] * df["eFG%"] + 
    numerator_weights['PEM'] * df["PEM"] + 
    numerator_weights['REBF'] * df["REBF"] + 
    numerator_weights['NRtg'] * df["NRtg"]
)

df.to_csv('./data/SHAP/RaptorMerged.csv', sep='\t', index=False)


# df.to_csv('./data/SHAP/RaptorMerged.csv', sep='\t', index=False)

# df.to_csv('./data/SHAP/RaptorMerged.csv', sep='\t', index=False)
# # Step 5: Visualize the SHAP Values
# # Summary plot: shows overall feature importance and effect direction
# shap.summary_plot(shap_values, X_test)

# # Optional: Dependence plot for a specific feature (e.g., 'FGM_2')
# shap.dependence_plot("FGM_2", shap_values.values, X_test)
