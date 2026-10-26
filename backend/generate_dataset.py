from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
N = 1200
OUT = Path(__file__).parent / "data" / "hotel_ratings.csv"

def main():
    rng = np.random.default_rng(SEED)
    hotel_type = rng.choice(["Boutique", "Business", "Resort", "Budget", "Luxury"], N, p=[.18,.24,.20,.22,.16])
    city = rng.choice(["Mumbai", "Jaipur", "Goa", "Delhi", "Bengaluru", "Udaipur"], N)
    price = np.clip(rng.normal(6500, 3200, N), 900, 24000).round(0)
    cleanliness = rng.integers(2, 6, N)
    service = rng.integers(2, 6, N)
    location_score = rng.integers(2, 6, N)
    amenities = rng.integers(1, 6, N)
    review_count = rng.integers(8, 2200, N)
    stars = rng.choice([2,3,4,5], N, p=[.08,.25,.42,.25])
    value = np.clip(5 - np.abs(price - (stars*1800+1800))/6500 + rng.normal(0,.8,N), 1, 5)
    noise = rng.normal(0, .38, N)
    rating = (0.25*stars + .23*cleanliness + .20*service + .15*location_score + .10*amenities + .07*value + noise)
    rating = np.clip(rating, 1, 5).round(1)
    df = pd.DataFrame({
        "hotel_type": hotel_type, "city": city, "price_per_night": price,
        "star_category": stars, "cleanliness_score": cleanliness,
        "service_score": service, "location_score": location_score,
        "amenities_score": amenities, "value_score": value.round(1),
        "review_count": review_count, "rating": rating
    })
    # Add a small number of missing values to make the cleaning/imputation practical visible.
    for col in ["price_per_night", "amenities_score", "value_score"]:
        idx = rng.choice(df.index, size=12, replace=False)
        df.loc[idx, col] = np.nan
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"Generated {len(df)} synthetic rows -> {OUT}")

if __name__ == "__main__":
    main()
