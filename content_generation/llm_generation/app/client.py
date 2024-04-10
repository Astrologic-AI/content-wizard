"""Example client file, placeholder for incoming code"""

from multi_inputs_chain import multi_input_chain
import random

# MULTI INPUT EXAMPLE
description = "Alignment of stars and planets influences your life's journey"
publish_date = "2024-04-11"
title = "Unlock Your Cosmic Potential"
platform = "Twitter"
max_characters = random.randint(300, 500)
instruction = "Navigate scientific astrology websites to find articles on planetary positions. Gather accurate data on major celestial bodies."

config_dict = {
    "description": description,
    "publish_date": publish_date,
    "platform": platform,
    "title": title,
    "max_characters": max_characters,
    "extra_field": "I am extrafield",
}

enhanced_config_dict = {
    **config_dict,
    "info_to_search": f"{instruction} {description} {config_dict['publish_date']}"
}

a = multi_input_chain.batch([enhanced_config_dict, enhanced_config_dict])
[print(a[i]["response"].content) for i in range(0, len(a))]
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
