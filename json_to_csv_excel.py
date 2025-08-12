import json
import csv
import pandas as pd
import sys
import os

# Choix du fichier JSON source selon argument
json_file = "data/regions_prefectures_communes.json"
csv_file = "data/regions_prefectures_communes.csv"
excel_file = "data/regions_prefectures_communes.xlsx"

if len(sys.argv) > 1 and sys.argv[1] == "ar":
    json_file = "data/regions_prefectures_communes_ar.json"
    csv_file = "data/regions_prefectures_communes_ar.csv"
    excel_file = "data/regions_prefectures_communes_ar.xlsx"

os.makedirs("data", exist_ok=True)

with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []
for region, prefectures in data.items():
    for prefecture, communes in prefectures.items():
        for commune in communes:
            rows.append([region, prefecture, commune])

with open(csv_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Région", "Préfecture", "Commune"])
    writer.writerows(rows)

df = pd.DataFrame(rows, columns=["Région", "Préfecture", "Commune"])
df.to_excel(excel_file, index=False)
