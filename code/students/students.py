#!/usr/bin/python3.4
# student file, contain information about the students
import pickle

# import basic
import sys
sys.path.append('..')
from basic import *

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
        # reason between approvation in mandatory disciplines and number of
        # discipline taken
        self.mand_rate = None
        # rate of approvation in the most hard disciplines of the semester
        self.hard_rate = None
    
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
    fill_grades(stu_info)

    # calculate student ira for the semesters
    #set_ira(stu_info)

    # calculate improvement rate
    #set_impr_rate(stu_info)

    # calculate fail rate
    #set_fail_rate(stu_info)

    # calculate pass rate
    #set_pass_rate(stu_info)

    # calculate drop rate
    #set_drop_rate(stu_info)

    # calculate mandatory rate
    #set_mand_rate(stu_info)

    # calculate hard rate
    #set_hard_rate(stu_info)

def get_students_info(): 
    """
    extracts from database all the students information
    saves the information as a dictionary of students and serializes it using
    pickle

    * the dictionary of students accept as a key the student id in database and has
    * as value the corresponding student object
    """
    # obtain info for the students contained in database
    stu_dict = get_database_info()
    
    # construct info for the derived attributes of a student
    get_derived_info(stu_dict)

    # saves object
    save_students('students_info', stu_dict)

def load_students(name, path = 'data/'): 
    """
    receives a name
    loads the student array saved as a pickle serialized object
    """
    stu_info = pickle.load(open(path + name, 'rb'))
    return stu_info

def save_students(name, stu_info, path = 'data/'): 
    """
    receives a name and a dictionary containing student info. 
    saves the student dictionary as a pickle object with a given name
    """
    file_target = open(path + name, 'wb')
    pickle.dump(stu_info, file_target)

# get all student relevant information and saves it as an object
#get_students_info()
# load student info, just a test
load_students('students_info')
