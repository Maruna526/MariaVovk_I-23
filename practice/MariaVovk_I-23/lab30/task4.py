import math
import math
import random
import time
from datetime import datetime
from pathlib import Path

print("Maria Vovk, І-23")

random.seed(2008)

BASE_DIR = Path(__file__).parent
RESULTS_DIR = BASE_DIR / "results"
HISTORY_FILE = RESULTS_DIR / "history.csv"


def load_history():
    """Зчитує результати попередніх запусків."""
    if not HISTORY_FILE.exists():
        return []

    with HISTORY_FILE.open("r", encoding="utf-8") as file:
        lines = file.readlines()[1:]

    history = []
    for line in lines:
        parts = line.strip().split(";")
        if len(parts) == 3:
            try:
                history.append({
                    "datetime": parts[0],
                    "score": int(parts[1]),
                    "seconds": float(parts[2]),
                })
            except ValueError:
                continue

    return history


def save_result(score, seconds):
    """Зберігає результат у CSV-файл."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    if not HISTORY_FILE.exists():
        with HISTORY_FILE.open("w", encoding="utf-8", newline="") as file:
            file.write("# datetime;score;seconds\n")

    with HISTORY_FILE.open("a", encoding="utf-8", newline="") as file:
        file.write(
            f"{datetime.now():%Y-%m-%d %H:%M:%S};"
            f"{score};{seconds:.2f}\n"
        )


def make_questions():
    """Створює п'ять математичних завдань."""
    number = random.randint(50, 150)
    factorial_number = random.randint(4, 7)
    first = random.randint(30, 100)
    second = random.randint(20, 80)
    comb_n = random.randint(6, 10)
    comb_k = random.randint(2, 4)
    percent_base = random.randint(200, 900)
    percent = random.choice([10, 15, 20, 25])

    return [
        (
            f"Обчисли квадратний корінь з {number ** 2}.",
            math.isqrt(number ** 2),
        ),
        (
            f"Обчисли факторіал числа {factorial_number}.",
            math.factorial(factorial_number),
        ),
        (
            f"Знайди НСД чисел {first} і {second}.",
            math.gcd(first, second),
        ),
        (
            f"Обчисли кількість комбінацій C({comb_n}, {comb_k}).",
            math.comb(comb_n, comb_k),
        ),
        (
            f"Знайди {percent}% від числа {percent_base}. "
            "Відповідь може бути дробовою.",
            percent_base * percent / 100,
        ),
    ]


def main():
    questions = make_questions()
    score = 0
    start_time = time.perf_counter()

    print("\nМатематичний тренажер")
    print("Введи відповідь на кожне з 5 завдань.\n")

    for index, (question, correct_answer) in enumerate(questions, start=1):
        print(f"{index}. {question}")
        user_answer = input("Твоя відповідь: ").strip()

        try:
            answer = float(user_answer.replace(",", "."))
            if math.isclose(
                answer,
                float(correct_answer),
                rel_tol=1e-9,
                abs_tol=1e-9,
            ):
                print("Правильно!\n")
                score += 1
            else:
                print(
                    f"Неправильно. Правильна відповідь: "
                    f"{correct_answer}\n"
                )
        except ValueError:
            print(
                f"Потрібно ввести число. Відповідь: "
                f"{correct_answer}\n"
            )

    seconds = time.perf_counter() - start_time
    save_result(score, seconds)

    print("-" * 35)
    print(f"Результат: {score}/5")
    print(f"Час виконання: {seconds:.2f} с")

    history = load_history()
    best = max(
        history,
        key=lambda item: (item["score"], -item["seconds"]),
    )

    print(
        f"Найкращий результат: {best['score']}/5 "
        f"за {best['seconds']:.2f} с"
    )
    print(f"Історія результатів: {HISTORY_FILE}")


if __name__ == "__main__":
    main()
