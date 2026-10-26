from pathlib import Path
import json
import math
import joblib
import numpy as np
import pandas as pd
from scipy import stats
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "hotel_ratings.csv"
MODEL = ROOT / "models" / "hotel_rating_model.joblib"
METRICS = ROOT / "models" / "metrics.json"
app = FastAPI(title="StayWise Hotel Rating API", version="1.0.0",
              description="Hotel rating prediction and SI statistical practicals.")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class HotelInput(BaseModel):
    hotel_type: str = "Boutique"
    city: str = "Jaipur"
    price_per_night: float = Field(6500, ge=300, le=100000)
    star_category: int = Field(4, ge=1, le=5)
    cleanliness_score: int = Field(4, ge=1, le=5)
    service_score: int = Field(4, ge=1, le=5)
    location_score: int = Field(4, ge=1, le=5)
    amenities_score: int = Field(4, ge=1, le=5)
    value_score: float = Field(4, ge=1, le=5)
    review_count: int = Field(250, ge=0, le=1000000)

def load_df():
    if not DATA.exists():
        raise HTTPException(503, "Dataset not generated. Run: python generate_dataset.py")
    return pd.read_csv(DATA)

def load_model():
    if not MODEL.exists():
        raise HTTPException(503, "Model not trained. Run: python train_model.py")
    return joblib.load(MODEL)

@app.get("/")
def root():
    return {"name":"StayWise API", "status":"ready", "docs":"/docs"}

@app.get("/api/health")
def health():
    return {"status":"ok", "dataset_exists": DATA.exists(), "model_exists": MODEL.exists()}

@app.get("/api/overview")
def overview():
    df = load_df()
    rating = df["rating"]
    clean = df.dropna()
    return {
        "rows": int(len(df)), "columns": int(len(df.columns)),
        "missing_cells": int(df.isna().sum().sum()),
        "mean_rating": round(float(rating.mean()), 2), "median_rating": round(float(rating.median()), 2),
        "std_rating": round(float(rating.std()), 2), "min_rating": float(rating.min()), "max_rating": float(rating.max()),
        "hotel_types": int(df["hotel_type"].nunique()), "cities": int(df["city"].nunique()),
        "rating_distribution": [{"rating": str(k), "count": int(v)} for k,v in rating.round().value_counts().sort_index().items()],
        "by_type": [{"name": str(k), "rating": round(float(v),2), "count": int((df.hotel_type==k).sum())}
                    for k,v in df.groupby("hotel_type")["rating"].mean().sort_values(ascending=False).items()],
        "by_city": [{"name": str(k), "rating": round(float(v),2), "count": int((df.city==k).sum())}
                    for k,v in df.groupby("city")["rating"].mean().sort_values(ascending=False).items()],
        "numeric_summary": df.select_dtypes(include="number").describe().round(2).reset_index(names="stat").to_dict(orient="records"),
        "missing_by_column": [{"name": c, "missing": int(n)} for c,n in df.isna().sum().items()],
        "outlier_counts": {c: int(((df[c] < df[c].quantile(.25)-1.5*(df[c].quantile(.75)-df[c].quantile(.25))) |
                                    (df[c] > df[c].quantile(.75)+1.5*(df[c].quantile(.75)-df[c].quantile(.25)))).sum())
                           for c in df.select_dtypes(include="number").columns},
        "sample": df.head(8).replace({np.nan: None}).to_dict(orient="records"),
        "dataset_note": "Synthetic teaching data; not real customer-review records."
    }

@app.post("/api/predict")
def predict(payload: HotelInput):
    bundle = load_model()
    row = pd.DataFrame([payload.model_dump()])
    pred = float(np.clip(bundle["pipeline"].predict(row)[0], 1, 5))
    return {"predicted_rating": round(pred, 2), "label": "Excellent" if pred>=4.5 else "Very good" if pred>=4 else "Good" if pred>=3.5 else "Fair" if pred>=3 else "Needs improvement",
            "model": bundle["model_name"], "scale": "1–5", "note": "Estimate from a synthetic teaching dataset; not a guarantee of guest ratings."}

