import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# Load data
df = pd.read_csv("body_fat_data.csv")

# Encode gender
encoder = LabelEncoder()
df["gender"] = encoder.fit_transform(df["gender"])

# Features & target
X = df[["sum_skinfold_mm", "age", "gender", "method"]]
y = df["body_fat_percent"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluation
pred = model.predict(X_test)
print("MAE:", round(mean_absolute_error(y_test, pred), 2))
print("R2 :", round(r2_score(y_test, pred), 3))

# Save model
joblib.dump(model, "body_fat_model.pkl")
joblib.dump(encoder, "gender_encoder.pkl")

print("✅ PKL files generated successfully")
