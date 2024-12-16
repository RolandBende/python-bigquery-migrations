from google.cloud import bigquery
from src.bigquery_migrations.migration import Migration

class CreateTableFromJsonSchemaExample(Migration):
    """
    See:
    https://github.com/googleapis/python-bigquery/tree/main/samples
    """

    def up(self):
        # TODO: Set table_id to the ID of the table to create.
        # table_id = "your_project.your_dataset.example_table"
        
        # TODO: Change schema_path variable to the path of your schema file.
        # schema_path = "path/to/schema.json"
        # To load a schema file use the schema_from_json method.
        # schema = self.client.schema_from_json(schema_path)
    
        # table = bigquery.Table(table_id, schema=schema)
        # table = self.client.create_table(table)
        class_name = self.__class__.__name__
        print(f"Class: {class_name}, Method: up")

    def down(self):
        # TODO: Set table_id to the ID of the table to fetch.
        # table_id = "your_project.your_dataset.example_table"
        
        # If the table does not exist, delete_table raises
        # google.api_core.exceptions.NotFound unless not_found_ok is True.
        # self.client.delete_table(table_id, not_found_ok=True)
        class_name = self.__class__.__name__
        print(f"Class: {class_name}, Method: down")