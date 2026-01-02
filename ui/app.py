import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="FedEx DCA AI Platform", layout="wide")
st.title("🚚 FedEx DCA AI Recovery Platform")

# -------------------------------------------------
# LOAD MODEL
# -------------------------------------------------
model = joblib.load("models/recovery_model.pkl")

# -------------------------------------------------
# FILE UPLOAD
# -------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload Overdue Accounts CSV",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Uploaded Data")
    st.dataframe(df, use_container_width=True)

    # -------------------------------------------------
    # FEATURES (MUST MATCH TRAINING)
    # -------------------------------------------------
    feature_cols = [
        "customer_type",
        "region",
        "past_defaults",
        "overdue_days",
        "amount_due"
    ]

    X = df[feature_cols]

    # -------------------------------------------------
    # ML PREDICTION
    # -------------------------------------------------
    df["recovery_probability"] = model.predict_proba(X)[:, 1]

    # -------------------------------------------------
    # SOP RULES
    # -------------------------------------------------
    def get_next_action(days):
        if days <= 7:
            return "Call Customer"
        elif days <= 15:
            return "Send Reminder"
        else:
            return "Escalate to Legal"

    df["Next_Action"] = df["overdue_days"].apply(get_next_action)

    # -------------------------------------------------
    # SLA RULES
    # -------------------------------------------------
    def get_sla_deadline(days, assigned_date):
        if days <= 7:
            return assigned_date + pd.Timedelta(days=2)
        elif days <= 15:
            return assigned_date + pd.Timedelta(days=3)
        else:
            return assigned_date + pd.Timedelta(days=5)

    def check_sla_breach(deadline):
        return pd.Timestamp("today") > deadline

    df["Assigned_Date"] = pd.to_datetime("today")

    df["SLA_Deadline"] = df.apply(
        lambda row: get_sla_deadline(row["overdue_days"], row["Assigned_Date"]),
        axis=1
    )

    df["SLA_Breached"] = df["SLA_Deadline"].apply(check_sla_breach)

    # -------------------------------------------------
    # PRIORITY SCORE
    # -------------------------------------------------
    df["priority_score"] = (
        0.4 * df["overdue_days"]
        + 0.3 * df["amount_due"] / 1000
        + 0.3 * (1 - df["recovery_probability"])
    )

    # -------------------------------------------------
    # FINAL TABLE
    # -------------------------------------------------
    st.subheader("🧠 AI Prioritized Recovery Cases")

    st.dataframe(
        df.sort_values("priority_score", ascending=False),
        use_container_width=True
    )

    # -------------------------------------------------
    # DASHBOARD
    # -------------------------------------------------
    st.subheader("📊 Recovery Insights")

    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots()
        ax1.hist(df["recovery_probability"], bins=10)
        ax1.set_title("Recovery Probability Distribution")
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = plt.subplots()
        ax2.hist(df["overdue_days"], bins=10)
        ax2.set_title("Overdue Days Distribution")
        st.pyplot(fig2)

    st.success("✅ SOP, SLA & AI logic successfully applied")
