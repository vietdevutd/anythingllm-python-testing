import requests
import time 

API_URL = "http://localhost:3001/api/v1/workspace/sql2/chat"   #anythingllm api 
API_KEY = "your anythingLLM api"

def translate_natural_to_sql(input_text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "message": input_text,
        "mode": "query"
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        sql_query = response.json().get("textResponse")
        return sql_query
    else:
        print(f"Failed to translate: {response.status_code}, {response.text}")
        return None

input_text = "with provided schema, give me the user that name start with 'huy, return only SQL"

start_time = time.time()
sql_query = translate_natural_to_sql(input_text)
end_time = time.time()
total_time = end_time - start_time

if sql_query:
    print(f"Translated SQL Query: {sql_query}")
    print(f"Total response time: {total_time:.1f} seconds")
else:
    print(f"Failed to get SQL query. Total response time: {total_time:.1f} seconds")
