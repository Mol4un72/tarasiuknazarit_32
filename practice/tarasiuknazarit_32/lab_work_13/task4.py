from pathlib import Path
from datetime import datetime
from math import isqrt, factorial, gcd, comb
import random
import sys

print("Nazar Tarasiuk, I-23")

YEAR = 2008
BASE_DIR = Path(__file__).resolve().parent
HISTORY_FILE = BASE_DIR / "results" / "history.csv"


def main():
    random.seed(YEAR)

    square_root = random.randint(5, 20)
    factorial_number = random.randint(3, 6)

    gcd_a = random.randint(24, 80)
    gcd_b = random.randint(12, 48)

    combination_n = random.randint(6, 10)
    combination_k = random.randint(2, combination_n - 1)

    percent = random.choice([5, 10, 15, 20, 25])
    amount = random.randrange(200, 1001, 20)

    questions = [
        (
            f"sqrt({square_root ** 2})",
            isqrt(square_root ** 2)
        ),
        (
            f"{factorial_number}!",
            factorial(factorial_number)
        ),
        (
            f"gcd({gcd_a}, {gcd_b})",
            gcd(gcd_a, gcd_b)
        ),
        (
            f"comb({combination_n}, {combination_k})",
            comb(combination_n, combination_k)
        ),
        (
            f"{percent}% of {amount}",
            percent * amount // 100
        ),
    ]

    start_time = datetime.now()
    score = 0

    for number, (question, correct_answer) in enumerate(questions, start=1):
        answer = input(f"{number}) {question} = ").strip()

        try:
            is_correct = int(answer) == correct_answer
        except ValueError:
            is_correct = False

        if is_correct:
            print("   correct")
            score += 1
        else:
            print(f"   wrong, answer: {correct_answer}")

    end_time = datetime.now()
    seconds = (end_time - start_time).total_seconds()

    print(f"score: {score}/5, time: {seconds:.1f} s")

    try:
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        file_exists = HISTORY_FILE.exists()

        with HISTORY_FILE.open("a", encoding="utf-8") as file:
            if not file_exists or HISTORY_FILE.stat().st_size == 0:
                file.write("# datetime;score;seconds\n")

            file.write(
                f"{end_time:%Y-%m-%d %H:%M};{score};{seconds:.1f}\n"
            )

        attempts = []

        with HISTORY_FILE.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                try:
                    timestamp, old_score, old_seconds = line.split(";")
                    attempts.append(
                        (int(old_score), float(old_seconds), timestamp)
                    )
                except ValueError:
                    print(
                        f"warning: invalid history row: {line}",
                        file=sys.stderr
                    )

        if attempts:
            best = max(attempts, key=lambda item: (item[0], -item[1]))
            print(
                f"attempts: {len(attempts)}, best: "
                f"{best[0]}/5 in {best[1]:.1f} s ({best[2]})"
            )

    except OSError as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()