from pathlib import Path
from datetime import datetime
from math import log, floor
import sys

print("Nazar Tarasiuk, I-23")

USAGE = "usage: python3 task3.py [--dry-run] <dir>"
BASE_DIR = Path(__file__).resolve().parent


def format_size(size):
    units = ["B", "KB", "MB", "GB"]
    if size <= 0:
        return "0.0 B"

    unit_index = min(floor(log(size, 1024)), len(units) - 1)
    value = size / (1024 ** unit_index)
    return f"{value:.1f} {units[unit_index]}"


def main():
    args = sys.argv[1:]
    dry_run = False

    if args and args[0] == "--dry-run":
        dry_run = True
        args = args[1:]

    if len(args) != 1:
        print(USAGE, file=sys.stderr)
        return 2

    directory = Path(args[0]).expanduser()

    if not directory.is_absolute():
        directory = Path.cwd() / directory

    if not directory.exists() or not directory.is_dir():
        print(f"error: {directory} is not a directory", file=sys.stderr)
        return 1

    files = [path for path in directory.iterdir() if path.is_file()]

    if not files:
        print("no files to organize")
        return 0

    entries = []
    for path in files:
        modified = datetime.fromtimestamp(path.stat().st_mtime)
        month_folder = modified.strftime("%Y-%m")
        entries.append((modified, path, month_folder))

    entries.sort(key=lambda item: item[0])

    # Перевірити всі конфлікти до переміщення будь-якого файлу
    for modified, source, month_folder in entries:
        destination = directory / month_folder / source.name
        if destination.exists():
            print(
                f"error: {destination} already exists, nothing was moved",
                file=sys.stderr
            )
            return 1

    for modified, source, month_folder in entries:
        size_text = format_size(source.stat().st_size)
        print(
            f"{source.name:<22} {size_text:>9}  "
            f"{modified:%d.%m.%Y %H:%M}  -> {month_folder}/"
        )

    folders_count = len({item[2] for item in entries})

    if dry_run:
        print(
            f"{len(entries)} files, {folders_count} folders "
            "(dry run, nothing moved)"
        )
        return 0

    try:
        for modified, source, month_folder in entries:
            destination_dir = directory / month_folder
            destination_dir.mkdir(exist_ok=True)
            source.rename(destination_dir / source.name)

        reports_dir = BASE_DIR / "reports"
        reports_dir.mkdir(exist_ok=True)

        run_time = datetime.now()
        report_path = reports_dir / (
            f"organize_{run_time:%Y%m%d_%H%M}.txt"
        )

        with report_path.open("w", encoding="utf-8") as report:
            report.write("Nazar Tarasiuk, I-23\n")
            report.write(f"Run: {run_time:%Y-%m-%d %H:%M:%S}\n")
            report.write(f"Directory: {directory}\n")
            for modified, source, month_folder in entries:
                report.write(
                    f"{source.name} -> {month_folder}/\n"
                )
            report.write(
                f"{len(entries)} files, {folders_count} folders\n"
            )

        print(f"{len(entries)} files, {folders_count} folders")
        print(f"report saved to: {report_path}")
        return 0

    except OSError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())