from pathlib import Path
import json

import bs4
from bs4 import BeautifulSoup

from settings import *


def get_soup(page):
    assert isinstance(page, Path)
    with open(page, "rb") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    assert soup is not None
    return soup


def print_page_if_not_exactly_1_recipe(page):
    assert isinstance(page, Path)
    count = 0
    soup = get_soup(page)
    ps = soup.find_all("p")
    for p in ps:
        if is_p_a_recipe(p):
            count += 1
    if count != 1:
        print(count, page)


def is_p_a_recipe(p):
    assert isinstance(p, bs4.element.Tag)

    html = str(p).lower()
    count = 0
    for prop in PROPERTIES:
        if prop in html:
            count += 1
    if "<strong>" in html and any(sim in html for sim in SIMULATIONS) and count >= 2:
        return True
    return False


def extract_recipe(p):
    assert isinstance(p, bs4.element.Tag)
    recipe = {}

    # find acros and monochrome simulations
    p_html = str(p).lower()
    map = {
        "<strong>acros": "acros",
        "<strong>acros+r": "acros+r",
        "<strong>acros+y": "acros+y",
        "<strong>acros+g": "acros+g",
        "<strong>monochrome": "monochrome",
        "<strong>monochrome+r": "monochrome+r",
        "<strong>monochrome+y": "monochrome+y",
        "<strong>monochrome+g": "monochrome+g",
    }
    for key in map.keys():
        if key in p_html:
            recipe["simulation"] = map[key]

    # find date for most recipes
    for item in p.strings:
        item = item.strip().lower()

        # find simulation for most cases
        if recipe.get("simulation", "") == "":
            if item in SIMULATIONS:
                recipe["simulation"] = item
                continue

        # find properties
        if ":" in item:
            parts = item.split(":")
            if len(parts) != 2:
                continue
            prop, value = parts
            prop = prop.strip()
            value = value.strip()
            if prop in PROPERTIES:
                recipe[prop] = value

            # check for misspelling
            if prop == "sharpeness":
                recipe["sharpness"] = value

    return recipe


def page_to_recipe(page):
    assert isinstance(page, Path)
    recipe = {}
    soup = get_soup(page)
    ps = soup.find_all("p")
    for p in ps:
        if is_p_a_recipe(p):
            recipe = extract_recipe(p)
            recipe["p_html"] = str(p)
            recipe["p_strings"] = list(p.strings)
            break

    assert recipe is not None, p

    # get filenames to links map
    with open(PATH_INDEX_JSON) as jsonfile:
        filenames_links = json.load(jsonfile)

    # add filename and link to recipe
    date, name = page.stem.split("__")
    recipe["name"] = name
    recipe["date"] = date
    recipe["link"] = filenames_links[page.stem]

    return recipe


recipes = []

# process html pages
pages = list(Path(DIR_PAGES).iterdir())
for page in pages:
    if page.name in SKIP_PAGES:
        continue

    recipe = page_to_recipe(page)
    assert recipe is not None, page
    recipes.append(recipe)

# get manual recipes
with open(PATH_MANUAL_JSON) as jsonfile:
    manual_recipes = json.load(jsonfile)
assert len(manual_recipes)

# combine recipes
recipes.extend(manual_recipes)

# write recipes
with open(PATH_RECIPES_JSON, "w") as jsonfile:
    json.dump(recipes, jsonfile, indent=2)
