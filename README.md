# fuji-recipes
Tools to get, parse, and clean Fujifilm JPEG recipes from [FujiXWeekly](https://fujixweekly.com/).

Currently supports [X-Trans IV recipes](https://fujixweekly.com/fujifilm-x-trans-iv-recipes/).

Some recipes have been skipped and are listed in `settings.py`:
- Recipes which require multiple exposure
- Additional push/pull variants of some recipes
- Sepia (because no one likes it)

Cleaning consisted of various operations to standardize the data format.

# workflow
1. Run `get_pages.py`
1. Run `parse_pages.py`
1. Run `clean_pages.ipynb`

# outputs
- `pages/`
  - `html` recipe pages
- `recipes/`
  - `index.html` copy of [X-Trans IV recipe index](https://fujixweekly.com/fujifilm-x-trans-iv-recipes/)
  - `index.json` map between recipe and link
  - `manual.json` manually entered recipes which could not be parsed easily
  - `recipes.json` parsed recipes which have not been cleaned
  - `recipes_table.csv` all fields broken out into columns
  - `recipes_long.csv` all fields combined into a paragraph
  - `recipes_short.csv` fields combined in a condensed format
