import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("csv_file", type=str, help="Шлях до CSV файлу")
args = parser.parse_args()

df = pd.read_csv(args.csv_file)

mean_price = np.mean(df["price_per_unit"])
median_quantity = np.median(df["quantity"])
std_price = np.std(df["price_per_unit"])

df["total_price"] = df["quantity"] * df["price_per_unit"]

total_profit_by_supplier = df.groupby("supplier")["total_price"].sum()
best_supplier = total_profit_by_supplier.idxmax()

category_quantity = df.groupby("category")["quantity"].sum()

low_supply = df[df["quantity"] < 100]
low_supply_filename = "low_supply.csv"
low_supply.to_csv(low_supply_filename, index=False)

sorted_df = df.sort_values(by="total_price", ascending=False)
print("Перші три рядки за загальною вартістю:")
print(sorted_df.head(3))

report_filename = "report.txt"
with open(report_filename, "w", encoding="utf-8") as f:
    f.write(f"Середня ціна: {mean_price}\n")
    f.write(f"Медіана кількості: {median_quantity}\n")
    f.write(f"Стандартне відхилення ціни: {std_price}\n")
    f.write(f"Постачальник з найбільшим прибутком: {best_supplier}\n")
    f.write(f"Файл з дефіцитними поставками: {low_supply_filename}\n")

category_quantity.plot(kind="bar", color="skyblue")
plt.title("Розподіл кількості препаратів за категоріями")
plt.xlabel("Категорія")
plt.ylabel("Кількість")
plt.savefig("category_distribution.png")
plt.close()