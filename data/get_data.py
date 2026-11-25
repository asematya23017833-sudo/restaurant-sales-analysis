"""Download the Maven Analytics Coffee Shop Sales dataset (public practice dataset).
Fetches the original .xlsx from a public GitHub mirror (byte-identical to the file
analyzed here, md5-checked) and converts it to data/coffee_shop_sales.csv.
Source page: https://mavenanalytics.io/data-playground/coffee-shop-sales
Mirror: https://github.com/Ahmedabbas75/Coffee-Shop-Sales
"""
import hashlib
import urllib.request
from pathlib import Path

import pandas as pd

URL = "https://raw.githubusercontent.com/Ahmedabbas75/Coffee-Shop-Sales/main/Coffee%20Shop%20Sales.xlsx"
MD5 = "bf42cb880a537fec202b836362c664da"

here = Path(__file__).resolve().parent
xlsx = here / "coffee_shop_sales.xlsx"
csv = here / "coffee_shop_sales.csv"
if not xlsx.exists():
    print("downloading workbook ...")
    urllib.request.urlretrieve(URL, xlsx)
assert hashlib.md5(xlsx.read_bytes()).hexdigest() == MD5, "checksum mismatch"
df = pd.read_excel(xlsx)
df.to_csv(csv, index=False)
print(f"{csv.name} written: {len(df):,} rows")
