# subjects file 
import pickle

import sys
sys.path.append('..')
from basic import *
from aux import *

import students as stu

NAME_SUB_STRUCTURE = 'sub_info'

class Subject():
    """
    class that represents a subject
    for a subject, we are interested in the number of credits for the subject and the
    approvation rate
    """
    def __init__(self, name, code, credits):
        """
        initializes a subject correctly
        receives:
            1. subject name
            2. subject code
            3. subject credits
        returns:
            nothing
        """
        self.name = name
        self.code = code
        self.credits = credits

        # statistics to know how many have coursed and how many got approved
        self.num_stu_coursed = 0 
        self.num_apprv = 0

    def get_appr_rate(self):
        """
        calculates and returns the approvation rate
        receives: 
            nothing
        returns: 
            approvation rate
        """
        #TODO: print(self.name, self.num_apprv, self.num_stu_coursed)
        appr_rate = self.num_apprv / float(self.num_stu_coursed)
        return appr_rate

    def update_info(self, grade):
        """
        update statistics to reflect if there was an approvation, a reprovation or
        not
        receives:
            1. student grade on the subject
        returns: 
            nothing
        """
        if grade.lower() in ['mm', 'ms', 'ss']:
            self.num_apprv += 1
            self.num_stu_coursed += 1
        elif grade.lower() in ['mi', 'ii']:
            self.num_stu_coursed += 1

        # handle the case of a subject that has number of student coursing it
        # equal 0 - put it equal to 1
        elif self.num_stu_coursed == 0:
            self.num_stu_coursed = 1 
        else: 
            pass

def build_all_subjects(stu_info):
    """
    obtain all subjects the students have coursed so
    far. saves this info in PATH + NAME_SUB_STRUCTURE
    receives:
        1. student dictionary
    returns:
        nothing
    """
    subj_info = {}
    
    for key_stu, stu in stu_info.items():
        update_info(subj_info, stu)

    pickle.dump(subj_info, open(PATH + NAME_SUB_STRUCTURE, 'wb'))
   
def load_subjects(stu_info):
    """
    load subjects using pickle.
    case not possible, build structure from scratch and then loads
    receives: 
        1. student dictionary
    returns: 
        list of subjects
    """
    try: 
        sub_lst = pickle.load(open(PATH + NAME_SUB_STRUCTURE, 'rb'))
    except FileNotFoundError:
        print('could not find subject structure, so will build from scratch')
        build_all_subjects(stu_info)
        sub_lst = pickle.load(open(PATH + NAME_SUB_STRUCTURE, 'rb'))
        print('finished building from scratch')
    return sub_lst

def update_info(subj_info, stu):
    """
    update the information of the subjects based on the info a given student has
    receives:
        1. the dictionary containing subjects seen so far 
        2. a student
    returns: 
        nothing
    """
    for key_grade, grades_lst in stu.grades.items():
        for pos in range(len(grades_lst)): 
            # it may be necessary to create a new subject
            code = stu.get_sub_info(key_grade, pos, 'code') 
            if not (code in subj_info):
                name = stu.get_sub_info(key_grade, pos, 'name') 
                credits = stu.get_sub_info(key_grade, pos, 'credits')
                new_sub = Subject(name, code, credits)
                subj_info[code] = new_sub

            # the information the subject will store is obtained by the student
            grade = stu.get_sub_info(key_grade, pos, 'grade')
            subj_info[code].update_info(grade)
