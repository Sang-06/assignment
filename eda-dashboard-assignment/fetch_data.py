import requests
import pandas as pd

def get_cleaned_data():
    url = "https://jsonplaceholder.typicode.com/posts"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            df = pd.DataFrame(response.json())
        else:
            print("Failed to fetch data")
            return pd.DataFrame()

    except requests.exceptions.RequestException:
        print("Connection error")
        return pd.DataFrame()

    # Rename userId to user_id
    df = df.rename(columns={'userId': 'user_id'})

    # Drop id column
    df = df.drop(columns=['id'])

    # Create post_length column
    df['post_length'] = df['body'].apply(len)

    return df
    