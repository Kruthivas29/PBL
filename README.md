---
title: E-Commerce EDA Dashboard
emoji: 🛒
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.32.0
app_file: app.py
pinned: false
license: mit
---

# 🛒 E-Commerce EDA Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

> **MBA Data Analytics · Individual Assignment**  
> Step 1: Data Cleaning & Transformation | Step 2: Descriptive Statistics | Step 3: EDA Charts

---

## 🚀 Live Demo

| Platform | Link |
|----------|------|
| **Streamlit Cloud** | [Deploy instructions below](#deploy-on-streamlit-cloud) |
| **HuggingFace Spaces** | [Deploy instructions below](#deploy-on-huggingface-spaces) |

---

## 📋 Project Overview

This dashboard performs end-to-end Exploratory Data Analysis on a synthetic **E-Commerce** dataset built to analyse customer purchase behaviour, product performance, and revenue patterns across an online retail platform.

> **Core Hypothesis:** Understanding product category performance, return rates, and customer acquisition channels reveals actionable levers to improve revenue and reduce churn.

### Dataset
- **Synthetic dataset** generated with a fixed seed for reproducibility
- **Multiple variables**: product categories, payment methods, customer ratings, revenue, discounts, delivery days, regions, and acquisition channels
- **Derived features**: revenue bands, discount tiers, return rate flags

---

## 📊 Dashboard Structure

| Step | Content |
|------|---------|
| **Step 1 – Data Cleaning** | Missing value detection, outlier handling, transformation log, feature engineering |
| **Step 2 – Descriptive Stats** | Full summary statistics table with skewness, kurtosis, and IQR |
| **Step 3 – EDA Charts** | 10 analytical charts with business insights |
| **Correlation Matrix** | Pearson correlation heatmap across key numerical variables |

### Charts Included
1. Total Revenue by Product Category (Bar)
2. Monthly Revenue Trend (Line)
3. Payment Method Distribution (Pie)
4. Avg Customer Rating by Category (Bar)
5. Product Return Rate by Category % (Bar)
6. Orders by Region (Bar)
7. Revenue by Acquisition Channel (Bar)
8. Revenue Band Distribution (Bar)
9. Delivery Days vs Customer Rating (Scatter)
10. Discount % vs Avg Rating (Scatter)
+ Pearson Correlation Heatmap

---

## 🛠️ Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ecommerce-eda.git
cd ecommerce-eda

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## 🌐 Deploy on Streamlit Cloud

> Free deployment in 3 steps — no credit card needed

**Step 1:** Push this repo to GitHub (public repo)
```bash
git init
git add .
git commit -m "Initial commit: E-Commerce EDA Dashboard"
git remote add origin https://github.com/YOUR_USERNAME/ecommerce-eda.git
git push -u origin main
```

**Step 2:** Go to [share.streamlit.io](https://share.streamlit.io)
- Click **"New app"**
- Select your GitHub repo: `YOUR_USERNAME/ecommerce-eda`
- Branch: `main`
- Main file path: `app.py`
- Click **"Deploy"**

**Step 3:** Your app is live at:  
`https://YOUR_USERNAME-ecommerce-eda-app-XXXXX.streamlit.app`

---

## 🤗 Deploy on HuggingFace Spaces

> The `README.md` front-matter is already configured for HuggingFace Spaces

**Step 1:** Create a new Space at [huggingface.co/spaces](https://huggingface.co/spaces)
- Name: `ecommerce-eda`
- SDK: **Streamlit**
- Visibility: Public

**Step 2:** Upload files via the web UI or Git:
```bash
# Using HuggingFace CLI
pip install huggingface_hub

huggingface-cli login
# Paste your HF token from huggingface.co/settings/tokens

# Clone your space
git clone https://huggingface.co/spaces/YOUR_HF_USERNAME/ecommerce-eda
cd ecommerce-eda

# Copy app files
cp /path/to/app.py .
cp /path/to/requirements.txt .
cp /path/to/README.md .
cp /path/to/ecommerce_raw_dataset.csv .

# Push
git add .
git commit -m "Deploy E-Commerce EDA Dashboard"
git push
```

**Step 3:** Your app is live at:  
`https://YOUR_HF_USERNAME-ecommerce-eda.hf.space`

---

## 📁 File Structure

```
ecommerce-eda/
├── app.py                      ← Main Streamlit app
├── ecommerce_raw_dataset.csv   ← Source dataset
├── requirements.txt            ← Python dependencies
└── README.md                   ← This file (also HuggingFace Spaces config)
```

---

## 🔧 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.9+ | Core language |
| Streamlit | Web app framework |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Plotly | Interactive charts |
| Matplotlib | Static chart rendering |

---

## 📚 Assignment Tasks Covered

| Step | Description |
|------|-------------|
| **Step 1** | Data Cleaning — missing values, outliers, duplicates, feature engineering |
| **Step 2** | Descriptive Statistics — mean, median, std dev, skewness, kurtosis, IQR |
| **Step 3** | EDA — 10 analytical charts + Pearson correlation heatmap with business insights |

---

## 📄 License

MIT License — free to use, modify, and distribute.
