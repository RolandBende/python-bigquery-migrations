import os
import unittest
from src.bigquery_migrations.migration_dir_handler import MigrationDirHandler


class MigrationDirHandlerTest(unittest.TestCase):
    
    def setUp(self):
        # Create a migrations dir path
        current_file_path = os.path.abspath(__file__)
        parent_dir = os.path.dirname(current_file_path)
        migrations_directory_name = "migrations"
        self.migrations_dir_path = os.path.join(parent_dir, migrations_directory_name)

    def test_check(self):
        not_existing_dir_path = 'not-existing-dir-path'
        with self.assertRaises(FileNotFoundError) as context:
            MigrationDirHandler.check(not_existing_dir_path)
        self.assertEqual("Migration directory not found: "+not_existing_dir_path, str(context.exception))
    
    def test_filename_list(self):
        under_test = MigrationDirHandler(self.migrations_dir_path)
        expected_value = [
            "2024_01_01_120000_create_dataset_example",
            "2024_01_02_120000_create_table_example",
            "2024_01_03_120000_create_table_from_json_schema_example"
        ]
        current_value = under_test.filename_list()
        self.assertEqual(expected_value, current_value)