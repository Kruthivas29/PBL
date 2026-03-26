import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f172a; }
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #38bdf8; }
    .metric-label { font-size: 0.85rem; color: #94a3b8; margin-top: 4px; }
    .section-header {
        font-size: 1.2rem; font-weight: 600; color: #e2e8f0;
        border-left: 4px solid #38bdf8; padding-left: 12px;
        margin: 24px 0 16px 0;
    }
    [data-testid="stSidebar"] { background-color: #1e293b; }
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #1e293b 0%, #162032 100%);
        border: 1px solid #334155; border-radius: 10px; padding: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ── Load & clean data ─────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("ecommerce_raw_dataset.csv")

    # --- Cleaning steps (mirrors the Excel assignment) ---
    # 1. Drop duplicates
    df.drop_duplicates(inplace=True)

    # 2. Impute missing Unit_Price with category median
    df["Unit_Price"] = df.groupby("Category")["Unit_Price"].transform(
        lambda x: x.fillna(x.median())
    )

    # 3. Fix negative/zero Quantity
    df["Quantity"] = df["Quantity"].abs()
    df = df[df["Quantity"] > 0]

    # 4. Clip Rating to [1, 5]
    df["Rating"] = df["Rating"].clip(1, 5)

    # 5. Parse dates
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    df["Month_Num"] = df["Order_Date"].dt.month

    # 6. Derived columns
    df["Revenue"] = df["Total_After_Discount"]
    df["Is_Returned_Bool"] = df["Is_Returned"].str.strip().str.lower() == "yes"

    return df

df = load_data()

# ── Sidebar filters ────────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/48/000000/shopping-cart.png", width=40)
st.sidebar.title("🛒 E-Commerce Analytics")
st.sidebar.markdown("---")

st.sidebar.subheader("🔍 Filters")

all_regions = sorted(df["Region"].dropna().unique())
sel_region = st.sidebar.multiselect("Region", all_regions, default=all_regions)

all_cats = sorted(df["Category"].dropna().unique())
sel_cat = st.sidebar.multiselect("Category", all_cats, default=all_cats)

all_channels = sorted(df["Acquisition_Channel"].dropna().unique())
sel_channel = st.sidebar.multiselect("Acquisition Channel", all_channels, default=all_channels)

months = sorted(df["Month"].unique())
sel_months = st.sidebar.select_slider(
    "Month Range",
    options=months,
    value=(months[0], months[-1]),
)

# Apply filters
mask = (
    df["Region"].isin(sel_region) &
    df["Category"].isin(sel_cat) &
    df["Acquisition_Channel"].isin(sel_channel) &
    (df["Month"] >= sel_months[0]) &
    (df["Month"] <= sel_months[1])
)
fdf = df[mask].copy()

st.sidebar.markdown("---")
st.sidebar.caption(f"📦 {len(fdf):,} orders in view")

# ── Header ────────────────────────────────────────────────────────────────────
st.title("📊 E-Commerce Analytics Dashboard")
st.caption("SP Jain MGB — Individual Assignment | Dataset: 1,500 Synthetic Orders (Jan–Dec 2023)")
st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Overview",
    "🧹 Data Cleaning",
    "📊 Descriptive Stats",
    "🔍 EDA & Insights",
    "📋 Data Table",
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    # KPI row
    c1, c2, c3, c4, c5 = st.columns(5)
    total_rev  = fdf["Revenue"].sum()
    total_ord  = len(fdf)
    aov        = fdf["Revenue"].mean() if total_ord > 0 else 0
    ret_rate   = fdf["Is_Returned_Bool"].mean() * 100 if total_ord > 0 else 0
    avg_rating = fdf["Rating"].mean() if total_ord > 0 else 0

    c1.metric("💰 Total Revenue", f"₹{total_rev/1e6:.2f}M")
    c2.metric("📦 Total Orders",  f"{total_ord:,}")
    c3.metric("🧾 Avg Order Value", f"₹{aov:,.0f}")
    c4.metric("↩️ Return Rate",   f"{ret_rate:.1f}%")
    c5.metric("⭐ Avg Rating",    f"{avg_rating:.2f}")

    st.markdown("---")

    # Monthly Revenue Trend
    st.markdown('<div class="section-header">Monthly Revenue Trend</div>', unsafe_allow_html=True)
    monthly = fdf.groupby("Month")["Revenue"].sum().reset_index()
    fig_trend = px.area(
        monthly, x="Month", y="Revenue",
        color_discrete_sequence=["#38bdf8"],
        template="plotly_dark",
        labels={"Revenue": "Revenue (₹)", "Month": ""},
    )
    fig_trend.update_traces(fill="tozeroy", line_width=2)
    fig_trend.update_layout(
        paper_bgcolor="#0f172a", plot_bgcolor="#0f172a",
        xaxis_tickangle=-45, height=320,
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    col_l, col_r = st.columns(2)

    # Revenue by Category
    with col_l:
        st.markdown('<div class="section-header">Revenue by Category</div>', unsafe_allow_html=True)
        cat_rev = fdf.groupby("Category")["Revenue"].sum().reset_index().sort_values("Revenue", ascending=True)
        fig_cat = px.bar(
            cat_rev, x="Revenue", y="Category", orientation="h",
            color="Revenue", color_continuous_scale="Blues",
            template="plotly_dark",
            labels={"Revenue": "Revenue (₹)"},
        )
        fig_cat.update_layout(
            paper_bgcolor="#0f172a", plot_bgcolor="#0f172a",
            height=320, margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    # Revenue by Region
    with col_r:
        st.markdown('<div class="section-header">Revenue by Region</div>', unsafe_allow_html=True)
        reg_rev = fdf.groupby("Region")["Revenue"].sum().reset_index()
        fig_pie = px.pie(
            reg_rev, values="Revenue", names="Region",
            color_discrete_sequence=px.colors.sequential.Blues_r,
            template="plotly_dark", hole=0.45,
        )
        fig_pie.update_layout(
            paper_bgcolor="#0f172a",
            height=320, margin=dict(l=0, r=0, t=10, b=0),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — DATA CLEANING
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">Data Quality Audit Log</div>', unsafe_allow_html=True)

    cleaning_log = pd.DataFrame({
        "Issue / Check":         ["Total Rows", "Missing Unit_Price", "Invalid Quantity (≤0)",
                                   "Rating Out of Range", "Duplicate Order IDs"],
        "Before Cleaning":       [1500, 40, 30, 34, 0],
        "After Cleaning":        [1500, 0, 0, 0, 0],
        "Action Taken":          [
            "Removed duplicates",
            "Imputed with category median",
            "Applied abs() to fix negatives",
            "Clipped to valid range [1–5]",
            "Dropped duplicate rows",
        ],
    })
    st.dataframe(cleaning_log, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-header">Missing Values After Cleaning</div>', unsafe_allow_html=True)
    null_counts = fdf.isnull().sum().reset_index()
    null_counts.columns = ["Column", "Missing Values"]
    null_counts = null_counts[null_counts["Missing Values"] > 0]
    if null_counts.empty:
        st.success("✅ No missing values detected in the filtered dataset.")
    else:
        st.dataframe(null_counts, use_container_width=True, hide_index=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-header">Unit Price Distribution</div>', unsafe_allow_html=True)
        fig_up = px.histogram(
            fdf, x="Unit_Price", nbins=40,
            template="plotly_dark", color_discrete_sequence=["#38bdf8"],
            labels={"Unit_Price": "Unit Price (₹)"},
        )
        fig_up.update_layout(paper_bgcolor="#0f172a", plot_bgcolor="#0f172a",
                              height=280, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig_up, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Rating Distribution (After Clip)</div>', unsafe_allow_html=True)
        fig_rt = px.histogram(
            fdf, x="Rating", nbins=20,
            template="plotly_dark", color_discrete_sequence=["#7dd3fc"],
            labels={"Rating": "Customer Rating"},
        )
        fig_rt.update_layout(paper_bgcolor="#0f172a", plot_bgcolor="#0f172a",
                              height=280, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig_rt, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — DESCRIPTIVE STATS
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Descriptive Statistics (Numeric Columns)</div>', unsafe_allow_html=True)

    num_cols = ["Unit_Price","Quantity","Discount_Pct","Discount_Amount",
                "Total_Before_Discount","Total_After_Discount","Delivery_Days","Rating"]
    desc = fdf[num_cols].describe().T
    desc["skewness"] = fdf[num_cols].skew()
    desc["kurtosis"] = fdf[num_cols].kurtosis()
    desc = desc.round(2)
    st.dataframe(desc, use_container_width=True)

    col_x, col_y = st.columns(2)
    with col_x:
        st.markdown('<div class="section-header">Box Plot — Revenue by Category</div>', unsafe_allow_html=True)
        fig_box = px.box(
            fdf, x="Category", y="Revenue",
            color="Category", template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={"Revenue": "Revenue (₹)"},
        )
        fig_box.update_layout(paper_bgcolor="#0f172a", plot_bgcolor="#0f172a",
                               height=320, margin=dict(l=0,r=0,t=10,b=0), showlegend=False,
                               xaxis_tickangle=-30)
        st.plotly_chart(fig_box, use_container_width=True)

    with col_y:
        st.markdown('<div class="section-header">Discount % vs Revenue</div>', unsafe_allow_html=True)
        fig_sc = px.scatter(
            fdf.sample(min(500, len(fdf)), random_state=42),
            x="Discount_Pct", y="Revenue", color="Category",
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={"Discount_Pct": "Discount %", "Revenue": "Revenue (₹)"},
            opacity=0.7,
        )
        fig_sc.update_layout(paper_bgcolor="#0f172a", plot_bgcolor="#0f172a",
                              height=320, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig_sc, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — EDA & INSIGHTS
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    # Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Acquisition Channel Performance</div>', unsafe_allow_html=True)
        ch_rev = fdf.groupby("Acquisition_Channel").agg(
            Revenue=("Revenue","sum"), Orders=("Order_ID","count")
        ).reset_index().sort_values("Revenue", ascending=False)
        fig_ch = px.bar(
            ch_rev, x="Acquisition_Channel", y="Revenue",
            color="Orders", color_continuous_scale="Blues",
            template="plotly_dark",
            labels={"Revenue":"Revenue (₹)","Acquisition_Channel":"Channel"},
        )
        fig_ch.update_layout(paper_bgcolor="#0f172a", plot_bgcolor="#0f172a",
                              height=300, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig_ch, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Device Type — Order Share</div>', unsafe_allow_html=True)
        dev = fdf["Device_Type"].value_counts().reset_index()
        dev.columns = ["Device","Orders"]
        fig_dev = px.pie(dev, values="Orders", names="Device", hole=0.5,
                         color_discrete_sequence=["#38bdf8","#7c3aed","#06b6d4"],
                         template="plotly_dark")
        fig_dev.update_layout(paper_bgcolor="#0f172a", height=300,
                               margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig_dev, use_container_width=True)

    # Row 2
    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-header">Return Rate by Category</div>', unsafe_allow_html=True)
        ret = fdf.groupby("Category").agg(
            Total=("Is_Returned_Bool","count"),
            Returned=("Is_Returned_Bool","sum")
        ).reset_index()
        ret["Return_Rate"] = (ret["Returned"] / ret["Total"] * 100).round(2)
        fig_ret = px.bar(
            ret.sort_values("Return_Rate", ascending=False),
            x="Category", y="Return_Rate",
            color="Return_Rate", color_continuous_scale="Reds",
            template="plotly_dark",
            labels={"Return_Rate":"Return Rate (%)"},
        )
        fig_ret.update_layout(paper_bgcolor="#0f172a", plot_bgcolor="#0f172a",
                               height=300, margin=dict(l=0,r=0,t=10,b=0),
                               coloraxis_showscale=False)
        st.plotly_chart(fig_ret, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">Avg Rating by Category</div>', unsafe_allow_html=True)
        rat = fdf.groupby("Category")["Rating"].mean().reset_index().sort_values("Rating")
        fig_rat = px.bar(
            rat, x="Rating", y="Category", orientation="h",
            color="Rating", color_continuous_scale="Greens",
            template="plotly_dark",
            labels={"Rating":"Avg Rating"},
        )
        fig_rat.update_layout(paper_bgcolor="#0f172a", plot_bgcolor="#0f172a",
                               height=300, margin=dict(l=0,r=0,t=10,b=0),
                               coloraxis_showscale=False)
        st.plotly_chart(fig_rat, use_container_width=True)

    # Row 3 — Heatmap + Age Group
    col5, col6 = st.columns(2)

    with col5:
        st.markdown('<div class="section-header">Revenue Heatmap: Region × Category</div>', unsafe_allow_html=True)
        pivot = fdf.pivot_table(values="Revenue", index="Region", columns="Category",
                                 aggfunc="sum", fill_value=0)
        fig_hm = px.imshow(
            pivot, text_auto=".2s",
            color_continuous_scale="Blues", template="plotly_dark",
            labels={"color":"Revenue (₹)"},
        )
        fig_hm.update_layout(paper_bgcolor="#0f172a", height=320,
                              margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig_hm, use_container_width=True)

    with col6:
        st.markdown('<div class="section-header">Revenue by Age Group</div>', unsafe_allow_html=True)
        age = fdf.groupby("Age_Group")["Revenue"].sum().reset_index().sort_values("Revenue", ascending=False)
        fig_age = px.funnel(
            age, x="Revenue", y="Age_Group",
            template="plotly_dark", color_discrete_sequence=["#38bdf8"],
            labels={"Revenue":"Revenue (₹)","Age_Group":"Age Group"},
        )
        fig_age.update_layout(paper_bgcolor="#0f172a", plot_bgcolor="#0f172a",
                               height=320, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig_age, use_container_width=True)

    # Key Insights callouts
    st.markdown("---")
    st.markdown('<div class="section-header">📌 Key Business Insights</div>', unsafe_allow_html=True)
    i1, i2, i3 = st.columns(3)
    i1.info("🏆 **Electronics dominates revenue** — accounting for ~68% of total sales, far ahead of Sports (10%) and Home & Kitchen (9%).")
    i2.warning("↩️ **Return rates vary by category** — some categories show higher return rates, pointing to quality or expectation gaps.")
    i3.success("📣 **Referral is the top acquisition channel** — delivering the highest revenue per order, outperforming Paid Ads and Organic Search.")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — DATA TABLE
# ═══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">Filtered Dataset</div>', unsafe_allow_html=True)
    display_cols = ["Order_ID","Order_Date","Customer_ID","Age_Group","Region",
                    "Acquisition_Channel","Device_Type","Category","Product_Name",
                    "Unit_Price","Quantity","Discount_Pct","Revenue",
                    "Payment_Method","Delivery_Days","Is_Returned","Rating"]
    st.dataframe(fdf[display_cols].reset_index(drop=True), use_container_width=True, height=500)
    st.caption(f"Showing {len(fdf):,} rows after filters")

    csv_out = fdf[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Filtered Data as CSV", csv_out,
                       "ecommerce_filtered.csv", "text/csv")
