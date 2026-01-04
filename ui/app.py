import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="FedEx DCA AI Dashboard",
    layout="wide"
)

# -------------------------------------------------
# Custom CSS (Professional Look)
# -------------------------------------------------
st.markdown("""
<style>
.metric-box {
    padding: 20px;
    border-radius: 12px;
    background-color: #f5f7fa;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
.metric-title {
    font-size: 16px;
    color: #555;
}
.metric-value {
    font-size: 26px;
    font-weight: bold;
    color: #111;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Title
# -------------------------------------------------
st.title("📦 FedEx Debt Collection AI Dashboard")
st.caption("Centralized Recovery | SOP | SLA Monitoring | Risk Insights")

# -------------------------------------------------
# Load Data
# -------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/overdue_accounts.csv")

df = load_data()

# -------------------------------------------------
# SLA LOGIC (INLINE – NO OTHER FILE CHANGE)
# -------------------------------------------------
df["Assigned_Date"] = pd.to_datetime("today")

def get_sla_deadline(overdue_days, assigned_date):
    if overdue_days <= 7:
        return assigned_date + timedelta(days=2)
    elif overdue_days <= 15:
        return assigned_date + timedelta(days=3)
    else:
        return assigned_date + timedelta(days=1)

df["SLA_Deadline"] = df.apply(
    lambda row: get_sla_deadline(row["overdue_days"], row["Assigned_Date"]),
    axis=1
)

df["SLA_Breached"] = df["SLA_Deadline"] < pd.Timestamp.now()

# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------
st.subheader("🔑 Key Performance Indicators")

total_amount = df["amount_due"].sum()
overdue_amount = df[df["overdue_days"] > 0]["amount_due"].sum()
recovered_amount = df[df["recovered"] == 1]["amount_due"].sum()
recovery_rate = (recovered_amount / total_amount) * 100
sla_breaches = df["SLA_Breached"].sum()

c1, c2, c3, c4, c5 = st.columns(5)

c1.markdown(f"""
<div class="metric-box">
<div class="metric-title">Total Receivable</div>
<div class="metric-value">₹ {total_amount:,.0f}</div>
</div>
""", unsafe_allow_html=True)

c2.markdown(f"""
<div class="metric-box">
<div class="metric-title">Overdue Amount</div>
<div class="metric-value">₹ {overdue_amount:,.0f}</div>
</div>
""", unsafe_allow_html=True)

c3.markdown(f"""
<div class="metric-box">
<div class="metric-title">Recovered Amount</div>
<div class="metric-value">₹ {recovered_amount:,.0f}</div>
</div>
""", unsafe_allow_html=True)

c4.markdown(f"""
<div class="metric-box">
<div class="metric-title">Recovery Rate</div>
<div class="metric-value">{recovery_rate:.2f}%</div>
</div>
""", unsafe_allow_html=True)

c5.markdown(f"""
<div class="metric-box">
<div class="metric-title">SLA Breaches</div>
<div class="metric-value">{sla_breaches}</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# -------------------------------------------------
# CHARTS SECTION
# -------------------------------------------------
colA, colB = st.columns(2)

with colA:
    st.subheader("📈 Amount Due by Customer Type")
    cust_chart = df.groupby("customer_type")["amount_due"].sum()

    fig1, ax1 = plt.subplots()
    cust_chart.plot(kind="bar", ax=ax1, color="#4F81BD")
    ax1.set_ylabel("Amount Due")
    ax1.set_xlabel("Customer Type")
    st.pyplot(fig1)

with colB:
    st.subheader("⏰ SLA Breach Status")

    sla_counts = df["SLA_Breached"].value_counts()

    labels = ["Breached" if i else "Within SLA" for i in sla_counts.index]
    colors = ["#e74c3c" if i else "#2ecc71" for i in sla_counts.index]

    fig2, ax2 = plt.subplots()
    ax2.pie(
        sla_counts.values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors
    )
    ax2.axis("equal")
    st.pyplot(fig2)

st.divider()

# -------------------------------------------------
# TABLE SECTION
# -------------------------------------------------
st.subheader("📋 Overdue Accounts with SLA Status")

display_cols = [
    "customer_id",
    "customer_type",
    "region",
    "amount_due",
    "overdue_days",
    "SLA_Deadline",
    "SLA_Breached"
]

st.dataframe(df[display_cols], use_container_width=True)

# -------------------------------------------------
# FILTER SECTION
# -------------------------------------------------
st.subheader("🚨 High Risk Accounts Filter")

risk_filter = st.slider(
    "Show customers with overdue days greater than:",
    min_value=0,
    max_value=int(df["overdue_days"].max()),
    value=30
)

filtered_df = df[df["overdue_days"] >= risk_filter]

st.dataframe(
    filtered_df[display_cols],
    use_container_width=True
)
