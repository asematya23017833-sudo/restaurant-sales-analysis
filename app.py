"""Coffee Shop Sales Analysis - Streamlit companion app (rebuild, Nov 2026).
Dataset: Maven Analytics Coffee Shop Sales (public substitute dataset).
"""
import pathlib
import subprocess
import sys

if not (pathlib.Path(__file__).parent / "data" / "coffee_shop_sales.csv").exists():
    subprocess.run([sys.executable, str(pathlib.Path(__file__).parent / "data" / "get_data.py")], check=True)

import duckdb
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Coffee Shop Sales Analysis", layout="wide")
st.title("Coffee Shop Sales Analysis")
st.caption("Maven Analytics Coffee Shop Sales, public dataset - 149,116 transactions, 3 NYC locations, H1 2023. Rebuild Nov 2026. Amounts shown in units; the data states no currency.")

@st.cache_data
def load():
    con = duckdb.connect()
    csv = "read_csv_auto('data/coffee_shop_sales.csv')"
    kpi = con.execute(f"SELECT COUNT(*) n, SUM(transaction_qty*unit_price) rev FROM {csv}").df()
    cat = con.execute(f"SELECT product_category c, SUM(transaction_qty*unit_price) v FROM {csv} GROUP BY 1 ORDER BY 2 DESC").df()
    loc = con.execute(f"SELECT store_location c, SUM(transaction_qty*unit_price) v FROM {csv} GROUP BY 1 ORDER BY 2 DESC").df()
    mon = con.execute(f"SELECT DATE_TRUNC('month', CAST(transaction_date AS DATE)) m, SUM(transaction_qty*unit_price) v FROM {csv} GROUP BY 1 ORDER BY 1").df()
    hr = con.execute(f"SELECT HOUR(CAST(transaction_time AS TIME)) h, SUM(transaction_qty*unit_price) v FROM {csv} GROUP BY 1 ORDER BY 1").df()
    return kpi, cat, loc, mon, hr

kpi, cat, loc, mon, hr = load()
c1, c2 = st.columns(2)
c1.metric("Transactions", f"{int(kpi['n'][0]):,}")
c2.metric("Revenue (units)", f"{kpi['rev'][0]:,.0f}")
st.subheader("Revenue by product category")
st.bar_chart(cat.set_index("c"))
left, right = st.columns(2)
left.subheader("Revenue by location"); left.bar_chart(loc.set_index("c"))
right.subheader("Revenue by hour"); right.bar_chart(hr.set_index("h"))
st.subheader("Monthly revenue")
st.line_chart(mon.set_index("m"))
