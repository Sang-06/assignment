import requests

url = "https://api.github.com/search/repositories"

params = {
    "q": "python",
    "sort": "stars",
    "order": "desc",
    "per_page": 5
}

response = requests.get(url, params=params)

data = response.json()

for repo in data["items"]:
    print("Repository:", repo["name"])
    print("Stars:", repo["stargazers_count"])
    print("-" * 30)
