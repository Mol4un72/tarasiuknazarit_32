
from pathlib import Path

import pytest

from expenses import parse_line, total_by_category, load_expenses


# Завдання 2: звичайні assert-тести

def test_parse_line_valid():
    record = parse_line("2026-09-21;food;85.50;lunch")

    assert record["category"] == "food"
    assert record["amount"] == 85.5


def test_parse_line_date():
    record = parse_line("2026-09-21;food;85.50;lunch")

    assert record["date"] == "2026-09-21"


def test_parse_line_comment():
    record = parse_line("2026-09-21;food;85.50;lunch")

    assert record["comment"] == "lunch"


# Завдання 3: перевірка винятків

def test_parse_line_bad_amount():
    with pytest.raises(ValueError):
        parse_line("2026-09-21;food;abc;lunch")


def test_parse_line_wrong_fields():
    with pytest.raises(ValueError):
        parse_line("2026-09-21;food;85.50")


# Завдання 4: параметризація
# ЗАМІНИ ці 5 прикладів на п'ять рядків зі свого expenses.csv

@pytest.mark.parametrize(
    "line, expected_category, expected_amount",
    [
        ("2026-09-21;food;85.50;lunch", "food", 85.50),
        ("2026-09-22;food;14.50;coffee", "food", 14.50),
        ("2026-09-23;transport;40.00;bus", "transport", 40.00),
        ("2026-09-24;books;180.00;book", "books", 180.00),
        ("2026-09-25;coffee;65.00;drink", "coffee", 65.00),
    ],
)
def test_parse_line_parametrized(line, expected_category, expected_amount):
    record = parse_line(line)

    assert record["category"] == expected_category
    assert record["amount"] == expected_amount


# Завдання 5: тимчасовий файл

def test_total_by_category(tmp_path):
    path = tmp_path / "expenses.csv"

    path.write_text(
        "# date;category;amount;comment\n"
        "2026-09-21;food;85.50;lunch\n"
        "\n"
        "2026-09-22;food;14.50;coffee\n",
        encoding="utf-8",
    )

    totals = total_by_category(load_expenses(path))

    assert totals == {"food": 100.0}


# Перевірка справжнього файлу
def test_real_expenses():
    path = Path(__file__).parent / "data" / "expenses.csv"

    totals = total_by_category(load_expenses(path))

    assert totals == {
        "Entertainment": 200.0,
        "Food": 640.0,
        "Study": 500.0,
        "Transport": 240.0,
    }
