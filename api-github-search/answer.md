# API GitHub Search – Answers

## 1. What is the role of query parameters in this request?

Query parameters are used to send additional information to the API to customize the request.

In this example:
- q=python → searches for repositories related to Python
- sort=stars → sorts repositories by number of stars
- order=desc → shows results in descending order
- per_page=5 → limits the results to 5 repositories

---

## 2. Why do we use response.json() instead of response.text?

We use response.json() because it converts the API response into a Python dictionary.

This makes it easier to access and work with data.

response.text gives raw text which is harder to use.