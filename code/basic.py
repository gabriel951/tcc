# basic definitions
import psycopg2

# work constants
YEAR_START = 2000
YEAR_END = 2015
YEAR_START_TRA = 2000 
YEAR_END_TRA = 2010
YEAR_START_TEST = 2011
YEAR_END_TEST = 2015

# file extension
FILE_NAME = 'C'
EXTENSION = '.csv'
CSV_PATH = '../mencoes/'
ENCODING = 'latin'
DATABASE_NAME = 'postgres'
MY_DATABASE = 'bd_unb'

# database connection
USER = 'postgres'
PASSWORD = 'amesma'
HOST = 'localhost'
PORT = '5432'

# index of the fields in the file
CODE_IND = 0
SEX_IND = 1
DEGREE_IND = 2
BDAY_IND = 4
LOCAL_IND = 6
QUOTA_IND = 7
SCHOOL_IND = 9
RACE_IND = 10
YEAR_IN_IND = 14
YEAR_END_IND = 17
COURSE_IND = 53
SUB_CODE_IND = 72
GRADE_IND = 73
SUB_NAME_IND = 74

# courses being considered
COURSES_CONSIDERED = ["ciência da computação", "estatística", "matemática"]

def close_conn(conn):
    """
    close connection from database
    """
    conn.close()

def get_conn():
    """
    returns a connection to the database
    """
    # try to connect to database 
    #try: 
    conn = psycopg2.connect(database=DATABASE_NAME, user=USER, password=PASSWORD, \
                host=HOST, port=PORT)
    #except:
    #    exit("failed to connect to database")

    # return 
    return conn

def get_mode_year(mode):
    """
    receives a string
    returns a tuple containing the limits for year of beggining and end
    """
    if mode == 'small':
        return (YEAR_START, YEAR_START + 1)
    elif mode == 'training':
        return (YEAR_START_TRA, YEAR_END_TRA)
    elif mode == 'testing':
        return (YEAR_START_TEST, YEAR_END_TEST)
    elif mode == 'all':
        return (YEAR_START, YEAR_END)
    else:
        exit('wrong call to get mode year')
