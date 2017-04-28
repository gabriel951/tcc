#!/usr/bin/python3.4
# this file contain the methods mainly related to the students
import statistics
import subjects as sub
from students import *
from outliers import *

def check_missing_values(stu_info, feature):
    """
    TODO: deprecated
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
    set correctly the credit rate and the accumulated credit rate of every student
    receives:
        1. dictionary containing all student information
    returns:
        nothing
    * credit rate is the number of credits a student took so far
    TODO (maybe later): I could use the credit rate divided by the number of credits expected by a
    course
    """
    # number of credit rate
    global credit_rate
    credit_rate = 0

    file_name = CSV_PATH + FILE_NAME + EXTENSION

    # read line by line, parsing the results and putting on database
    with open(file_name, newline = '', encoding = ENCODING) as fp:
        reader = csv.reader(fp)

        # skip first line
        next(reader, None)

        # iterate through the rows, inserting in the table
        for row in reader:
            parse_insert_credit_rate(stu_info, row)
            
    print("\tnumber of credit rate added: %s" % (credit_rate))

    # handle missing iras
    handle_miss_credit_rate(stu_info)

    # get accumulated number of credits info
    for key, stu in stu_info.items():
        num_semesters = stu.get_num_semesters()
        acc_credits = 0 
        for pos in range(num_semesters):
            acc_credits += stu.credit_rate[pos]
            stu.credit_rate_acc[pos] = acc_credits

def fill_condition(stu_info):
    """
    fills the condition list for every student
    receives: 
        1. dictionary containing the student information
    returns: 
        nothing
    """
    # just to keep track how we are going
    students_done = 0

    for key, stu in stu_info.items(): 
        stu.set_condition()
        
        # keep track how we are going
        #students_done += 1
        #if students_done % 100 == 0: 
        #    print('\t finished filling condition for 100 more students')
        
    print('finished filling condition for all students')

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
            (code, name, grade, year, sem, credits) = stu.get_sub_info(sub_name, index, 'all')
            cur_pos = stu.yearsem_2_pos(year, sem)
            if cur_pos > pos or cur_pos == ERROR: 
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
        print('\t\t\tstudent %d has not coursed any subject until pos: %d' % (stu.reg, pos))
        fp.write('student %d has not coursed any subject until pos: %d\n' % (stu.reg, pos))
        # no need to log cases, have analysed this already
        #stu.log_info(fp)

def fill_drop_pass_fail_rate(stu_info, mode, do_quick): 
    """
    set correctly the drop_rate or fail_rate or pass_rate for every student
    receives: 
        1. a dictionary containing all student information
        2. mode informing whether we want the pass rate, the fail rate or the drop
        rate. Should be 'drop', 'pass' or 'fail'
        3. a boolean indicates whether we should focus only on the last semester or
        in all semesters 
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
        if not do_quick:
            for pos in range(num_semesters):
                fill_drop_pass_fail_rate_sem(stu, pos, mode, fp) 
        else:
            fill_drop_pass_fail_rate_sem(stu, num_semesters - 1, mode, fp)


        # if it's a patological case, register it
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
    DEPRECATED
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
    global outliers_dict

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
    query = 'select code_stu, code_sub, semester, year, grade, name, credits \
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
        if not (student_id in outliers_dict): 
            student = stu_info[student_id]
            student.set_grades(row)
            

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
    
    # handle missing values
    handle_miss_hard_rate(stu_info)
    fp.close()

    print('finished filling hard rate')

def fill_impr_rate(stu_info):
    """
    fill the student objects with information regarding the improvement rate
    receives:
        1. a dictionary containing all students. 
    returns: 
        nothing
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
    handle_miss_impr_rate(stu_info)

    print('finished_calculating improvement rate')

def fill_ira(stu_info):
    """
    read the csv file for the student IRA and put the student IRA as an information
    receives:
        1. a dictionary containing all students. 
    returns:
        nothing
    """
    global ira_filled
    file_name = CSV_PATH + FILE_NAME + EXTENSION

    # read line by line, parsing the results and putting on database
    with open(file_name, newline = '', encoding = ENCODING) as fp:
        reader = csv.reader(fp)

        # skip first line
        next(reader, None)

        # iterate through the rows, inserting in the table
        for row in reader:
            parse_insert_ira(stu_info, row)
            
    print("\tnumber of iras added: %s" % (ira_filled))

    # handle missing iras
    handle_miss_ira(stu_info)

    # fill ira accumulated
    fill_ira_acc(stu_info)

