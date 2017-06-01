# basic definitions
import psycopg2

# work constants
YEAR_START = 2000
YEAR_END = 2016
YEAR_START_TRA = 2000 
YEAR_END_TRA = 2009
YEAR_START_TEST = 2010
YEAR_END_TEST = 2016

# age threshold decided in order to split students 
# young students are up to age threshold INCLUSIVELY
AGE_THRESHOLD = 30 

# file extension
FILE_NAME = 'novos_dados'
EXTENSION = '.csv'
CSV_PATH = '../mencoes/'
ENCODING = 'latin'
DATABASE_NAME = 'postgres'
MY_DATABASE = 'bd_unb'
SEP_CSV_FILE = '\t'

# database connection
USER = 'postgres'
PASSWORD = 'amesma'
HOST = 'localhost'
PORT = '5432'

# index of the fields in the csv file
CODE_IND = 0
SEX_IND = 1
BDAY_IND = 2
LOCAL_IND = 3
QUOTA_IND = 4
SCHOOL_IND = 5
RACE_IND = 6
COURSE_IND = 7
OPT_COURSE_IND = 8 # option for the course
YEAR_SEM_IN_UNB_IND = 9 # year and semester student entered in unb
YEAR_SEM_IN_OPT_IND = 10 # year and semester student entered in his option
WAY_IN_IND = 11
YEAR_SEM_END_IND = 12 # year and semester student left unb
WAY_OUT_IND = 13
YEAR_SEM_SUB_IND = 14 # year and semester student coursed a given discipline
IRA_IND = 15
CREDITS_FORM_IND = 16
CREDITS_COURSE_IND = 17
CREDITS_DONE_IND = 18
CREDITS_TO_DO_IND = 19
CREDITS_APPROVED_SEM_IND = 20
SUB_CODE_IND = 21
SUB_NAME_IND = 22
SUB_CREDITS_IND = 23
SUB_GRADE_IND = 24

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

# group of courses been considered
TI_COURSES = [MECHATRONICS_ENGINEERING, NETWORK_ENGINEERING]
LIC_COURSES = [CIC_NON_BACHELOR]
COMP_COURSES = [CIC_BACHELOR, SOFTWARE_ENGINEERING, COMPUTER_ENGINEERING]

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
WAY_OUT_CONSIDERED.append('Desligamento Jubilamento')
WAY_OUT_CONSIDERED.append('Deslig - não cumpriu condição')
WAY_OUT_CONSIDERED.append('Repr 3 vezes na mesma disc obr')
WAY_OUT_CONSIDERED.append('Mudança de Curso')
WAY_OUT_CONSIDERED.append('Mudança de Turno')
WAY_OUT_CONSIDERED.append('Novo Vestibular')
WAY_OUT_CONSIDERED.append('Outros')
WAY_OUT_CONSIDERED.append('Vestibular p/outra Habilitação')
WAY_OUT_CONSIDERED.append('Desligamento-Força de Convênio')
WAY_OUT_CONSIDERED.append('Desligamento Voluntário')
WAY_OUT_CONSIDERED.append('Desligamento Falt Documentação')
WAY_OUT_CONSIDERED.append('Desligamento por Força de Intercãmbio')
WAY_OUT_CONSIDERED.append('Desligamento Decisão  Judicial')
WAY_OUT_CONSIDERED.append('Anulação de Registro')
WAY_OUT_CONSIDERED.append('Ex-Aluno (Decreto 477)')
WAY_OUT_CONSIDERED.append('Transferência')
WAY_OUT_CONSIDERED.append('Formatura')
WAY_OUT_CONSIDERED.append('Falecimento')

# way out that were considered migration
MIGRATION_WAY_OUT = []
# TODO: Outros should be migration?
MIGRATION_WAY_OUT.append('Outros')
MIGRATION_WAY_OUT.append('Mudança de Curso')
MIGRATION_WAY_OUT.append('Mudança de Turno')
MIGRATION_WAY_OUT.append('Novo Vestibular')
MIGRATION_WAY_OUT.append('Vestibular p/outra Habilitação')
MIGRATION_WAY_OUT.append('Transferência')

# way out that were considered evasion
EVASION_WAY_OUT = []
EVASION_WAY_OUT.append('Desligamento - Abandono')
EVASION_WAY_OUT.append('Desligamento Decisão  Judicial')
EVASION_WAY_OUT.append('Desligamento Jubilamento')
EVASION_WAY_OUT.append('Deslig - não cumpriu condição')
EVASION_WAY_OUT.append('Repr 3 vezes na mesma disc obr')
EVASION_WAY_OUT.append('Desligamento-Força de Convênio')
EVASION_WAY_OUT.append('Desligamento Voluntário')
EVASION_WAY_OUT.append('Desligamento Falt Documentação')
EVASION_WAY_OUT.append('Desligamento por Força de Intercãmbio')
EVASION_WAY_OUT.append('Anulação de Registro')
EVASION_WAY_OUT.append('Ex-Aluno (Decreto 477)')

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
