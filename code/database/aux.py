# auxiliar file for handling the database.
from basic import *

def get_age(birth_date, year):
    """ 
    receives a string containing the date in the format dd/mm/yyyy
    returns the age of the person in the year he/she begginned math
    """
    # get year born
    dates = birth_date.split('/') # take off " "
    year_born = int(dates[2])

    # calculate and assert age
    age = year - year_born

    # assert 
    assert (age > 0 and age < 100)

    return age

def get_local(uf):
    """ 
    receives a string containing the uf of the person
    returns a code depending if the guy is local, or comes from another region or 
    there is a missing value
    """
    if uf == "df":
        return 1
    elif len(uf) >= 1:
        return 2
    else:
        return 3

def get_time_periods():
    """ 
    return list of time periods we're considering
    """
    time_periods = []
    for year in range(YEAR_START, YEAR_END + 1):
        time_periods.append((year, 1))
        time_periods.append((year, 2))
    return time_periods
