import sqlite3


def create_table() -> None:         # создание таблицы
    connection = sqlite3.connect("expenses.db")         # подключаемся к базе. Если файла нет, SQLite создаст его.
    cursor = connection.cursor()                        # инструмент, через который мы отправляем SQL-команды.
                                                        # CREATE TABLE IF NOT EXISTS expenses — создать таблицу expenses, если её ещё нет.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL
    )
    """)

    connection.commit()         # сохранить - закрыть
    connection.close()


def add_description_column() -> None:           # добавить новую колонку в существующую таблицу
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    try:            # Почему try/except: если ты запустишь программу второй раз, колонка уже будет существовать, и SQLite выдаст ошибку.
        cursor.execute("""
        ALTER TABLE expenses
        ADD COLUMN description TEXT NOT NULL DEFAULT ''
        """)
        # измени таблицу expenses - добавь колонку description - тип TEXT - значение по умолчанию — пустая строка

        connection.commit()
    except sqlite3.OperationalError:
        pass
    finally:
        connection.close()


def add_expense(title: str, amount: float, category: str, date: str, description: str) -> bool:       # добавить расход
    title = title.strip()               # убираем лишние пробелы
    category = category.strip().lower()
    date = date.strip()
    description = description.strip()

    if not title:           # если строка пустая — не добавляем расход.
        return False

    if amount <= 0:
        return False

    if not category:
        return False

    if not date:
        return False

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO expenses (title, amount, category, date, description)
    VALUES (?, ?, ?, ?, ?)
    """, (title, amount, category, date, description))

    connection.commit()         # сохраняет изменение в базе.
    connection.close()

    return True


def expense_exists(             # функция проверки существующего расхода.
    title: str,
    amount: float,
    category: str,
    date: str,
    description: str
) -> bool:
    title = title.strip()
    category = category.strip().lower()
    date = date.strip()
    description = description.strip()

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT 1
    FROM expenses
    WHERE title = ?
      AND amount = ?
      AND category = ?
      AND date = ?
      AND description = ?
    LIMIT 1
    """, (title, amount, category, date, description))
    # Мы не получаем весь расход, а только проверяем, есть ли подходящая запись.

    expense = cursor.fetchone()

    connection.close()

    return expense is not None


def get_expenses() -> list[tuple]:              # показать расходы из базы
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, title, amount, category, date, description
    FROM expenses
    ORDER BY date DESC, id DESC
    """)
    # ORDER BY date DESC - сортировка по дате
    # покажи только те строки, где category равна введённой категории
    # сначала новые даты, а внутри одной даты — новые добавленные расходы выше


    expenses = cursor.fetchall()        # забери все строки, которые нашёл SQL-запрос, и положи их в переменную expenses

    connection.close()

    return expenses


def search_expenses_by_title(query: str) -> list[tuple]:        # поиск расходов по названию title
    query = query.strip()           # убираем лишние пробелы

    if not query:           # если пользователь ничего не ввёл — возвращаем пустой список
        return []

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, title, amount, category, date, description
    FROM expenses
    WHERE title LIKE ?
    ORDER BY date DESC, id DESC
    """, (f"%{query}%",))
    # найти title, где "коф" есть где угодно внутри строки

    expenses = cursor.fetchall()

    connection.close()

    return expenses


def search_expenses_by_description(query: str) -> list[tuple]:          # функция поиска расходов по описанию.
    query = query.strip()

    if not query:
        return []

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, title, amount, category, date, description
    FROM expenses
    WHERE description LIKE ?
    ORDER BY date DESC, id DESC
    """, (f"%{query}%",))

    expenses = cursor.fetchall()

    connection.close()

    return expenses


def get_expenses_by_category(category: str) -> list[tuple]:         # фильтр расходов по категории.
    category = category.strip().lower()

    if not category:
        return []

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, title, amount, category, date, description
    FROM expenses
    WHERE category = ?
    ORDER BY date DESC, id DESC
    """, (category,))
    # покажи только те строки, где category равна введённой категории
    # сначала новые даты, а внутри одной даты — новые добавленные расходы выше

    expenses = cursor.fetchall()

    connection.close()

    return expenses


def get_categories() -> list[str]:              # список всех категорий
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT DISTINCT category
    FROM expenses
    ORDER BY category
    """)
    # получи уникальные категории из таблицы expenses

    categories = cursor.fetchall()      # fetchall() вернёт список кортежей

    connection.close()

    result = []

    for category in categories:         # А нам нужен обычный список строк
        result.append(category[0])

    return result