@app.get("/api/models")
def models():
    if not METRICS.exists():
        raise HTTPException(503, "Model metrics not found. Run: python train_model.py")
    return json.loads(METRICS.read_text())

@app.get("/api/analytics")
def analytics():
    df = load_df()
    numeric = df.select_dtypes(include="number")
    corr = numeric.corr().round(3)
    pairs = []
    for col in numeric.columns:
        if col != "rating":
            valid = df[[col,"rating"]].dropna()
            if len(valid) > 2:
                pr, pp = stats.pearsonr(valid[col], valid["rating"])
                sr, sp = stats.spearmanr(valid[col], valid["rating"])
                pairs.append({"feature":col, "covariance":round(float(valid[col].cov(valid["rating"])),4),
                              "pearson_r":round(float(pr),4), "pearson_p":float(pp),
                              "spearman_r":round(float(sr),4), "spearman_p":float(sp)})
    # Example inference tests at alpha = 0.05
    types = [g["rating"].dropna().values for _,g in df.groupby("hotel_type")]
    f_stat, anova_p = stats.f_oneway(*types)
    premium = df[df["star_category"] >= 4]["rating"].dropna()
    standard = df[df["star_category"] < 4]["rating"].dropna()
    t_stat, t_p = stats.ttest_ind(premium, standard, equal_var=False)
    contingency = pd.crosstab(df["hotel_type"], df["star_category"])
    chi2, chi_p, dof, _ = stats.chi2_contingency(contingency)
    rating = df["rating"].dropna().to_numpy()
    rng = np.random.default_rng(42)
    sample_means = [float(np.mean(rng.choice(rating, size=30, replace=True))) for _ in range(500)]
    se = float(rating.std(ddof=1)/math.sqrt(len(rating)))
    ci = stats.t.interval(.95, len(rating)-1, loc=float(rating.mean()), scale=stats.sem(rating))
    return {
        "correlations": pairs,
        "correlation_matrix": [{"feature":c, **{c2:float(corr.loc[c,c2]) for c2 in corr.columns}} for c in corr.columns],
        "anova":{"statistic":round(float(f_stat),4),"p_value":float(anova_p),"alpha":0.05,"significant":bool(anova_p<.05),
                 "interpretation":"At least one hotel-type mean differs statistically." if anova_p<.05 else "No statistically significant mean difference detected."},
        "t_test":{"statistic":round(float(t_stat),4),"p_value":float(t_p),"alpha":0.05,"significant":bool(t_p<.05),
                  "groups":"Star category 4–5 vs 1–3",
                  "interpretation":"The group means differ statistically." if t_p<.05 else "No statistically significant group-mean difference detected."},
        "chi_square":{"statistic":round(float(chi2),4),"p_value":float(chi_p),"dof":int(dof),"alpha":0.05,"significant":bool(chi_p<.05),
                      "interpretation":"Hotel type and star category show association in this sample." if chi_p<.05 else "No statistically significant association detected."},
        "confidence_interval":{"mean":round(float(rating.mean()),3),"lower":round(float(ci[0]),3),"upper":round(float(ci[1]),3),"confidence":0.95},
        "clt":{"sample_size":30,"repetitions":500,"sample_mean_average":round(float(np.mean(sample_means)),3),
               "standard_error":round(se,4),"sample_means":[round(x,3) for x in sample_means[:60]]},
        "distribution":{"normal_mean":round(float(rating.mean()),3),"normal_std":round(float(rating.std(ddof=1)),3),
                        "uniform_min":1,"uniform_max":5,"binomial_n":5,"binomial_p":0.5}
    }

@app.get("/api/dataset.csv")
def download_dataset():
    df = load_df()
    return StreamingResponse(iter([df.to_csv(index=False)]), media_type="text/csv",
                             headers={"Content-Disposition":"attachment; filename=hotel_ratings.csv"})
