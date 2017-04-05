#!/usr/bin/python3.4
# python file to make test related to the files given to me
from insertion import *

# constants
# maximum number of values a column possess
MAX_DIFF_VALUES = 100000

def study_row(row, index, diff_values):
    """
    analyses if the column with given index in the row passed presents a value 
    different from diff_values. If it does, append to diff_values

    receives:
        1. a row of a csv file 
        2. an index, 
        3. a list of different values found so far
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

    # skip if not from graduation
    if info[DEGREE_IND].lower() != "graduacao":
        return
    
    valid_lines += 1

    if not (info[index] in diff_values): 
        diff_values.append(info[index])

# shows how many different values a column has for a given year and semester
def test_column_values(index):
    """
    print all diferent values found for a particular database column
    receives:   
        1. index of the column
    returns:
        nothing
    """
    global lines_read, valid_lines

    # file for writing the different values encontered
    log = open('../logs/dif_values_index_' + str(index) + '.txt', 'w')
    log.write("different values encountered for the csv file\n")

    file_name = CSV_PATH + FILE_NAME + EXTENSION

    # get connection
    conn = get_conn()

    # different values found so far
    diff_values = []

    # read line by line, parsing the results and putting on database
    with open(file_name, newline = '', encoding = ENCODING) as fp:
        reader = csv.reader(fp)

        # iterate through the rows, inserting in the table
        for row in reader:
            study_row(row, index, diff_values)
            if len(diff_values) > MAX_DIFF_VALUES: 
                print("too much diff_values")
            
        # show diff values
        diff_values.sort()
        log.write(str(diff_values))

    # close connection
    close_conn(conn)

    # close file pointer
    fp.close()

    print("lines: %s valid_lines: %s" % (lines_read, valid_lines))

# test values for some columns in the database
def test_database():
    """
    test the values for columns in database
    returns: 
        nothing
    receives: 
        nothing
    """
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
    #ind_list.append(WAY_IN_IND)
    #ind_list.append(WAY_OUT_IND)

    for ind in ind_list:
        test_column_values(ind)

if __name__ == "__main__":
    #test_database()
    insert_database()
    #clean_database()
