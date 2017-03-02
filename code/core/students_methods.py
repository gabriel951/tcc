#!/usr/bin/python3.4
# this file contain the methods mainly related to the students
from students import *
from outliers import *

def check_missing_values(stu_info, feature):
    """
    reports whether there are students with missing values for a given feature
    receives: 
        1. a dictionary containing the students
        2. the feature we are concerned
    returns:
        nothing
    log: 
        log problematic students on file 'missing_values.txt'
    """
    # file pointer, register problematic students
    fp = open('../logs/missing_values.txt', 'w')

    ## iterate through student, check if any student has ANY missing value
    # ira
    if feature == 'ira': 
        for key, stu in stu_info.items():
            miss_values = 0 
            for pos in range(len(stu.ira)):
                if stu.ira[pos] == NOT_KNOWN:
                    miss_values += 1
                    stu.log_info(fp)
                    break
        fp.write("%d students with missing values problems in ira" % (miss_values))

    fp.close()

def fill_credit_rate(stu_info):
    """
    receives a dictionary containing all student information
    set correctly the credit rate of every student

    * credit rate is the number of credits a student took each semester
    """
    # TODO: I cant fill the credit rate unless i know how many credits each subject
    # has

def fill_condition(stu_info):
    """
    receives a dictionary containing the student information
    fills the condition list for every student
    """
    for key, stu in stu_info: 
        num_semesters = stu.get_num_semesters()
        for i in range(num_semesters):
            i = i + 1
            #stu.in_condition_sem(i):

        # TODO: handle list transformation
def fill_drop_pass_fail_rate_sem(stu, pos, mode, fp):
    """
    fill the drop/pass/fail rate for a given student, for the semester passed
    receives: 
        1. the student
        2. the position for which we want to know the rate
        3. mode informing whether we want the pass rate, the fail rate or the drop
        rate. Should be 'drop', 'pass' or 'fail'
        4. a file pointer, to write case of students that did not course any subject
    returns: 
        nothing
    writes:
        it may write in a file students that haven't coursed any subject until
        pos
    """
    # obtain function to apply and variable of interes
    if mode == 'drop':
        func_apply = student_dropped
        var_interest = stu.drop_rate
    elif mode == 'fail':
        func_apply = student_failed
        var_interest = stu.fail_rate
    elif mode == 'pass':
        func_apply = student_passed
        var_interest = stu.pass_rate

    # iterate through every subject
    sub_coursed = 0
    sub_ok = 0 
    for sub_name, info_list in stu.grades.items():
        for index in range(len(info_list)):
            # make sure the subject was coursed in the period we are considering
            (code, name, grade, year, sem) = stu.get_sub_info(sub_name, index, 'all')
            cur_pos = stu.yearsem_2_pos(year, sem)
            if cur_pos > pos: 
                continue

            # skip DP 
            if grade.lower() == 'dp':
                continue

            # compute statistics
            sub_coursed += 1
            if func_apply(grade): 
                sub_ok += 1
             
    # set attribute correctly 
    try: 
        var_interest[pos] = float(sub_ok) / sub_coursed
    except ZeroDivisionError: 
        var_interest[pos] = 0.0
        print('\t\t\tstudent %d has not coursed any subject in pos: %d' % (stu.reg, pos))
        fp.write('student %d has not coursed any subject in pos: %d\n' % (stu.reg, pos))
        # no need to log cases, have analysed this already
        #stu.log_info(fp)

def fill_drop_pass_fail_rate(stu_info, mode): 
    """
    set correctly the drop_rate or fail_rate or pass_rate for every student
    receives: 
        1. a dictionary containing all student information
        2. mode informing whether we want the pass rate, the fail rate or the drop
        rate. Should be 'drop', 'pass' or 'fail'
    returns: 
        nothing
    """
    # open file that report patological cases
    if mode == 'drop':
        fp = open('../logs/drop_rate_patological_cases.txt', 'w')
    elif mode == 'fail':
        fp = open('../logs/fail_rate_patological_cases.txt', 'w')
    elif mode == 'pass':
        fp = open('../logs/pass_rate_patological_cases.txt', 'w')
    else:
        exit('function fill_drop_pass_fail_rate called with wrong arguments')

    for key, stu in stu_info.items(): 
        # get current student grades
        cur_stu_grades = stu.grades

        # for all positions the student is in 
        num_semesters = stu.get_num_semesters()
        for pos in range(num_semesters):
            fill_drop_pass_fail_rate_sem(stu, pos, mode, fp) 


        # TODO: if rate is problematic (when the student left), 
        # register patological case
        LAST_ELEM = -1 
        if mode == 'drop' and stu.drop_rate[LAST_ELEM] > 0.99: 
            stu.log_info(fp)
        if mode == 'fail' and stu.fail_rate[LAST_ELEM] > 0.99: 
            stu.log_info(fp)
        elif mode == 'pass' and stu.pass_rate[LAST_ELEM] < 0.01:
            stu.log_info(fp)

    # close file
    fp.close()
    print('finished filling %s rate' % (mode))

