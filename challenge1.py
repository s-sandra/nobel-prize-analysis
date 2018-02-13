import json
import pandas as pd

# loads nobel prize data into nobel_data object
with open("nobel.json","r") as data:
    nobel_data = json.load(data)

# creates dataframe storing gender and year of award
rows = []
for laureate in nobel_data["laureates"]:

    # each laureate is a dictionary
    gender = laureate["gender"]

    # checks for bogus entries
    if laureate["born"] != "0000-00-00" and laureate["died"] != "0000-00-00":
        year = laureate["prizes"][0]["year"]
        # each prizes in laureate is a list containing a dictionary

    rows.append({"gender" : gender, "year" : year})
gender_and_year = pd.DataFrame(rows)