def fill_ira_acc(stu_info):
    """
    fill the ira accumulated atribute for every student, based on the iras
    receives: 
        1. dictionary containing student info
    returns: 
        nothing
    """
    # iterate through every student
    for key, stu in stu_info.items():
        # iterate through student semester 
        for sem in range(1, stu.get_num_semesters() + 1):
            # calculate ira accumulated
            total = 0.0
            for pos in range(sem): 
                weight = pos + 1 # since the pos counting start at 0 
                total += stu.ira[pos] * weight
            total /= sum(range(1, sem + 1)) # divide by sum of weights
            stu.ira_acc[sem - 1] = total

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
    fill information regarding the position the student is in (compared to every
    other student on the same course and semester) 
    receives: 
        1. a student dictionary
    returns: 
        nothing
    """
    # avoid magic numbers ;)
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
        # and as value a list of tuples: [(ira_acc, registration), ...] 
        # dictionary of performance for students
        perf = {}

        # add every student IRA to the performance dict
        for key, stu in stu_info.items():

            # case the student has already graduated, skip this student
            sem_in_unb = stu.get_num_semesters()
            if cur_sem >= sem_in_unb:
                continue

            # get student ira
            ira = stu.ira_acc[cur_sem]
            assert(ira != NOT_KNOWN)

            # add to dict
            if not ((stu.course, stu.year_in, stu.sem_in) in perf):
                perf[(stu.course, stu.year_in, stu.sem_in)] = [] 
            perf[(stu.course, stu.year_in, stu.sem_in)].append((ira, stu.reg))

        # sort every list in dictionary - by first element
        for key_dict, val in perf.items(): 
            val.sort(key = lambda tup: tup[IRA_POS], reverse = True)

        # for every student, fill his position on the list
        for key, stu in stu_info.items():
            sem_in_unb = stu.get_num_semesters()

            # skip if student graduated before the current semester
            # the = in the comparison is because indexing in python starts at 0
            if cur_sem >= sem_in_unb: 
                continue

            # fill position
            perf_lst = perf[(stu.course, stu.year_in, stu.sem_in)]
            position = NOT_FOUND 
            for i in range(len(perf_lst)):
                if perf_lst[i][REG_POS] == stu.reg:
                    position = i 
                    break
            assert (position != NOT_FOUND)
            stu.position[cur_sem] = position

    print('finished filling position')

def filter_dict_by(function, dic): 
    """
    filter entries from the dictionary, according to the value returned by the
    function passed
    receives: 
        1. function to apply
        2. dictionary to iterate
    returns: 
        new dictionary, with entries filtered
    """
    filtered_dic = {}
    for key, val in dic.items(): 
        if function(val):
            filtered_dic[key] = val
    return filtered_dic

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
    #fill_grades(stu_info)

    # calculate student ira for the semesters 
    #fill_ira(stu_info)

    # calculate improvement rate 
    fill_impr_rate(stu_info)

    # calculate fail rate, pass rate and drop rate
    #fill_drop_pass_fail_rate(stu_info, 'fail', False)
    #fill_drop_pass_fail_rate(stu_info, 'pass', False)
    #fill_drop_pass_fail_rate(stu_info, 'drop', False)

    # calculate credit rate 
    #fill_credit_rate(stu_info)

    # calculate hard rate - need to check the code later
    #fill_hard_rate(stu_info)

    # calculate if student is in condition 
    #fill_condition(stu_info)

    # calculate position of the student for the semester he is in 
    fill_position(stu_info)

    #print('\nfinished constructing derived info\n\n')

def get_database_info():
    """
    query the database to obtain student info that can be obtained
    receives:
        nothing
    returns
        a dictionary containing student info
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
        STU_CODE_IND = 0

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
                student_id = row[STU_CODE_IND]
                stu_info[key] = Student(student_id, row)

        print('finished loading the students dictionary')
        return stu_info

def get_grad_info(stu_info, func_filter): 
    """
    get the amount of students in a course and the proportion that graduated, for
    that course
    receives: 
        1. student dictionary
        2. a function to filter the students that will be selected
    returns: 
        tuple of the form (<amount of students in the course> , <proportion that
        graduated>). 
        ** the amount returned correspond to all students, including those that did
        not graduate
    """

    tot_amount = 0
    grad_amount = 0
    for key, stu in stu_info.items(): 
        if func_filter(stu): 
            tot_amount += 1
            if stu.able_to_grad(): 
                grad_amount += 1
    
    proportion = float(grad_amount) / tot_amount

    return (tot_amount, proportion)

