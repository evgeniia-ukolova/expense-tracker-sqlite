from datetime import datetime, date
import csv
import shutil

from paths import DATABASE_PATH, CSV_PATH, BACKUPS_DIR, BACKUP_PATH


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
    print("21. Создать резервную копию базы")
    print("22. Восстановить базу из резервной копии")
    print("23. Выйти")




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

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as file:           # Создаёт или перезаписывает файл expenses.csv
        writer = csv.writer(file)                                                   # Создаёт специальный объект для записи данных в формате CSV
        writer.writerow(["ID", "Название", "Сумма", "Категория", "Дата", "Описание"])   # Записывает первую строку файла — названия столбцов
        writer.writerows(expenses)                                                      # Записывает сразу все расходы, которые пришли в функцию

    print("Расходы экспортированы в expenses.csv")


def read_expenses_from_csv() -> tuple[list[tuple], int]:            # функция чтения расходов из CSV с пропуском ошибок, возвращает два значения
    expenses = []
    invalid_count = 0           # Счётчик ошибочных строк

    try:
        with open(CSV_PATH, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)

            next(reader, None)

            for row in reader:                  # Если в строке неправильное количество столбцов, строка пропускается
                if len(row) != 6:               # Считает, сколько значений находится в строке (ID, Название, Сумма, Категория, Дата, Описание)
                    invalid_count += 1          # если значений не 6, строка неправильная, + счётчик ошибочных строк на 1.
                    continue

                _, title, amount, category, expense_date, description = row

                title = title.strip()
                category = category.strip()
                expense_date = expense_date.strip()
                description = description.strip()

                try:                        # Если сумму невозможно превратить в число, пропускается только эта строка.
                    amount = float(amount)
                except ValueError:
                    invalid_count += 1
                    continue

                if not title or not category or amount <= 0:
                    invalid_count += 1
                    continue

                try:
                    datetime.strptime(expense_date, "%Y-%m-%d")         # Проверяет, что дата записана строго в формате
                except ValueError:
                    invalid_count += 1
                    continue

                expenses.append((
                    title,
                    amount,
                    category,
                    expense_date,
                    description
                ))

    except FileNotFoundError:
        print(f"Файл {CSV_PATH.name} не найден")
        return [], 0

    return expenses, invalid_count


def create_database_backup() -> None:           # функция создания резервной копии базы
    if not DATABASE_PATH.exists():
        print("База данных не найдена")
        return

    BACKUPS_DIR.mkdir(exist_ok=True)

    shutil.copy2(DATABASE_PATH, BACKUP_PATH)

    print(f"Резервная копия создана: {BACKUP_PATH}")


def restore_database_backup() -> None:          # Функция восстановления резервной копии
    if not BACKUP_PATH.exists():
        print("Резервная копия не найдена")
        return

    confirmation = input(
        "Текущая база будет заменена резервной копией. Продолжить? (да/нет): "
    ).strip().lower()

    if confirmation != "да":
        print("Восстановление отменено")
        return

    shutil.copy2(BACKUP_PATH, DATABASE_PATH)

    print("База данных восстановлена из резервной копии")
