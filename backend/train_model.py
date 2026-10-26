from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "hotel_ratings.csv"
MODEL_DIR = ROOT / "models"
FEATURES = ["hotel_type", "city", "price_per_night", "star_category", "cleanliness_score",
            "service_score", "location_score", "amenities_score", "value_score", "review_count"]
TARGET = "rating"
CAT = ["hotel_type", "city"]
NUM = [c for c in FEATURES if c not in CAT]

def main():
    df = pd.read_csv(DATA)
    X, y = df[FEATURES], df[TARGET]
    preprocessor = ColumnTransformer([
        ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), NUM),
        ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                          ("onehot", OneHotEncoder(handle_unknown="ignore"))]), CAT)
    ])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)
    models = {
        "Linear Regression": LinearRegression(),
        "Ridge": Ridge(alpha=1.0),
        "Lasso": Lasso(alpha=.01, max_iter=10000),
        "Decision Tree": DecisionTreeRegressor(max_depth=8, random_state=42),
        "Random Forest": RandomForestRegressor(n_estimators=240, min_samples_leaf=2, random_state=42, n_jobs=-1)
    }
    results, fitted = [], {}
    for name, estimator in models.items():
        pipe = Pipeline([("preprocessor", preprocessor), ("model", estimator)])
        pipe.fit(X_train, y_train)
        pred = np.clip(pipe.predict(X_test), 1, 5)
        mse = mean_squared_error(y_test, pred)
        results.append({"model": name, "mae": round(mean_absolute_error(y_test, pred), 4),
                        "mse": round(mse, 4), "rmse": round(float(np.sqrt(mse)), 4),
                        "r2": round(r2_score(y_test, pred), 4)})
        fitted[name] = pipe
    best = max(results, key=lambda x: x["r2"])
    best_name = best["model"]
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump({"pipeline": fitted[best_name], "features": FEATURES, "target": TARGET, "model_name": best_name},
                MODEL_DIR / "hotel_rating_model.joblib")
    (MODEL_DIR / "metrics.json").write_text(json.dumps({"best_model": best_name, "models": results}, indent=2))
    print("Best model:", best_name)
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
