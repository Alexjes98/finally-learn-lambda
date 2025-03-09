# Function tested correctly

The function correctly tested on AWS


## Result:

```shell
{
  "statusCode": 200,
  "body": "{\"message\": \"Lambda function executed successfully\", \"processed_timestamp\": \"2025-03-09T17:46:34.446099\", \"request_id\": \"e20fdbbb-13a7-4e47-9f5b-da914179ea09\", \"jwt_token\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiIiwiYWN0aW9uIjoiIiwidGltZXN0YW1wIjoiMjAyNS0wMy0wOVQxNzo0NjozNC40NDYwOTkiLCJyZXF1ZXN0X2lkIjoiZTIwZmRiYmItMTNhNy00ZTQ3LTlmNWItZGE5MTQxNzllYTA5In0.u5k6MJX7sloYPpJVu-GZGtgQcO3-pdOu8gDx2oYhnLY\", \"processed_event\": {\"HTTPMETHOD\": \"GET\", \"PATH\": \"/\", \"QUERYSTRINGPARAMETERS\": {\"name\": \"User\"}, \"HEADERS\": {\"Content-Type\": \"application/json\"}, \"BODY\": {\"user_id\": \"123\", \"action\": \"test\"}, \"ISBASE64ENCODED\": false, \"BIRTHDATE\": \"1990-05-15\"}}"
}
```

## Log Output 

```shell
START RequestId: 9bc79658-c3dd-4d20-8a0d-2eb3f397ebf6 Version: $LATEST
{'httpMethod': 'GET', 'path': '/', 'queryStringParameters': {'name': 'User'}, 'headers': {'Content-Type': 'application/json'}, 'body': {'user_id': '123', 'action': 'test'}, 'isBase64Encoded': False, 'birthDate': '1990-05-15'}
Successfully processed request for user_id: , action: 
END RequestId: 9bc79658-c3dd-4d20-8a0d-2eb3f397ebf6
REPORT RequestId: 9bc79658-c3dd-4d20-8a0d-2eb3f397ebf6	Duration: 135.06 ms	Billed Duration: 136 ms	Memory Size: 256 MB	Max Memory Used: 58 MB	Init Duration: 432.13 ms
```