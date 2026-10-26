from pathlib import Path
from datetime import date, timedelta
from math import fsum, sqrt
import sys

print("Nazar Tarasiuk, I-23")

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "data" / "expenses.csv"

try:
    expenses = []

    with CSV_FILE.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            fields = line.split(";")
            if len(fields) != 4:
                print(
                    f"warning: line {line_number}: expected 4 fields",
                    file=sys.stderr
                )
                continue

            try:
                expense_date = date.fromisoformat(fields[0].strip())
                amount = float(fields[2].strip().replace(",", "."))

                if amount < 0:
                    raise ValueError("negative amount")

                expenses.append((expense_date, amount))

            except ValueError:
                print(
                    f"warning: invalid data on line {line_number}",
                    file=sys.stderr
                )

    if not expenses:
        raise ValueError("No valid expense records found")

    daily = {}
    for expense_date, amount in expenses:
        daily[expense_date] = daily.get(expense_date, [])
        daily[expense_date].append(amount)

    first_date = min(daily)
    last_date = max(daily)
    period_days = (last_date - first_date).days + 1

    print(
        f"period: {first_date:%d.%m.%Y} ({first_date:%A}) - "
        f"{last_date:%d.%m.%Y} ({last_date:%A}), {period_days} days"
    )
    print()
    print(f"{'weekday':<12} {'total':>10}")

    weekday_totals = [0.0] * 7
    for current_date, amounts in daily.items():
        weekday_totals[current_date.weekday()] += fsum(amounts)

    for weekday in range(7):
        weekday_name = date(2026, 1, 5 + weekday).strftime("%A")
        print(f"{weekday_name:<12} {weekday_totals[weekday]:>10.2f}")

    all_daily_totals = []
    current_date = first_date

    while current_date <= last_date:
        all_daily_totals.append(fsum(daily.get(current_date, [])))
        current_date += timedelta(days=1)

    total = fsum(all_daily_totals)
    average = total / period_days
    variance = fsum(
        (value - average) ** 2 for value in all_daily_totals
    ) / period_days
    standard_deviation = sqrt(variance)

    top_index = max(range(period_days), key=lambda i: all_daily_totals[i])
    top_date = first_date + timedelta(days=top_index)
    no_spend_days = sum(value == 0 for value in all_daily_totals)

    next_month = date(
        last_date.year + (last_date.month == 12),
        1 if last_date.month == 12 else last_date.month + 1,
        1
    )
    first_of_month = date(last_date.year, last_date.month, 1)
    days_in_month = (next_month - first_of_month).days
    days_left = days_in_month - last_date.day
    month_forecast = average * days_in_month

    print(f"\ntotal:        {total:.2f}")
    print(f"per day:      {average:.2f} +- {standard_deviation:.2f}")
    print(
        f"top day:      {top_date:%d.%m.%Y} "
        f"({top_date:%A}), {all_daily_totals[top_index]:.2f}"
    )
    print(f"no-spend days: {no_spend_days}")
    print(
        f"days in {last_date:%B}: {days_in_month}, "
        f"left after {last_date:%d.%m}: {days_left}"
    )
    print(f"month forecast: {month_forecast:.2f}")

    for test_date in (date(2026, 12, 15), date(2028, 2, 10)):
        next_month_date = date(
            test_date.year + (test_date.month == 12),
            1 if test_date.month == 12 else test_date.month + 1,
            1
        )
        month_start = date(test_date.year, test_date.month, 1)
        print(
            f"check {test_date}: "
            f"{(next_month_date - month_start).days} days in month"
        )

except (OSError, ValueError) as error:
    print(f"error: {error}", file=sys.stderr)
    sys.exit(1)