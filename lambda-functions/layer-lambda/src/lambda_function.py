import json
import logging
import requests
from utils.helper import format_response, calculate_age

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """
    A Lambda function that uses Lambda layers for dependencies and local module imports.
    
    This function:
    1. Receives an event
    2. Uses the helper module from a local import
    3. Uses external dependencies from the Lambda layer
    4. Returns a formatted response
    """
    logger.info("Received event: %s", json.dumps(event))
    
    try:
        # Extract birth date from the event if provided
        birth_date = event.get('birthDate', '1990-01-01')
        
        # Calculate age using the helper function (demonstrates local import)
        age = calculate_age(birth_date)
        
        # Use requests from the Lambda layer
        response = requests.get('https://httpbin.org/uuid')
        uuid_data = response.json()
        
        # Create response using helper function
        return format_response(200, {
            'message': 'Lambda function with layers executed successfully',
            'age': age,
            'birthDate': birth_date,
            'uuid': uuid_data.get('uuid'),
            'event': event
        })
    except Exception as e:
        logger.error("Error: %s", str(e))
        return format_response(500, {
            'message': f'Error: {str(e)}'
        }) 