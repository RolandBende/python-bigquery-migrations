import os
import unittest
from unittest.mock import patch
import io
from contextlib import redirect_stdout
from src.bigquery_migrations.migration_manager import MigrationManager


class MigrationManagerTest(unittest.TestCase):
    
    def setUp(self):
        # Create a trap to suppress print output 
        self.text_trap = io.StringIO()

        # Create a mock GBQ client instance
        patcher = patch('google.cloud.bigquery.Client')
        self.mock_bigquery_client = patcher.start()
        self.addCleanup(patcher.stop)

        # Create a migrations dir path
        current_file_path = os.path.abspath(__file__)
        parent_dir = os.path.dirname(current_file_path)
        migrations_directory_name = "migrations"
        self.migrations_dir_path = os.path.join(parent_dir, migrations_directory_name)

    def test_00_list_migrations(self):
        migration_manager = MigrationManager(self.mock_bigquery_client, self.migrations_dir_path)
        expected_value = [
            "2024_01_01_120000_create_dataset_example",
            "2024_01_02_120000_create_table_example",
            "2024_01_03_120000_create_table_from_json_schema_example",
            "2024_01_04_120000_create_another_table_example"
        ]
        current_value = migration_manager.list_migrations()
        self.assertEqual(expected_value, current_value)

    def test_01_run(self):
        migration_manager = MigrationManager(self.mock_bigquery_client, self.migrations_dir_path)
        with redirect_stdout(self.text_trap):
            current_value = migration_manager.run()
        self.assertEqual(type([]), type(current_value))
        last_migration, last_timestamp = migration_manager.get_last_migration()
        self.assertEqual("2024_01_04_120000_create_another_table_example", last_migration)

    def test_02_rollback_from_the_last(self):
        migration_manager = MigrationManager(self.mock_bigquery_client, self.migrations_dir_path)
        migrateFrom = "2024_01_04_120000_create_another_table_example"
        migrateTo = "2024_01_03_120000_create_table_from_json_schema_example"
        with redirect_stdout(self.text_trap):
            return_value = migration_manager.rollback_last()
        self.assertEqual(type(()), type(return_value))
        rolledback, actual = return_value
        self.assertEqual(migrateFrom, rolledback)
        self.assertEqual(migrateTo, actual)
    
    def test_03_rollback_specified(self):
        migration_manager = MigrationManager(self.mock_bigquery_client, self.migrations_dir_path)
        migrateFrom = "2024_01_03_120000_create_table_from_json_schema_example"
        migrateTo = "2024_01_02_120000_create_table_example"
        with redirect_stdout(self.text_trap):
            return_value = migration_manager.rollback(migrateFrom)
        self.assertEqual(type(()), type(return_value))
        rolledback, actual = return_value
        self.assertEqual(migrateFrom, rolledback)
        self.assertEqual(migrateTo, actual)
    
    def test_04_rollback_no_more_left(self):
        migration_manager = MigrationManager(self.mock_bigquery_client, self.migrations_dir_path)
        migrateFrom = "2024_01_01_120000_create_dataset_example"
        migrateTo = None
        with redirect_stdout(self.text_trap):
            current_value = migration_manager.rollback(migrateFrom)
        self.assertEqual(type(()), type(current_value))
        rolledback, actual = current_value
        self.assertEqual(migrateFrom, rolledback)
        self.assertEqual(migrateTo, actual)
    
    def test_05_reset(self):
        migration_manager = MigrationManager(self.mock_bigquery_client, self.migrations_dir_path)
        with redirect_stdout(self.text_trap):
            current_value = migration_manager.reset()
        self.assertEqual(type([]), type(current_value))
        last_migration, last_timestamp = migration_manager.get_last_migration()
        self.assertEqual(None, last_migration)

if __name__ == "__main__":
    unittest.main()