import json
import requests
from datetime import datetime
from dateutil.parser import parse
import jwt
from utils.helpers import format_response, process_data

def validate_event(event: dict) -> tuple[bool, str]:
    """
    Simple event validation without using Pydantic
    """
    required_fields = ['user_id', 'action']
    for field in required_fields:
        if not event.get("body", {}).get(field):
            return False, f"Missing required field: {field}"
    return True, ""

def handler(event: dict, context) -> dict:
    """
    A simple Lambda function demonstrating various Python packages.
    
    Features:
    1. Basic request validation
    2. HTTP requests with the requests library
    3. Date parsing with dateutil
    4. JWT token generation
    5. Local utility usage
    """
    print(event)
    try:
        # Validate incoming event
        is_valid, error_message = validate_event(event)
        if not is_valid:
            raise ValueError(error_message)
        
        # Extract and validate event data
        user_id = event.get('user_id', '')
        action = event.get('action', '')
        timestamp = event.get('timestamp', datetime.now().isoformat())
        
        # Parse and format the timestamp
        parsed_timestamp = parse(timestamp)
        
        # Make an example HTTP request
        response = requests.get('https://httpbin.org/uuid')
        request_id = response.json().get('uuid', '')
        
        # Generate a sample JWT token
        token_payload = {
            'user_id': user_id,
            'action': action,
            'timestamp': parsed_timestamp.isoformat(),
            'request_id': request_id
        }
        jwt_token = jwt.encode(
            token_payload,
            'your-secret-key',  # In production, use AWS Secrets Manager
            algorithm='HS256'
        )
        
        # Process data using local utility
        processed_event = process_data(event)
        
        # Prepare response
        response_body = {
            'message': 'Lambda function executed successfully',
            'processed_timestamp': parsed_timestamp.isoformat(),
            'request_id': request_id,
            'jwt_token': jwt_token,
            'processed_event': processed_event
        }
        
        print(f"Successfully processed request for user_id: {user_id}, action: {action}")
        
        return format_response(200, json.dumps(response_body))
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        error_response = {
            'message': f'Error: {str(e)}'
        }
        return format_response(500, json.dumps(error_response)) 