# auxiliar file for handling the database.
import sys
sys.path.append('..')
from basic import *
from basic import *

def get_age(birth_date, year):
    """ 
    get age of the person in the year he/she begginned the course
    receives:
        1. string containing the date in the format yyyy-mm-dd
        2. year student begginned the course
    returns:
        age of the person in the year he/she begginned the course
    """
    # get year born
    dates = birth_date.split('-') 
    year_born = int(dates[0])

    # calculate and assert age
    age = year - year_born

    # assert 
    assert (age > 0 and age < 100)
    return age

def get_code(info):
    """
    parse and return the code for a given student
    receives: 
        1. string containing the code, in the format 'ALUNO xxxxx'
        2. the year the student got in unb
        3. the semester the student got in unb
    returns:
        integer correspondent to the student code
    """
    # get year and semester student entered
    (year_in, sem_in) = get_year_sem(info[YEAR_SEM_IN_OPT_IND], False)

    # get original code, in the csv file
    code_str = info[CODE_IND]
    contents = code_str.split(' ')
    original_code = contents[1]

    # calculate and return code
    code = int(str(original_code) + str(year_in) + str(sem_in))
    return code

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

def get_local(uf):
    """ 
    get whether the person is from DF or from another region
    receives:
        1. a string containing the uf of the person
    returns: 
        a string regarding the locality of the student 
    """
    if uf == "df":
        return "df"
    elif len(uf) >= 1:
        return "outros"
    else:
        return "indisponível"

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

def get_time_periods():
    """ 
    return list of time periods we're considering
    """
    time_periods = []
    for year in range(YEAR_START, YEAR_END + 1):
        time_periods.append((year, 1))
        time_periods.append((year, 2))
    return time_periods

def get_year_sem(year_sem_string, check_consistency):
    """
    get year and semester of a given student
    receives:
        1. string containing the information
        2. boolean to indicate if we should check check_consistency
    returns:
        tuple on the format (year, sem)
    """
    # handle case of entrie equal to 0, which is used in the csv file to explain a
    # student has not graduated yet. 
    if year_sem_string == '0': 
        return (9999, 1) # return a year bigger than the one we are considering, so 
                         # student will not get included in database


    year = int(year_sem_string[:-1])
    sem = int(year_sem_string[-1])
    if check_consistency:
        assert (year >= YEAR_START and year <= YEAR_END)
        assert (sem == 0 or sem == 1 or sem == 2)
    return (year, sem)
