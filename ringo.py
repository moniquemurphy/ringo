import argparse
import os
import random
import requests
import shutil
import sys

# take in a list of words in txt format, convert to list
# for every item in the list, go to duckduckgo and get a random image from the first 10 results, save to images directory
# for every item in the list, go to forvo and get a random recording, save to sounds dir
# if no result, write out to a text file

from duckduckgo_search import DDGS
from images.ddglangs import DDG_COUNTRIES
from sounds.forvoapi import search_sound
from sounds.forvolangs import FORVO_LANG_CODES

def search_image(word, ddg_lang):
    ddgs = DDGS()

    ddgs_images_gen = ddgs.images(
        keywords=word,
        region=ddg_lang,
        safesearch="on",
        size=None,
        color="color",
        type_image=None,
        layout=None,
        license_image=None,
        max_results=10
    )

    # first_ten_results = []

    # result_counter = 0
    # while result_counter < 11:
    #     for r in ddgs_images_gen:
    #         first_ten_results.append(r)
    #         result_counter += 1

    image_found = save_image(random.choice(ddgs_images_gen)["image"], word)
    return image_found

def save_image(image_url, keyword):
    # Always save as ".jpg", no matter the original extension. This makes automating cards importing into Anki much easier.

    filename = keyword + ".jpg"
    path = "images/files/" + filename
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

def main():
    parser = argparse.ArgumentParser(description="Read a text file of words and download images from \
        DuckDuckGo, sound from Forvo, or both. Requires API key for Forvo downloads.")
    parser.add_argument("words_file", help="Path to text file with words to query")
    parser.add_argument("--ddg_lang", help="DuckDuckGo country/language code. Provide to retrieve images.")
    parser.add_argument("--forvo_lang", help="Forvo language code. Provide to retrieve sounds.")
    args = parser.parse_args()

    if not args.forvo_lang and not args.ddg_lang:
        sys.stderr.write("You have not set any flags! See --help for usage.")

    if args.forvo_lang and not os.getenv("FORVO_API_KEY"):
        sys.stderr.write("If you set the sounds flag, you must set an environment variable called FORVO_API_KEY.")
        sys.exit()

    if args.ddg_lang and not args.ddg_lang in DDG_COUNTRIES:
        sys.stderr.write("Please supply a valid DuckDuckGo country code to search for images.")
        sys.exit()

    if args.forvo_lang and not args.forvo_lang in FORVO_LANG_CODES:
        sys.stderr.write("Please supply a valid Forvo language code to search for sounds.")
        sys.exit()

    with open(args.words_file) as f:
        words = f.readlines()
        words = [x.strip() for x in words]

    images_not_found = open("images_not_found.txt", "w")
    sounds_not_found = open("sounds_not_found.txt", "w")

    if args.ddg_lang and args.forvo_lang:
        for word in words:
            print("Retrieving image and sound for: ", word)
            image_found = search_image(word, args.ddg_lang)
            if not image_found:
                print("Image not found for ", word)
                images_not_found.write(word+ "\n")
            sound_found = search_sound(word, args.forvo_lang)
            if not sound_found:
                print("Sound not found for ", word)
                sounds_not_found.write(word+ "\n")

    if args.ddg_lang and not args.forvo_lang:
        for word in words:
            print("Retrieving image for: ", word)
            image_found = search_image(word, args.ddg_lang)
            if not image_found:
                print("Image not found for ", word)
                images_not_found.write(word + "\n")

    if args.forvo_lang and not args.ddg_lang:
        for word in words:
            print("Retrieving sound for: ", word)
            sound_found = search_sound(word, args.forvo_lang)
            if not sound_found:
                print("Sound not found for ", word)
                sounds_not_found.write(word+ "\n")

if __name__ == "__main__":
    main()