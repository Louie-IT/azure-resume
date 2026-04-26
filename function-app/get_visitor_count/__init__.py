import logging
import os
import json
import azure.functions as func
from azure.cosmos import CosmosClient, exceptions

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Read environment variables
    endpoint = os.environ.get("COSMOS_ENDPOINT")
    key = os.environ.get("COSMOS_KEY")
    db_name = os.environ.get("DATABASE_NAME")
    container_name = os.environ.get("APP_CONTAINER_NAME")

    if not endpoint or not key or not container_name:
        return func.HttpResponse(json.dumps({"error": "Missing credentials"}), status_code=500)

    try:
        client = CosmosClient(endpoint, credential=key)
        db = client.get_database_client(db_name)
        container = db.get_container_client(container_name)

        try:
            # Try to read the item
            response = container.read_item(item='1', partition_key='1')
            current_count = response.get('count', 0)
        except exceptions.CosmosResourceNotFoundError:
            # Item doesn't exist, create it with count 0
            logging.info("Counter item not found. Creating new one.")
            response = container.create_item(body={"id": "1", "count": 0})
            current_count = 0

        # Increment
        new_count = current_count + 1
        response['count'] = new_count
        
        # Save
        container.upsert_item(body=response)

        return func.HttpResponse(
            json.dumps({"count": new_count}),
            status_code=200,
            headers={"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
        )

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)