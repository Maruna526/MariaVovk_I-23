import math
import sys
from datetime import datetime
from pathlib import Path
import shutil

print("Maria Vovk, І-23")

BASE_DIR = Path(__file__).parent


def format_size(size):
    if size == 0:
        return "0 B"

    units = ["B", "KB", "MB", "GB"]
    unit_index = min(int(math.log(size, 1024)), len(units) - 1)
    value = size / (1024 ** unit_index)

    return f"{value:.1f} {units[unit_index]}"


def main():
    args = sys.argv[1:]
    dry_run = False

    if args and args[0] == "--dry-run":
        dry_run = True
        args = args[1:]

    if len(args) != 1:
        print(
            "usage: python task3.py [--dry-run] <dir>",
            file=sys.stderr,
        )
        sys.exit(2)

    directory = Path(args[0]).resolve()

    if not directory.exists() or not directory.is_dir():
        print(f"error: {directory} is not a directory", file=sys.stderr)
        sys.exit(1)

    files = sorted(
        (item for item in directory.iterdir() if item.is_file()),
        key=lambda item: item.stat().st_mtime,
    )

    if not files:
        print("У каталозі немає файлів.")
        sys.exit(0)

    plan = []

    for file_path in files:
        stat = file_path.stat()
        modified = datetime.fromtimestamp(stat.st_mtime)
        folder_name = modified.strftime("%Y-%m")
        destination = directory / folder_name / file_path.name

        print(
            f"{file_path.name:<22} "
            f"{format_size(stat.st_size):>10}  "
            f"{modified:%d.%m.%Y %H:%M}  -> {folder_name}/"
        )

        plan.append((file_path, destination, folder_name))

    # Перевіряємо весь план перед переміщенням.
    for _, destination, _ in plan:
        if destination.exists():
            print(
                f"error: {destination} already exists, nothing was moved",
                file=sys.stderr,
            )
            sys.exit(1)

    folder_count = len({folder_name for _, _, folder_name in plan})

    if dry_run:
        print(
            f"{len(files)} files, {folder_count} folders "
            "(dry run, nothing moved)"
        )
        sys.exit(0)

    for _, destination, _ in plan:
        destination.parent.mkdir(parents=True, exist_ok=True)

    for file_path, destination, _ in plan:
        shutil.move(str(file_path), str(destination))

    reports_dir = BASE_DIR / "reports"
    reports_dir.mkdir(exist_ok=True)

    report_time = datetime.now()
    report_path = reports_dir / (
        f"organize_{report_time:%Y%m%d_%H%M}.txt"
    )

    with report_path.open("w", encoding="utf-8") as report:
        report.write("Звіт про сортування файлів\n")
        report.write(f"Дата: {report_time:%d.%m.%Y %H:%M}\n")
        report.write(f"Каталог: {directory}\n")
        report.write(f"Кількість файлів: {len(files)}\n")
        report.write(f"Кількість папок: {folder_count}\n")

        for file_path, destination, _ in plan:
            report.write(f"{file_path.name} -> {destination.parent.name}/\n")

    print(f"{len(files)} files, {folder_count} folders")
    print(f"report saved to: {report_path}")


if __name__ == "__main__":
    main()