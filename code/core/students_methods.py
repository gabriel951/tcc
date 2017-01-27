#!/usr/bin/python3.4
# this file contain the methods mainly related to the students
from students import *

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
            pass
            #stu.in_condition_sem(i):

        # TODO: handle list transformation

def fill_drop_rate(stu_info): 
    """
    receives a dictionary containing all student information
    set correctly the IRA of every student
    """
    # open file that report patological cases
    fp = open('../logs/drop_rate_patological_cases.txt', 'w')

    for key in stu_info: 
        # get current student grades
        stu = stu_info[key]
        cur_stu_grades = stu.grades

        # iterate through every subject
        subjects_coursed = 0
        subjects_dropped = 0 
        for sub_name, info_list in cur_stu_grades.items():
            for index in range(len(info_list)):
                subjects_coursed += 1
                grade = stu.get_sub_info(sub_name, index, 'grade')
                if student_dropped(grade): 
                    subjects_dropped += 1
                 
        # set attribute correctly 
        stu_info[key].drop_rate = float(subjects_dropped) / subjects_coursed  

        # if drop rate is problematic, register patological case
        if stu_info[key].drop_rate > 0.99: 
            stu.log_info(fp)
            #stu.show_student()

    # close file
    fp.close()
    print('finished filling drop rate')

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

def fill_fail_rate(stu_info):
    """
    receives a dictionary
    set correctly the fail rate of every student
    """
    # open file that report patological cases
    fp = open('../logs/fail_rate_patological_cases.txt', 'w')

    for key in stu_info: 
        # get current student grades
        stu = stu_info[key]
        cur_stu_grades = stu.grades

        # iterate through every subject
        subjects_coursed = 0
        subjects_failed = 0 
        for sub_name, info_list in cur_stu_grades.items():
            for index in range(len(info_list)):
                subjects_coursed += 1
                grade = stu.get_sub_info(sub_name, index, 'grade')
                if student_failed(grade): 
                    subjects_failed += 1
                 
        # set attribute correctly 
        stu_info[key].fail_rate = float(subjects_failed) / subjects_coursed  

        # if fail rate is problematic, register patological case
        if stu_info[key].fail_rate > 0.99: 
            stu.log_info(fp)
            #stu.show_student()

    # close file
    fp.close()
    print('finished filling the fail rate')

def fill_grades(stu_info, mode = 'normal'):
    """
    receives a student info dictionary 
    mode is an optional parameter that can be normal or quick 
        if normal, fill grades of all years from 2000 to 2015.
        if quick, fill grades of year 2000, semester 1
    query database and add grades of the student to the student dictionary
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
        # get student id and corresponding student
        student_id = row[CODE_STU_RIND]
        student = stu_info[student_id]

        student.set_grades(row)

    print('finished filling grades')

def fill_hard_rate(stu_info):
    """
    receives the student dictionary, 
    fills every student hard rate - the ration of approvation in the most difficult
    subject the student has coursed 
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
    receives a dictionary containing all students. 
    read the csv file for the student IRA and put the student IRA as an information
    """
    # get all years and semesters to be considered
    if mode == 'quick': 
        fill_ira_year_semester(stu_info, 2008, 1)
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
        handle_miss_ira(stu_info)
        print('finished filling missing iras')
    else:
        exit('mode option incorrect')

    
    print('finished filling ira')

def fill_ira_year_semester(stu_info, year, semester):
    """
    receives a dictionary containing all students. 
    read the csv file for the student IRA and put the student IRA as an information
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

def fill_pass_rate(stu_info):
    """
    receives a dictionary
    set correctly the pass rate of every student
    """
    # open file that report patological cases
    fp = open('../logs/pass_rate_patological_cases.txt', 'w')
    
    for key in stu_info: 
        # get current student grades
        stu = stu_info[key]
        cur_stu_grades = stu.grades

        # iterate through every subject
        subjects_coursed = 0
        subjects_passed = 0 
        for sub_name, info_list in cur_stu_grades.items():
            for index in range(len(info_list)):
                subjects_coursed += 1
                grade = stu.get_sub_info(sub_name, index, 'grade')
            if student_passed(grade): 
                subjects_passed += 1
                 
        # set attribute correctly 
        pass_rate = float(subjects_passed) / subjects_coursed  
        stu.pass_rate = pass_rate

        # if pass rate is problematic, register patological case
        if pass_rate < 0.01: 
            stu.log_info(fp)
            #stu.show_student()

    # close file
    fp.close()

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
                pass

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
                stu_info[key] = Student(student_id)
                stu_info[key].set_attrib(row)


        # handle cases of students that left by ways unrelated to grades
        #handle_special_stu(stu_info)
        
        print('finished loading the students dictionary')
        return stu_info

def get_derived_info(stu_info):
    """
    receives a dictionary containing student info
    iterates over the csv files, filling information relative to student derived
    attributes   
    """
    # fill student grades
    fill_grades(stu_info)

    # calculate student ira for the semesters - TODO: handle case of empty iras
    #fill_ira(stu_info)

    # calculate improvement rate - TODO: handle case of improvement rate
    #fill_impr_rate(stu_info)

    # calculate fail rate - ok
    #fill_fail_rate(stu_info)

    # calculate pass rate - ok
    #fill_pass_rate(stu_info)

    # calculate drop rate - ok
    #fill_drop_rate(stu_info)

    # calculate credit rate and mandatory rate - TODO: need the credit amount for the
    # disciplines
    #fill_credit_rate(stu_info)

    # calculate mandatory rate
    #fill_mand_rate(stu_info)

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
    
    # construct info for the derived attributes of a student
    get_derived_info(stu_dict)

    # saves object
    save_students(NAME_STU_STRUCTURE, stu_dict)

    # TODO: check missing values
    check_missing_values(stu_dict)
    exit()

def handle_special_stu(stu_info):
    """
    eliminate from the dictionary the students that left unb by non-academic reasons
    """
    # number of special cases
    #spc_cases = 0

    #for key in stu_info: 
    #    stu = stu_info[key]
    #    if stu.lower() == '': 
    #        spc_cases += 1
    #        del stu_info[key]
    #    elif:

    #    else: 
    #        pass

    #print('eliminated %d special cases students' % (spc_cases))

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

# get all student relevant information and saves it as an object
#get_students_info()

# load student info, just a test
#load_students('NAME_STU_STRUCTURE')
