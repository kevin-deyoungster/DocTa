"""
This adapter script handles converting user lists from clients into a format which our 
online platform can take in.
"""

import pandas as pd

COUNTRY = "GH"
LANGUAGE = "en"

countries = {"GH": "+233"}


def convert_number(raw_number, country):
    # lazy replacing, replace first 0 with +233
    new_number = countries[country] + raw_number
    return new_number


df = pd.read_excel("test_input.xlsx")

# (df)
df["lastName"] = df["FULLNAME"].apply(lambda x: x.strip().split(" ")[-1])
df["firstName"] = df["FULLNAME"].apply(lambda x: " ".join(x.strip().split(" ")[:-1]))
df["phoneNumber"] = df["PHONE NO."].apply(lambda x: convert_number(str(x)[0:], COUNTRY))
df["country"] = COUNTRY
df["language"] = LANGUAGE

df2 = pd.DataFrame(index=range(len(df.index)))
print(df2)
df2["firstName;lastName;phoneNumber;country;language"] = (
    df["firstName"]
    + ";"
    + df["lastName"]
    + ";"
    + df["phoneNumber"]
    + ";"
    + df["country"]
    + ";"
    + df["language"]
)
# print(df["LASTNAME"])
print(df2)
df2.to_csv("test_output.csv", index=False)

