import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import argparse
import os
import tkinter as tk
from tkinter import filedialog

def analyze_feature_significance(df, target_col='Win', test_size=0.2, n_permutations=100, 
                                 random_state=42, xgb_params=None):
    """
    Analyze the statistical significance of features in predicting a binary outcome.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe containing features and target variable
    target_col : str, default='Win'
        Name of the binary target column (containing 0 or 1)
    test_size : float, default=0.2
        Proportion of data to use for testing
    n_permutations : int, default=100
        Number of permutations to run for statistical significance test
    random_state : int, default=42
        Random seed for reproducibility
    xgb_params : dict, default=None
        Additional parameters for XGBClassifier
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing feature names, importance scores, p-values, and significance flags
    """
    # Check if target column exists
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataframe")
    
    # Check if target is binary
    unique_values = df[target_col].unique()
    if not set(unique_values).issubset({0, 1}):
        raise ValueError(f"Target column must contain only 0 and 1 values, found {unique_values}")
    
    # Prepare data
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Default XGBoost parameters if none provided
    if xgb_params is None:
        xgb_params = {
            'n_estimators': 100,
            'learning_rate': 0.1,
            'max_depth': 5,
            'min_child_weight': 1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'objective': 'binary:logistic',
            'eval_metric': 'logloss',
            'use_label_encoder': False,
            'random_state': random_state
        }
    
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Train base model
    model = XGBClassifier(**xgb_params)
    model.fit(X_train, y_train)
    
    # Get feature importance from the model
    importance_dict = {}
    for feature, importance in zip(X.columns, model.feature_importances_):
        importance_dict[feature] = importance
    
    # Calculate baseline accuracy
    y_pred = model.predict(X_test)
    baseline_accuracy = accuracy_score(y_test, y_pred)
    
    # Permutation test for statistical significance
    print(f"Running {n_permutations} permutations to determine statistical significance...")
    p_values = {}
    permutation_importances = {feature: [] for feature in X.columns}
    
    for _ in tqdm(range(n_permutations), desc="Calculating permutation importance"):
        for feature in X.columns:
            # Create a copy of test data
            X_test_permuted = X_test.copy()
            
            # Permute single feature
            X_test_permuted[feature] = np.random.permutation(X_test_permuted[feature].values)
            
            # Predict with permuted feature
            y_pred_permuted = model.predict(X_test_permuted)
            permuted_accuracy = accuracy_score(y_test, y_pred_permuted)
            
            # Store importance drop
            importance_drop = baseline_accuracy - permuted_accuracy
            permutation_importances[feature].append(importance_drop)
    
    # Calculate p-values based on permutation test
    for feature in X.columns:
        # Count how many times permutation importance was >= actual importance
        count_greater_equal = sum(1 for x in permutation_importances[feature] if x >= importance_dict[feature])
        p_values[feature] = (count_greater_equal + 1) / (n_permutations + 1)  # Add 1 for Laplace smoothing
    
    # Create results DataFrame
    results = pd.DataFrame({
        'Feature': list(importance_dict.keys()),
        'XGBoost_Importance': list(importance_dict.values()),
        'p_value': [p_values[feature] for feature in importance_dict.keys()]
    })
    
    # Add significance flag
    results['Significant'] = results['p_value'] < 0.05
    
    # Sort by importance
    results = results.sort_values('XGBoost_Importance', ascending=False).reset_index(drop=True)
    
    return results

def plot_feature_significance(results, figsize=(12, 8), save_path=None):
    """
    Plot feature importance and significance.
    
    Parameters:
    -----------
    results : pandas.DataFrame
        DataFrame returned by analyze_feature_significance function
    figsize : tuple, default=(12, 8)
        Size of the figure
    save_path : str, default=None
        Path to save the figure. If None, the figure is displayed
    """
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)
    
    # Sort data for plotting
    plot_data = results.sort_values('XGBoost_Importance', ascending=True)
    
    # Plot feature importance
    colors = ['green' if sig else 'red' for sig in plot_data['Significant']]
    ax1.barh(plot_data['Feature'], plot_data['XGBoost_Importance'], color=colors)
    ax1.set_title('Feature Importance (green = statistically significant)')
    ax1.set_xlabel('Importance Score')
    
    # Plot p-values
    ax2.barh(plot_data['Feature'], plot_data['p_value'], color=colors)
    ax2.axvline(x=0.05, color='black', linestyle='--', alpha=0.7)
    ax2.set_title('Feature Significance (p-values)')
    ax2.set_xlabel('p-value (lower is more significant)')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save or display figure
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {save_path}")
    else:
        plt.show()
    
    return fig

