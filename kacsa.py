import requests;
import re;
import json;
import time;

def get_image_url(keywords, max_results=None):
    url = 'https://duckduckgo.com/';
    params = {
    	'q': keywords
    };

    res = requests.post(url, data=params)
    searchObj = re.search(r'vqd=([\d-]+)\&', res.text, re.M|re.I);

    headers = {
        'authority': 'duckduckgo.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-fetch-dest': 'empty',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://duckduckgo.com/',
        'accept-language': 'hu-HU,hu;q=0.9',
    }

    params = (
        ('l', 'hu-HU'),
        ('o', 'json'),
        ('q', keywords),
        ('vqd', searchObj.group(1)),
        ('f', ',,,'),
        ('p', '1'),
        ('v7exp', 'a'),
    )

    requestUrl = url + "i.js";

    res = requests.get(requestUrl, headers=headers, params=params);
    data = json.loads(res.text);

    # print(data["results"][0])
    try:
        return data["results"][0]["image"]
    except IndexError:
        return None