def get_model_info():
    """
    get a list containing a model data and a description of the model 
    the models studied are 2 * 3 = 6. 2 because we divide by age between young people
    and old people. 3 because we divide by 3 groups of course. 
    receives: 
        1. nothing
    returns: 
        list where each entrie is of the form: <model_data, brief_model_description>
    """
    # load student info 
    stu_info = load_students(NAME_STU_STRUCTURE, path = '../core/data/')

    # list of models
    models_lst = []
    models_lst.append((stu_info, 'all_students'))

    # young students from ti courses
    filtered_data = filter_dict_by(lambda stu: stu.age <= AGE_THRESHOLD and \
            stu.course in TI_COURSES, stu_info)
    models_lst.append((filtered_data, 'young_students_ti_courses'))
    #print(len(filtered_data))

    # old students from ti courses
    filtered_data = filter_dict_by(lambda stu: stu.age > AGE_THRESHOLD and \
            stu.course in TI_COURSES, stu_info)
    models_lst.append((filtered_data, 'old_students_ti_courses'))
    #print(len(filtered_data))

    # young students from lic courses
    filtered_data = filter_dict_by(lambda stu: stu.age <= AGE_THRESHOLD and \
            stu.course in LIC_COURSES, stu_info)
    models_lst.append((filtered_data, 'young_students_lic_courses'))
    #print(len(filtered_data))

    # old students from lic courses
    filtered_data = filter_dict_by(lambda stu: stu.age > AGE_THRESHOLD and \
            stu.course in LIC_COURSES, stu_info)
    models_lst.append((filtered_data, 'old_students_lic_courses'))
    #print(len(filtered_data))

    # young students from comp courses
    filtered_data = filter_dict_by(lambda stu: stu.age <= AGE_THRESHOLD and \
            stu.course in COMP_COURSES, stu_info)
    models_lst.append((filtered_data, 'young_students_comp_courses'))
    #print(len(filtered_data))

    # old students from comp courses
    filtered_data = filter_dict_by(lambda stu: stu.age > AGE_THRESHOLD and \
            stu.course in COMP_COURSES, stu_info)
    models_lst.append((filtered_data, 'old_students_comp_courses'))
    #print(len(filtered_data))

    return models_lst;

def get_students_info(): 
    """
    extracts from database all the students information. Calculates derived
    attributes.
    saves the information as a dictionary of students and serializes it using
    pickle

    * the dictionary of students accept as a key the student cod_mat in database and has
    * as value the corresponding student object

    receives:
        nothing
    returns:
        nothing
    """
    # obtain info for the students contained in database
    stu_dict = get_database_info()
    
    # handle outliers
    handle_outliers(stu_dict)

    # construct info for the derived attributes of a student
    #get_derived_info(stu_dict)

    # saves object
    save_students(NAME_STU_STRUCTURE, stu_dict)

def handle_miss_credit_rate(stu_info):
    """
    handle missing credit rate of students by imputation
    if we have a missing value, assume the student didn't course any credits that
    semester
    receives:
        1. student dictionary, containing all student information
    returns: 
        nothing
    """
    # account for the number of missing credit rate
    miss_credit_rate = 0

    # iterate through every student, and every semester. If there's a missing value,
    # the imputation value is 0 (student didn't course subject after all)
    for key, stu in stu_info.items():
        for pos in range(stu.get_num_semesters()):
            if stu.credit_rate[pos] == NOT_KNOWN:
                stu.credit_rate[pos] = 0
                miss_credit_rate += 1

    print('There were %d missing credit rate' % (miss_credit_rate))

def handle_miss_hard_rate(stu_info):
    """
    fills the missing hard rates for the student
    receives:
        1. student dictionary
    returns:
        nothing
    """
    # account for the number of missing rates
    missing_hard_rates = 0 

    # get average hard rate for first semester
    hard_rates = []
    for key, stu in stu_info.items():
        if stu.hard_rate[0] != NOT_KNOWN:
            hard_rates.append(stu.hard_rate[0])
    average_hard_rate = statistics.mean(hard_rates)

    for key, stu in stu_info.items():
        num_sem = stu.get_num_semesters()
        for pos in range(num_sem):
            if stu.hard_rate[pos] == NOT_KNOWN:
                missing_hard_rates += 1

                # case the first hard rate is not know, put value equal to average
                if pos == 0:
                    stu.hard_rate[pos] = average_hard_rate
            
                # use imputation case student hard rate is missing
                else:
                    stu.hard_rate[pos] = stu.hard_rate[pos - 1]

    print('There were %d missing hard rates' % (missing_hard_rates))

