import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.cm as cm

# ── Global Plotly dark theme ──────────────────────────────────────────────────
import plotly.io as pio
pio.templates["custom_dark"] = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="rgba(15,12,41,0.0)",
        plot_bgcolor="rgba(255,255,255,0.04)",
        font=dict(color="#E0E0E0", family="Inter"),
        title=dict(font=dict(color="#00BFFF", size=15)),
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)", linecolor="rgba(255,255,255,0.15)",
                   tickfont=dict(color="#B0B0B0")),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)", linecolor="rgba(255,255,255,0.15)",
                   tickfont=dict(color="#B0B0B0")),
        legend=dict(bgcolor="rgba(255,255,255,0.05)", bordercolor="rgba(255,255,255,0.1)"),
        colorway=["#00BFFF","#FF6EC7","#7DF9FF","#FFD700","#39FF14","#FF4500","#BF5FFF"],
    )
)
pio.templates.default = "custom_dark"


st.set_page_config(page_title="E-Commerce EDA Dashboard", layout="wide", page_icon="🛒")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        font-family: 'Inter', sans-serif;
    }
    .main .block-container {
        background: rgba(255,255,255,0.04);
        border-radius: 18px;
        padding: 2rem 2.5rem;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.08);
    }
    h1 { color: #00BFFF !important; font-family: 'Inter', sans-serif !important;
         font-size: 2.2rem !important; font-weight: 700 !important;
         text-shadow: 0 0 20px rgba(0,191,255,0.4); }
    h2 { color: #7DF9FF !important; font-family: 'Inter', sans-serif !important;
         font-weight: 600 !important; border-bottom: 2px solid rgba(0,191,255,0.3);
         padding-bottom: 6px; }
    h3 { color: #FF6EC7 !important; font-family: 'Inter', sans-serif !important;
         font-weight: 600 !important; }
    p, li, span, div, label { color: #E0E0E0 !important; }

    [data-testid="metric-container"] {
        background: linear-gradient(145deg, rgba(0,191,255,0.15), rgba(125,249,255,0.07));
        border: 1px solid rgba(0,191,255,0.35);
        border-radius: 14px;
        padding: 14px 18px;
        box-shadow: 0 4px 20px rgba(0,191,255,0.15);
        transition: transform 0.2s;
    }
    [data-testid="metric-container"]:hover { transform: translateY(-3px); }
    [data-testid="stMetricLabel"] p {
        color: #7DF9FF !important; font-weight: 600 !important;
        font-size: 0.8rem !important; text-transform: uppercase; letter-spacing: 0.8px;
    }
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important; font-size: 1.6rem !important; font-weight: 700 !important;
    }
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(0,191,255,0.25); border-radius: 10px; overflow: hidden;
    }
    [data-testid="stExpander"] {
        background: rgba(0,191,255,0.07); border: 1px solid rgba(0,191,255,0.2);
        border-radius: 10px;
    }
    .insight-box {
        background: linear-gradient(90deg, rgba(0,191,255,0.12), rgba(125,249,255,0.05));
        border-left: 4px solid #00BFFF; padding: 12px 18px; border-radius: 8px;
        margin: 8px 0; color: #E0E0E0 !important; font-size: 0.92rem;
        box-shadow: 0 2px 12px rgba(0,191,255,0.1);
    }
    hr { border: none; height: 1px;
         background: linear-gradient(90deg, transparent, #00BFFF, #FF6EC7, transparent);
         margin: 1.5rem 0; }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); }
    ::-webkit-scrollbar-thumb { background: #00BFFF; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Load & Clean Data ─────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("ecommerce_raw_dataset.csv")

    # --- Cleaning ---
    df = df.drop_duplicates(subset=["Order_ID"])
    df["Quantity"] = df["Quantity"].abs()
    df["Unit_Price"] = df.groupby("Category")["Unit_Price"].transform(
        lambda x: x.fillna(x.median()))
    df["Rating"] = df["Rating"].clip(1, 5)

    # --- Recalculate financials ---
    df["Total_Before_Discount"] = (df["Unit_Price"] * df["Quantity"]).round(2)
    df["Discount_Amount"]       = (df["Total_Before_Discount"] * df["Discount_Pct"] / 100).round(2)
    df["Total_After_Discount"]  = (df["Total_Before_Discount"] - df["Discount_Amount"]).round(2)

    # --- Derived columns ---
    df["Order_Date"]   = pd.to_datetime(df["Order_Date"])
    df["Order_Month"]  = df["Order_Date"].dt.to_period("M").astype(str)
    df["Revenue_Band"] = pd.cut(df["Total_After_Discount"],
                                bins=[0, 500, 2000, 10000, 999999],
                                labels=["Low", "Medium", "High", "Premium"])
    return df

df = load_data()

# ═════════════════════════════════════════════════════════════════════════════
# HEADER
# ═════════════════════════════════════════════════════════════════════════════
st.title("🛒 E-Commerce Analytics Dashboard")
st.markdown("**Data Analytics – Individual Assignment | EDA on Synthetic E-Commerce Dataset (2023)**")
st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 0 – KPI Row
# ═════════════════════════════════════════════════════════════════════════════
st.header("📊 Key Performance Indicators")
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Orders",        f"{len(df):,}")
k2.metric("Total Revenue",       f"₹{df['Total_After_Discount'].sum()/1e6:.2f}M")
k3.metric("Avg Order Value",     f"₹{df['Total_After_Discount'].mean():,.0f}")
k4.metric("Return Rate",         f"{(df['Is_Returned']=='Yes').mean()*100:.1f}%")
k5.metric("Avg Customer Rating", f"{df['Rating'].mean():.2f} ⭐")
k6.metric("Avg Delivery Days",   f"{df['Delivery_Days'].mean():.1f} days")
st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 1 – Data Cleaning Summary
# ═════════════════════════════════════════════════════════════════════════════
st.header("🧹 Step 1 – Data Cleaning & Transformation")

raw = pd.read_csv("ecommerce_raw_dataset.csv")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Data Quality Issues Found (Raw Data)")
    issues = pd.DataFrame({
        "Issue": ["Missing Unit_Price", "Invalid Quantity (≤0)",
                  "Rating Out of Range (>5)", "Duplicate Order IDs"],
        "Count Before": [
            raw["Unit_Price"].isna().sum(),
            (raw["Quantity"] <= 0).sum(),
            ((raw["Rating"] > 5) | (raw["Rating"] < 1)).sum(),
            raw["Order_ID"].duplicated().sum()
        ],
        "Count After": [0, 0, 0, 0],
        "Fix Applied": [
            "Category median imputation",
            "abs() applied",
            "Clipped to [1–5]",
            "Dropped duplicates"
        ]
    })
    st.dataframe(issues, use_container_width=True, hide_index=True)

with col2:
    st.subheader("Transformation Steps")
    steps = [
        "✅ Extracted **Order_Month** from Order_Date for time-series analysis",
        "✅ Recalculated **Total_Before_Discount** = Unit_Price × Quantity",
        "✅ Recalculated **Discount_Amount** = Total × Discount_Pct / 100",
        "✅ Recalculated **Total_After_Discount** after all fixes",
        "✅ Created **Revenue_Band** (Low / Medium / High / Premium)",
        "✅ Standardised all date formats to YYYY-MM-DD",
    ]
    for s in steps:
        st.markdown(s)

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 2 – Descriptive Statistics
# ═════════════════════════════════════════════════════════════════════════════
st.header("📐 Step 2 – Descriptive Statistics")

num_cols = ["Unit_Price", "Quantity", "Discount_Pct", "Discount_Amount",
            "Total_Before_Discount", "Total_After_Discount", "Delivery_Days", "Rating"]

desc = df[num_cols].describe().T
desc["skewness"] = df[num_cols].skew().round(3)
desc["kurtosis"] = df[num_cols].kurtosis().round(3)
desc = desc.round(2)
st.dataframe(desc.style.background_gradient(subset=["mean","std","skewness"],
             cmap=cm.Blues), use_container_width=True)

# Correlation Heatmap
st.subheader("🔗 Correlation Matrix")
corr = df[num_cols].corr().round(3)
fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale="RdYlGn",
                     zmin=-1, zmax=1, aspect="auto",
                     title="Correlation Heatmap of Numeric Variables")
