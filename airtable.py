import os
from pyairtable import Table
import json
import time
import get_proxy
import fragpage
from pprint import pprint

# TODO fix no spaces at line break in 3kcoments
# TODO 10k review characters
# TODO sumarise sliders into 'sprint/summer, all year, ' based on fields under lits artile item

api_key = 'keyYswtVaqDhfXOjg'
table = Table(api_key, 'appPRMsLKzXB2CU3I', 'Fragrantica API Import copy copy')

records = table.all(formula='({comments3k} = BLANK())', sort=["-recent_magnitude"])
for i, record in enumerate(records):

    airtable_id = record["id"]
    fragrantica_url = record["fields"]["url"]
    proxy = get_proxy.random_proxy()

    # fragrantica_url = "https://www.fragrantica.com/perfume/Ariana-Grande/Cloud-50384.html"

    try:
        frag = fragpage.scrape_page(proxy, fragrantica_url)
    except Exception as e:
        print('error scraping')
        print(e)
        continue
    print('saving to airtable..')
    try:
        table.update(airtable_id, {
            "comments3k": frag["comments3k"],
            "description": frag["description"],
            "group": frag["group"],
            "quote": frag["quote"],
            "perfumers": frag["perfumers"],
            "accords": frag["accords"],
            "love": float(frag["love"]),
            "like": float(frag["like"]),
            "ok": float(frag["ok"]),
            "dislike": float(frag["dislike"]),
            "hate": float(frag["hate"]),
            "winter": float(frag["winter"]),
            "spring": float(frag["spring"]),
            "summer": float(frag["summer"]),
            "fall": float(frag["fall"]),
            "day": float(frag["day"]),
            "night": float(frag["night"]),
            "top_notes": frag["top_notes"],
            "middle_notes": frag["middle_notes"],
            "base_notes": frag["base_notes"],
            "loose_notes": frag["loose_notes"],
            "all_notes": frag["all_notes"],
            "longevity_very_weak": float(frag["longevity_very_weak"]),
            "longevity_weak": float(frag["longevity_weak"]),
            "longevity_moderate": float(frag["longevity_moderate"]),
            "longevity_long_lasting": float(frag["longevity_long_lasting"]),
            "longevity_eternal": float(frag["longevity_eternal"]),
            "sillage_intimate": float(frag["sillage_intimate"]),
            "sillage_moderate": float(frag["sillage_moderate"]),
            "sillage_strong": float(frag["sillage_strong"]),
            "sillage_enormous": float(frag["sillage_enormous"]),
            "gender_female": float(frag["gender_female"]),
            "gender_more_female": float(frag["gender_more_female"]),
            "gender_unisex": float(frag["gender_unisex"]),
            "gender_more_male": float(frag["gender_more_male"]),
            "gender_male": float(frag["gender_male"]),
            "price_value_way_overpriced": float(frag["price_value_way_overpriced"]),
            "price_value_overpriced": float(frag["price_value_overpriced"]),
            "price_value_ok": float(frag["price_value_ok"]),
            "price_value_good_value": float(frag["price_value_good_value"]),
            "price_value_great_value": float(frag["price_value_great_value"])
            })
        print('airtable updated successfuly')
        # exit()
    except Exception as e:
        print('error saving to airtable')
        print(e)
        continue
