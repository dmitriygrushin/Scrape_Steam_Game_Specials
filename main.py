from utils.extract import extract_full_body_html
from utils.parse import parse_raw_attributes
from utils.process import format_and_transform, save_to_file
from config.tools import get_config

""" Learning Outcomes: """
"""
Learning Outcome #1: JavaScript Scraping with Playwright
    https://store.streampowered.com/specials
    * title
    * link to thumbnail
    * category tags
    * rating
    * # of reviews
    * original price
    * discounted price
    * discount %
    
Learning Outcome #2: Code Organization & Project Structure & Separation of Concerns
    [render JS with Playwright] 
    -- html --> 
        [extract elements from HTML based on .json config] - config.json = generic utility i.e. parse_raw_attributes 
            -- raw attributes -->
                [apply functional transforms, if any]
                    -- save --> 
                        [yyyy_mm_dd_extract.csv] """

"""
    Good tip for refactoring:
        define your ideas syntax then define the function
        nodes = parse_raw_attributes(html, config.get('container')), then write the logic inside the function
"""

if __name__ == '__main__':
    config = get_config()

    # wait for the selected container to load, then extract the HTML <body> from the URL
    # 1. extract html body
    html = extract_full_body_html(
        from_url=config.get("url"),
        wait_for=config.get("container").get("selector"))

    # returns the nodes that correspond to the selected container
    # returns {'store_sale_divs': [<Node div>, <Node div>, ..., <Node div>]}
    # 2. from the HTML body get the game nodes
    nodes = parse_raw_attributes(html, [config.get('container')])

    game_data = []
    # {'store_sale_divs': [<Node div>, <game info container>, ..., <Node div>]}
    # from each game info container node extract their attributes based on the config item list
    # 3. Loop through all game nodes
    for node in nodes.get("store_sale_divs"):
        # items: [{name, selector, ...}, {name, selector, ...}, ...] that will be extracted from each game node
        # 4. for each game node get it's desired attributes as a dict
        attrs = parse_raw_attributes(node, config.get('items'))

        # post-process attrs i.e. some attrs need extra methods to get desired data
        attrs = format_and_transform(attrs)

        game_data.append(attrs)

    save_to_file("extract", game_data)
