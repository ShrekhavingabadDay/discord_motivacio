import json
import requests
import random

def get_cursed_image():

    r = requests.get("https://www.reddit.com/r/cursedimages/new/.json?limit=1000")

    j = json.loads(r.text)
    

    images = [ x["data"]["url_overridden_by_dest"] for x in j["data"]["children"] ]

    return random.choice(images)
