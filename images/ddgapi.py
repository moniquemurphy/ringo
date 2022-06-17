import requests
import re
import json
import time
import logging
import shutil
from random import randint

def search_image(keywords, country_code, max_results=None):
    url = 'https://duckduckgo.com/'
    params = {
        'q': keywords
    };

    #   First make a request to above URL, and parse out the 'vqd'
    #   This is a special token, which should be used in the subsequent request
    res = requests.post(url, data=params)
    searchObj = re.search(r'vqd=([\d-]+)\&', res.text, re.M|re.I);

    if not searchObj:
        return -1;

    headers = {
        'authority': 'duckduckgo.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-fetch-dest': 'empty',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://duckduckgo.com/',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('l', country_code),
        ('o', 'json'),
        ('q', keywords),
        ('vqd', searchObj.group(1)),
        ('f', ',,,'),
        ('p', '1'),
        ('v7exp', 'a'),
    )

    request_url = url + "i.js"

    # Get results from the first page, pick a random image
    # logger.debug("Hitting Url : %s", request_url)

    while True:
        try:
            res = requests.get(request_url, headers=headers, params=params)
            data = json.loads(res.text)
            break
        except (ValueError, ConnectionError, TimeoutError) as e:
            print("Sleeping...")
            time.sleep(5)
            continue

    if len(data["results"]) > 0:
        image_saved = pick_random_image(data["results"], keywords)
        if image_saved:
            return True
        else:
            print("Trying again...")
            pick_random_image(data["results"], keywords)
    else:
        return False

def pick_random_image(objs, keyword):
    index = randint(0, 10)
    image_saved = save_image(objs[index]["image"], keyword)
    return image_saved

def save_image(image_url, keyword):
    # Always save as ".jpg", no matter the original extension. This makes automating cards importing into Anki much easier.

    filename = keyword + ".jpg"
    path = "images/" + filename
    try:
        r = requests.get(image_url, stream=True)
        r.raise_for_status()

        r.raw.decode_content = True

        with open(path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print("Image saved: ", filename)
        return True
    except (requests.HTTPError, requests.exceptions.SSLError, requests.exceptions.ConnectionError, TimeoutError, requests.exceptions.ReadTimeout):
        return False