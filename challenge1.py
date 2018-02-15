import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

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
countries = []
for laureate in laureates:
    if(not(laureate['born'] == '0000-00-00' and laureate['died'] == '0000-00-00') and (laureate['gender'] == 'male' or laureate['gender'] == 'female')):
        for prize in laureate['prizes']:
            affiliations = prize['affiliations'][0]

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
            category = prize["category"]
            rows.append({"gender" : gender, "year" : year, "category" : category})

gender_and_year = pd.DataFrame(rows)
del gender_and_year["category"]

gender_and_year = gender_and_year[(gender_and_year.gender == "male") | (gender_and_year.gender == "female")] # considers only male and female genders
gender_and_year_frequency = pd.crosstab(gender_and_year.gender, gender_and_year.year)
gender_frequency = gender_and_year.gender.value_counts()
gender_frequency.plot(kind="bar")
plt.title("Gender of Nobel Prize Recipients")
plt.xlabel("Gender")
plt.ylabel("Frequency")
plt.show()
plt.close()

gender_year_graph = gender_and_year_frequency.plot(kind="bar")
gender_year_graph.xaxis.set_major_locator(ticker.MultipleLocator(10))
plt.close()

gender_and_category = pd.DataFrame(rows)
del gender_and_category["year"]
category_gender_frequency = pd.crosstab(gender_and_category.category, gender_and_category.gender)
category_gender_frequency.plot(kind="bar")
plt.title("Gender Frequency in Nobel Prize Categories")
plt.xlabel("Category")
plt.ylabel("Frequency")
plt.show()