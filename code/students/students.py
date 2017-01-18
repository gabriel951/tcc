#!/usr/bin/python3.4
# student file, contain information about the students
import pickle
import csv

# import basic and aux
import sys
sys.path.append('..')
from basic import *
from aux import *

# name of the structure that will contain the students information
NAME_STU_STRUCTURE = 'students_info'

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
        returns the semester the student is in
        """
        current_semester = (year - self.year_in) * 2 + (semester - self.sem_in)
        return current_semester

    def show_student(self):
        """
        print a student info 
        """
        print("studente info")

        # iterate over all attributes of a class 
        for attr, value in self.__dict__.items():
            # print the attribute name and the attribute value
            print(attr, value)

        print("------------")

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
        self.way_out = tup[13]

    def set_ira(self, ira, year, semester):
        """
        receives a tuple containing student information (no derived attributes) and
        the year and semester of the information. 
        insert in the student the IRA correctly
        """
        if self.ira == None:
            # student ira should be a list containing iras for each semester
            self.ira = []
            num_semesters = self.get_num_semesters()
            for i in range(num_semesters):
                self.ira.append('not known')
            
        # insert ira in the right position
        # we don't need a -1 in the position
        pos = self.get_semester(year, semester) 
        try: 
            self.ira[pos] = ira
        except IndexError: 
            print(pos, num_semesters) 

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
    CODE_SUB_RIND = 1
    SEMESTER_RIND = 2
    YEAR_RIND = 3
    GRADE_RIND = 4 
    NAME_RIND = 5

    # for every row in database
    for row in rows:
        # get student id and corresponding student
        student_id = row[CODE_STU_RIND]
        student = stu_info[student_id]

        # get subject name, grade, year and semester coursed
        data = []
        data.append(row[CODE_SUB_RIND])
        data.append(row[NAME_RIND])
        data.append(row[GRADE_RIND])
        data.append(row[YEAR_RIND])
        data.append(row[SEMESTER_RIND])

        # add grade of student to the dictionary
        student.grades[row[NAME_RIND]] = data

def get_database_info():
    """
    receives nothing
    query the database to obtain student info that can be obtained
    returns a dictionary containing student info
    """
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
    
    return stu_info

def get_derived_info(stu_info):
    """
    receives a dictionary containing student info
    iterates over the csv files, filling information relative to student derived
    attributes   
    """
    # fill student grades
    #fill_grades(stu_info)

    # calculate student ira for the semesters - TODO (can be done)
    set_ira(stu_info)

    # calculate improvement rate - TODO (can be done)
    #set_impr_rate(stu_info)

    # calculate fail rate - ok
    #set_fail_rate(stu_info)

    # calculate pass rate - ok
    #set_pass_rate(stu_info)

    # calculate drop rate - ok
    #set_drop_rate(stu_info)

    # calculate mandatory rate - TODO (can be done)
    #set_mand_rate(stu_info)

    # calculate hard rate - TODO (can be done)
    #set_hard_rate(stu_info)

    # calculate if student is in condition - TODO (can be done)
    #set_condition(stu_info)

    # calculate position of the student for the semester he is in 
    #- TODO (can be done)
    #set_condition(stu_info)

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

def load_students(name, path = 'data/'): 
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

def save_students(name, stu_info, path = 'data/'): 
    """
    receives a name and a dictionary containing student info. 
    saves the student dictionary as a pickle object with a given name
    """
    file_target = open(path + name, 'wb')
    pickle.dump(stu_info, file_target)

def set_drop_rate(stu_info): 
    """
    receives a dictionary containing all student information
    set correctly the IRA of every student
    """
    for key in stu_info: 
        # get current student grades
        cur_stu_grades = stu_info[key].grades

        # iterate through every subject
        subjects_coursed = 0
        subjects_dropped = 0 
        for sub_name, info in cur_stu_grades.items():
            subjects_coursed += 1
            grade = info[2] # grade is third information on the list
            if grade not in ['II', 'MI', 'MM', 'MS', 'SS', 'CC']: 
                subjects_dropped += 1
                 
        # set attribute correctly 
        stu_info[key].drop_rate = float(subjects_dropped) / subjects_coursed  

def set_fail_rate(stu_info):
    """
    receives a dictionary
    set correctly the fail rate of every student
    """
    for key in stu_info: 
        # get current student grades
        cur_stu_grades = stu_info[key].grades

        # iterate through every subject
        subjects_coursed = 0
        subjects_failed = 0 
        for sub_name, info in cur_stu_grades.items():
            subjects_coursed += 1
            grade = info[2] # grade is third information on the list
            if grade == 'MI' or grade == 'II': 
                subjects_failed += 1
                 
        # set attribute correctly 
        stu_info[key].fail_rate = float(subjects_failed) / subjects_coursed  

def set_ira(stu_info, mode = 'normal'):
    """
    receives a dictionary containing all students. 
    read the csv file for the student IRA and put the student IRA as an information
    """
    # get all years and semesters to be considered
    if mode == 'quick': 
        set_ira_year_semester(stu_info, 2000, 1)
    elif mode == 'normal': 
        print('starting insertion')
        time_periods = get_time_periods()
        for (year, semester) in time_periods:
            print("starting for (%d %d)" % (year, semester))
            set_ira_year_semester(stu_info, year, semester)
        print('ending insertion')
    else:
        exit('mode option incorrect')

def set_ira_year_semester(stu_info, year, semester):
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
            
    print("number of iras added: %s" % (ira_filled))

def set_pass_rate(stu_info):
    """
    receives a dictionary
    set correctly the pass rate of every student
    """
    for key in stu_info: 
        # get current student grades
        cur_stu_grades = stu_info[key].grades

        # iterate through every subject
        subjects_coursed = 0
        subjects_passed = 0 
        for sub_name, info in cur_stu_grades.items():
            subjects_coursed += 1
            grade = info[2] # grade is third information on the list
            if grade == 'MM' or grade == 'MS' or grade == 'SS': 
                subjects_passed += 1
                 
        # set attribute correctly 
        stu_info[key].pass_rate = float(subjects_passed) / subjects_coursed  

# get all student relevant information and saves it as an object
get_students_info()

# load student info, just a test
#load_students('students_info')
