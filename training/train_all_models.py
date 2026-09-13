import os
import sys
import joblib
import pandas as pd

# --------------------------------------------------
# ADD PROJECT ROOT TO PYTHON PATH
# --------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from training.data_loader import (
    load_dataset,
    get_features_target
)

from training.data_cleaning import clean_data
from training.feature_engineering import create_features

from training.train_linear_regression import train_linear_regression
from training.train_random_forest import train_random_forest
from training.train_gradient_boosting import train_gradient_boosting
from training.train_xgboost import train_xgboost
from training.train_lightgbm import train_lightgbm
from training.train_catboost import train_catboost
from training.train_stacking import train_stacking

from training.model_evaluation import evaluate_all_models

from anomaly.anomaly_detector import train_anomaly_model


# --------------------------------------------------
# DATASET
# --------------------------------------------------

DATASET_PATH = os.path.join(
    PROJECT_ROOT,
    "dataset",
    "china.csv"
)


def main():

    print("\n========================================")
    print(" AI SOFTWARE MAINTENANCE MODEL TRAINING")
    print("========================================")

    # --------------------------------------------------
    # 1. LOAD DATASET
    # --------------------------------------------------

    print("\nLoading dataset...")

    df = load_dataset(DATASET_PATH)

    print(f"Dataset shape: {df.shape}")

    # --------------------------------------------------
    # 2. DATA CLEANING
    # --------------------------------------------------

    print("\nCleaning dataset...")

    df = clean_data(df)

    print(f"Cleaned dataset shape: {df.shape}")

    # --------------------------------------------------
    # 3. FEATURE ENGINEERING
    # --------------------------------------------------

    print("\nCreating features...")

    df = create_features(df)

    # --------------------------------------------------
    # 4. GET FEATURES AND TARGET
    # --------------------------------------------------

    X, y = get_features_target(df)

    print(f"\nNumber of features: {X.shape[1]}")
    print(f"Number of samples: {X.shape[0]}")

    print("\nFeatures:")

    for feature in X.columns:
        print(f"  - {feature}")

    print("\nTarget: Effort")

    # --------------------------------------------------
    # 5. TRAIN / TEST SPLIT
    # --------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    print("\nTraining samples:", len(X_train))
    print("Testing samples:", len(X_test))

    # --------------------------------------------------
    # 6. CREATE DIRECTORIES
    # --------------------------------------------------

    os.makedirs(
        os.path.join(PROJECT_ROOT, "models"),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(PROJECT_ROOT, "analysis_results"),
        exist_ok=True
    )

    # --------------------------------------------------
    # 7. FEATURE SCALING
    # --------------------------------------------------

    print("\nScaling features...")

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)

    X_test_scaled = scaler.transform(X_test)

    scaler_path = os.path.join(
        PROJECT_ROOT,
        "models",
        "scaler.pkl"
    )

    joblib.dump(
        scaler,
        scaler_path
    )

    print(
        "Scaler saved:",
        scaler_path
    )

    # --------------------------------------------------
    # 8. LINEAR REGRESSION
    # --------------------------------------------------

    print("\nTraining Linear Regression...")

    linear_model = train_linear_regression(
        X_train_scaled,
        y_train
    )

    # --------------------------------------------------
    # 9. RANDOM FOREST
    # --------------------------------------------------

    print("Training Random Forest...")

    random_forest = train_random_forest(
        X_train,
        y_train
    )

    # --------------------------------------------------
    # 10. GRADIENT BOOSTING
    # --------------------------------------------------

    print("Training Gradient Boosting...")

    gradient_boosting = train_gradient_boosting(
        X_train,
        y_train
    )

    # --------------------------------------------------
    # 11. XGBOOST
    # --------------------------------------------------

    print("Training XGBoost...")

    xgboost_model = train_xgboost(
        X_train,
        y_train
    )

    # --------------------------------------------------
    # 12. LIGHTGBM
    # --------------------------------------------------

    print("Training LightGBM...")

    lightgbm_model = train_lightgbm(
        X_train,
        y_train
    )

    # --------------------------------------------------
    # 13. CATBOOST
    # --------------------------------------------------

    print("Training CatBoost...")

    catboost_model = train_catboost(
        X_train,
        y_train
    )

    # --------------------------------------------------
    # 14. STACKING ENSEMBLE
    # --------------------------------------------------

    print("Training Stacking Ensemble...")

    stacking_model = train_stacking(
        X_train,
        y_train
    )

    # --------------------------------------------------
    # 15. ISOLATION FOREST
    # --------------------------------------------------

    print("\nTraining Isolation Forest Anomaly Detector...")

    anomaly_model = train_anomaly_model(
        X_train
    )

    print(
        "Isolation Forest saved:"
        " models/isolation_forest.pkl"
    )

    # --------------------------------------------------
    # 16. MODEL COLLECTION
    # --------------------------------------------------

    models = {

        "Linear Regression": (
            linear_model,
            X_test_scaled
        ),

        "Random Forest": (
            random_forest,
            X_test
        ),

        "Gradient Boosting": (
            gradient_boosting,
            X_test
        ),

        "XGBoost": (
            xgboost_model,
            X_test
        ),

        "LightGBM": (
            lightgbm_model,
            X_test
        ),

        "CatBoost": (
            catboost_model,
            X_test
        ),

        "Stacking Ensemble": (
            stacking_model,
            X_test
        )
    }

    # --------------------------------------------------
    # 17. MODEL EVALUATION
    # --------------------------------------------------

    print("\n========================================")
    print(" MODEL EVALUATION")
    print("========================================")

    results = []

    for name, (model, test_data) in models.items():

        print(f"\nEvaluating {name}...")

        predictions = model.predict(test_data)

        mae = mean_absolute_error(
            y_test,
            predictions
        )

        rmse = mean_squared_error(
            y_test,
            predictions
        ) ** 0.5

        r2 = r2_score(
            y_test,
            predictions
        )

        results.append({

            "Model": name,

            "MAE": mae,

            "RMSE": rmse,

            "R2": r2
        })

    # --------------------------------------------------
    # 18. MODEL COMPARISON
    # --------------------------------------------------

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        by="RMSE"
    )

    print("\n========================================")
    print(" MODEL COMPARISON")
    print("========================================")

    print(
        results_df.to_string(
            index=False
        )
    )

    # --------------------------------------------------
    # 19. SAVE MODEL COMPARISON
    # --------------------------------------------------

    comparison_path = os.path.join(
        PROJECT_ROOT,
        "analysis_results",
        "model_comparison.csv"
    )

    results_df.to_csv(
        comparison_path,
        index=False
    )

    print(
        "\nModel comparison saved:",
        comparison_path
    )

    # --------------------------------------------------
    # 20. BEST MODEL
    # --------------------------------------------------

    best_model = results_df.iloc[0]

    print("\n========================================")
    print(" BEST MODEL")
    print("========================================")

    print(
        f"Model : {best_model['Model']}"
    )

    print(
        f"MAE   : {best_model['MAE']:.4f}"
    )

    print(
        f"RMSE  : {best_model['RMSE']:.4f}"
    )

    print(
        f"R2    : {best_model['R2']:.4f}"
    )

    # --------------------------------------------------
    # 21. FINAL STATUS
    # --------------------------------------------------

    print("\n========================================")
    print(" TRAINING COMPLETED SUCCESSFULLY")
    print("========================================")

    print("\nGenerated model files:")

    print("  models/scaler.pkl")
    print("  models/linear_regression.pkl")
    print("  models/random_forest.pkl")
    print("  models/gradient_boosting.pkl")
    print("  models/xgboost.pkl")
    print("  models/lightgbm.pkl")
    print("  models/catboost.pkl")
    print("  models/stacking_ensemble.pkl")
    print("  models/isolation_forest.pkl")

    print("\nModel comparison:")
    print("  analysis_results/model_comparison.csv")

    print("\nYour ML training pipeline is ready.")


if __name__ == "__main__":
    main()