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

def get_course(std_inf):
    """
    receives a student tuple
    returns a string containing the course of a student in proper format
    """
    COURSE_IND_TUPLE = 8
    course = std_inf[COURSE_IND_TUPLE]
    if course == 'ciência da computação':
        return 'CIC'
    elif course == 'engenharia mecatrônica':
        return 'mecatrônica'
    elif course == 'engenharia de redes de comunicação':
        return 'redes'
    elif course == 'engenharia de computação':
        return 'computação'
    elif course == 'engenharia de software':
        return 'eng_softw'
    else:
        print(std_inf, course)
        exit('course not identified')

def get_race(std_inf):
    """
    receives a student tuple
    return a string containing the race of a student in proper format
    """
    RACE_IND_TUPLE = 6
    race = std_inf[RACE_IND_TUPLE]
    # remove first and last whitespaces
    race = race.strip()
    if race == '0':
        return 'indisponível'
    elif race == '000':
        return 'indisponível'
    elif race == 'nao cadastrada':
        return 'indisponível'
    elif race == 'nao dispoe de informacao':
        return 'indisponível'
    elif race in ['amarela', 'branca', 'parda', 'preta', 'indigena']:
        return race
    else:
        print(race)
        exit('race not identified')

def get_local(uf):
    """ 
    receives a string containing the uf of the person
    returns a code depending if the guy is local, or comes from another region or 
    there is a missing value
    """
    if uf == "df":
        return "df"
    elif len(uf) >= 1:
        return "outros"
    else:
        return "indisponível"

def get_time_periods():
    """ 
    return list of time periods we're considering
    """
    time_periods = []
    for year in range(YEAR_START, YEAR_END + 1):
        time_periods.append((year, 1))
        time_periods.append((year, 2))
    return time_periods
