
# Maria Vovk, I-23
import csv
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
from tabulate import tabulate

file_path = Path(__file__).parent / "data" / "expenses.csv"

totals = defaultdict(lambda: {"count": 0, "total": Decimal("0.00")})

with file_path.open("r", encoding="utf-8-sig", newline="") as file:
    for line in file:
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        row = next(csv.reader([line], delimiter=";"))
        if len(row) < 3:
            continue

        category = row[1].strip()
        amount = Decimal(row[2].strip().replace(",", "."))

        totals[category]["count"] += 1
        totals[category]["total"] += amount

table = [
    [category, values["count"], f'{values["total"]:.2f}']
    for category, values in sorted(totals.items())
]

total_count = sum(values["count"] for values in totals.values())
total_amount = sum(
    (values["total"] for values in totals.values()),
    Decimal("0.00")
)
table.append(["TOTAL", total_count, f"{total_amount:.2f}"])

print(tabulate(
    table,
    headers=["category", "count", "total"],
    tablefmt="github"
))
