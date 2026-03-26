# 🛒 E-Commerce Analytics Dashboard

**SP Jain MGB — Individual Assignment**  
Interactive Streamlit dashboard for analysing 1,500 synthetic e-commerce orders (Jan–Dec 2023).

## 📊 Features

| Tab | Contents |
|-----|----------|
| Overview | KPIs, Monthly Revenue Trend, Category & Region breakdown |
| Data Cleaning | Audit log, missing value check, distribution plots |
| Descriptive Stats | Summary statistics, box plots, scatter |
| EDA & Insights | Channel performance, return rates, heatmap, age-group funnel |
| Data Table | Filterable raw table + CSV download |

## 🚀 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Deploy on Streamlit Community Cloud

1. Push this repo to GitHub (include `ecommerce_raw_dataset.csv`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. New app → select your repo → `app.py` → Deploy

## 📁 Files

```
├── app.py                    # Main Streamlit application
├── ecommerce_raw_dataset.csv # Raw dataset (1,500 orders)
├── requirements.txt          # Python dependencies
└── README.md
```

## 🧹 Data Cleaning Steps Applied

- Duplicate rows removed
- Missing `Unit_Price` imputed with category median
- Invalid `Quantity` (≤0) corrected using `abs()`
- `Rating` clipped to valid range [1–5]
- `Order_Date` parsed to datetime; Month extracted