def fill_empty_iras(stu_info):
    """
    receives the dictionary of students. Search every student list of iras, and
    fill the ira for the semester that we didnt have the information in the database
    """
    # number of student with missing iras
    miss_ira = 0 

    for key, stu in stu_info.items():

        # whether current student has one or more ira missed
        missed_ira = 0

        # calculate missed iras
        for i in range(len(stu.ira)): 
            if stu.ira[i] == NOT_KNOWN: 
                stu.calculate_ira(i)
                missed_ira = 1

        # update miss_ira
        miss_ira += missed_ira

def fill_grades(stu_info, mode = 'normal'):
    """
    query database and add grades of the student to the student dictionary
    receives:
        1. a student info dictionary 
        2. (optional) mode - parameter that can be normal or quick if normal, fill
        grades of all years from 2000 to 2015.  if quick, fill grades of year 2000,
        semester 1
    returns: 
        nothing
    """
    # check if there's any restriction
    if mode == 'normal':
        restriction = ''
    elif mode == 'quick':
        restriction = ' where year == 2000 and semester == 1'
    else: 
        exit('function fill_grades called with wrong arguments')

    # query database in order to obtain student code, subject name and subject grade
    conn = get_conn()
    cur = conn.cursor()
    query = 'select code_stu, code_sub, semester, year, grade, name \
                from %s.student_subject inner join %s.subject \
                on %s.student_subject.code_sub = %s.subject.code' \
                % (MY_DATABASE, MY_DATABASE, MY_DATABASE, MY_DATABASE)
    query += restriction + ';'
    cur.execute(query)
    rows = cur.fetchall()

    # rows indices - RIND
    CODE_STU_RIND = 0

    # for every row in database
    for row in rows:
        # get student id and corresponding student - it may have been deleted as an
        # outlier, so watch key error
        student_id = row[CODE_STU_RIND]
        try: 
            student = stu_info[student_id]
            student.set_grades(row)
        except KeyError:
            # TODO: check if it really was deleted as an outlier
            pass

    print('finished filling grades')

def fill_hard_rate(stu_info):
    """
    fills every student hard rate - the ratio of approvation in the most difficult
    subject the student has coursed 
    receives:
        1. student dictionary, 
    return:
        nothing
    """
    # pointer to register patological cases
    fp = open('../logs/hard_rate_patological_cases.txt', 'w')

    # load dictionary of subjects
    subj_dic = sub.load_subjects(stu_info)

    # iterate through all students, filling the hard rate
    for key, stu in stu_info.items():
        stu.set_hard_rate(subj_dic)
    
    fp.close()

def fill_impr_rate(stu_info):
    """
    receives a dictionary containing all students. 
    fill the student objects with information regarding the improvement rate
    """
    # file logger
    fp = open('../logs/impr_rate_patological_cases.txt', 'w')

    # list of all courses
    course_lst = load_all_courses()

    # iterate through every student
    for key in stu_info:
        # fill the student improvement rate
        stu_info[key].set_improvement_rate(fp, course_lst)

    fp.close()

    # TODO: update values that could not be calculated - use imputation

    print('finished_calculating improvement rate')

