import json

_config = {
    "url": "https://store.steampowered.com/specials",
    "meta": {
        "name": "Steam Sales Scraper",
        "description": "Extracts the highest discounted games from Steam Specials",
        "version": 0.1
    },
    # a class which contains the data we need from each game.
    # multiple games have the same container i.e. Steam's special has 12 games shown before clicking show more
    "container": {
        "name": "store_sale_divs",
        "selector": 'div[class*="salepreviewwidgets_StoreSaleWidgetContainer"]',
        "match": "all",
        "type": "node"
    },
    # the idea is if we want another item all we need to do is add another obj here that captures the fields
    "items": [
        {
            # give each item a custom title
            "name": "title",
            # inside each container you're above to select each item you want by their selector
            "selector": 'div[class*="StoreSaleWidgetTitle"]',
            # there could be multiple, but we want the first one inside the main container
            "match": "first",
            # we either want the simple text or a node if the item is i.e. an image tag
            "type": "text"
        },
        {
            "name": "thumbnail",
            "selector": 'img[class*="CapsuleImage"]',
            "match": "first",
            "type": "node"
        },
        {
            "name": "tags",
            "selector": 'div[class*="StoreSaleWidgetTags"] > a',
            "match": "all",
            "type": "text"
        },
        {
            "name": "release_date",
            "selector": 'div[class*="WidgetReleaseDateAndPlatformCtn"] > div[class*="StoreSaleWidgetRelease"]',
            "match": "first",
            "type": "text"
        },
        {
            "name": "review_score",
            "selector": 'div[class*="ReviewScoreValue"] > div',
            "match": "first",
            "type": "text"
        },
        {
            "name": "reviewed_by",
            "selector": 'div[class*="ReviewScoreCount"]',
            "match": "first",
            "type": "text"
        },
        {
            "name": "price_currency",
            "selector": 'div[class*="StoreSalePriceBox"]',
            "match": "first",
            "type": "text"
        },
        {
            "name": "sale_price",
            "selector": 'div[class*="StoreSalePriceBox"]',
            "match": "first",
            "type": "text"
        },
        {
            "name": "original_price",
            "selector": 'div[class*="StoreOriginalPrice"]',
            "match": "first",
            "type": "text"
        }
    ]
}


def get_config(load_from_file=False):
    """ i.e. name: title, selectors: ("div[...]", "p"), match: css_first, type: text()

    config.json -> py dict (like _config), so the opposite of generate_config()

    load from json file or load from _config above if arg is true """
    if load_from_file:
        with open("config.json", "r") as f:
            return json.load(f)
    return _config


def generate_config():
    """dumping _config -> config.json file"""
    with open("config.json", "w") as f:
        json.dump(_config, f, indent=4)


if __name__ == "__main__":
    generate_config()
