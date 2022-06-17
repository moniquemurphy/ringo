# ringo 🍎
Generate images and sound for flashcards using DuckDuckGo and the Forvo API. DuckDuckGo image search is a modified version (with much gratitude!) of [duckduckgo-images-api](https://github.com/deepanprabhu/duckduckgo-images-api).

This is an active project. Feedback is much appreciated.

## Prerequisites
* Python 3
* (Recommended) Virtual Environment
* If you want to download sounds, you need a subscription to the [Forvo API]("https://api.forvo.com/") and to set the key as the environment variable `FORVO_API_KEY`. You can still download images without a Forvo API Key.

## Install
Run the following commands in your terminal:
```
git clone https://github.com/moniquemurphy/ringo.git && cd ringo
pip install -r requirements.txt
```

## Use
This is a command line interface tool. That means you run it from Terminal (Mac/Linux), CMD (Windows), or whatever program you use to run the command line on your machine. You will `cd` into the `ringo` folder wherever you have saved it on your computer.

You will need a `.txt` file of words you want to look up. It's easiest if you save it in the same directory that contains the file `ringo.py`.

To view help for the tool, type the command `python ringo.py --help`.

### Get Just Images
If you don't have a Forvo API key, you can still save images for a list of words. You will need to decide which country/language to use to search. You can see all the DuckDuckGo country codes in `images/ddglangs.py` or use [this page](https://duckduckgo.com/params) for reference. This script picks a random image from the first 10 results on DuckDuckGo and saves it to the `images` directory.

The following command searches DuckDuckGo for images in `words.txt` using the Japan country code.

```
python ringo.py --ddg_lang jp-jp words.txt
```


### Get Just Sounds
If you do have a Forvo API key, make sure you have saved it as an environment variable calledl `FORVO_API_KEY`. You will need to tell the tool which language to constrain your search to. You can see all the Forvo language codes in `sounds/forvolangs.py` or use [this page](https://forvo.com/languages-codes/) for reference. The cheapest Forvo API plan is $2 per month and allows 500 requests per day. Unfortunately, it doesn't seem possible to combine the search and save for a particular sound into one request, so each individual word will use up 2 requests. This is still much faster than doing it manually, though!

The following command searches Forvo for Japanese sounds for the words in `words.txt`.

```
python ringo.py --forvo_lang ja words.txt
```

### Get Sounds and Images
You can combine all of the flags to get both sounds and images.

```
python ringo.py --ddg_lang jp-jp --forvo_lang ja words.txt
```

### Items not found
If a word wasn't found in either search, you can look at `images_not_found.txt` and `sounds_not_found.txt`. If you're feeling kind, you can request the sounds not found be added to Forvo.

### Bonus: Anki Usage
When you're done downloading, you can move both images and sounds into your `collection.media` folder. (Stay tuned for a guide to cleaning up your Anki cards to automate everything nicely).

