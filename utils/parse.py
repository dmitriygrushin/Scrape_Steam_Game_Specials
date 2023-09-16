from typing import Union
from selectolax.parser import Node, HTMLParser

"""
parse_raw_attributes(html, [config.get('container')])
tools._config = ...

    "container": {
        "name": "store_sale_divs",
        "selector": 'div[class*="salepreviewwidgets_StoreSaleWidgetContainer"]',
        "match": "all",
        "type": "node"
    }, ...
    
    or
    parse_raw_attributes(node, config.get('items')) 
    ...
    "items": [
        # attributes/items that will be extracted
        {
            "name": "title",
            "selector": "div[class*=\"StoreSaleWidgetTitle\"]",
            "match": "first",
            "type": "text"
        }, ...
    
"""


def parse_raw_attributes(node: Union[Node, str], items: list[dict]) -> dict:
    """
    Based on the obj you pass this func will return a dict of {name: node(s)/str} based on the selector you passed

    the node contains the attributes and items is a list of attributes you want to extract
        items: are the attributes that you would like to extract from the node
            so, each item is an attribute you would like to get from the node


    sample parsed var:
    ---------------------
    name,   matched_node(s)
    ---------------------
    {'title': 'Titanfall® 2',
    'thumbnail': < Node img >,
    'tags': ['FPS', 'Multiplayer', 'Mechs', 'Shooter', 'Action', ...],
    'release_date': 'Jun 18, 2020',
    'review_score': 'Very Positive',
    'reviewed_by': '| 157,299 User Reviews',
    'price_currency': '$2.99',
    'sale_price': '$2.99',
    'original_price': '$29.99'}
    """

    # Union [Node, str] means the arg takes type Node or str

    if not issubclass(Node, type(node)):
        # i.e. initial var html body passed via: parse_raw_attributes(html, [config.get('container')]) will be a string
        # that needs to be turned into a tree so that you can use css selectors
        node = HTMLParser(node)

    # k:v = name:node/text
    parsed = {}

    for item in items:
        match = item.get("match")
        type_ = item.get("type")
        selector = item.get("selector")  # what CSS to extract from the node
        name = item.get("name")  # title, thumbnail, tags, release_date, ...

        if match == "all":
            # will select multiple tags that match the selector i.e. tags
            matched = node.css(selector)

            if type_ == "text":
                # i.e. there are multiple tags that matched, so go add all tag nodes, get their text, add in a list
                parsed[name] = [node.text() for node in matched]
            elif type_ == "node":
                parsed[name] = matched

        elif match == "first":
            matched = node.css_first(selector)

            if type_ == "text":
                parsed[name] = "N/A" if not matched else matched.text()
            elif type_ == "node":
                parsed[name] = matched

    return parsed
