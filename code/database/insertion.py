#!/usr/bin/python3.4
# python file to read records and put them on database
import csv
import psycopg2 

# import basic
import sys
sys.path.append('..')
from basic import *

from aux import *

# lines read, valid lines, insertions done so far
lines_read = 0
valid_lines = 0
insertions = 0

def execute_query(query, cur, conn):
    """
    try to execute query, rolling back if there's already an entry
    """
    global insertions

    try:
        cur.execute(query)
        insertions += 1
    except psycopg2.IntegrityError:
        conn.rollback()

    conn.commit()

def insert_database(year, semester):
    """
    inserts data on the database for a given year and
    semester in unb 
    """
    global lines_read, valid_lines, insertions
    file_name = CSV_PATH + FILE_NAME + str(year) + str(semester) + EXTENSION

    # get connection and cursor
    conn = get_conn()
    cur = conn.cursor()

    # read line by line, parsing the results and putting on database
    with open(file_name, newline = '', encoding = ENCODING) as fp:
        reader = csv.reader(fp)

        # iterate through the rows, inserting in the table
        for row in reader:
            parse_insert(row, cur, conn, year, semester)
            
    # close connection
    close_conn(conn)

    print("insertions: %d" % (insertions))

def insert_student(info, cur, conn, year):
    """
    receives a list with the information, the cursor and a connection
    insert students on database
    """
    global insertions

    # get student information #[1:-1] to remove quotes
    code = int(info[CODE_IND])
    sex = info[SEX_IND][1:-1].lower()
    age = get_age(info[BDAY_IND][1:-1], year)
    quota = info[QUOTA_IND][1:-1].lower()
    school_type = info[SCHOOL_IND][1:-1].lower()
    race = info[RACE_IND][1:-1].lower()
    local = get_local(info[LOCAL_IND][1:-1].lower())
    course = info[COURSE_IND].lower()
    year_in = int(info[YEAR_IN_IND][1:-1])
    year_end = int(info[YEAR_END_IND][1:-1])

    # insert in the database, in case not present
    query = "insert into %s.student (cod_mat, sex, age, quota, school_type, race, \
            local, course, year_in, year_end) values (%d, '%s', %d, '%s', '%s', \
            '%s', %d, '%s', %d, %d)" \
                % (MY_DATABASE, code, sex, age, quota, school_type, race, local, \
                    course, year_in, year_end)

    execute_query(query, cur, conn)

def insert_subject(info, cur, conn):
    """
    receives a list with the information, the cursor and a connection
    insert subject on database
    """
    global insertions

    # get subject information #[1:-1] to remove quotes
    code = int(info[SUB_CODE_IND])
    name = info[SUB_NAME_IND][1:-1].lower()

    # insert in the database, in case not present
    query = "insert into %s.subject (code, name) values (%d, '%s')" \
                % (MY_DATABASE, code, name) 

    execute_query(query, cur, conn)

def insert_subject_student(info, cur, conn, year, semester):
    """
    insert a relation of student and subject he has coursed
    """
    global insertions

    # get student and subject information #[1:-1] to remove quotes
    code_stu = int(info[CODE_IND])
    code_sub = int(info[SUB_CODE_IND])
    grade = info[GRADE_IND][1:-1]

    # insert in the database, in case not present
    query = "insert into %s.student_subject (code_stu, code_sub, grade, semester, \
    year) values (%d, %d, '%s', %d, %d)" \
                % (MY_DATABASE, code_stu, code_sub, grade, semester, year) 

    execute_query(query, cur, conn)

def parse_insert(row, cur, conn, year, semester):
    """
    receives a row of the csv file (as a list), a cursor, a connection, and the year 
    inserts the fields in the database
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

    # obtain degree and course
    info[DEGREE_IND] = info[DEGREE_IND][1:-1]
    info[COURSE_IND] = info[COURSE_IND][1:-1]
    
    # skip if not from graduation
    if info[DEGREE_IND].lower() != "graduacao":
        return

    # skip if not from an interesting course
    if info[COURSE_IND].lower() not in COURSES_CONSIDERED:
        return

    # skip if not in the time period we're considering
    if int(info[YEAR_IN_IND]) < YEAR_START or int(info[YEAR_END_IND]) > YEAR_END: 
        return

    insert_student(info, cur, conn, year)
    insert_subject(info, cur, conn)
    insert_subject_student(info, cur, conn, year, semester)