def select_file():
    """Open a file dialog to select a CSV file"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select CSV file",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    root.destroy()
    return file_path

def interactive_mode():
    """Run the analysis in interactive mode with file dialog"""
    # Ask user to select a file
    file_path = select_file()
    
    if not file_path:
        print("No file selected. Exiting.")
        return
    
    # Load the CSV file
    print(f"Loading data from {file_path}...")
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading file: {e}")
        return
    
    print(f"Data shape: {df.shape}")
    print(f"Columns: {', '.join(df.columns)}")
    
    # Check for Win column
    if 'Win' not in df.columns:
        print("Warning: 'Win' column not found in the dataset.")
        print(f"Available columns: {', '.join(df.columns)}")
        target_col = input("Enter the name of your target column: ")
    else:
        target_col = 'Win'
    
    # Set default output paths
    output_dir = os.path.dirname(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    csv_output = os.path.join(output_dir, f"{base_name}_feature_significance.csv")
    plot_output = os.path.join(output_dir, f"{base_name}_feature_significance.png")
    
    # Number of permutations
    try:
        n_permutations = int(input("Enter number of permutations (default: 100): ") or "100")
    except ValueError:
        print("Invalid input. Using default value of 100 permutations.")
        n_permutations = 100
    
    # Run analysis
    try:
        results = analyze_feature_significance(
            df, 
            target_col=target_col, 
            n_permutations=n_permutations
        )
    except Exception as e:
        print(f"Error during analysis: {e}")
        return
    
    # Display results
    print("\nFeature Significance Results:")
    print(results)
    
    # Save results
    results.to_csv(csv_output, index=False)
    print(f"Results saved to {csv_output}")
    
    # Plot and save results
    plot_feature_significance(results, save_path=plot_output)
    
    print("\nAnalysis complete!")

def command_line_mode():
    """Run the analysis with command line arguments"""
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Analyze feature significance using XGBoost')
    parser.add_argument('csv_file', type=str, nargs='?', help='Path to CSV file')
    parser.add_argument('--target', type=str, default='Win', help='Name of target column (default: Win)')
    parser.add_argument('--test-size', type=float, default=0.2, help='Test size for train/test split (default: 0.2)')
    parser.add_argument('--permutations', type=int, default=100, help='Number of permutations (default: 100)')
    parser.add_argument('--output', type=str, help='Output CSV file (default: based on input filename)')
    parser.add_argument('--plot', type=str, help='Output plot file (default: based on input filename)')
    parser.add_argument('--seed', type=int, default=42, help='Random seed (default: 42)')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    args = parser.parse_args()
    
    # If interactive flag is set or no CSV file is provided, run in interactive mode
    if args.interactive or not args.csv_file:
        interactive_mode()
        return
    
    # Check if file exists
    if not os.path.isfile(args.csv_file):
        print(f"Error: File '{args.csv_file}' not found")
        return
    
    # Set default output paths if not provided
    output_dir = os.path.dirname(args.csv_file)
    base_name = os.path.splitext(os.path.basename(args.csv_file))[0]
    
    if not args.output:
        args.output = os.path.join(output_dir, f"{base_name}_feature_significance.csv")
        
    if not args.plot:
        args.plot = os.path.join(output_dir, f"{base_name}_feature_significance.png")
    
    # Load and analyze data
    print(f"Loading data from {args.csv_file}...")
    df = pd.read_csv(args.csv_file)
    
    print(f"Data shape: {df.shape}")
    print(f"Columns: {', '.join(df.columns)}")
    
    # Check for missing values
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        print(f"Warning: Dataset contains {missing_count} missing values. Consider preprocessing.")
    
    # Analyze feature significance
    try:
        results = analyze_feature_significance(
            df, 
            target_col=args.target, 
            test_size=args.test_size, 
            n_permutations=args.permutations,
            random_state=args.seed
        )
    except Exception as e:
        print(f"Error during analysis: {e}")
        return
    
    # Display results
    print("\nFeature Significance Results:")
    print(results)
    
    # Save results
    results.to_csv(args.output, index=False)
    print(f"Results saved to {args.output}")
    
    # Plot and save results
    plot_feature_significance(results, save_path=args.plot)

# This is what runs when you press the "Run" button
if __name__ == "__main__":
    # Check if any command line arguments were provided
    import sys
    if len(sys.argv) > 1:
        command_line_mode()
    else:
        interactive_mode()