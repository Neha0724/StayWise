# StayWise — Hotel Rating Prediction & Statistical Analysis

A full-stack SI practical project built with **React + Vite + Tailwind CSS** and a **FastAPI + scikit-learn** backend.

> **Dataset transparency:** `backend/data/hotel_ratings.csv` is a reproducible synthetic teaching dataset generated for this project. It is not scraped or real customer-review data. Use a real hotel dataset before making real-world claims.

## Features
- Hotel rating prediction (1–5) using a trained Random Forest Regressor
- Model comparison: Linear Regression, Ridge, Lasso, Decision Tree, Random Forest
- MAE, MSE, RMSE and R² metrics
- Data overview, missing-value checks, descriptive statistics and outlier counts
- Histogram-style rating distribution, rating-by-category summaries and correlation analysis
- Pearson/Spearman correlation with p-values
- Welch independent t-test, one-way ANOVA and chi-square test examples
- Confidence interval for mean rating and CLT sampling demonstration
- CSV dataset download and prediction form
- Responsive dashboard with a warm ivory / terracotta palette balanced by cool teal / slate

## Run locally

### 1. Backend
Requires Python 3.10+.

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python generate_dataset.py
python train_model.py
uvicorn app.main:app --reload
```

Backend: http://127.0.0.1:8000  
API docs: http://127.0.0.1:8000/docs

### 2. Frontend (new terminal)
Requires Node.js 18+.

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

The Vite development server proxies `/api` to FastAPI.

## Suggested project explanation
1. **Problem:** estimate an expected hotel rating from property and guest-experience attributes.
2. **Target:** `rating` (continuous 1–5 score), so this is a regression task.
3. **Preprocessing:** imputation, one-hot encoding for categories, standard scaling for numeric features.
4. **Models:** Linear Regression, Ridge, Lasso, Decision Tree Regressor, Random Forest Regressor.
5. **Evaluation:** held-out test set with MAE, MSE, RMSE and R².
6. **Statistical analysis:** descriptive statistics, distributions, confidence intervals, correlation, t-test, ANOVA and chi-square.
7. **Limitations:** synthetic data is for demonstration; model scores measure fit to generated patterns, not real hotel-market performance.

## Practical coverage
- **Lab 2:** data loading, cleaning, shape/info, descriptive stats, missing values, histograms, box/outlier summaries, bar/pie/scatter/line-style views, CSV export.
- **Lab 3:** normal/uniform/binomial distribution concepts and probability summaries.
- **Lab 4:** CLT sampling distribution, standard error, point estimate and confidence interval.
- **Practical 4 assignment / Lab 5:** mean, median, standard deviation, confidence intervals and one-sample tests.
- **Practical 6:** independent t-test, paired t-test, one-way ANOVA, chi-square test.
- **Practical 6 B/C:** covariance, Pearson/Spearman correlation and significance tests.
- **Lab 7 / Practical 7:** regression, train/test split, scaling, encoding, model comparison, MAE/MSE/RMSE/R² and saved model.

Not every practical's original dataset is reused; the methods are applied to the hotel-rating problem where appropriate.