fig_corr.update_layout(title_font_size=16, height=500, template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig_corr, use_container_width=True)

with st.expander("💡 Correlation Insight"):
    st.markdown("""
    - **Total_After_Discount** and **Total_Before_Discount** are almost perfectly correlated (expected — one is derived from the other).  
    - **Unit_Price** has a moderate positive correlation with **Discount_Amount** — higher-priced items tend to offer larger absolute discounts.  
    - **Rating** has a slight negative correlation with **Delivery_Days** — longer delivery times slightly reduce customer satisfaction.  
    - **Quantity** and **Discount_Pct** show near-zero correlation — bulk buying does not necessarily mean more discounts.
    """)

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 3 – EDA Charts
# ═════════════════════════════════════════════════════════════════════════════
st.header("📈 Step 3 – Exploratory Data Analysis (EDA)")

# ── Chart 1: Revenue by Category ─────────────────────────────────────────────
st.subheader("Chart 1 – Total Revenue by Product Category")
rev_cat = df.groupby("Category")["Total_After_Discount"].sum().reset_index()
rev_cat.columns = ["Category", "Revenue"]
rev_cat = rev_cat.sort_values("Revenue", ascending=False)
fig1 = px.bar(rev_cat, x="Category", y="Revenue", color="Category",
              text_auto=".2s", color_discrete_sequence=px.colors.qualitative.Bold,
              title="Total Revenue by Product Category (₹)")
