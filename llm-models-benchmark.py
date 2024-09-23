import requests
import time
#install pandas:
# pip install pandas
import pandas as pd

API_KEY = 'AnythingLLM_API_KEY'

def post_to_anythingllm(workspace: str, message: str, mode: str = "query"):
    url = f"http://localhost:3001/api/v1/workspace/{workspace}/chat"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "message": message,
        "mode": mode
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json().get("textResponse")
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

def measure_execution_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time

def main():
    message = "With provided schema, give me all users that have name start with huy"
    workspaces = ["llama3-dot-1-stock-sql-coder", "llama3-sql-coder"]  # Add more workspaces as needed

    results = []  # List to hold results for each workspace

    for workspace in workspaces:
        print(f"\nMeasuring time for workspace: {workspace}")
        result, exec_time = measure_execution_time(post_to_anythingllm, workspace, message)
        
        if result is not None and "Request failed" not in result:
            results.append({"Workspace": workspace, "Result": result, "Execution Time (seconds)": f"{exec_time:.2f}"})
        else:
            print(f"Failed to get a valid response from {workspace}")

    # Create a DataFrame from the results
    df = pd.DataFrame(results)
    print("\nResults:")
    print(df)

if __name__ == "__main__":
    main()
