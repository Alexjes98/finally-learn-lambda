import json
import datetime
import dateutil.parser
from dateutil.relativedelta import relativedelta

def format_response(status_code, body):
    """
    Helper function to format Lambda responses.
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }

def parse_date(date_string):
    """
    Parse a date string using dateutil from the Lambda layer.
    """
    try:
        return dateutil.parser.parse(date_string)
    except Exception:
        return None

def calculate_age(birth_date_string):
    """
    Calculate age from a birthdate string.
    """
    if not birth_date_string:
        return None
    
    birth_date = parse_date(birth_date_string)
    if not birth_date:
        return None
    
    today = datetime.datetime.now()
    age = relativedelta(today, birth_date).years
    
    return age 