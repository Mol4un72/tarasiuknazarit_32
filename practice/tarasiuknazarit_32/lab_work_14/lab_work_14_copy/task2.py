from pathlib import Path
from collections import defaultdict
from math import fsum
import sys

from tabulate import tabulate

print("Nazar Tarasiuk, I-23")

CSV_FILE = Path(__file__).resolve().parent / "data" / "expenses.csv"


def main():
    categories = defaultdict(list)

    try:
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

                category = fields[1].strip()
                try:
                    amount = float(fields[2].strip().replace(",", "."))
                    if not category or amount < 0:
                        raise ValueError
                except ValueError:
                    print(
                        f"warning: invalid amount/category on line {line_number}",
                        file=sys.stderr
                    )
                    continue

                categories[category].append(amount)

    except OSError as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)

    if not categories:
        print("error: no valid expense records found", file=sys.stderr)
        sys.exit(1)

    rows = []
    all_amounts = []

    for category in sorted(categories):
        amounts = categories[category]
        rows.append([category, len(amounts), fsum(amounts)])
        all_amounts.extend(amounts)

    rows.append(["TOTAL", len(all_amounts), fsum(all_amounts)])

    print(tabulate(
        rows,
        headers=["category", "count", "total"],
        tablefmt="github",
        floatfmt=".2f"
    ))


if __name__ == "__main__":
    main()