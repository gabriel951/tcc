#!/usr/bin/python3.4
# student file, contain information about the students
import pickle
import csv

# import basic and aux
import sys
sys.path.append('..')
from basic import *
from aux import *

from grades import *
from courses import *

# name of the structure that will contain the students information
NAME_STU_STRUCTURE = 'students_info'

# value to indicate we haven't filled a given field yet
NOT_KNOWN = 'not know'

# global variables
ira_filled = 0 # number of students with ira calculated

class Student(): 
    """
    class that represents the student
    """
    def __init__(self, id_num): 
        """
        initializes a student, does not put any information
        """
        # id number
        self.id_num = id_num

        # registration
        self.reg = None
        
        ## dictionary that keeps all the grades of student
        self.grades = {}

        ## social data follows
        self.sex = None
        self.age = None
        self.quota = None
        self.school_type = None
        self.race = None
        self.local = None
        self.course = None
        self.year_in = None
        self.sem_in = None
        self.year_out = None
        self.sem_out = None
        self.way_in = None
        self.way_out = None

        ## performance data follows
        self.ira = None 

        # reason between grades of current semester and last semester
        self.improvement_rate = None 
        # reason between subjects coursed and subjects failed
        self.fail_rate = None 
        # reason between subjects coursed and subjects passed
        self.pass_rate = None 
        # reason between subjects coursed and subjects dropped
        self.drop_rate = None 
        # reason between credits in disciplines per semester and number of credits in
        # the course
        self.credit_rate = None
        # reason between credits in mandatory disciplines per semester and number of
        # credits in the course
        self.mand_credit_rate = None
        # rate of approvation in the most hard disciplines of the semester
        self.hard_rate = None
        # boolean that indicates whether a student is in condition or not
        self.in_condition = None
        # position of the student relative to the semester he is in 
        self.position = None
    
    def calculate_ira_yearsem(self, year, sem):
        """
        receives an year and a semester, calculates the ira the student will have in
        the passed ira and semester

        * similar calculations found in method get_sem_grade
        """
        assert (sem == 1 or sem == 2)

        # special case counter
        spc_counter = 0

        # variables for ira calculation
        ira_sum = 0
        drop_mand_sub = 0
        drop_opt_sub = 0 
        num_sub = 0 

        # iterate through all the subjects student coursed
        for subject, data_list in self.grades.items(): 
            for pos in range(len(data_list)): 
                # pass if subject not coursed yet
                code_sub = self.get_sub_info(subject, pos, 'code')
                year_sub = self.get_sub_info(subject, pos, 'year')
                sem_sub = self.get_sub_info(subject, pos, 'sem')
                grade_sub = self.get_sub_info(subject, pos, 'grade')
                if year_coursed > year or \
                    (year_coursed == year and sem_coursed >= sem): 
                        pass

                
                # student dropped case
                if student_dropped(grade):
                    num_sub += 1
                    if is_mand_sub(code_sub, self.course, self.year_in, self.sem_in):



                 

    def get_num_semesters(self):
        """
        receives a student with correct information regarding the year and semester
        the student left.
        Returns the number of semesters the student was in the university
        """
        num_semesters = (self.year_out - self.year_in) * 2 + \
                (self.sem_out - self.sem_in)
        # necessary to account for the current semester
        num_semesters += 1
        return num_semesters

    def get_semester(self, year, semester):
        """
        receives a student, an year and a semester. 
        returns the semester the student is in.

        * the count start in semester 0 
        """
        current_semester = (year - self.year_in) * 2 + (semester - self.sem_in)
        return current_semester

    def get_sem_grade(self, year, semester):
        """
        receives a student
        calculates and return the IRA of the given semester for that student 
        """
        # make sure no semester equal 0 is received
        assert (semester == 1 or semester == 2)

        # position in the list of data
        code_pos = 0 
        name_pos = 1 
        grade_pos = 2 
        year_pos = 3 
        sem_pos = 4 

        # variables necessary for ira calculation
        drop_mand_sub = 0
        drop_opt_sub = 0 
        num_sub = 0 
        sum_weights = 0

        # iterate through every grade
        for subject, data_list in self.grades.items(): 
            # iterate through all times student has done the subject
            for data in data_list: 
                # only proceed if data coursed in the year and semester
                if data[year_pos] != year or data[sem_pos] != semester:
                    pass                

                # if the student dropped
                if student_dropped(data[grade_pos]):
                    # if the discipline is mandatory
                    if is_mand_sub(data[code_pos], self.course, self.year_in,
                            self.sem_out):
                        drop_mand_sub += 1
                    else:
                        drop_opt_sub += 1

                # weight of the grade
                grade_weight = get_grade_weight(data[grade_pos])
                if grade_weight == None: 
                    # dont consider
                    pass
                else:
                    # increment the number of subjects coursed
                    num_sub += 1
                    sum_weights += grade_weight
        
        # calculate ira
        penalty_factor = 1 - ((0.6 * drop_mand_sub + 0.4 * drop_opt_sub) / num_sub)
        grade_factor = float(sum_weights) / num_sub
        ira_semester = penalty_factor * grade_factor

        assert (ira_semester >= 0 and ira_semester <= 5.0)
        return ira_semester

    def get_sub_info(self, key, pos, info):
        """
        receives a key to access the grades dictionary correct item, the position in
        the list we are in and the information we want
        return the information

        * possible values include: code, grade, 
        """
        if info == 'code':
            return self.grades[key][pos][0] # code is the first item
        elif info == 'name':
            return self.grades[key][pos][1] # name is the second item
        elif info == 'grade':
            return self.grades[key][pos][2] # grade is the third item
        elif info == 'year':
            return self.grades[key][pos][3] # year is the fourth item
        elif info == 'sem':
            return self.grades[key][pos][4] # semester is the fifth item
        else: 
            exit('value passed to get_sub_info is incorrect')
    
    def log_info(self, fp):
        """
        receives a file object
        logs the student info in the file using the file object
        
        * very similar to the show_student function
        """
        fp.write("------------\n")
        fp.write("student info\n")

        # temporary buffer
        temp_buff = []

        # iterate over all attributes of a class 
        for attr, value in self.__dict__.items():
            # saves the attribute name and the attribute value
            if attr != 'grades':
                temp_buff.append((attr, value))
         
        # sort list by value of first element of tuple
        temp_buff.sort(key=lambda tup: tup[0])

        # temp values
        for elem in temp_buff:
            fp.write('\t' + str(elem[0]) + ':   ' + str(elem[1]) + '\n')

        # print grades
        fp.write('\t printing grades --- \n')
        for attr, value in self.grades.items():
            fp.write('\t\t' + str(attr) + ':   ' + str(value) + '\n')
        fp.write('\t ------------------ \n')

        fp.write("------------\n")

    def pos_2_yearsem(self, pos, year, sem):
        """
        receives a position the student is in, a year and a semester
        returns the year and semester correspondent

        * pos = 0 means the year and semester the student got in unb
        """
        if pos == 0:
            return (year, sem)
        else:
            pos -= 1
            if sem == 1:
                new_year = year
                new_sem = 2
            else:
                new_year = year + 1
                new_sem = 1
            return self.pos_2_yearsem(pos, new_year, new_sem)

    def set_attrib(self, tup):
        """
        receives a tuple containing student information (no derived attributes)
        set the attributes correctly
        """
        ## the magic numbers are the position in the row
        # set attributes
        self.id_num = tup[0]
        self.reg = tup[1]
        self.sex = tup[2]
        self.age = tup[3]
        self.quota = tup[4]
        self.school_type = tup[5]
        self.race = tup[6]
        self.local = tup[7]
        self.course = tup[8]
        self.year_in = tup[9]
        self.sem_in = tup[10]
        self.year_out = tup[11]
        self.sem_out = tup[12]
        self.way_in = tup[13]
        self.way_out = tup[14]

        # for code consistency reasons, change the name of the courses
        self.set_course_name()

    def set_course_name(self):
        """
        the course name the student has may be a variation of the standard one 
        this function ensure that we don't have this distortion
        """
        # if name is in the official name list, nothing to do 
        if self.course in COURSES_OFF_NAME:
            pass
        elif self.course.lower() in ['ciência da computação']: 
            self.course = CIC_BACHELOR
        elif self.course.lower() in ['computação']:
            self.course = CIC_NON_BACHELOR
        elif self.course.lower() in ['engenharia de computação']:
            self.course = COMPUTER_ENGINEERING
        elif self.course.lower() in ['engenharia de software']:
            self.course = SOFTWARE_ENGINEERING
        elif self.course.lower() in ['engenharia de redes de comunicação']:
            self.course = NETWORK_ENGINEERING
        elif self.course.lower() in ['engenharia mecatrônica']:
            self.course = MECHATRONICS_ENGINEERING
        else: 
            print('case not handled. Course: %s' % (self.course))
            exit()

    def set_grades(self, row):
        """
        receives a row of the csv file containing student info
        extracts the grades of the student and put it in the 
        """
        # rows indices - RIND
        CODE_SUB_RIND = 1
        SEMESTER_RIND = 2
        YEAR_RIND = 3
        GRADE_RIND = 4 
        NAME_RIND = 5

        # get subject name, grade, year and semester coursed
        data = []
        data.append(row[CODE_SUB_RIND])
        data.append(row[NAME_RIND])
        data.append(row[GRADE_RIND])
        data.append(row[YEAR_RIND])
        data.append(row[SEMESTER_RIND])

        ## add grade of student to the dictionary
        # if it's the first time the student coursed subject
        if row[NAME_RIND] not in self.grades:
            self.grades[row[NAME_RIND]] = []

        # be sure not to add an info that we already have
        for lst_data in self.grades[row[NAME_RIND]]: 
            if data == lst_data:
                return
        self.grades[row[NAME_RIND]].append(data)
        
    def set_improvement_rate(self):
        """
        calculates the improvement rate for every student
        """
        # build list of values, case not already built
        if self.improvement_rate == None:
            self.improvement_rate = []
            num_semesters = self.get_num_semesters()
            for i in range(num_semesters):
                self.improvement_rate.append(NOT_KNOWN)
        
        # iterate through every year, setting position
        cur_year = self.year_in
        cur_semester = self.sem_in
        for pos in range(num_semesters):
            self.set_improvement_rate_semester(cur_year, cur_semester, pos)

            # update current year/semester
            if cur_semester == 1: 
                cur_semester = 2 
            else:
                cur_year += 1
                cur_semester = 1

    def set_improvement_rate_semester(self, year, semester, pos):
        """
        receives a year, a semester and the position to insert in a list
        calculates the improvement rate for a given year and semester
        insert in the list self.improvement_rate, in the position indicated
        """
        # if position equals 0, missing value
        if pos == 0:
            self.improvement_rate[pos] = 'first_semester, no improvement_rate'
            return
        
        # get year and semester of the past semester
        if semester == 2: 
            past_semester = 1
            past_year = year
        else: 
            past_semester = 2
            past_year = year - 1

        # calculates grade for past semester and for current semester
        past_sem_grade = self.get_sem_grade(past_year, past_semester)
        cur_sem_grade = self.get_sem_grade(year, semester)
        self.improvement_rate[pos] = cur_sem_grade / past_sem_grade

    def set_miss_iras(self):
        """
        fills the ira of students that couldnt be obtained by database
        """
        for pos in range(len(self.ira)):
            # if the ira is missing
            if self.ira[pos] == NOT_KNOWN:
                # get correspondent year and semester
                (cur_year, cur_sem) = self.pos_2_yearsem(pos, self.year_in, \
                        self.sem_in)
                
                # calculate ira for the year and semester passed
                self.calculate_ira_yearsem(pos, year, sem)
            
    def set_ira(self, ira, year, semester):
        """
        receives a tuple containing student information (no derived attributes) and
        the year and semester of the information. 
        insert in the student the IRA correctly
        """
        # does not consider summer school
        if semester == 0: 
            pass

        # student ira should be a list containing iras for each semester
        # build that list in case value is None
        if self.ira == None:
            self.ira = []
            num_semesters = self.get_num_semesters()
            for i in range(num_semesters):
                self.ira.append(NOT_KNOWN)
            
        # insert ira in the right position
        pos = self.get_semester(year, semester) 
        try: 
            self.ira[pos] = ira
        except IndexError: 
            self.show_arriv_left()
            print('\t possible error handled: tried to insert info for year %d and semester %d' \
                    % (year, semester))

    def set_mand_rate(self, course_lst):
        """
        set the mandatory rate for a given student
        """
        num_sub = 0
        mand_sub = 0

        # get course student is in 
        
        # count all subjects coursed and how many are mandatory
        for (grade, data_list) in self.grades.items():
            # iterate through all the data in the data list
            for pos in range(len(data_list)):
                num_sub += 1
                code_sub = self.get_sub_info(grade, pos, 'code')
                if is_mand_sub(code_sub, self.course, self.year_in, self.sem_in):
                    mand_sub += 1
        
        self.mand_credit_rate = float(mand_sub) / num_sub

    def show_student(self):
        """
        print a student info 
        """
        print("------------")
        print("student info")

        # temporary buffer
        temp_buff = []

        # iterate over all attributes of a class 
        for attr, value in self.__dict__.items():
            # saves the attribute name and the attribute value
            if attr != 'grades':
                temp_buff.append((attr, value))
         
        # sort list by value of first element of tuple
        temp_buff.sort(key=lambda tup: tup[0])

        # temp values
        for elem in temp_buff:
            print('\t' + str(elem[0]) + ':   ' + str(elem[1]))

        # print grades
        print('\t printing grades --- ')
        for attr, value in self.grades.items():
            print('\t\t' + str(attr) + ':   ' + str(value))
        print('\t ------------------ ')

        print("------------")

    def show_arriv_left(self):
        """
        receives a student
        shows when the student arrived in university and when the student left
        returns nothing
        """
        print('\tstudent %d arrived in year: %d and semester: %d' \
                % (self.id_num, self.year_in, self.sem_in))
        print('\tstudent  %d left in year: %d and semester: %d' \
                % (self.id_num, self.year_out, self.sem_out))

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

