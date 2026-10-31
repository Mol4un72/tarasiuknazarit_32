
from pathlib import Path


def parse_line(line):
    fields = line.strip().split(";")

    if len(fields) != 4:
        raise ValueError("Expected 4 fields")

    date, category, amount, comment = fields

    try:
        amount = float(amount.replace(",", "."))
    except ValueError:
        raise ValueError("Amount must be a number")

    return {
        "date": date,
        "category": category,
        "amount": amount,
        "comment": comment,
    }


def total_by_category(records):
    totals = {}

    for record in records:
        category = record["category"]
        totals[category] = totals.get(category, 0) + record["amount"]

    return {
        category: round(total, 2)
        for category, total in totals.items()
    }


def load_expenses(path):
    records = []

    with Path(path).open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            records.append(parse_line(line))

    return records