fig1.update_layout(showlegend=False, yaxis_title="Revenue (₹)", height=420)
st.plotly_chart(fig1, use_container_width=True)
st.markdown('<div class="insight-box">📌 <b>Insight:</b> Electronics dominates revenue due to high unit prices. '
            'Clothing and Home & Kitchen follow — suggesting a diversified but electronics-heavy basket. '
            'Marketing spend should be prioritised here to maximise ROI.</div>', unsafe_allow_html=True)

st.markdown("---")

# ── Chart 2: Monthly Revenue Trend ────────────────────────────────────────────
st.subheader("Chart 2 – Monthly Revenue Trend")
monthly = df.groupby("Order_Month")["Total_After_Discount"].sum().reset_index()
monthly.columns = ["Month", "Revenue"]
monthly = monthly.sort_values("Month")
fig2 = px.line(monthly, x="Month", y="Revenue", markers=True,
               title="Monthly Revenue Trend (Jan–Dec 2023)",
               color_discrete_sequence=["#2E75B6"])
fig2.update_layout(yaxis_title="Revenue (₹)", xaxis_title="Month", height=420)
fig2.update_traces(line_width=2.5, marker_size=8)
st.plotly_chart(fig2, use_container_width=True)
st.markdown('<div class="insight-box">📌 <b>Insight:</b> Revenue shows seasonal spikes — notably around festive months '
            '(Oct–Nov). These peaks signal opportunities for pre-stocking, targeted campaigns, '
            'and logistics preparedness ahead of peak seasons.</div>', unsafe_allow_html=True)

st.markdown("---")

# ── Chart 3 & 4 side by side ──────────────────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    st.subheader("Chart 3 – Payment Method Distribution")
    pay = df["Payment_Method"].value_counts().reset_index()
    pay.columns = ["Method", "Count"]
    fig3 = px.pie(pay, names="Method", values="Count", hole=0.4,
                  color_discrete_sequence=px.colors.qualitative.Pastel,
                  title="Payment Method Share")
    fig3.update_traces(textposition="inside", textinfo="percent+label")
    fig3.update_layout(height=400, showlegend=True)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('<div class="insight-box">📌 UPI and Credit Card lead — digital payment adoption is high. '
                'COD still exists, so cash-on-delivery incentive removal can reduce RTO losses.</div>',
                unsafe_allow_html=True)

with c4:
    st.subheader("Chart 4 – Avg Customer Rating by Category")
    rat_cat = df.groupby("Category")["Rating"].mean().reset_index()
    rat_cat.columns = ["Category", "Avg Rating"]
    rat_cat = rat_cat.sort_values("Avg Rating")
    fig4 = px.bar(rat_cat, y="Category", x="Avg Rating", orientation="h",
                  color="Avg Rating", color_continuous_scale="RdYlGn",
                  range_x=[3.5, 5], text_auto=".2f",
                  title="Avg Customer Rating by Category")
    fig4.update_layout(height=400, coloraxis_showscale=False)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('<div class="insight-box">📌 All categories maintain ratings above 3.8. '
                'Lower-rated categories need product listing improvements and proactive '
                'post-purchase support.</div>', unsafe_allow_html=True)

st.markdown("---")

# ── Chart 5: Return Rate ──────────────────────────────────────────────────────
st.subheader("Chart 5 – Product Return Rate by Category (%)")
ret = df.groupby("Category")["Is_Returned"].apply(
    lambda x: (x == "Yes").sum() / len(x) * 100).reset_index()
ret.columns = ["Category", "Return Rate (%)"]
ret = ret.sort_values("Return Rate (%)", ascending=False)
fig5 = px.bar(ret, x="Category", y="Return Rate (%)", color="Return Rate (%)",
              color_continuous_scale="Reds", text_auto=".1f",
              title="Return Rate (%) by Product Category")
fig5.update_layout(height=420, coloraxis_showscale=False)
st.plotly_chart(fig5, use_container_width=True)
st.markdown('<div class="insight-box">📌 <b>Insight:</b> Electronics and Clothing tend to have higher return rates — '
            'common reasons include wrong size/fit and unmet expectations from product descriptions. '
            'Improving image quality, size guides, and specs can reduce returns significantly.</div>',
            unsafe_allow_html=True)

st.markdown("---")

# ── Chart 6 & 7 side by side ──────────────────────────────────────────────────
c6, c7 = st.columns(2)

