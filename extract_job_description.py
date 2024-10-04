import requests
import time
import json

API_URL = "http://localhost:3001/api/v1/workspace/llama3-dot-2/chat"
API_KEY = "anything llm key"
def extract_job_desc(input):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "message": input,
        "mode": "chat"
    }
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        job_desc_json = response.json().get("textResponse")
        if job_desc_json:
            try:
                job_desc_dict = json.loads(job_desc_json)
                return job_desc_dict
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
        else:
            print("No 'textResponse' in the response JSON.")
    else:
        print(f"Failed to translate: {response.status_code}, {response.text}")
        return None
# need to append job description to have values
input = """
extract company name, skillsets, exp requirement, education requirement, work location as JSON output
"""

start_time = time.time()
job_desc_dict = extract_job_desc(input)
end_time = time.time()
total_time = end_time - start_time

if job_desc_dict:
    print(f"JSON Job Description Output: {job_desc_dict}")
    print(f"Total response time: {total_time:.1f} seconds")
else:
    print(f"Failed to get job description. Total response time: {total_time:.1f} seconds")