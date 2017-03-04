#!/usr/bin/python3.4
# python file to read records and put them on database
import csv
import psycopg2 

# import basic and aux
import sys
sys.path.append('..')
from basic import *
from aux import *

# lines read, valid lines, insertions done so far
lines_read = 0
valid_lines = 0
insertions = 0

def clean_database():
    """
    after the database is built, substitute appropriate values to increase
    consistency
    """
    # get connection and cursor
    conn = get_conn()
    cur = conn.cursor()

    # get list of all student
    table = 'student'
    query = 'select * from %s.%s;' % (MY_DATABASE, table)
    cur.execute(query)
    rows = cur.fetchall()

    # update student info, one by one
    for row in rows:
        update_student_info(conn, cur, row)

    close_conn(conn)

def execute_query(query, cur, conn):
    """
    try to execute query, rolling back if there's already an entry
    """
    global insertions

    try:
        cur.execute(query)
        insertions += 1
        # just to show work being done
        if insertions % 100 == 0: 
            print("insertions: %d" % (insertions))

    except psycopg2.IntegrityError:
        conn.rollback()
    #except psycopg2.ProgrammingError:
    #    print(query)
    #    exit()

    conn.commit()

def insert_database():
    """
    insert student and subject on database
    receives:
        nothing
    returns:
        nothing
    """
    global lines_read, valid_lines, insertions
    file_name = CSV_PATH + FILE_NAME + EXTENSION

    # get connection and cursor
    conn = get_conn()
    cur = conn.cursor()

    print("insertions: %d" % (insertions))

    # read line by line, parsing the results and putting on database
    with open(file_name, newline = '', encoding = ENCODING) as fp:
        reader = csv.reader(fp)

        # skip first line
        next(reader, None)

        # iterate through the rows, inserting in the table
        for row in reader:
            parse_insert(row, cur, conn)

            
    # close connection
    close_conn(conn)

    print("insertions: %d" % (insertions))

def insert_student(info, cur, conn):
    """
    insert student info contained in a row of the csv file in a database 
    receives:
        1. list with the information
        2. the cursor 
        3. connection
    returns:
        nothing
    """
    global insertions

    # get year and semester student entered - will be needed for the age
    # that's why outside order
    (year_in, sem_in) = get_year_sem(info[YEAR_SEM_IN_OPT_IND], True)

    # get student information #[1:-1] may be needed to remove quotes
    code = get_code(info[CODE_IND])
    sex = info[SEX_IND].lower()
    age = get_age(info[BDAY_IND], year_in)
    local = get_local(info[LOCAL_IND].lower())
    quota = info[QUOTA_IND].lower()
    school_type = info[SCHOOL_IND].lower()
    race = info[RACE_IND].lower()
    course = info[COURSE_IND].lower()
    # year in and semester in were already calculated
    #year_in
    #sem_in
    (year_end, sem_end) = get_year_sem(info[YEAR_SEM_END_IND], True)
    way_in = info[WAY_IN_IND]
    way_out = info[WAY_OUT_IND]

    # insert in the database, in case not present
    query = "insert into %s.student (cod_mat, sex, age, quota, school_type, race, \
            local, course, year_in, semester_in, year_end, semester_end, way_in, way_out) values \
            (%d, '%s', %d, '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d, '%s', '%s')" \
                % (MY_DATABASE, code, sex, age, quota, school_type, race, local, \
                    course, year_in, sem_in, year_end, sem_end, way_in, way_out)

    execute_query(query, cur, conn)

def insert_subject(info, cur, conn):
    """
    insert student info contained in a row of the csv file in a database 
    receives:
        1. list with the information
        2. cursor 
        3. connection
    returns:
        nothing
    """
    global insertions

    # get subject information #[1:-1] may be needed to remove quotes
    code = int(info[SUB_CODE_IND])
    name = info[SUB_NAME_IND].lower()
    credits = int(info[SUB_CREDITS_IND])

    # fix in case name has the ' or a lot of spaces that we don't need
    name = name.replace("'", "") 
    name = name.replace("   ", "")

    # insert in the database, in case not present
    query = "insert into %s.subject (code, name, credits) values (%d, '%s', %d)" \
                % (MY_DATABASE, code, name, credits) 

    execute_query(query, cur, conn)

def insert_subject_student(info, cur, conn):
    """
    insert a relation of student and subject he has coursed
    receives:
        1. row containing student and subject info
        2. cursor
        3. connection
    returns: 
        nothing
    """
    global insertions

    # get student and subject information #[1:-1] to remove quotes
    (year, sem) = get_year_sem(info[YEAR_SEM_SUB_IND], True)
    code_stu = get_code(info[CODE_IND])
    code_sub = int(info[SUB_CODE_IND])
    grade = info[SUB_GRADE_IND]

    # insert in the database, in case not present
    query = "insert into %s.student_subject (code_stu, code_sub, grade, semester, \
    year) values (%d, %d, '%s', %d, %d)" \
                % (MY_DATABASE, code_stu, code_sub, grade, sem, year) 

    execute_query(query, cur, conn)

def parse_insert(row, cur, conn):
    """
    reads a row on a csv file and inserts the correct info on a database
    receives:
        1. a row of the csv file (as a list)
        2. a cursor
        3. a connection 
    returns:
        nothing
    """
    global lines_read, valid_lines

    # return case of empty row
    if len(row) == 0:
        return 
    lines_read += 1

    # get row content - the row is a list with only one entry
    content = row[0]
    for i in range(1, len(row)):
        content += row[i]

    # split content in list 
    info = content.split(';')

    # skip if not in the time period we're considering
    (year_in, sem_in) = get_year_sem(info[YEAR_SEM_IN_OPT_IND], False)
    (year_end, sem_end) = get_year_sem(info[YEAR_SEM_END_IND], False)
    if year_in < YEAR_START or year_in > YEAR_END: 
        return
    if year_end < YEAR_START or year_end > YEAR_END: 
        return

    insert_student(info, cur, conn)
    insert_subject(info, cur, conn)
    insert_subject_student(info, cur, conn)

def update_student_info(conn, cur, row):
    """
    updates the student information, regarding the course and the race
    receives:
        1. a connection
        2. a cursor 
        3. a tuple,
    returns: 
        nothing
    """
    CODE_IND_TUPLE = 1
    # get query
    new_course = get_course(row)
    new_race = get_race(row)
    query = "update %s.student set course = '%s', race = '%s' where cod_mat = %d;" \
            % (MY_DATABASE, new_course, new_race, row[CODE_IND_TUPLE])

    # execute
    execute_query(query, cur, conn)
