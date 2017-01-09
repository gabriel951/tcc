#!/usr/bin/python3.4

# student file, contain information about the students
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
        self.show_student()
        

def fill_grades(stu_info):
    """
    receives a student info dictionary
    opens csv files to find subjects coursed by the students and then 
    put these info in the student info dictionary
    """
def get_database_info():
    """
    receives nothing
    query the database to obtain student info that can be obtained
    returns a dictionary containing student info
    """
    stu_info = {}
    TABLE = 'student'

    # constants
    STU_COD_MAT_IND = 1
    STU_ID_IND = 0

    # query database
    query = 'select * from %s.%s ' % (MY_DATABASE, TABLE)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()

    # iterate over every row
    for row in rows: 
        key = row[STU_COD_MAT_IND]
        print(row)

        # in case this student is a new one 
        if not key in stu_info: 
            # add student, case the registration is a new one
            student_id = row[STU_ID_IND]
            stu_info[key] = Student(student_id)
            stu_info[key].set_attrib(row)
    
    return stu_info

def get_students_info(): 
    """
    extracts from database all the students information
    saves the information as a dictionary of students and serializes it using
    pickle

    * the dictionary of students accept as a key the student registration and has a
    * value the corresponding student object
    """
    # obtain info for the students contained in database
    stu_dict = get_database_info()
    exit()
    
    # construct info for the derived attributes of a student
    obtain_derived_info(stu_dict)

    # saves object
    save_students('students_info', stu_dict)

def load_students(): 
    """
    receives a name
    loads the student array saved as a pickle serialized object
    """

def obtain_derived_info(stu_info):
    """
    receives a dictionary containing student info
    iterates over the csv files, filling information relative to student derived
    attributes   
    """
    # fill student grades
    fill_grades(stu_info)

    # calculate student ira for the semesters
    set_ira(stu_info)

    # calculate improvement rate
    set_impr_rate(stu_info)

    # calculate fail rate
    set_fail_rate(stu_info)

    # calculate pass rate
    set_pass_rate(stu_info)

    # calculate drop rate
    set_drop_rate(stu_info)

    # calculate mandatory rate
    set_mand_rate(stu_info)

    # calculate hard rate
    set_hard_rate(stu_info)

def save_students(name, stu_info, path = 'data/'): 
    """
    receives a name and a dictionary containing student info. 
    saves the student dictionary as a pickle object with a given name
    """

# get all student relevant information and saves it as an object
get_students_info()
# load student info, just a test
#load_students()