def handle_miss_impr_rate(stu_info):
    """
    fills improvement rate that are still missing values
    receives:
        1. dictionary containing all student info
    returns:
        nothing
    """
    # account for the number of missing improvement rate
    miss_impr_rate = 0

    # iterate through every student, and every semester. If there's a missing value,
    # the imputation value becomes 1.0
    for key, stu in stu_info.items():
        for pos in range(stu.get_num_semesters()):
            if stu.improvement_rate[pos] == NOT_KNOWN:
                stu.improvement_rate[pos] = 1.0
                miss_impr_rate += 1

    print('There were %d missing improvement rate' % (miss_impr_rate))

def handle_miss_ira(stu_info):
    """
    fills the missing iras for the student
    receives:
        1. student dictionary
    returns:
        nothing
    """
    # account for the number of missing iras
    missing_iras = 0 

    # get average ira for first semester
    iras = []
    for key, stu in stu_info.items():
        if stu.ira[0] != NOT_KNOWN:
            iras.append(stu.ira[0])
    average_ira = statistics.mean(iras)

    for key, stu in stu_info.items():
        num_sem = stu.get_num_semesters()
        for pos in range(num_sem):
            if stu.ira[pos] == NOT_KNOWN:
                missing_iras += 1

                # case the first ira is not know, put value equal to average
                if pos == 0:
                    stu.ira[pos] = average_ira
            
                # use imputation case student ira is missing
                else:
                    stu.ira[pos] = stu.ira[pos - 1]
    print('There were %d missing iras' % (missing_iras))

def load_students(name, path = PATH): 
    """
    receives a name
    loads the student array saved as a pickle serialized object
    """
    stu_info = pickle.load(open(path + name, 'rb'))
    return stu_info

def parse_insert_ira(stu_info, row): 
    """
    put info of a row of the csv file in the student ira
    receives:
        1. student dictionary 
        2. a row, containing the ira information. 
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
    info = content.split(SEP_CSV_FILE)

    # get student code and return case not a student of interest - it may be an
    # outlier or a student that has not graduated yet
    code = get_code(info)
    if code not in stu_info: 
        return

    # get ira information
    ira = float(info[IRA_IND]) 
    assert (ira >= 0 and ira <= 5.0)

    # put ira in the student info
    cur_stu = stu_info[code]
    (year, sem) = get_year_sem(info[YEAR_SEM_SUB_IND], True)
    pos = cur_stu.yearsem_2_pos(year, sem)
    if pos == ERROR: 
        return
    cur_stu.ira[pos] = ira

    # increment the number of ira filleds
    ira_filled += 1

def parse_insert_credit_rate(stu_info, row): 
    """
    put info of a row of the csv file in the student credit rate - the info is the
    number of credits a given student coursed in a given semester
    receives:
        1. student dictionary 
        2. a row, containing the ira information. 
    returns:
        nothing
    """
    global credit_rate

    # return case of empty row
    if len(row) == 0:
        return 

    # get row content - the row is a list with only one entry
    content = row[0]
    for i in range(1, len(row)):
        content += row[i]

    # split content in list 
    info = content.split(SEP_CSV_FILE)

    # get student code and return case not a student of interest - it may be an
    # outlier or a student that has not graduated yet
    code = get_code(info)
    if code not in stu_info: 
        return

    # get credit rate information
    credit = int(info[CREDITS_APPROVED_SEM_IND])

    # put credit rate in the student info
    cur_stu = stu_info[code]
    (year, sem) = get_year_sem(info[YEAR_SEM_SUB_IND], True)
    pos = cur_stu.yearsem_2_pos(year, sem)
    if pos == ERROR: 
        return
    cur_stu.credit_rate[pos] = credit

    # increment the number of credits filleds
    credit_rate += 1

def save_students(name, stu_info, path = PATH): 
    """
    saves the student dictionary as a pickle object with a given name
    receives:
        1. name to save 
        2. dictionary containing student info. 
        3. (optional) path to save the students
    returns: 
        nothing
    """
    file_target = open(path + name, 'wb')
    pickle.dump(stu_info, file_target)

    print('saving student on %s/%s' % (name, path))

if __name__ == "__main__":
    # get all student relevant information and saves it as an object
    get_students_info()

    # load student info, just a test
    #load_students('NAME_STU_STRUCTURE')
