# Restaurant / Coffee Shop Sales Analysis

Sales analysis dashboard by product category, store location and time-of-day customer behavior, with monthly trend tracking.

> **Provenance:** Rebuilt in November 2026 after the original project files were lost. All numbers below were measured on this rebuild against the public dataset named here.

> **Power BI note:** this repo ships the real dataset, the DAX measures, the Power Query steps, and a runnable verified companion analysis (charts in `charts/`). A native `.pbix` file cannot be authored on Linux; open the dataset in Power BI Desktop and apply `dax/measures.dax` + `powerquery/steps.pq` to reproduce the dashboard in minutes.

## Dataset
Maven Analytics Coffee Shop Sales (public): `data/coffee_shop_sales.csv`, 149,116 transactions at 3 NYC locations, 2023-01-01 to 2023-06-30. Substitute dataset; the original restaurant sales file was lost.

## Measured results (this rebuild)
- Total revenue: **USD 698,812**
- Top categories: Coffee $270K, Tea $196K, Bakery $82K
- Locations run near-even ($230K-$237K each); revenue peaks mid-morning (see `charts/revenue_by_hour.png`)
- Charts (verified): `charts/revenue_by_category.png`, `charts/location_month.png`, `charts/revenue_by_hour.png`

## Run
```bash
pip install -r requirements.txt
python src/build_dashboard_data.py
```
