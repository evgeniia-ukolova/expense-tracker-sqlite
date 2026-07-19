from datetime import datetime

from database import (
    create_table,
    add_expense,
    get_expenses,
    get_total,
    delete_expense,
    get_expenses_by_category,
    get_total_by_category,
    get_expenses_by_month,
    get_total_by_month,
    update_expense,
    search_expenses_by_title,
    get_totals_by_categories,
    get_totals_by_months,
    get_expenses_count_by_month,
    get_average_expense_by_month,
    get_max_expense_by_month,
    get_min_expense_by_month,
    add_description_column,
    get_categories,
    search_expenses_by_description,
    expense_exists
)

from utils import (
    show_menu, 
    get_int, 
    get_number, 
    get_date, 
    get_month, 
    export_expenses_to_csv, 
    read_expenses_from_csv,
    create_database_backup,
    restore_database_backup
)


def format_date(date: str) -> str:          # форматированиe даты
    date_object = datetime.strptime(date, "%Y-%m-%d")       # 2026-07-07
    return date_object.strftime("%d.%m.%Y")                 # 07.07.2026


def print_expense(expense: tuple) -> None:          # просто чтобы сократить код
    expense_id, title, amount, category, date, description = expense
    display_date = format_date(date)

    if description:
        print(f"ID: {expense_id} | {display_date} | {category} | {title} — {amount:.2f} | {description}")
    else:
        print(f"ID: {expense_id} | {display_date} | {category} | {title} — {amount:.2f}")   # если описание есть — показываем его. Если пустое — не выводим лишний разделитель


def show_expenses() -> None:        # показать расходы
    expenses = get_expenses()       # получаем расходы из базы.

    if not expenses:
        print("Расходов нет")
        return

    for expense in expenses:
        print_expense(expense)


def show_total() -> None:           # общая сумма расходов
    total = get_total()
    print(f"Общая сумма расходов: {total:.2f}")


def remove_expense() -> None:           # удаление расхода по ID.
    show_expenses()

    expense_id = get_int("ID расхода для удаления: ")

    if delete_expense(expense_id):
        print("Расход удалён")
    else:
        print("Расход не найден")


def show_expenses_by_category() -> None:        # фильтр расходов по категории.
    category = input("Категория: ")

    expenses = get_expenses_by_category(category)

    if not expenses:
        print("Расходов в этой категории нет")
        return

    for expense in expenses:
        print_expense(expense)

def show_total_by_category() -> None:       # общую сумму по категории
    category = input("Категория: ")

    total = get_total_by_category(category)

    print(f"Сумма по категории '{category}': {total:.2f}")


def show_expenses_by_month() -> None:           # фильтр расходов по месяцу.
    month = get_month("Месяц в формате YYYY-MM: ")

    expenses = get_expenses_by_month(month)

    if not expenses:
        print("Расходов за этот месяц нет")
        return

    for expense in expenses:
        print_expense(expense)


def show_total_by_month() -> None:          # сумму расходов за месяц.
    month = get_month("Месяц в формате YYYY-MM: ")

    total = get_total_by_month(month)

    print(f"Сумма за месяц {month}: {total:.2f}")


def edit_expense() -> None:         # редактирование расхода по ID.
    show_expenses()

    expense_id = get_int("ID расхода для редактирования: ")

    title = input("Новое название: ")
    amount = get_number("Новая сумма: ")
    category = input("Новая категория: ")
    date = get_date("Дата в формате YYYY-MM-DD, Enter — сегодня: ")
    description = input("Новое описание: ")

    if update_expense(expense_id, title, amount, category, date, description):
        print("Расход изменён")
    else:
        print("Расход не найден или данные некорректны")


def search_expenses() -> None:          # поиск расходов по названию title
    query = input("Введите часть названия расхода: ")

    expenses = search_expenses_by_title(query)

    if not expenses:
        print("Расходы не найдены")
        return

    for expense in expenses:
        print_expense(expense)


def search_expenses_by_description_text() -> None:          # функция поиска расходов по описанию.
    query = input("Введите часть описания расхода: ")

    expenses = search_expenses_by_description(query)

    if not expenses:
        print("Расходы не найдены")
        return

    for expense in expenses:
        print_expense(expense)


