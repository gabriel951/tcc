# subjects file 

import sys
sys.path.append('..')
from basic import *
from aux import *

import students as stu

NAME_SUB_STRUCTURE = 'sub_info'

class Subject():
    """
    class that represents a subject
    """
    def __init__(self, name, code):
        """
        initializes a subject putting the name, the code
        and setting the statistics variable 
        """
        self.name = name
        self.code = code

        # statistics to know how many have coursed and how many got approved
        self.num_stu_coursed = 0 
        self.num_apprv = 0

    def get_appr_rate(self):
        """
        calculates and returns the approvation rate
        """
        return self.num_apprv / float(self.num_stu_coursed)

    def updata_info(self, grade):
        """
        receives a grade 
        update statistics to reflect if there was an approvation, a reprovation or
        not
        """
        if grade.lower() in ['mm', 'ms', 'ss']:
            self.num_apprv += 1
            self.num_stu_coursed += 1
        elif grade.lower() in ['mi', 'ii']:
            self.num_stu_coursed += 1
        else:
            pass

def build_all_subjects(stu_info)
    """
    from the dictionary of students, obtain all subjects the students have coursed so
    far
    saves this info in PATH + NAME_SUB_STRUCTURE
    """
    subj_info = {}
    
    for key_stu, stu in stu_info.items():
        update_info(subj_info, stu)

    pickle.dump(subj_info, open(PATH + NAME_SUB_STRUCTURE, 'wb'))
   
def load_subjects(stu_info):
    """
    try to load subjects from pickle structure. 
    case not possible, build structure from scratch
    returns a list
    """
    try: 
        sub_lst = pickle.open(PATH + NAME_SUB_STRUCTURE, 'rb')
    except FileNotFoundError:
        print('could not find subject structure, so will build from scratch')
        build_all_subjects(stu_info)
        sub_lst = pickle.open(PATH + NAME_SUB_STRUCTURE, 'rb')
    finally:
        return sub_lst

def update_info(subj_info, stu):
    """
    receives the dictionary containing subjects seen so far and a student
    update the information of the subjects based on the info the student has 
    """
    for key_grade, grades_lst in stu.grades.items():
        for pos in range(len(grades_lst)): 
            # it may be necessary to create a new subject
            if not (stu.get_sub_info(key_grade, pos, 'code') in subj_info):
                name = stu.get_sub_info(key_grade, pos, 'name') 
                code = stu.get_sub_info(key_grade, pos, 'code') 
                new_sub = Subject(name, code)
                subj_info[code] = new_sub

            # the information the subject will store is obtained by the student
            grade = stu.get_sub_info(key_grade, pos, 'grade')
            subj_info[code].update_info(grade)

