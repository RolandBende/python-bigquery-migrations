import os
import unittest
from unittest.mock import patch
from src.bigquery_migrations.migration_factory import MigrationFactory


class MigrationFactoryTest(unittest.TestCase):
    
    def setUp(self):
        # Create a mock GBQ client instance
        patcher = patch('google.cloud.bigquery.Client')
        self.mock_bigquery_client = patcher.start()
        self.addCleanup(patcher.stop)

        # Create a migrations dir path
        current_file_path = os.path.abspath(__file__)
        parent_dir = os.path.dirname(current_file_path)
        migrations_directory_name = "migrations"
        self.migrations_dir_path = os.path.join(parent_dir, migrations_directory_name)

    def test_generate_class_name_from_filename(self):
        under_test = MigrationFactory(self.mock_bigquery_client, self.migrations_dir_path)
        expected_value = 'CreateTableExample'
        current_value = under_test.generate_class_name_from_filename('2024_01_02_120000_create_table_example.py')
        self.assertEqual(expected_value, current_value)