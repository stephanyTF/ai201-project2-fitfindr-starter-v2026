"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings

#added imports for clean description function
import nltk #already did pip install nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')


# ── Tool 1: search_listings ───────────────────────────────────────────────────
#Added: Clean Desscription func

def clean_description(description: str) -> set:
    """
    Clean the description string by removing punctuation and converting to lowercase.
    Keeps only alphanumeric words
    Keeps no phrases together like 'no rips' 
    Removes stop words from the description string.


    Args:
        description: The description string to clean.

    """

    extra_stop_words = ["along", "sit", "sits", "fit", "fits", "like"]


    # lowercasing  and keeps only alphanumeric  words
    word_lst = [word.lower() for word in word_tokenize(description) if word.lower().isalnum()]

    #keep no phrases
    n = len(word_lst)

    for _ in range(n):
        if word_lst[_] == "no" and _ != n-1:
            next_word = word_lst[_+1]
            word_lst[_+1]= "no" +" "+ next_word

    # if "no" in word_lst:
    #     word_lst.remove("no")
    word_lst = [word for word in word_lst if word not in ("no",)]


    #remove stop words (has to be after keeping the no phrases together since no is a stop word)
    stop_words = set(stopwords.words('english'))
    word_lst = [word for word in word_lst if word not in stop_words]

    #filters out extra stop words
    word_lst = [word for word in word_lst if word not in extra_stop_words]
    #print(set(word_lst))

    return set(word_lst)



def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    # TODO: 
    #1. Load every listing with load_listings().
    listings = list(load_listings())
    search_results_lst = []
    score_listing_dict = {}


    description_keywords = clean_description(description)

    for article in listings:
        #2. Filter by max_price and by size, when each is provided.
        if max_price is not None and article['price'] > max_price:
            continue
        if size is not None and size.lower() not in article['size'].lower():
            continue

        #3. Score what's left by keyword overlap with `description`.
        listing_keywords = clean_description(article['description']) #Clean up `description`.

        overlap = description_keywords.intersection(listing_keywords)
        
        #4. Drop anything scoring zero.
        if len(overlap) > 0:
            #add to the listing to the dictionary
            score_listing_dict[article['id']] = len(overlap)
            search_results_lst.append(article)


    #5. Sort by score from the score listing dict, highest first.

    #fill up search results from clothes listing if listing is in score_listing_dict
    search_results_lst = [article for article in listings if article['id'] in score_listing_dict]

    #sort search results by score, highest first
    search_results_lst.sort(key=lambda x: score_listing_dict[x['id']], reverse=True)

    return search_results_lst[:config.SEARCH_RESULT_LIMIT]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    # TODO: replace this with your implementation
    # 1. Check whether wardrobe['items'] is empty.
    if not wardrobe['items']:
        # 2. If it is, ask the model for general styling ideas for this item.
        prompt = f"Give general styling ideas for this item: {new_item['description']}"
        return generate(prompt)

    # 3. If it isn't, format the wardrobe items into the prompt and ask for specific combinations.
    wardrobe_items = "\n".join([f"- {item['name']}" for item in wardrobe['items']])
    prompt = f"Suggest outfits using this new item: {new_item['description']} and the following wardrobe items:\n{wardrobe_items}"
    

    return generate(prompt)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    # TODO: replace this with your implementation
    return ""
