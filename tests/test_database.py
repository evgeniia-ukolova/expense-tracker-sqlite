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


    def test_update_expense(self):          # расход по ID успешно редактируется и все новые значения сохраняются в базе.
        database.add_expense(
            "Кофе",
            250,
            "кафе",
            "2026-07-22",
            "Капучино"
        )

        expense_id = database.get_expenses()[0][0]

        updated = database.update_expense(
            expense_id,
            "Такси",
            500,
            "Транспорт",
            "2026-07-23",
            "Поездка домой"
        )

        expenses = database.get_expenses()
        expense = expenses[0]

        self.assertTrue(updated)
        self.assertEqual(expense[1], "Такси")
        self.assertEqual(expense[2], 500)
        self.assertEqual(expense[3], "транспорт")
        self.assertEqual(expense[4], "2026-07-23")
        self.assertEqual(expense[5], "Поездка домой")


    def test_delete_expense(self):          # расход по ID успешно удаляется и база после удаления становится пустой.
        database.add_expense(
            "Кофе",
            250,
            "кафе",
            "2026-07-22",
            "Капучино"
        )

        expense_id = database.get_expenses()[0][0]

        deleted = database.delete_expense(expense_id)
        expenses = database.get_expenses()

        self.assertTrue(deleted)
        self.assertEqual(expenses, [])


if __name__ == "__main__":
    unittest.main()