def fill_impr_rate(stu_info):
    """
    receives a dictionary containing all students. 
    fill the student objects with information regarding the improvement rate
    """
    # iterate through every student
    for key in stu_info:
        # fill the student improvement rate
        stu_info[key].set_improvement_rate()

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
    set correctly the mandatory rate for a given student

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
        student.set_mand_rate(course)

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

def get_database_info():
    """
    receives nothing
    query the database to obtain student info that can be obtained
    returns a dictionary containing student info
    """
    # try to load student from pickle object
    try: 
        stu_info = load_students(NAME_STU_STRUCTURE)
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
        
        return stu_info

def get_derived_info(stu_info):
    """
    receives a dictionary containing student info
    iterates over the csv files, filling information relative to student derived
    attributes   
    """
    # fill student grades
    fill_grades(stu_info)

    # calculate student ira for the semesters 
    fill_ira(stu_info)

    # calculate improvement rate 
    #fill_impr_rate(stu_info)

    # calculate fail rate
    #fill_fail_rate(stu_info)

    # calculate pass rate
    #fill_pass_rate(stu_info)

    # calculate drop rate
    #fill_drop_rate(stu_info)

    # calculate mandatory rate
    #fill_mand_rate(stu_info)

    # calculate hard rate - TODO (can be done)
    #fill_hard_rate(stu_info)

    # calculate if student is in condition - TODO (can be done)
    #set_condition(stu_info)

    # calculate position of the student for the semester he is in 
    #- TODO (can be done)
    #set_condition(stu_info)

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
    print('finished loading the students dictionary')
    
    # construct info for the derived attributes of a student
    get_derived_info(stu_dict)

    # saves object
    save_students(NAME_STU_STRUCTURE, stu_dict)
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
