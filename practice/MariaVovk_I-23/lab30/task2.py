from datetime import date, timedelta
from pathlib import Path
import math
import sys

print("Maria Vovk, І-23")

BASE_DIR = Path(__file__).parent
EXPENSES_FILE = BASE_DIR / "data" / "expenses.csv"


def main():
    expenses = {}

    if not EXPENSES_FILE.exists():
        print(f"Помилка: файл {EXPENSES_FILE} не знайдено", file=sys.stderr)
        sys.exit(1)

    with EXPENSES_FILE.open("r", encoding="utf-8-sig") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split(";")

            try:
                if len(parts) < 3:
                    raise ValueError("недостатньо полів")

                expense_date = date.fromisoformat(parts[0].strip())
                amount = float(parts[2].strip())

                if amount < 0:
                    raise ValueError("сума не може бути від'ємною")

                expenses.setdefault(expense_date, []).append(amount)

            except ValueError as error:
                print(
                    f"Попередження: рядок {line_number} пропущено: {error}",
                    file=sys.stderr,
                )

    if not expenses:
        print("Помилка: немає коректних записів про витрати", file=sys.stderr)
        sys.exit(1)

    first_date = min(expenses)
    last_date = max(expenses)
    period_days = (last_date - first_date).days + 1

    print(
        f"period: {first_date:%d.%m.%Y} ({first_date:%A}) - "
        f"{last_date:%d.%m.%Y} ({last_date:%A}), {period_days} days"
    )

    weekday_names = [
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday",
    ]
    weekday_totals = [0.0] * 7

    for current_date, amounts in expenses.items():
        weekday_totals[current_date.weekday()] += math.fsum(amounts)

    print("\nweekday      total")
    for weekday, total in zip(weekday_names, weekday_totals):
        print(f"{weekday:<12} {total:8.2f}")

    daily_totals = []
    current_date = first_date

    while current_date <= last_date:
        daily_totals.append(math.fsum(expenses.get(current_date, [])))
        current_date += timedelta(days=1)

    total_expenses = math.fsum(daily_totals)
    average = total_expenses / period_days
    variance = math.fsum(
        (amount - average) ** 2 for amount in daily_totals
    ) / period_days
    standard_deviation = math.sqrt(variance)

    top_index = max(range(period_days), key=lambda index: daily_totals[index])
    top_date = first_date + timedelta(days=top_index)
    no_spend_days = sum(amount == 0 for amount in daily_totals)

    print(f"\ntotal:        {total_expenses:.2f}")
    print(f"per day:      {average:.2f} +- {standard_deviation:.2f}")
    print(
        f"top day:      {top_date:%d.%m.%Y} "
        f"({top_date:%A}), {daily_totals[top_index]:.2f}"
    )
    print(f"no-spend days: {no_spend_days}")

    month_start = last_date.replace(day=1)

    if last_date.month == 12:
        next_month = date(last_date.year + 1, 1, 1)
    else:
        next_month = date(last_date.year, last_date.month + 1, 1)

    days_left = (next_month - last_date).days - 1
    days_left = (next_month - last_date).days
    month_forecast = average * days_in_month

    print(
        f"days in {last_date:%B}: {days_in_month}, "
        f"left after {last_date:%d}: {days_left}"
    )
    print(f"month forecast: {month_forecast:.2f}")

    december_days = (date(2027, 1, 1) - date(2026, 12, 1)).days
    february_days = (date(2028, 3, 1) - date(2028, 2, 1)).days

    print("\nПеревірка кількості днів у місяці:")
    print(f"2026-12-15: {december_days} днів у грудні")
    print(f"2028-02-10: {february_days} днів у лютому")


if __name__ == "__main__":
    main()