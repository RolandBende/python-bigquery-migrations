import os
import unittest
from src.bigquery_migrations.migration_log_handler import MigrationLogHandler


class MigrationLogHandlerTest(unittest.TestCase):
    
    def setUp(self):
        # Create a migrations dir path
        current_file_path = os.path.abspath(__file__)
        parent_dir = os.path.dirname(current_file_path)
        migrations_directory_name = "migrations"
        migrations_dir_path = os.path.join(parent_dir, migrations_directory_name)

        # Create an log handler instance
        self.under_test = MigrationLogHandler(migrations_dir_path)