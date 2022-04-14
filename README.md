# Simple Password Safety classifier

Simple password safety analyzer aims to simplify the analysis of large amounts of passwords in research environment.
This specific program is designed in a way to process 3 different control groups, and to return a final score for each
password in each group. The minimum score is 0 and the maximum is 8 (depending on the amount of criterias).
The criterias taken in consideration here are:  

    * length   
    * upper/lower case
    * special characters
    * alfanumeric
    * names or surnames
    * presence of dictionary words (Dutch, English, or German).
    * presence of dates of birth
    * presence of recent dates (hardcoded 2010 - 2022)
    

## Usage

Fill in the passwords in the `data/Passwords.xlsx` file, build and run the program. The output scores will be
written in the `scores_output.xlsx` file.