import os
import re
import json

import requests
import bs4
from bs4 import BeautifulSoup

from settings import *


def find_duplicates(iterable):
    seen = set()
    dupes = []
    for x in iterable:
        if x in seen:
            dupes.append(x)
        else:
            seen.add(x)
    return dupes


def remove_duplicates(recipes):
    uniq = []
    seen = set()
    for recipe in recipes:
        if recipe[1] in seen:
            continue
        else:
            uniq.append(recipe)
            seen.add(recipe[1])
    return uniq


def extract_date(link):
    assert isinstance(link, str)
    result = re.search(r"(\d+\/\d+\/\d+)", link)
    assert result is not None
    date = result.group(1)
    return date.replace("/", "-")


def generate_filename(name, link):
    assert isinstance(name, str)
    assert isinstance(link, str)
    date = extract_date(link)
    assert date != ""
    return f"{date}__{name}"


def save_url(url, path):
    assert isinstance(url, str)
    assert isinstance(path, str)
    res = requests.get(url)
    assert res is not None
    with open(path, "wb+") as f:
        f.write(res.content)
    assert os.path.exists(path)


# make directory
if not os.path.exists(DIR_PAGES):
    os.mkdir(DIR_PAGES)
    assert os.path.exists(DIR_PAGES)

# save index
if not os.path.exists(PATH_INDEX):
    save_url(URL_INDEX, PATH_INDEX)
    assert os.path.exists(PATH_INDEX)

# read index
with open(PATH_INDEX, "rb") as f:
    soup = BeautifulSoup(f.read(), "html.parser")
assert soup is not None

# find parent elements
parents = soup.find_all("p", class_="has-text-align-center")
assert len(parents)

# get links and names
recipes = []
for parent in parents:
    assert isinstance(parent, bs4.element.Tag), parent.prettify()

    # find link
    el_link = parent.find("a")
    assert isinstance(el_link, bs4.element.Tag), parent.prettify()

    link = el_link.attrs["href"]
    assert isinstance(link, str), parent.prettify()

    # find name
    el_name = el_link.find(class_="has-inline-color")
    name = el_name.contents[0]

    assert isinstance(name, str), parent.prettify()

    recipes.append((name, link))

# remove duplicates
recipes = remove_duplicates(recipes)

# save recipes
filenames_links = {}
for (name, link) in recipes:
    filename = generate_filename(name, link)
    filepath = os.path.join(DIR_PAGES, filename) + ".html"
    filenames_links[filename] = link
    if not os.path.exists(filepath):
        save_url(link, filepath)

# write json of links with their filenames
with open(PATH_INDEX_JSON, "w") as jsonfile:
    json.dump(filenames_links, jsonfile, indent=2)
