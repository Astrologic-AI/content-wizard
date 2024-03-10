"""Example client file, placeholder for incoming code"""

import requests

response = requests.post(
    "http://localhost:8000/generate_post_content/invoke",
    json={"input": "Piscis great sign"},
)
result = response.json()
print(result)
