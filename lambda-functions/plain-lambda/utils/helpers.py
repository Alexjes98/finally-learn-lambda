def format_response(status_code, body):
    """Helper function to format Lambda responses"""
    return {
        'statusCode': status_code,
        'body': body
    }

def process_data(input_data):
    """Example data processing function"""
    # Simple data transformation
    if isinstance(input_data, dict):
        processed = {k.upper(): v.upper() if isinstance(v, str) else v 
                    for k, v in input_data.items()}
        return processed
    return input_data 