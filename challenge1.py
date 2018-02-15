import json
import pandas as pd

# loads nobel prize data into nobel_data object
with open("nobel.json","r") as data:
    nobel_data = json.load(data)

# formats data into DataFrames for analysis.


#%%-----
#question3
laureates = nobel_data['laureates']
genders = []
shares = []
for laureate in laureates:
    if(not(laureate['born'] == '0000-00-00' and laureate['died'] == '0000-00-00') and (laureate['gender'] == 'male' or laureate['gender'] == 'female')):
        for x in range(len(laureate['prizes'])):
            genders.append(laureate['gender'])
        for prize in laureate['prizes']:
            shares.append(laureate['prizes'])
#shares = laureates[:]['prizes'][:]['share']
print(genders)

#%%-----
# creates DataFrame storing gender and year of award for each recipient.
rows = []
for laureate in nobel_data["laureates"]:
    gender = laureate["gender"]

    # checks for bogus entries
    if laureate["born"] != "0000-00-00" and laureate["died"] != "0000-00-00":

        # gets years of all prizes recipient has won
        for prize in laureate["prizes"]:
            year = prize["year"]
            rows.append({"gender" : gender, "year" : year})

gender_and_year = pd.DataFrame(rows)
gender_and_year = gender_and_year[(gender_and_year.gender == "male") | (gender_and_year.gender == "female")] # considers only male and female genders
print(gender_and_year)
