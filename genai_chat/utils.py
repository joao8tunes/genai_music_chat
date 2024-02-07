#!/usr/bin/env python
# encoding: utf-8

# João Antunes <joao8tunes@gmail.com>
# https://github.com/joao8tunes

"""
General utilities.
"""

from fuzzywuzzy.fuzz import \
    ratio, partial_ratio, token_sort_ratio, token_set_ratio, partial_token_sort_ratio, partial_token_set_ratio
from bs4 import BeautifulSoup
from hashlib import md5
import markdown
import logging
import json


def compare_strings(s1: str, s2: str, fuzzy_method: str = "ratio", case_sensitive: bool = True) -> float:
    """
    Compare strings based on fuzzy logic methods.

    Parameters
    ----------
    s1: str
        String.
    s2: str
        String.
    fuzzy_method: str
        Fuzzy method to compare strings.
    case_sensitive: bool
        Whether is case sensitive.

    Returns
    -------
    similarity: float
        Similarity between strings `s1` and `s2` in range [0,1].

    References
    ----------
    .. [1] Fuzzy String Matching in Python Tutorial: https://www.datacamp.com/community/tutorials/fuzzy-string-python

    .. [2] TheFuzz: https://github.com/seatgeek/thefuzz
    """
    supported_fuzzy_methods = (
            "ratio",
            "partial_ratio",
            "token_sort_ratio",
            "token_set_ratio",
            "partial_token_sort_ratio",
            "partial_token_set_ratio"
    )

    assert fuzzy_method in supported_fuzzy_methods, \
        f"fuzzy method '{fuzzy_method}' not supported ({', '.join(supported_fuzzy_methods)})."

    strings_similarity = ratio

    if fuzzy_method == 'partial_ratio':
        strings_similarity = partial_ratio
    elif fuzzy_method == 'token_sort_ratio':
        strings_similarity = token_sort_ratio
    elif fuzzy_method == 'token_set_ratio':
        strings_similarity = token_set_ratio
    elif fuzzy_method == 'partial_token_sort_ratio':
        strings_similarity = partial_token_sort_ratio
    elif fuzzy_method == 'partial_token_set_ratio':
        strings_similarity = partial_token_set_ratio

    if case_sensitive:
        similarity = strings_similarity(s1, s2) / 100.0
    else:
        similarity = strings_similarity(s1.lower(), s2.lower()) / 100.0

    return similarity


def merge_dict(a: dict, b: dict) -> dict:
    """
    Merges two simple and non-hierarchical dictionaries.

    Parameters
    ----------
    a: dict
        Dictionary.
    b: dict
        Dictionary.

    Returns
    -------
    x: dict
        Merged dictionary.

    References
    ----------
    .. [1] Using `Dict` class to merge complex/hierarchical dictionaries: https://stackoverflow.com/a/70908985/16109419
    """
    x, y = a, b

    if not isinstance(a, dict):
        x = a.__json__()

    if not isinstance(b, dict):
        y = b.__json__()

    x.update(y)

    return x


def md5_hash(string: str) -> str:
    """
    Hash a string using the MD5 algorithm.

    Parameters
    ----------
    string: str
        String to convert to MD5 hash.

    Returns
    -------
    string_hash: str
        MD5 hash.
    """
    string_hash = md5(string.encode()).hexdigest()

    return string_hash


def extract_json_from_text(text: str) -> dict:
    """
    Extract JSON content from text.

    Parameters
    ----------
    text: str
        Text.

    Returns
    -------
    json_content: dict
        JSON content.
    """
    json_content = None

    text = " ".join(text.replace("\n", " ").split()).replace("'", "\"")

    try:
        # Find the starting position of the first '{' (opening of the JSON)
        opening_position = text.find('{')

        # Check if the opening of the JSON is found
        if opening_position != -1:
            # Find the closing position of the corresponding '}'
            closing_position = text.find('}', opening_position + 1)

            # Check if the closing brace is found
            if closing_position != -1:
                # Extract the JSON substring
                json_string = text[opening_position:closing_position + 1]

                # Load the JSON
                json_object = json.loads(json_string)
                json_content = json_object
            else:
                logging.warning("Closing brace '}' not found.")
        else:
            logging.warning("Opening brace '{' not found.")
    except json.JSONDecodeError as e:
        logging.warning(f"Error decoding the JSON: {str(e)}")
        pass

    return json_content


def strip_markdown_from_text(text: str) -> str:
    """
    Strip Markdown formatting from a given text.

    Parameters
    ----------
    text : str
        The input text containing Markdown formatting.

    Returns
    -------
    str
        The text with Markdown formatting removed.

    Notes
    -----
    This function uses the `markdown` and `BeautifulSoup` libraries to convert
    Markdown-formatted text to HTML and then extract the plain text.

    Examples
    --------
    >>> markdown_text = "# Heading\\nSome *italic* and **bold** text."
    >>> stripped_text = strip_markdown_from_text(markdown_text)
    >>> print(stripped_text)
    'Heading\\nSome italic and bold text.'
    """
    # Converting Markdown to HTML:
    html = markdown.markdown(text)

    # Parsing HTML using BeautifulSoup:
    soup = BeautifulSoup(html, features="html.parser")

    # Getting plain text from HTML:
    cleaned_text = soup.get_text()

    return cleaned_text
