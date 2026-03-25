import os
import requests

api_key = os.getenv("API_KEY")

url = "https://api.example.com/data"

headers = {
    "Authorization": f"Bearer {api_key}"
}

try:
    # Step 4: send GET request
    response = requests.get(url, headers=headers)

    # Step 5: Handle status codes
    if response.status_code == 200:
        print(response.json())

    elif response.status_code == 429:
        print("Rate limit reached. Try again later.")

    else:
        print("Request failed", response.status_code)

except requests.exceptions.RequestException:
    print("Request failed due to connection error")


