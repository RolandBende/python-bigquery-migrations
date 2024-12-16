from google.cloud import bigquery
from src.bigquery_migrations.migration import Migration

class CreateDatasetExample(Migration):
    """
    See:
    https://github.com/googleapis/python-bigquery/tree/main/samples
    """

    def up(self):
        # TODO: Set dataset_id to the ID of the dataset to create.
        # dataset_id = "{}.your_dataset".format(self.client.project)
        
        # TODO: Construct a full Dataset object to send to the API.
        # dataset = bigquery.Dataset(dataset_id)
        
        # TODO: Specify the geographic location where the dataset should reside.
        # dataset.location = "EU"
        
        # Send the dataset to the API for creation, with an explicit timeout.
        # Raises google.api_core.exceptions.Conflict if the Dataset already
        # exists within the project.
        # dataset = self.client.create_dataset(dataset, timeout=30)
        class_name = self.__class__.__name__
        print(f"Class: {class_name}, Method: up")

    def down(self):
        # TODO: Set dataset_id to the ID of the dataset to fetch.
        # dataset_id = 'your-project.your_dataset'
        
        # Use the delete_contents parameter to delete a dataset and its contents.
        # Use the not_found_ok parameter to not receive an error if the dataset has already been deleted.
        '''
        self.client.delete_dataset(
            dataset_id, delete_contents=True, not_found_ok=True
        )
        '''
        class_name = self.__class__.__name__
        print(f"Class: {class_name}, Method: down")