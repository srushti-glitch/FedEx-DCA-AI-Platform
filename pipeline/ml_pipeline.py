import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# -------------------------------------------------
# 1️⃣ Load Dataset
# -------------------------------------------------
df = pd.read_csv("data/overdue_accounts.csv")

# -------------------------------------------------
# 2️⃣ Features & Target
# -------------------------------------------------
X = df.drop(columns=["customer_id", "recovered"])
y = df["recovered"]

# -------------------------------------------------
# 3️⃣ Column Types
# -------------------------------------------------
categorical_features = ["customer_type", "region"]
numerical_features = [
    "past_defaults",
    "overdue_days",
    "amount_due"
]

# -------------------------------------------------
# 4️⃣ Preprocessing
# -------------------------------------------------
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", StandardScaler(), numerical_features)
    ]
)

# -------------------------------------------------
# 5️⃣ ML Pipeline
# -------------------------------------------------
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", RandomForestClassifier(
            n_estimators=150,
            max_depth=8,
            random_state=42
        ))
    ]
)

# -------------------------------------------------
# 6️⃣ Train-Test Split
# -------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -------------------------------------------------
# 7️⃣ Train Model
# -------------------------------------------------
pipeline.fit(X_train, y_train)

# -------------------------------------------------
# 8️⃣ Evaluation
# -------------------------------------------------
y_pred = pipeline.predict(X_test)

print("\n📊 MODEL EVALUATION REPORT\n")
print(classification_report(y_test, y_pred))

# -------------------------------------------------
# 9️⃣ Save Model
# -------------------------------------------------
joblib.dump(pipeline, "models/recovery_model.pkl")

print("\n✅ Model trained & saved successfully at models/recovery_model.pkl")
