import argparse
import os
import sys

# take in a list of words in txt format, convert to list
# for every item in the list, go to duckduckgo and get a random image from the first 10 results, save to images directory
# for every item in the list, go to forvo and get a random recording, save to sounds dir
# if no result, write out to a text file

from images.ddgapi import search_image
from images.ddglangs import DDG_COUNTRIES
from sounds.forvoapi import search_sound
from sounds.forvolangs import FORVO_LANG_CODES

def main():
    parser = argparse.ArgumentParser(description="Read a text file of words and download images from \
        DuckDuckGo, sound from Forvo, or both. Requires API key for Forvo downloads.")
    parser.add_argument("words_file", help="Path to text file with words to query")
    parser.add_argument("--ddg_lang", help="DuckDuckGo country/language code. Required if images flag is set.")
    parser.add_argument("--forvo_lang", help="Forvo language code. Required if sounds flag is set.")
    args = parser.parse_args()

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