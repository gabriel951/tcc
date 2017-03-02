# basic definitions
import psycopg2

# work constants
YEAR_START = 2000
YEAR_END = 2015
YEAR_START_TRA = 2000 
YEAR_END_TRA = 2009
YEAR_START_TEST = 2010
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

# index of the fields in the csv file
CODE_IND = 0
SEX_IND = 1
DEGREE_IND = 2
BDAY_IND = 4
LOCAL_IND = 6
QUOTA_IND = 7
SCHOOL_IND = 9
RACE_IND = 10
YEAR_IN_IND = 14
SEM_IN_IND = 15
WAY_IN_IND = 16
YEAR_END_IND = 17
SEM_END_IND = 18 
WAY_OUT_IND = 19
IRA_IND = 34
COURSE_IND = 53
SUB_CODE_IND = 72
GRADE_IND = 73
SUB_NAME_IND = 74

# courses being considered - the names are the ones that appear on the database
COURSES_CONSIDERED = ["ciência da computação", "engenharia de computação", \
"engenharia de redes de comunicação", "engenharia de software", \
"engenharia mecatrônica", "computação"]

# official names for all the courses, this must be used in all the code
CIC_BACHELOR = 'cic_bacharelado'
CIC_NON_BACHELOR = 'cic_licenciatura'
COMPUTER_ENGINEERING = 'engenharia_computacao'
SOFTWARE_ENGINEERING = 'engenharia_software'
MECHATRONICS_ENGINEERING = 'engenharia_mecatronica'
NETWORK_ENGINEERING = 'engenharia_redes'

# courses official name list
COURSES_OFF_NAME = [] 
COURSES_OFF_NAME.append(CIC_BACHELOR)
COURSES_OFF_NAME.append(CIC_NON_BACHELOR)
COURSES_OFF_NAME.append(COMPUTER_ENGINEERING)
COURSES_OFF_NAME.append(SOFTWARE_ENGINEERING)
COURSES_OFF_NAME.append(MECHATRONICS_ENGINEERING)
COURSES_OFF_NAME.append(NETWORK_ENGINEERING)

# all the way out considered in this research
WAY_OUT_CONSIDERED = []
WAY_OUT_CONSIDERED.append('Desligamento - Abandono')
WAY_OUT_CONSIDERED.append('Deslig - Nao Cumpriu condicao')
WAY_OUT_CONSIDERED.append('Rep 3 vezes na mesma Disc Obrig')
WAY_OUT_CONSIDERED.append('Novo Vestibular')
WAY_OUT_CONSIDERED.append('Vestibular p/outra Habilitacao')
WAY_OUT_CONSIDERED.append('Desligamento Forca de Convenio')
WAY_OUT_CONSIDERED.append('Desligamento Voluntario')
WAY_OUT_CONSIDERED.append('Desligamento Falta Documentacao')
WAY_OUT_CONSIDERED.append('Desligamento Decisao Judicial')
WAY_OUT_CONSIDERED.append('Anulacao de Registro')
WAY_OUT_CONSIDERED.append('Ex-Aluno (Decreto 477)')
WAY_OUT_CONSIDERED.append('Transferencia')
WAY_OUT_CONSIDERED.append('Formatura')
WAY_OUT_CONSIDERED.append('Falecimento')

# path for serialized objects
PATH = 'data/'

# avoid magic number - last element on a list
LAST_ELEM = -1

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
