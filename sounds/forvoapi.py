import os
import requests
import re
import json
import time
import shutil
from random import randint

def search_sound(word, language_code):
    url = 'https://apifree.forvo.com/key/' + os.environ.get('FORVO_API_KEY') + '/format/json/action/word-pronunciations/word/' + word + '/language/' + language_code

    res = requests.get(url, verify='forvo-com-chain.pem')
    data = json.loads(res.text)

    # save a random production to sounds/ directory
    num_productions=data["attributes"]["total"]
    if num_productions > 0:
        index = randint(0, num_productions-1)
        grab_sound_url = data["items"][index]["pathmp3"]
        return save_sound(grab_sound_url, word)

def save_sound(url, keyword):
    filename = keyword + ".mp3"
    path = "sounds/files/" + filename
    r = requests.get(url, stream=True, verify='forvo-com-chain.pem')
    if r.status_code == 200:
        r.raw.decode_content = True

        with open(path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print("Sound saved: ", filename)
        return True

    else:
        return False