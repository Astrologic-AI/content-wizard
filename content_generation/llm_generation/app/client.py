"""Example client file, placeholder for incoming code"""

import requests

response = requests.post(
    "http://localhost:8000/generate_post_content/invoke",
    json={"input": "Piscis Horoscope for 2024-03-09"},
)
result = response.json()["output"]

# Print result in green
print("\033[92m" + result + "\033[0m")
