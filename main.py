""""
Simple password safety analyzer based on Dutch, English, and German dictionaries, and few common
criterias of general password strength.
"""

import pandas as pd
import numpy as np

__author__ = "German Savchenko"
__copyright__ = ""
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "German Savchenko"
__email__ = "german.savchenko@gmail.com"

pswds = []
excel_data_df = pd.read_excel('data/Passwords.xlsx', sheet_name='Sheet1')
# get column names
headers = excel_data_df.columns.ravel()

# load data from the excel file containing passwords into 3 lists
for i in range(3):
    pswds.append(excel_data_df[headers[i]].tolist())
    print(pswds[i])

scores = np.zeros((3, len(pswds[0])))
special_characters = "\"!@#$%^&*()-+?_=,.~<>/\\\'"

# load dictionaries of words, filter out short words
# english dictionary
enDict = []
with open('data/english.txt') as file:
    while line := file.readline().rstrip():
        if len(line) > 5: enDict.append(line)
# dutch dictionary
nlDict = []
with open('data/dutch.txt') as file:
    while line := file.readline().rstrip():
        if len(line) > 5: nlDict.append(line)

# german dictionary
deDict = []
with open('data/german.txt') as file:
    while line := file.readline().rstrip():
        if len(line) >= 4: deDict.append(line)

# collection of common names and surnames
namesDict = []
with open('data/names.txt') as file:
    while line := file.readline().rstrip():
        if len(line) >= 4: namesDict.append(line)
with open('data/lastnames.txt') as file:
    while line := file.readline().rstrip():
        if len(line) >= 4: namesDict.append(line)

# date arrays
# year 1950 - 2004
birthDatesDict = np.arange(start=1950, stop=2005)
# year 2010 - 2021
recentDatesDict = np.arange(start=2010, stop=2022)

# lists for separate scores (3 dimensions per list)
passwordLength = np.zeros((3, len(pswds[0])))
numbersAndLetters = np.zeros((3, len(pswds[0])))
upperAndLowerCases = np.zeros((3, len(pswds[0])))
specialCharacters = np.zeros((3, len(pswds[0])))
dictionaryWords = np.zeros((3, len(pswds[0])))
namesOrSurnames = np.zeros((3, len(pswds[0])))
datesOfBirth = np.zeros((3, len(pswds[0])))
recentDates = np.zeros((3, len(pswds[0])))

for j in range(3):
    for i in range(len(pswds[j])):
        scoreCount = 0
        current = str(pswds[j][i])
        # check if longer that 8 characters
        if len(current) > 8: scoreCount += 1; passwordLength[j, i] = 1
        # check if contains numbers and letters
        if not current.isnumeric() and not current.isalpha(): scoreCount += 1; numbersAndLetters[j, i] = 1
        # check if contains upper and lower case characters
        if any(x.isupper() for x in current) and any(x.islower() for x in current): scoreCount += 1; upperAndLowerCases[
            j, i] = 1
        # check for special characters
        if any(x in special_characters for x in current): scoreCount += 1; specialCharacters[j, i] = 1
        # check for dictionary words (dutch, english, german(only most common words for german))
        # casefold is used to compare strings with case insensitivity
        if not (any(x.casefold() in current.casefold() for x in enDict)
                or any(y.casefold() in current.casefold() for y in deDict)
                or any(z.casefold() in current.casefold() for z in nlDict)): scoreCount += 1; dictionaryWords[j, i] = 1
        # check for names
        if not (any(str(x.casefold()) in current.casefold() for x in namesDict)): scoreCount += 1; namesOrSurnames[j, i] = 1
        # check for dates of birth
        if not (any(str(x) in current for x in birthDatesDict)): scoreCount += 1; datesOfBirth[j, i] = 1
        # check for recent dates
        if not (any(str(x) in current for x in recentDatesDict)): scoreCount += 1; recentDates[j, i] = 1
        # save the total score of the specific password
        scores[j, i] = scoreCount

print(scores[j, i])
output = pd.DataFrame({'passwordLength1': passwordLength[0],
                       'numbersAndLetters1': numbersAndLetters[0],
                       'upperAndLowerCases1': upperAndLowerCases[0],
                       'specialCharacters1': specialCharacters[0],
                       'dictionaryWords1': dictionaryWords[0],
                       'namesOrSurnames1': namesOrSurnames[0],
                       'datesOfBirth1': datesOfBirth[0],
                       'recentDates1': recentDates[0],
                       'passwordLength2': passwordLength[1],
                       'numbersAndLetters2': numbersAndLetters[1],
                       'upperAndLowerCases2': upperAndLowerCases[1],
                       'specialCharacters2': specialCharacters[1],
                       'dictionaryWords2': dictionaryWords[1],
                       'namesOrSurnames2': namesOrSurnames[1],
                       'datesOfBirth2': datesOfBirth[1],
                       'recentDates2': recentDates[1],
                       'passwordLength3': passwordLength[2],
                       'numbersAndLetters3': numbersAndLetters[2],
                       'upperAndLowerCases3': upperAndLowerCases[2],
                       'specialCharacters3': specialCharacters[2],
                       'dictionaryWords3': dictionaryWords[2],
                       'namesOrSurnames3': namesOrSurnames[2],
                       'datesOfBirth3': datesOfBirth[2],
                       'recentDates3': recentDates[2],
                       'totalScore1': scores[0],
                       'totalScore2': scores[1],
                       'totalScore3': scores[2]})


writer = pd.ExcelWriter("scores_output.xlsx", engine='xlsxwriter') # create pandas writer for excel

output.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False)


workbook = writer.book # get the xlsxwriter workbook and worksheet objects.
worksheet = writer.sheets['Sheet1']


header_format = workbook.add_format({ # add a header format.
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'fg_color': '#D7E4BC',
    'border': 1})


for col_num, value in enumerate(output.columns.values): # write the column headers with the defined format.
    worksheet.write(0, col_num + 1, value, header_format)


writer.save() # close the Pandas Excel writer and output the Excel file.