def show_totals_by_categories() -> None:        # cумма по категориям
    totals = get_totals_by_categories()

    if not totals:
        print("Расходов нет")
        return

    for category, total in totals:
        print(f"{category} — {total:.2f}")


def show_totals_by_months() -> None:        # итоговая сумма по месяцам
    totals = get_totals_by_months()

    if not totals:
        print("Расходов нет")
        return

    for month, total in totals:
        print(f"{month} — {total:.2f}")


def show_expenses_count_by_month() -> None:         # вывод количества расходов в месяц
    month = get_month("Месяц в формате YYYY-MM: ")

    count = get_expenses_count_by_month(month)

    print(f"Количество расходов за месяц {month}: {count}")


def show_average_expense_by_month() -> None:            # средний расход за месяц
    month = get_month("Месяц в формате YYYY-MM: ")

    average = get_average_expense_by_month(month)

    print(f"Средний расход за месяц {month}: {average:.2f}")


def show_max_expense_by_month() -> None:            # самый большой расход за месяц
    month = get_month("Месяц в формате YYYY-MM: ")

    expense = get_max_expense_by_month(month)

    if expense is None:
        print("Расходов за этот месяц нет")
        return

    print("Самый большой расход за месяц:")
    print_expense(expense)


def show_min_expense_by_month() -> None:            # самый маленький расход за месяц
    month = get_month("Месяц в формате YYYY-MM: ")

    expense = get_min_expense_by_month(month)

    if expense is None:
        print("Расходов за этот месяц нет")
        return

    print("Самый маленький расход за месяц:")
    print_expense(expense)


def show_categories() -> None:          # список всех категорий
    categories = get_categories()

    if not categories:
        print("Категорий пока нет")
        return

    print("Категории:")

    for category in categories:
        print(f"- {category}")


def import_expenses_from_csv() -> None:         # функция чтения расходов из CSV.
    expenses = read_expenses_from_csv("expenses.csv")

    if not expenses:
        print("Нет расходов для импорта")
        return

    imported_count = 0
    skipped_count = 0

    for title, amount, category, date, description in expenses:
        if expense_exists(title, amount, category, date, description):
            skipped_count += 1
            continue

        if add_expense(title, amount, category, date, description):
            imported_count += 1

    print(f"Импортировано расходов: {imported_count}")
    print(f"Пропущено дубликатов: {skipped_count}")







def main() -> None:
    create_table()
    add_description_column()

    while True:
        show_menu()

        choice = get_int("Выберите действие: ")

        if choice == 1:
            show_expenses()

        elif choice == 2:
            title = input("Название расхода: ")
            amount = get_number("Сумма: ")
            category = input("Категория: ")
            date = get_date("Дата в формате YYYY-MM-DD: ")
            description = input("Описание: ")

            if add_expense(title, amount, category, date, description):
                print("Расход добавлен")
            else:
                print("Расход не добавлен")

        elif choice == 3:
            show_total()

        elif choice == 4:
            remove_expense()

        elif choice == 5:
            show_expenses_by_category()

        elif choice == 6:
            show_total_by_category()

        elif choice == 7:
            show_expenses_by_month()

        elif choice == 8:
            show_total_by_month()

        elif choice == 9:
            edit_expense()

        elif choice == 10:
            search_expenses()

        elif choice == 11:
            show_totals_by_categories()

        elif choice == 12:
            show_totals_by_months()

        elif choice == 13:
            show_expenses_count_by_month()

        elif choice == 14:
            show_average_expense_by_month()

        elif choice == 15:
            show_max_expense_by_month()

        elif choice == 16:
            show_min_expense_by_month()

        elif choice == 17:
            show_categories()

        elif choice == 18:
            search_expenses_by_description_text()

        elif choice == 19:      
            expenses = get_expenses()               # получает все расходы из базы
            export_expenses_to_csv(expenses)

        elif choice == 20:
            import_expenses_from_csv()

        elif choice == 21:
            create_database_backup()

        elif choice == 22:
            restore_database_backup()

        elif choice == 23:
            print("Выход")
            break

        else:
            print("Неизвестная команда")


if __name__ == "__main__":
    try:                                    # Python запускает основную программу.
        main()
    except KeyboardInterrupt:               # Если в терминале нажать Ctrl + C, мы ловим это прерывание.
        print("\nПрограмма завершена")




