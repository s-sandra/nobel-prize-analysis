import json
import pandas as pd
import numpy as np

# loads nobel prize data into nobel_data object
with open("nobel.json","r") as data:
    nobel_data = json.load(data)

# format data into array for analysis.


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
            shares.append(prize['share'])

shares = np.asarray(shares)
print(shares)

#shares = np.where(shares=='1', False, True)
#print(shares)
genders_shares = pd.DataFrame([genders, list(shares)],index=['gender','shares']).swapaxes(0,1)
print(genders_shares)

genders_shares = genders_shares.apply(pd.to_numeric, errors='ignore')
print(genders_shares)

genders_shares.boxplot('shares', by='gender', showmeans=True)

#%%-----
#question4


#%%-----
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

gender_and_year = gender_and_year[(gender_and_year.gender == "male") | (gender_and_year.gender == "female")]
print(gender_and_year)