def get_expenses_by_month(month: str) -> list[tuple]:       # фильтр расходов по месяцу.
    month = month.strip()

    if not month:
        return []

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, title, amount, category, date, description
    FROM expenses
    WHERE date LIKE ?
    ORDER BY date DESC, id DESC
    """, (month + "%",))
    # покажи только те строки, где category равна введённой категории
    # сначала новые даты, а внутри одной даты — новые добавленные расходы выше


    expenses = cursor.fetchall()

    connection.close()

    return expenses


def get_total_by_month(month: str) -> float:        # сумму расходов за месяц.
    month = month.strip()

    if not month:
        return 0

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT SUM(amount)
    FROM expenses
    WHERE date LIKE ?
    """, (month + "%",))

    total = cursor.fetchone()[0]

    connection.close()

    if total is None:
        return 0

    return total


def get_total() -> float:               # общая сумма расходов
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT SUM(amount)
    FROM expenses
    """)
    # сложи все значения из колонки amount

    total = cursor.fetchone()[0]        # берёт из этого кортежа само число

    connection.close()

    if total is None:
        return 0

    return total


def get_totals_by_categories() -> list[tuple]:          # cумма по категориям
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT category, SUM(amount)
    FROM expenses
    GROUP BY category
    ORDER BY SUM(amount) DESC
    """)
    # сгруппируй расходы по category и для каждой категории посчитай сумму от самой большой суммы к меньшей

    totals = cursor.fetchall()

    connection.close()

    return totals


def get_total_by_category(category: str) -> float:          # общую сумму по категории
    category = category.strip().lower()

    if not category:
        return 0

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT SUM(amount)
    FROM expenses
    WHERE category = ?
    """, (category,))

    total = cursor.fetchone()[0]        # берёт из этого кортежа само число

    connection.close()

    if total is None:
        return 0

    return total


def get_expenses_count_by_month(month: str) -> int:         # вывод количества расходов в месяц
    month = month.strip()

    if not month:
        return 0

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM expenses
    WHERE date LIKE ?
    """, (month + "%",))
    # посчитать количество расходов, у которых дата начинается с выбранного месяца

    count = cursor.fetchone()[0]

    connection.close()

    return count


def get_average_expense_by_month(month: str) -> float:          # средний расход за месяц
    month = month.strip()

    if not month:
        return 0

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT AVG(amount)
    FROM expenses
    WHERE date LIKE ?
    """, (month + "%",))
    # посчитать среднее значение amount, только у расходов выбранного месяца

    average = cursor.fetchone()[0]

    connection.close()

    if average is None:
        return 0

    return average


def get_max_expense_by_month(month: str) -> tuple | None:       # самый большой расход за месяц
    month = month.strip()

    if not month:
        return None

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, title, amount, category, date, description
    FROM expenses
    WHERE date LIKE ?
    ORDER BY amount DESC
    LIMIT 1
    """, (month + "%",))
    # отсортировать расходы по сумме от большей к меньшей и взять только первый

    expense = cursor.fetchone()     # забирает одну строку, потому что мы ждём один расход

    connection.close()

    return expense


def get_min_expense_by_month(month: str) -> tuple | None:           # самый маленький расход за месяц
    month = month.strip()

    if not month:
        return None

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, title, amount, category, date, description
    FROM expenses
    WHERE date LIKE ?
    ORDER BY amount ASC
    LIMIT 1
    """, (month + "%",))

    expense = cursor.fetchone()

    connection.close()

    return expense


def get_totals_by_months() -> list[tuple]:          # итоговая сумма по месяцам
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT SUBSTR(date, 1, 7), SUM(amount)
    FROM expenses
    GROUP BY SUBSTR(date, 1, 7)
    ORDER BY SUBSTR(date, 1, 7) DESC
    """)
    # берёт из даты первые 7 символов.
    # сгруппируй расходы по месяцу

    totals = cursor.fetchall()

    connection.close()

    return totals


def delete_expense(expense_id: int) -> bool:        # удаление расхода по ID.
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM expenses
    WHERE id = ?
    """, (expense_id,))

    deleted_count = cursor.rowcount

    connection.commit()
    connection.close()

    return deleted_count > 0


def update_expense(                     # редактирование расхода по ID.
    expense_id: int,
    title: str,
    amount: float,
    category: str,
    date: str,
    description: str
) -> bool:
    title = title.strip()
    category = category.strip().lower()
    date = date.strip()
    description = description.strip()

    if not title:
        return False

    if amount <= 0:
        return False

    if not category:
        return False

    if not date:
        return False

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE expenses
    SET title = ?, amount = ?, category = ?, date = ?, description = ?
    WHERE id = ?
    """, (title, amount, category, date, description, expense_id))    
    # обнови расход с конкретным ID, замени ему title, amount, category и date
    # WHERE id = ? обязательно. Без него можно случайно обновить все расходы.

    updated_count = cursor.rowcount

    connection.commit()
    connection.close()

    return updated_count > 0














