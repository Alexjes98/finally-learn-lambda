import json
import requests
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """
    A simple Lambda function that uses external dependencies.
    
    This function:
    1. Receives an event
    2. Makes an HTTP request using the requests library
    3. Creates a pandas DataFrame and performs a simple calculation
    4. Returns a formatted response
    """
    logger.info("Received event: %s", json.dumps(event))
    
    try:
        # Use the requests library to make an HTTP request
        response = requests.get("https://httpbin.org/json")
        response_data = response.json()
        
        # Use pandas and numpy to perform a simple calculation
        df = pd.DataFrame({
            'numbers': np.random.randint(0, 100, size=5)
        })
        mean_value = df['numbers'].mean()
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Plain Lambda function executed successfully',
                'mean_value': float(mean_value),
                'http_response': response_data,
                'event': event
            })
        }
    except Exception as e:
        logger.error("Error: %s", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Error: {str(e)}'
            })
        } 