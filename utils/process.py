import re
from datetime import datetime
from selectolax.parser import Node
import pandas as pd


def get_attrs_from_node(node: Node, attr: str):
    if node is None or not issubclass(Node, type(node)):
        raise ValueError("The function  expects a Selectolax node to be provided")

    return node.attributes.get(attr)


def get_first_n(input_list: list, n: int = 5):
    return input_list[:n]


def reformat_date(date_raw: str, input_format: str = '%b %d, %Y', output_format: str = '%Y-%m-%d'):
    dt_obj = datetime.strptime(date_raw, input_format)
    return datetime.strftime(dt_obj, output_format)


def regex(input_str: str, pattern: str, do_what: str = "findall"):
    if do_what == "findall":  # findall by pattern
        return re.findall(pattern, input_str)
    elif do_what == "split":  # split by pattern
        return re.split(pattern, input_str)
    else:
        raise ValueError("The function expects 'findall' or 'split' to be provided")


def format_and_transform(attrs: dict):
    """Takes the attrs and does post-processing.
    i.e. Some attrs need extra methods to extract desired data or reformat data
    attrs = {"title", "Game_1", "thumbnail": "...", "tags": ["...", ...], ...}
    """

    """
    transforms dict: is a guide on how to post-process the attrs
    Having a lambda in "lambda n: func(...)" the func doesn't run until the lambda is called
        If the lambda was NOT used then the func will automatically execute
    Having a lambda also allows you to set default func params (i.e. attr) for each type (i.e. thumbnail) cleaner.
        Adding a default attr for each type in the actual func will be messy.
    """
    transforms = {
        "thumbnail": lambda n: get_attrs_from_node(n, "src"),
        "tags": lambda input_list: get_first_n(input_list, 5),
        "release_date": lambda date: "N/A" if date == '' else reformat_date(date, '%b %d, %Y', '%Y-%m-%d'),

        # the r in r'\d+' for raw string, so it doesn't escape any chars we don't want that are part of the regex
        "reviewed_by": lambda raw: ''.join(regex(raw, r'\d+', "findall")),  # ''.join(...) means join by nothing
        "price_currency": lambda raw: "N/A" if not any(char.isdigit() for char in raw) else
        regex(raw, r'(\$)(\d+\.\d+)', "split")[1],
        "sale_price": lambda raw: "N/A" if not any(char.isdigit() for char in raw) else float(
            regex(raw, r'(\$)(\d+\.\d+)', "split")[2]),
        "original_price": lambda raw: transforms["sale_price"](raw)  # just call sale_price since it has the same lambda
    }

    # using transforms as a guide on post-processing the attrs
    for k, v in transforms.items():
        # i.e. if "thumbnail" in attrs
        if k in attrs:
            # attrs["thumbnails"] -> <Node img>
            # attrs["thumbnails"] = v(<Node img>)
            # v(attrs[k]) uses the reference method in transforms that's stored as a value
            # you just pass the node and the rest is handled based on the type of node by the transform dict lambda
            attrs[k] = v(attrs[k])

    attrs["discount_pct"] = "N/A"

    if issubclass(type(attrs["original_price"]), float):
        attrs["discount_pct"] = round((attrs["original_price"] - attrs["sale_price"]) / attrs["original_price"] * 100, 3)

    return attrs


def save_to_file(filename="extract", data: list[dict] = None):
    if data is None:
        raise ValueError("The function expects data to be provided as a list of dictionaries")

    df = pd.DataFrame(data)
    filename = f"{datetime.now().strftime('%Y_%m_%d')}_{filename}.csv"
    df.to_csv(filename, index=False)
