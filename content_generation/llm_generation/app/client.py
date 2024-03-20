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
post_idea_description = "Generate a string about an astrology Twitter post idea"
post_date = "2024-03-09"
post_idea_title = "Astrology Twitter Post Idea"
platform = "Twitter"

config_dict = {
    "post_idea_description": post_idea_description,
    "post_date": post_date,
    "platform": platform,
    "post_idea_title": post_idea_title,
    "extra_field": "I am extrafield",
}


a = multi_input_chain.invoke(config_dict)
print(a["response"])
#%%
multi_input_chain.batch([config_dict, config_dict])

config_dict = {
    "description": post_idea_description,
    "platform": "Twitter",
    "publish_date": post_date,
    "title": post_idea_title,
}