def fill_ira(stu_info, mode = 'normal'):
    """
    read the csv file for the student IRA and put the student IRA as an information
    receives:
        1. a dictionary containing all students. 
    returns:
        nothing
    """
    # get all years and semesters to be considered
    if mode == 'quick': 
        fill_ira_year_semester(stu_info, 2000, 1)
    elif mode == 'normal': 
        # fill ira correctly
        print('\tstarting insertion')
        time_periods = get_time_periods()
        for (year, semester) in time_periods:
            print('\tstarting for (%d %d)' % (year, semester))
            fill_ira_year_semester(stu_info, year, semester)
        print('ending insertion')
        print('will start filling info for iras that are not known')
        # TODO: can't handle missing iras because i don't have information 
        # regarding the credit 
        #handle_miss_ira(stu_info)
        print('finished filling missing iras')
    else:
        exit('mode option incorrect')

    
    print('finished filling ira')

def fill_ira_year_semester(stu_info, year, semester):
    """
    read the csv file for the student IRA and put the student IRA as an information
    receives:
        1. a dictionary containing all students. 
    returns: 
        nothing
    """
    global ira_filled
    file_name = CSV_PATH + FILE_NAME + str(year) + str(semester) + EXTENSION

    # read line by line, parsing the results and putting on database
    with open(file_name, newline = '', encoding = ENCODING) as fp:
        reader = csv.reader(fp)

        # iterate through the rows, inserting in the table
        for row in reader:
            parse_insert_ira(stu_info, row, year, semester)
            
    print("\tnumber of iras added: %s" % (ira_filled))

def fill_mand_rate(stu_info):
    """
    receives dictionary containing student info
    set correctly the mandatory rate for a given student and the credit rate

    * the mandatory rate is the reason between the number of mandatory subjects taken 
    so far and the number of subjects taken so far
    """
    # load all courses
    try: 
        courses = pickle.load(open(path + name, 'rb'))
    except FileNotFoundError:
        register_all_courses()
        courses = pickle.load(open(path + name, 'rb'))

    # for each student, put the course 
    for key, student in stu_info.items():
        student.set_mand_rate(courses)

    print('finished filling mandatory rate')

def fill_position(stu_info):
    """
    receives a student dictionary
    put the information regarding the position the student is in (compared to every
    other student on the same course and semester) 
    """
    # avoid magic ;)
    NOT_FOUND = -1 
    IRA_POS = 0 
    REG_POS = 1

    # get maximum number of semesters 
    max_sem = NOT_FOUND
    for key, stu in stu_info.items():
        cur_sem = stu.get_num_semesters()
        if cur_sem > max_sem: 
            max_sem = cur_sem
    assert (max_sem != NOT_FOUND)

    # determine position for every semester
    for cur_sem in range(max_sem):
        # dictionary contain as key a tuple: (code_key, year_in, sem_in)
        # and as value a list of tuples: [(ira, registration), ...] 
        # dictionary of performance for students
        perf = {}

        # add every student IRA to the performance dict
        for key, stu in stu_info.items():
            sem_in_unb = stu.get_num_semesters()

            # case the student has already graduated, ira is the one for the last
            # semester
            if cur_sem > sem_in_unb:
                ira = stu.ira[sem_in_unb]
            else: 
                ira = stu.ira[cur_sem]

            # add to dict
            if not ((stu.course, stu.year_in, stu.sem_in) in perf):
                perf[(stu.course, stu.year_in, stu.sem_in)] = [] 
            perf[(stu.course, stu.year_in, stu.sem_in)].append((ira, stu.reg))

        # sort every list in dictionary - by first element
        for key, val in perf.items(): 
            val.sort(key = lambda tup: tup[IRA_POS])

        # for every student, fill his position on the list
        for key, stu in stu_info.items():
            sem_in_unb = stu.get_num_semesters()
            if cur_sem > sem_in_unb: 
                continue

            perf_lst = perf[(stu.course, stu.year_in, stu.sem_in)]
            position = NOT_FOUND 
            for i in range(len(perf_lst)):
                if perf_lst[i][REG_POS] == stu.reg:
                    position = i 
                    break
            assert (position != NOT_FOUND)

            stu.position[cur_sem] = position

