# тест добавления и получения расхода

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import database


class TestDatabase(unittest.TestCase):

    def setUp(self):            # перед каждым тестом создаёт отдельную временную базу данных, чтобы не затронуть настоящие расходы.
        self.temp_directory = TemporaryDirectory()

        self.original_database_path = database.DATABASE_PATH

        database.DATABASE_PATH = (
            Path(self.temp_directory.name) / "test_expenses.db"
        )

        database.create_table()
        database.add_description_column()

    def tearDown(self):         # после каждого теста удаляет временную базу и возвращает программе настоящий путь к expenses.db.
        database.DATABASE_PATH = self.original_database_path
        self.temp_directory.cleanup()

    def test_add_and_get_expense(self):         # расход правильно добавляется в базу и затем читается из неё.
        database.add_expense(
            "Кофе",
            250,
            "кафе",
            "2026-07-22",
            "Капучино"
        )

        expenses = database.get_expenses()

        self.assertEqual(len(expenses), 1)

        expense = expenses[0]

        self.assertEqual(expense[1], "Кофе")
        self.assertEqual(expense[2], 250)
        self.assertEqual(expense[3], "кафе")
        self.assertEqual(expense[4], "2026-07-22")
        self.assertEqual(expense[5], "Капучино")

    
    def test_new_database_is_empty(self):           # новая тестовая база изначально пустая
        expenses = database.get_expenses()

        self.assertEqual(expenses, [])


    def test_expense_exists(self):          # функция правильно находит существующий расход и не находит несуществующий.
        database.add_expense(
            "Кофе",
            250,
            "кафе",
            "2026-07-22",
            "Капучино"
        )

        exists = database.expense_exists(
            "Кофе",
            250,
            "кафе",
            "2026-07-22",
            "Капучино"
        )

        not_exists = database.expense_exists(
            "Чай",
            100,
            "кафе",
            "2026-07-22",
            ""
        )

        self.assertTrue(exists)
        self.assertFalse(not_exists)


if __name__ == "__main__":
    unittest.main()