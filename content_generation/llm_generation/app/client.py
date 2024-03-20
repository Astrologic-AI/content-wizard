"""Example client file, placeholder for incoming code"""

from multi_inputs_chain import multi_input_chain
import random

# MULTI INPUT EXAMPLE
description = "Generate a string about an astrology Twitter post idea"
publish_date = "2024-03-09"
title = "Astrological Wellness"
platform = "Twitter"
max_characters = random.randint(150, 300)

config_dict = {
    "description": description,
    "publish_date": publish_date,
    "platform": platform,
    "title": title,
    "max_characters": max_characters,
    "extra_field": "I am extrafield",
}
a = multi_input_chain.invoke(config_dict)
print(a["response"].content)
# %%
# import requests
# Generate strings for the request
# multi_input_chain.batch([config_dict, config_dict])

# Server example
# response = requests.post(
#     "http://localhost:8000/generate_post_content/invoke",
#     json={"input": "Piscis Horoscope for 2024-03-09"},
# )
# print(response.content)
