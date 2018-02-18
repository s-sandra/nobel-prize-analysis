import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats.stats

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
genders4 = []
for laureate in laureates:
    if(not(laureate['born'] == '0000-00-00' and laureate['died'] == '0000-00-00') and (laureate['gender'] == 'male' or laureate['gender'] == 'female')):
        for prize in laureate['prizes']:
            affiliations = prize['affiliations']
            for affiliation in affiliations:
                if('country' in affiliation):
                    genders4.append(laureate['gender'])
                    countries.append(affiliation['country'])
                    
countries = list(np.where(np.asarray(countries) == 'Alsace (then Germany, now France)', 'Germany', countries))

genders_affCountries = pd.DataFrame([countries, genders4]).swapaxes(0,1)
genders_affCountries.columns = ['Country', 'Gender']
#scipy.stats.chi2_contingency(genders_affCountries)

print(genders_affCountries)
genders_affCountries_crosstab = pd.crosstab(genders_affCountries.Country, genders_affCountries.Gender, margins=True)
genders_affCountries_crosstab = genders_affCountries_crosstab.sort_values(by="female",ascending=False)
print(genders_affCountries_crosstab)

genders_affCountries_crosstab = pd.crosstab(genders_affCountries.Country, genders_affCountries.Gender)
genders_affCountries_crosstab = genders_affCountries_crosstab.sort_values(by="female",ascending=False)
print(genders_affCountries_crosstab.apply(lambda r: r/r.sum(), axis=1))
genders_affCountries_chi2 = scipy.stats.chi2_contingency(genders_affCountries_crosstab)

#%%-----
# creates DataFrame storing gender and year of award for each recipient.
rows = []
institutions = []
for laureate in nobel_data["laureates"]:
    gender = laureate["gender"]

    # checks for bogus entries
    if laureate["born"] != "0000-00-00":

        # gets years and category of all prizes recipient has won
        for prize in laureate["prizes"]:
            year = prize["year"]
            category = prize["category"]
            rows.append({"gender" : gender, "year" : year, "category" : category})

            # gets affiliated institution of recipient
            for affiliation in prize["affiliations"]:

                # some recipients aren't affiliated with an institution
                if affiliation:
                    if "name" in affiliation:
                        institution = affiliation["name"]
                        institutions.append({"gender" : gender, "institution" : institution})

gender_and_year = pd.DataFrame(rows)
gender_and_year = gender_and_year[["gender","year"]]

gender_and_year = gender_and_year[(gender_and_year.gender == "male") | (gender_and_year.gender == "female")] # considers only male and female genders
gender_frequency = gender_and_year.gender.value_counts()
gender_frequency.plot(kind="bar")
plt.title("Gender of Nobel Prize Recipients")
plt.xlabel("Gender")
plt.ylabel("Frequency")
plt.xticks(rotation="horizontal")
# plt.show()
plt.close()

gender_and_year_frequency = pd.crosstab(gender_and_year.year, gender_and_year.gender)
gender_year_chi2 = scipy.stats.chi2_contingency(gender_and_year_frequency)

start_decade = 1901
end_decade = 1909
# groups gender counts per year into decades.
for year in range(0,len(gender_and_year_frequency),10):
    gender_and_year_frequency.loc[str(start_decade) : str(end_decade)] = gender_and_year_frequency.loc[str(start_decade) : str(end_decade)].cumsum()
    start_decade = end_decade + 1
    end_decade = end_decade + 10

gender_and_year_frequency = gender_and_year_frequency.loc[["1909","1919","1929","1939","1949","1959","1969","1979","1989","1999","2009","2017"]]
gender_and_year_frequency.index = pd.Series(["1900s","1910s","1920s","1930s","1940s","1950s","1960s","1970s","1980s","1990s","2000s","2010s"])

gender_year_graph = gender_and_year_frequency.plot(kind="bar")
plt.title("Gender Distribution of Nobel Laureates by Decade")
plt.xlabel("Decade")
plt.ylabel("Frequency")
# plt.show()
plt.close()

gender_and_category = pd.DataFrame(rows)
gender_and_category = gender_and_category[["gender","category"]]

category_gender_frequency = pd.crosstab(gender_and_category.category, gender_and_category.gender)
category_gender_frequency = category_gender_frequency.sort_values(by="male",ascending=False)
category_gender_frequency.plot(kind="bar")
plt.title("Gender Frequency by Nobel Prize Category")
plt.xlabel("Category")
plt.ylabel("Frequency")
plt.xticks(rotation="horizontal")
# plt.show()
plt.close()

category_chi2 = scipy.stats.chi2_contingency(category_gender_frequency)

gender_and_institution = pd.DataFrame(institutions)

# gets top five institutions with the most nobel prize recipients
top_institutions = gender_and_institution.institution.value_counts().head(5).to_frame().reset_index()
top_institutions.columns = ["institution", "frequency"]
institution_gender_counts = pd.merge(top_institutions,gender_and_institution, on="institution")
del institution_gender_counts["frequency"]

institution_gender_counts = pd.crosstab(institution_gender_counts.institution, institution_gender_counts.gender)
institution_gender_counts = institution_gender_counts.sort_values(by="male", ascending=False)
institution_gender_counts.index = pd.Series(["UC","Harvard","Caltech","MIT", "Stanford"])

institution_gender_counts.plot(kind="bar")
plt.title("Gender of Nobel Laureates in Top Universities")
plt.xlabel("Universities with Most Laureates")
plt.ylabel("Gender Frequency")
plt.xticks(rotation="horizontal")
# plt.show()
plt.close()