import unittest
from unittest.mock import MagicMock, patch
import json
import azure.functions as func
from azure.cosmos import exceptions

# Import your actual function
from get_visitor_count import main 

class TestVisitorCounter(unittest.TestCase):

    @patch('get_visitor_count.CosmosClient')
    def test_successful_increment(self, mock_client_class):
        """Test that the counter increments correctly when item exists."""
        
        # 1. Setup Mocks
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        mock_db = MagicMock()
        mock_container = MagicMock()
        
        mock_client.get_database_client.return_value = mock_db
        mock_db.get_container_client.return_value = mock_container
        
        # Mock the existing item in DB
        existing_item = {"id": "1", "count": 5}
        mock_container.read_item.return_value = existing_item
        
        # Mock environment variables
        with patch.dict('os.environ', {
            'COSMOS_ENDPOINT': 'https://fake.endpoint.com',
            'COSMOS_KEY': 'fake-key',
            'DATABASE_NAME': 'azure-cv',
            'APP_CONTAINER_NAME': 'Counter'
        }):
            # 2. Create a Fake HTTP Request (Added body=b'')
            req = func.HttpRequest(method='GET', url='http://localhost/api/main', body=b'')
            
            # 3. Execute the function
            response = main(req)
            
            # 4. Assertions
            self.assertEqual(response.status_code, 200)
            
            # Parse response body
            body = json.loads(response.get_body().decode('utf-8'))
            self.assertEqual(body['count'], 6) # 5 + 1
            
            # Verify Cosmos DB interactions
            mock_container.read_item.assert_called_once_with(item='1', partition_key='1')
            mock_container.upsert_item.assert_called_once()
            
            # Verify the updated item passed to upsert
            updated_item = mock_container.upsert_item.call_args[1]['body']
            self.assertEqual(updated_item['count'], 6)

    @patch('get_visitor_count.CosmosClient')
    def test_counter_not_found_creates_new(self, mock_client_class):
        """Test behavior when the Counter item does not exist (creates new)."""
        
        # Setup Mocks
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_db = MagicMock()
        mock_container = MagicMock()
        
        mock_client.get_database_client.return_value = mock_db
        mock_db.get_container_client.return_value = mock_container
        
        # Simulate "Item Not Found"
        mock_container.read_item.side_effect = exceptions.CosmosResourceNotFoundError(status_code=404, message="Not Found")
        
        # Mock environment variables
        with patch.dict('os.environ', {
            'COSMOS_ENDPOINT': 'https://fake.endpoint.com',
            'COSMOS_KEY': 'fake-key',
            'DATABASE_NAME': 'azure-cv',
            'APP_CONTAINER_NAME': 'Counter'
        }):
            # Added body=b''
            req = func.HttpRequest(method='GET', url='http://localhost/api/main', body=b'')
            response = main(req)
            
            self.assertEqual(response.status_code, 200)
            body = json.loads(response.get_body().decode('utf-8'))
            self.assertEqual(body['count'], 1) # Starts at 0, increments to 1
            
            # Verify create_item was called
            mock_container.create_item.assert_called_once()

    @patch('get_visitor_count.CosmosClient')
    def test_missing_credentials_returns_error(self, mock_client_class):
        """Test that missing env vars return 500 error."""
        
        # Clear env vars
        with patch.dict('os.environ', {}, clear=True):
            # Added body=b''
            req = func.HttpRequest(method='GET', url='http://localhost/api/main', body=b'')
            response = main(req)
            
            self.assertEqual(response.status_code, 500)
            body = json.loads(response.get_body().decode('utf-8'))
            self.assertIn("error", body)

if __name__ == '__main__':
    unittest.main()