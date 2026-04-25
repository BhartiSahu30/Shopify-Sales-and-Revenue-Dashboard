import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Shopify Dashboard", layout="wide")

# ---------------- CINEMATIC UI ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}
.main {
    background: transparent;
}
h1 {
    color: #00E5FF;
    text-align: center;
    font-size: 42px;
}
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.1);
    border-radius: 15px;
    padding: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("product.csv")
df.columns = df.columns.str.strip()

# ---------------- SIDEBAR ----------------
st.sidebar.header("🎛️ Filters")

category = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

company = st.sidebar.multiselect(
    "Company",
    df["Company"].unique(),
    default=df["Company"].unique()
)

revenue_filter = st.sidebar.slider(
    "Minimum Revenue ($)",
    int(df["Estimated_Revenue_in_2025_USD"].min()),
    int(df["Estimated_Revenue_in_2025_USD"].max()),
    int(df["Estimated_Revenue_in_2025_USD"].min())
)

top_n = st.sidebar.slider("Top Products", 5, 20, 10)

# ---------------- FILTER ----------------
filtered_df = df[
    (df["Category"].isin(category)) &
    (df["Company"].isin(company)) &
    (df["Estimated_Revenue_in_2025_USD"] >= revenue_filter)
]

# ---------------- KPIs ----------------
total_revenue = filtered_df["Estimated_Revenue_in_2025_USD"].sum()
total_units = filtered_df["Estimated_Total_Units_Sold_in_2025"].sum()
avg_trend = filtered_df["Trend_Score"].mean()

top_row = filtered_df.sort_values(
    "Estimated_Revenue_in_2025_USD", ascending=False
).head(1)

top_product = (
    top_row["Product_Name"].values[0] + " (" + top_row["Company"].values[0] + ")"
    if not top_row.empty else "N/A"
)

# ---------------- TITLE ----------------
st.title("🛒 Shopify Sales Intelligence Dashboard")

# ---------------- KPI ----------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Revenue", f"${total_revenue:,.0f}")
col2.metric("📦 Units Sold", f"{total_units:,}")
col3.metric("🔥 Trend Score", f"{avg_trend:.1f}")
col4.metric("🏆 Top Product", top_product)

# ---------------- TOP PRODUCTS FIX ----------------
st.subheader("🏆 Top Products by Revenue")

top_products = filtered_df.sort_values(
    "Estimated_Revenue_in_2025_USD", ascending=False
).head(top_n)

fig1 = px.bar(
    top_products,
    x="Estimated_Revenue_in_2025_USD",
    y="Product_Name",
    orientation="h",
    color="Estimated_Revenue_in_2025_USD",
    text="Company"   # shows company name
)

# 🔥 FIX LABEL CUT ISSUE
fig1.update_layout(
    yaxis=dict(automargin=True),
    margin=dict(l=200)  # increase left space
)

st.plotly_chart(fig1, width="stretch")

# ---------------- CATEGORY ----------------
st.subheader("📊 Category Distribution")

fig2 = px.pie(
    filtered_df,
    values="Estimated_Revenue_in_2025_USD",
    names="Category",
    hole=0.4
)

st.plotly_chart(fig2, width="stretch")

# ---------------- TREND ----------------
st.subheader("🔥 Trend Analysis")

fig3 = px.scatter(
    filtered_df,
    x="Estimated_Total_Units_Sold_in_2025",
    y="Estimated_Revenue_in_2025_USD",
    size="Trend_Score",
    color="Company",
    hover_name="Product_Name"
)

st.plotly_chart(fig3, width="stretch")

# ---------------- TABLE ----------------
st.subheader("📋 Product Data")

st.dataframe(filtered_df, use_container_width=True)

# ---------------- INSIGHTS ----------------
st.subheader("💡 Insights")

st.write(f"• Top product: **{top_product}**")
st.write("• High trend score products are future growth drivers")
st.write("• Electronics category dominates revenue contribution")