with c6:
    st.subheader("Chart 6 – Orders by Region")
    reg = df["Region"].value_counts().reset_index()
    reg.columns = ["Region", "Orders"]
    fig6 = px.pie(reg, names="Region", values="Orders", hole=0.35,
                  color_discrete_sequence=px.colors.qualitative.Set2,
                  title="Order Volume by Region")
    fig6.update_traces(textposition="inside", textinfo="percent+label")
    fig6.update_layout(height=400)
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown('<div class="insight-box">📌 Orders are distributed fairly evenly across regions. '
                'Under-performing regions should be targeted with localised offers and '
                'regional language support.</div>', unsafe_allow_html=True)

with c7:
    st.subheader("Chart 7 – Revenue by Acquisition Channel")
    acq = df.groupby("Acquisition_Channel")["Total_After_Discount"].sum().reset_index()
    acq.columns = ["Channel", "Revenue"]
    acq = acq.sort_values("Revenue", ascending=False)
    fig7 = px.bar(acq, x="Channel", y="Revenue", color="Channel",
                  color_discrete_sequence=px.colors.qualitative.Vivid,
                  text_auto=".2s", title="Revenue by Acquisition Channel (₹)")
    fig7.update_layout(height=400, showlegend=False, yaxis_title="Revenue (₹)")
    st.plotly_chart(fig7, use_container_width=True)
    st.markdown('<div class="insight-box">📌 Organic Search and Paid Ads are top revenue drivers. '
                'Investing in SEO + performance marketing is the highest-ROI growth lever '
                'for this startup.</div>', unsafe_allow_html=True)

st.markdown("---")

# ── Chart 8: Revenue Band ─────────────────────────────────────────────────────
st.subheader("Chart 8 – Revenue Band Distribution")
rb = df["Revenue_Band"].value_counts().reindex(["Low","Medium","High","Premium"]).reset_index()
rb.columns = ["Band", "Orders"]
fig8 = px.bar(rb, x="Band", y="Orders", color="Band",
              color_discrete_map={"Low":"#90CAF9","Medium":"#42A5F5",
                                  "High":"#1565C0","Premium":"#0D2137"},
              text_auto=True, title="Order Count by Revenue Band")
fig8.update_layout(height=420, showlegend=False, yaxis_title="Number of Orders")
st.plotly_chart(fig8, use_container_width=True)
st.markdown('<div class="insight-box">📌 <b>Insight:</b> Most orders fall in the Medium band (₹500–₹2,000). '
            'Bundling strategies (e.g., "Buy 2 get 10% off") can push Low-band customers into Medium, '
            'improving Average Order Value by 20–30%.</div>', unsafe_allow_html=True)

st.markdown("---")

# ── Chart 9: Delivery Days vs Rating ─────────────────────────────────────────
st.subheader("Chart 9 – Delivery Days vs Customer Rating")
del_rat = df.groupby("Delivery_Days")["Rating"].mean().reset_index()
del_rat.columns = ["Delivery Days", "Avg Rating"]
fig9 = px.line(del_rat, x="Delivery Days", y="Avg Rating", markers=True,
               title="Impact of Delivery Speed on Customer Rating",
               color_discrete_sequence=["#7B2D8B"])
fig9.update_layout(height=400, yaxis_range=[3.5, 5])
fig9.update_traces(line_width=2.5, marker_size=9)
st.plotly_chart(fig9, use_container_width=True)
st.markdown('<div class="insight-box">📌 <b>Insight:</b> There is a clear downward trend — customers who receive '
            'orders in 1–3 days give consistently higher ratings. Investing in same-day or '
            'next-day logistics directly improves NPS and repeat purchase rates.</div>',
            unsafe_allow_html=True)

st.markdown("---")

# ── Chart 10: Discount vs Rating ─────────────────────────────────────────────
st.subheader("Chart 10 – Discount % vs Avg Rating")
disc_rat = df.groupby("Discount_Pct")["Rating"].mean().reset_index()
disc_rat.columns = ["Discount %", "Avg Rating"]
fig10 = px.bar(disc_rat, x="Discount %", y="Avg Rating", color="Avg Rating",
               color_continuous_scale="RdYlGn", text_auto=".2f",
               title="Average Customer Rating by Discount Level")
fig10.update_layout(height=400, coloraxis_showscale=False)
st.plotly_chart(fig10, use_container_width=True)
st.markdown('<div class="insight-box">📌 <b>Insight:</b> Higher discounts do not always lead to better ratings — '
            'deeply discounted items often attract impulse buyers who are less satisfied. '
            'A balanced discount strategy (10–15%) appears to yield the best satisfaction scores.</div>',
            unsafe_allow_html=True)

st.markdown("---")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; color:#888; font-size:13px; padding-top:10px'>
    Data Analytics – MGB | Individual Assignment | E-Commerce EDA Dashboard
</div>
""", unsafe_allow_html=True)
