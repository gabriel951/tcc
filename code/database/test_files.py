#!/usr/bin/python3.4
# python file to make test related to the files given to me
from insertion import *

# constants
# maximum number of values a column possess
MAX_DIFF_VALUES = 100000

def study_row(row, index, diff_values, mode = 'selected_courses'):
    """
    receives a row, an index, a list of different values found so far
    mode is an optional, and determine whether we should consider only the courses on
    our list or all courses. 

    analyses if the column with given index in the row passed presents a value 
    different from diff_values

    if it presents, append to diff_values
    """
    global lines_read, valid_lines

    # return case of empty row
    if len(row) == 0:
        return 

    lines_read += 1

    # get row content - the row is a list with possibly more than one entry
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
    if mode == 'selected_courses':
        if info[COURSE_IND].lower() not in COURSES_CONSIDERED:
            return
    
    valid_lines += 1

    if not (info[index] in diff_values): 
        diff_values.append(info[index])

# shows how many different values a column has for a given year and semester
def test_column_values(time_periods, index, mode = 'selected_courses'):
    """
    receives a time period list of the form [(year, semester), ...]
    an index for the column to be analysed
    print all diferent values found for that particular column
    """
    global lines_read, valid_lines

    # file for writing the different values encontered
    log = open('../logs/dif_values_index_' + str(index) + '.txt', 'w')
    log.write("different values encountered for the csv file\n")

    # for every time period
    for time_period in time_periods:
        lines_read = 0
        valid_lines = 0
        
        # get file name
        year = time_period[0]
        semester = time_period[1]
        file_name = CSV_PATH + FILE_NAME + str(year) + str(semester) + EXTENSION
        print("starting study for: " + file_name)

        # get connection
        conn = get_conn()

        # different values found so far
        diff_values = []

        # read line by line, parsing the results and putting on database
        with open(file_name, newline = '', encoding = ENCODING) as fp:
            reader = csv.reader(fp)

            # iterate through the rows, inserting in the table
            for row in reader:
                study_row(row, index, diff_values, mode)
                if len(diff_values) > MAX_DIFF_VALUES: 
                    print("too much diff_values")
                
            # show diff values
            diff_values.sort()
            log.write(str(diff_values))

        # close connection
        close_conn(conn)

        # close file pointer
        fp.close()

        print("lines: %s valid_lines: %s" %(lines_read, valid_lines))

# test to see if it can insert in the database
def test_insertion(mode = 'quick'):
    """
    mode can be quick or normal
    if quick, only insert for one semester
    if normal insert for all time period considered
    """
    if mode == 'quick':
        insert_database(2000, 1)

    elif mode == 'normal':
        print("starting insertion")
        time_periods = get_time_periods()
        for (year, semester) in time_periods:
            print("starting for (%d %d)" % (year, semester))
            insert_database(year, semester)
        print("finishing insertion")
    else:
        exit("error in mode passed")

# test values for some columns in the database
def test_database():

    # just for quick test use this variable instead of time_periods
    test_time = [(2000, 1)]

    # list of time period we're considering
    time_periods = get_time_periods()

    # list of index we are considering - for this study, were not considering
    #CODE_IND and BDAY_IND
    ind_list = []
    #ind_list.append(SEX_IND)
    #ind_list.append(DEGREE_IND)
    #ind_list.append(COURSE_IND)
    #ind_list.append(LOCAL_IND)
    #ind_list.append(QUOTA_IND)
    #ind_list.append(SCHOOL_IND)
    #ind_list.append(RACE_IND)
    #ind_list.append(YEAR_IN_IND)
    #ind_list.append(SEM_IN_IND)
    #ind_list.append(YEAR_END_IND)
    #ind_list.append(YEAR_END_IND)
    #ind_list.append(SUB_CODE_IND)
    #ind_list.append(SUB_NAME_IND)
    ind_list.append(WAY_IN_IND)
    #ind_list.append(WAY_OUT_IND)

    for ind in ind_list:
        test_column_values(test_time, ind, mode = 'selected_courses')

#test_database()
#test_insertion()
test_insertion('normal')
#clean_database()
