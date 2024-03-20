"""Example client file, placeholder for incoming code"""

# %%
import requests
from multi_inputs_chain import multi_input_chain

# %%
# Server example
response = requests.post(
    "http://localhost:8000/generate_post_content/invoke",
    json={"input": "Piscis Horoscope for 2024-03-09"},
)
print(response.content)
# %%
# MULTI INPUT INOKE/BATCH EXAMPLE
# Generate strings for the request

description = "Generate a string about an astrology Twitter post idea"
publish_date = "2024-03-09"
title = "Astrological Wellness"
platform = "Twitter"

config_dict = {
    "description": description,
    "publish_date": publish_date,
    "platform": platform,
    "title": title,
    "extra_field": "I am extrafield",
}

a = multi_input_chain.invoke(config_dict)
print(a["response"])
#%%
multi_input_chain.batch([config_dict, config_dict])
