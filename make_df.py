import pandas as pd

from settings import *

df = pd.read_json(PATH_RECIPES_JSON, orient="records")
assert isinstance(df, pd.DataFrame)

# fill NaN in sharpness with sharpening values
df["sharpness"].fillna(value=df["sharpening"], inplace=True)

# fill remaining NaN with 0
df["sharpness"].fillna(value=0, inplace=True)

# drop sharpening column
df.drop(columns=["sharpening"], inplace=True)

# print rows without sharpness
# print(df[df["sharpness"].isna()])

# print(df.head())
# print(list(df))
