import json
import requests
import logging
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw
import io
import base64
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Event(BaseModel):
    user_id: str = Field(..., description="The user ID")
    action: str = Field(..., description="The action to perform")
    
def validate_event(event: dict) -> tuple[bool, str]:
    """
    Validate the event using Pydantic
    """
    try:
        logger.info("Validating event: %s", json.dumps(event))
        body = event.get("body", {})
        Event(**body)
        return True, ""
    except ValidationError as e:
        return False, str(e)

def handler(event, context):
    """
    A Lambda function packaged as a Docker image.
    
    This function:
    1. Receives an event
    2. Makes an HTTP request and parses HTML content with BeautifulSoup
    3. Creates a simple image using Pillow
    4. Returns a formatted response with the generated image as base64
    """
    logger.info("Received event: %s", json.dumps(event))
    
    try:
        is_valid, error_message = validate_event(event)
        if not is_valid:
            raise ValueError(error_message)
           
        user_id = event.get("body", {}).get("user_id")
        action = event.get("body", {}).get("action")
        logger.info("User ID: %s, Action: %s", user_id, action)
        # Use BeautifulSoup to parse HTML content
        response = requests.get("https://www.google.com")
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string
        
        # Create a simple image using Pillow
        img = Image.new('RGB', (300, 100), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((10, 10), "Docker Lambda Function", fill=(255, 255, 0))
        d.text((10, 50), f"Parsed Title: {title[:20]}...", fill=(255, 255, 0))
        
        # Convert image to base64
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': 'Docker Lambda function executed successfully',
                'parsed_title': title,
                'image': img_str,
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