def get_database_info():
    """
    receives nothing
    query the database to obtain student info that can be obtained
    returns a dictionary containing student info
    """
    # try to load student from pickle object
    try: 
        stu_info = load_students(NAME_STU_STRUCTURE)
        print('finished loading the students dictionary')
        return stu_info
    except FileNotFoundError:
        print('could not load student info, so will build structure from database')
            
        stu_info = {}
        TABLE = 'student'

        # constants
        STU_ID_IND = 0
        STU_CODE_IND = 1

        # query database
        query = 'select * from %s.%s ' % (MY_DATABASE, TABLE)
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()

        # iterate over every row
        for row in rows: 
            key = row[STU_CODE_IND]

            # in case this student is a new one 
            if not key in stu_info: 
                # add student, case the registration is a new one
                student_id = row[STU_ID_IND]
                stu_info[key] = Student(student_id, row)
                #stu_info[key].set_attrib(row)

        print('finished loading the students dictionary')
        return stu_info

def get_derived_info(stu_info):
    """
    iterates over the csv files, filling information relative to student derived
    attributes    
    receives:
        1. a dictionary containing student info
    returns:
        nothing
    """
    # fill student grades
    fill_grades(stu_info)

    # calculate student ira for the semesters - TODO: handle case of empty iras
    #fill_ira(stu_info)

    # calculate improvement rate - TODO: handle case of improvement rate
    #fill_impr_rate(stu_info)

    # calculate fail rate, pass rate and drop rate
    fill_drop_pass_fail_rate(stu_info, 'fail')
    fill_drop_pass_fail_rate(stu_info, 'pass')
    fill_drop_pass_fail_rate(stu_info, 'drop')

    # calculate credit rate and mandatory rate - TODO: need the credit amount for the
    # disciplines
    #fill_credit_rate(stu_info)

    # calculate hard rate - need to check the code later
    #fill_hard_rate(stu_info)

    # calculate if student is in condition - TODO (can be done)
    #fill_condition(stu_info)

    # calculate position of the student for the semester he is in 
    #- TODO (can be done)
    #fill_position(stu_info)

    print('\nfinished constructing derived info\n\n')

def get_students_info(): 
    """
    extracts from database all the students information
    saves the information as a dictionary of students and serializes it using
    pickle

    * the dictionary of students accept as a key the student cod_mat in database and has
    * as value the corresponding student object
    """
    # obtain info for the students contained in database
    stu_dict = get_database_info()
    
    # TODO: handle outliers
    handle_outliers(stu_dict)

    # construct info for the derived attributes of a student
    get_derived_info(stu_dict)

    # saves object
    save_students(NAME_STU_STRUCTURE, stu_dict)

    # TODO: check missing values
    check_missing_values(stu_dict, 'ira')

def handle_miss_ira(stu_info):
    """
    receives the student dictionary
    fills the missing iras
    """
    for key, stu in stu_info.items():
        stu.set_miss_iras()

def load_students(name, path = PATH): 
    """
    receives a name
    loads the student array saved as a pickle serialized object
    """
    stu_info = pickle.load(open(path + name, 'rb'))
    return stu_info

def parse_insert_ira(stu_info, row, year, semester): 
    """
    receives a row, containing the ira information. 
    put that info in the student ira
    """
    global ira_filled

    # return case of empty row
    if len(row) == 0:
        return 

    # get row content - the row is a list with only one entry
    content = row[0]
    for i in range(1, len(row)):
        content += row[i]

    # split content in list 
    info = content.split(';')

    # skip if not from graduation 
    # you dont need to understand this, but this code fragment is essential because
    # the first line of the csv file is a header information, that must be skipped
    info[DEGREE_IND] = info[DEGREE_IND][1:-1]
    if info[DEGREE_IND].lower() != "graduacao":
        return

    # get student code and return case not a student of interest
    code = int(info[CODE_IND])
    if code not in stu_info: 
        return

    # get ira information - in the csv file, the ira is between 0 and 50 000
    ira = int(info[IRA_IND])
    ira = ira / float(10000)
    assert (ira >= 0 and ira <= 5.0)

    # put ira in the student info
    stu_info[code].set_ira(ira, year, semester)

    # increment the number of ira filleds
    ira_filled += 1

def save_students(name, stu_info, path = PATH): 
    """
    receives a name and a dictionary containing student info. 
    saves the student dictionary as a pickle object with a given name
    """
    file_target = open(path + name, 'wb')
    pickle.dump(stu_info, file_target)

    print('saving student on %s/%s' % (name, path))

if __name__ == "__main__":
    # get all student relevant information and saves it as an object
    get_students_info()

    # load student info, just a test
    #load_students('NAME_STU_STRUCTURE')
