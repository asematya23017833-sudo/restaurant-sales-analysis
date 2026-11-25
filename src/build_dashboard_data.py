"""Restaurant / Coffee Shop Sales Analysis - rebuild (Nov 2026).

Dataset: Maven Analytics Coffee Shop Sales (public), 149,116 transactions at
three NYC store locations, Jan-Jun 2023. Substitute dataset: the original
restaurant sales file was lost. KPI dashboards by product category, store
location, and time (monthly trend + hour-of-day behavior).
"""
import json
from pathlib import Path

import duckdb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
con = duckdb.connect()
CSV = f"{ROOT}/data/coffee_shop_sales.csv"

kpis = con.execute(f"""
SELECT COUNT(*) AS transactions,
       ROUND(SUM(transaction_qty * unit_price), 2) AS total_revenue_usd,
       COUNT(DISTINCT store_location) AS locations,
       MIN(transaction_date) AS first_date, MAX(transaction_date) AS last_date
FROM read_csv_auto('{CSV}')
""").df()

by_cat = con.execute(f"""
SELECT product_category, ROUND(SUM(transaction_qty * unit_price), 0) AS revenue, SUM(transaction_qty) AS units
FROM read_csv_auto('{CSV}') GROUP BY 1 ORDER BY 2 DESC
""").df()

by_loc = con.execute(f"""
SELECT store_location, ROUND(SUM(transaction_qty * unit_price), 0) AS revenue
FROM read_csv_auto('{CSV}') GROUP BY 1 ORDER BY 2 DESC
""").df()

by_month = con.execute(f"""
SELECT DATE_TRUNC('month', CAST(transaction_date AS DATE)) AS month,
       ROUND(SUM(transaction_qty * unit_price), 0) AS revenue
FROM read_csv_auto('{CSV}') GROUP BY 1 ORDER BY 1
""").df()

by_hour = con.execute(f"""
SELECT HOUR(CAST(transaction_time AS TIME)) AS hour, ROUND(SUM(transaction_qty * unit_price), 0) AS revenue
FROM read_csv_auto('{CSV}') GROUP BY 1 ORDER BY 1
""").df()

plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(10, 4))
ax.barh(by_cat["product_category"][::-1], by_cat["revenue"][::-1])
ax.set_title("Revenue by product category"); ax.set_xlabel("USD")
fig.tight_layout(); fig.savefig(ROOT / "charts" / "revenue_by_category.png", dpi=120); plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].bar(by_loc["store_location"], by_loc["revenue"]); axes[0].set_title("Revenue by store location")
axes[0].tick_params(axis="x", rotation=15)
axes[1].plot(pd.to_datetime(by_month["month"]), by_month["revenue"], marker="o"); axes[1].set_title("Monthly revenue")
fig.tight_layout(); fig.savefig(ROOT / "charts" / "location_month.png", dpi=120); plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(by_hour["hour"].astype(str), by_hour["revenue"])
ax.set_title("Revenue by hour of day (customer daypart behavior)"); ax.set_xlabel("Hour"); ax.set_ylabel("USD")
fig.tight_layout(); fig.savefig(ROOT / "charts" / "revenue_by_hour.png", dpi=120); plt.close(fig)

summary = {"kpis": kpis.to_dict("records")[0],
           "top_categories": by_cat.head(5).to_dict("records"),
           "by_location": by_loc.to_dict("records")}
(ROOT / "results.json").write_text(json.dumps(summary, indent=2, default=str))
print(json.dumps(summary, indent=2, default=str))
