import requests

# Setup correct API URL
API_URL = "hhttp://localhost:3001/api/v1/workspace/Jobify/chat"  # Check if this should be 'chat' or another endpoint like 'extract'
API_KEY = "AnythingAPIKey"

# Function to send resume details for extraction
def extract_resume_details(workspace_slug, resume_data):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Adjust payload to match the expected request body structure
    data = {
        "message": resume_data,
        "mode": "query",  # Change to "chat" if the interaction is conversational
        "sessionId": f"session_{workspace_slug}"  # Create a session ID if needed
    }

    try:
        response = requests.post(API_URL, json=data, headers=headers)
        response.raise_for_status()  # Raises an exception for HTTP errors
        return response.json()       # Parse the response JSON
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")

if __name__ == "__main__":
    resume_data = "John Doe, Developer, 5 years experience in Python, Java. Phone: 123-456-7890"

    extracted_data = extract_resume_details("Jobify", resume_data)

    if extracted_data:
        print(f"Extracted Data: {extracted_data}")
    else:
        print("No data found or an error occurred.")