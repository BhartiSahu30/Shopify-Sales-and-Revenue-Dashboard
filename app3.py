import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Shopify Sales Dashboard", layout="wide")

# ---------------- CUSTOM UI ----------------
st.markdown("""
<style>
.main {
    background-color: #F5F7FA;
}
h1, h2, h3 {
    color: #1E88E5;
}
div[data-testid="metric-container"] {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("shopify_trending_products_2025.csv")
df.columns = df.columns.str.strip()

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔍 Filters")

# Category Filter
category = st.sidebar.multiselect(
    "Select Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

# Revenue Filter
revenue_filter = st.sidebar.slider(
    "Minimum Revenue ($)",
    int(df["Estimated_Revenue_in_2025_USD"].min()),
    int(df["Estimated_Revenue_in_2025_USD"].max()),
    int(df["Estimated_Revenue_in_2025_USD"].min())
)

# Top N Filter
top_n = st.sidebar.slider("Top Products to Display", 5, 20, 10)

# ---------------- FILTER DATA ----------------
filtered_df = df[
    (df["Category"].isin(category)) &
    (df["Estimated_Revenue_in_2025_USD"] >= revenue_filter)
]

# ---------------- KPIs ----------------
total_revenue = filtered_df["Estimated_Revenue_in_2025_USD"].sum()
total_units = filtered_df["Estimated_Total_Units_Sold_in_2025"].sum()
avg_trend = filtered_df["Trend_Score"].mean()

top_product = filtered_df.sort_values(
    "Estimated_Revenue_in_2025_USD", ascending=False
).iloc[0]["Product_Name"] if not filtered_df.empty else "N/A"

# ---------------- TITLE ----------------
st.title("🛒 Shopify Sales & Revenue Dashboard (2025)")

# ---------------- KPI CARDS ----------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
col2.metric("📦 Units Sold", f"{total_units:,}")
col3.metric("🔥 Avg Trend Score", f"{avg_trend:.1f}" if not pd.isna(avg_trend) else "0")
col4.metric("🏆 Top Product", top_product)

# ---------------- CHART 1: TOP PRODUCTS ----------------
st.subheader("🏆 Top Revenue Generating Products")

top_products = filtered_df.sort_values(
    "Estimated_Revenue_in_2025_USD", ascending=False
).head(top_n)

fig1 = px.bar(
    top_products,
    x="Estimated_Revenue_in_2025_USD",
    y="Product_Name",
    orientation="h",
    color="Estimated_Revenue_in_2025_USD",
    title="Top Products by Revenue"
)

st.plotly_chart(fig1, width="stretch")

# ---------------- CHART 2: CATEGORY DISTRIBUTION ----------------
st.subheader("📊 Revenue Distribution by Category")

category_data = filtered_df.groupby("Category")[
    "Estimated_Revenue_in_2025_USD"
].sum().reset_index()

fig2 = px.pie(
    category_data,
    values="Estimated_Revenue_in_2025_USD",
    names="Category",
    hole=0.4
)

st.plotly_chart(fig2, width="stretch")

# ---------------- CHART 3: TREND ANALYSIS ----------------
st.subheader("🔥 Trend vs Revenue Analysis")

fig3 = px.scatter(
    filtered_df,
    x="Estimated_Total_Units_Sold_in_2025",
    y="Estimated_Revenue_in_2025_USD",
    size="Trend_Score",
    color="Category",
    hover_name="Product_Name",
    title="Units Sold vs Revenue (Bubble = Trend Score)"
)

st.plotly_chart(fig3, width="stretch")

# ---------------- REGION / CATEGORY COMPARISON ----------------
st.subheader("📈 Category Performance")

bar_data = filtered_df.groupby("Category")[
    "Estimated_Revenue_in_2025_USD"
].sum().reset_index()

fig4 = px.bar(
    bar_data,
    x="Category",
    y="Estimated_Revenue_in_2025_USD",
    color="Category"
)

st.plotly_chart(fig4, width="stretch")

# ---------------- DATA TABLE ----------------
st.subheader("📋 Detailed Product Data")

st.dataframe(filtered_df, use_container_width=True)

# ---------------- BUSINESS INSIGHTS ----------------
st.subheader("💡 Key Business Insights")

if not filtered_df.empty:
    st.write(f"• The top-performing product is **{top_product}**, contributing significantly to revenue.")
    st.write(f"• Total revenue generated is **${total_revenue:,.0f}**.")
    st.write(f"• Average trend score is **{avg_trend:.1f}**, indicating strong market demand.")
    st.write("• Products with high trend score and high revenue represent the best growth opportunities.")
else:
    st.warning("No data available for selected filters.")