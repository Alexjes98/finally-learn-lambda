import json
import requests
import logging
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw
import io
import base64

logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
        # Use BeautifulSoup to parse HTML content
        response = requests.get("https://example.com")
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