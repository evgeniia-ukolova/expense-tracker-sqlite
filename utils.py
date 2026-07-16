from datetime import datetime, date
import csv

def show_menu() -> None:
    print()
    print("1. Показать расходы")
    print("2. Добавить расход")
    print("3. Показать общую сумму")
    print("4. Удалить расход")
    print("5. Показать расходы по категории")
    print("6. Показать сумму по категории")
    print("7. Показать расходы за месяц")
    print("8. Показать сумму за месяц")
    print("9. Редактировать расход")
    print("10. Найти расход по названию")
    print("11. Показать суммы по всем категориям")
    print("12. Показать суммы по месяцам")
    print("13. Показать количество расходов за месяц")
    print("14. Показать средний расход за месяц")
    print("15. Показать самый большой расход за месяц")
    print("16. Показать самый маленький расход за месяц")
    print("17. Показать категории")
    print("18. Найти расход по описанию")
    print("19. Экспортировать расходы в CSV")
    print("20. Импортировать расходы из CSV")
    print("21. Выйти")




def get_int(message: str) -> int:           # запрос целого числа: для выбора пункта меню и удаления по ID
    while True:
        try:
            number = int(input(message))
            return number
        except ValueError:
            print("Введите целое число")


def get_number(message: str) -> float:          # запрос дробного числа: общая сумма расхода
    while True:
        try:
            number = float(input(message))
            return number
        except ValueError:
            print("Введите число")


def get_date(message: str) -> str:          # валидация даты
    while True:
        value = input(message).strip()

        if not value:                                   # если пользователь ничего не ввёл
            return date.today().strftime("%Y-%m-%d")    # То возвращаем сегодняшнюю дату

        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Введите дату в формате YYYY-MM-DD")


def get_month(message: str) -> str:         # валидация месяца
    while True:
        month = input(message).strip()

        try:
            datetime.strptime(month, "%Y-%m")
            return month
        except ValueError:
            print("Введите месяц в формате YYYY-MM")


def export_expenses_to_csv(expenses):           # функция экспорта расходов
    
    if not expenses:
        print("Нет расходов для экспорта")
        return

    with open("expenses.csv", "w", newline="", encoding="utf-8") as file:           # Создаёт или перезаписывает файл expenses.csv
        writer = csv.writer(file)                                                   # Создаёт специальный объект для записи данных в формате CSV
        writer.writerow(["ID", "Название", "Сумма", "Категория", "Дата", "Описание"])   # Записывает первую строку файла — названия столбцов
        writer.writerows(expenses)                                                      # Записывает сразу все расходы, которые пришли в функцию

    print("Расходы экспортированы в expenses.csv")


def read_expenses_from_csv(filename: str) -> list[tuple]:           # функция чтения расходов из CSV.
    expenses = []

    try:
        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)           # Создаёт объект для чтения CSV

            next(reader, None)                  # Пропускает первую строку с заголовками

            for row in reader:
                if len(row) != 6:
                    continue

                _, title, amount, category, date, description = row         # Разбирает строку CSV. ID кладём в _, потому что он нам не нужен.

                expenses.append((
                    title,
                    float(amount),          # Преобразует сумму из текста в число
                    category,
                    date,
                    description
                ))

    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return []

    except ValueError:
        print("В CSV есть некорректная сумма")
        return []

    return expenses




