# student file, contain information about the students
import pickle
import csv

# TODO: in my report, describe how imputation happenned for each feature

import sys
sys.path.append('..')
from basic import *
from aux import *

from grades import *
from courses import *
import subjects as sub

# name of the structure that will contain the students information
NAME_STU_STRUCTURE = 'students_info'

# value to indicate we haven't filled a given field yet
NOT_KNOWN = 'not know'
ERROR = -20 # if it was a low value like -1 i could access a value on the list

# global variables
ira_filled = 0 # number of students with ira calculated

class Student(): 
    """
    class that represents the student
    """
    def __init__(self, id_num, row): 
        """
        receives a row containing student info
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

        # set attributes
        self.set_attrib(row)

        ## performance data follows

        # obtain list with size equal to the number of semesters a student stayed in
        # unb and value NOT KNOWN. This list will be used for initialization
        lst_unknown = []
        num_semesters = self.get_num_semesters()
        for i in range(num_semesters):
            lst_unknown.append(NOT_KNOWN)

        # ira of the student in a given semester
        self.ira = lst_unknown[:] 
        # ira of the student in all his semesters in unb
        self.ira_acc = lst_unknown[:]

        # reason between grades of current semester and last semester
        self.improvement_rate = lst_unknown[:]
        # reason between subjects coursed and subjects failed
        self.fail_rate = lst_unknown[:] 
        # reason between subjects coursed and subjects passed
        self.pass_rate = lst_unknown[:] 
        # reason between subjects coursed and subjects dropped
        self.drop_rate = lst_unknown[:] 
        # number of credits coursed in a semester with approvation
        self.credit_rate = lst_unknown[:]
        # number of credits "accumulated": coursed in all semesters before with approvation
        self.credit_rate_acc = lst_unknown[:]
        # rate of approvation in the most hard disciplines of the semester
        self.hard_rate = lst_unknown[:]
        # boolean that indicates whether a student is in condition or not
        self.in_condition = lst_unknown[:]
        # position of the student relative to the semester he is in 
        self.position = lst_unknown[:]
        # previous chance of the student evading university, calculated by the
        # model 
        self.evasion_chance = {}

    def calculate_ira_yearsem(self, year, sem):
        """
        DEPRECATED 
        receives an year and a semester, calculates the ira the student will have in
        the passed ira and semester

        * similar calculations found in method get_sem_grade
        """
        # TODO: code not complete because i don't have the number of credits the
        # student has taken
        #assert (sem == 1 or sem == 2)
        
        ## special case counter
        #spc_counter = 0

        ## variables for ira calculation
        #ira_sum = 0
        #drop_mand_sub = 0
        #drop_opt_sub = 0 
        #num_sub = 0 

        ## iterate through all the subjects student coursed
        #for subject, data_list in self.grades.items(): 
        #    for pos in range(len(data_list)): 
        #        # pass if subject not coursed yet
        #        code_sub = self.get_sub_info(subject, pos, 'code')
        #        year_sub = self.get_sub_info(subject, pos, 'year')
        #        sem_sub = self.get_sub_info(subject, pos, 'sem')
        #        grade_sub = self.get_sub_info(subject, pos, 'grade')
        #        if year_coursed > year or \
        #            (year_coursed == year and sem_coursed >= sem): 
        #                pass

        #        
        #        # student dropped case
        #        if student_dropped(grade):
        #            num_sub += 1
        #            if is_mand_sub(code_sub, self.course, self.year_in, self.sem_in):
        pass

    def can_finish(self, pos):
        """
        checks if a student in a given position is in the last semester of the course
        and if the student can complete 
        receives: 
            1. position of the student we are considering. This count start at 0.
        returns: 
            True case the student is not in the last semester or if the student can
            complete the course. False otherwise. 
        """
        # checks if student is in last semester of course, return True case he isnt
        course = load_course(self.course, self.year_in, self.sem_in)
        if pos < (course.max_sem - 1): 
            return True

        # get how many credits the student has and how many the course demand to
        # graduate
        credits_student_has = self.credit_rate_acc[pos]
        credits_to_graduate = course.credits_graduate

        # decide if student can graduate, based on the number of credits left
        if (credits_graduate - credits_student_has) > course.max_credits_sem:
            return False
        else: 
            return True
        
    def check_2repr(self, pos):
        """
        check whether the student has two reprovations in a given subject for 
        a given position
        receives: 
            1. position of the student were are interested
        returns:
            boolean indicating if student has 2 reprovations. 

        * pos = 0 means the year and semester the student got in unb 
        """
        (cur_year, cur_sem) = self.pos_2_yearsem(pos, self.year_in, self.sem_in)
    
        for key_grd, grd_lst in self.grades.items(): 
            num_fails = 0 
            for pos in range(len(grd_lst)):
                (code, name, grade, year, sem, credits) = self.get_sub_info(key_grd, pos, 'all') 
                if student_failed(grade):
                    if year < cur_year or (year == cur_year and sem <= cur_sem):
                        num_fails += 1
            if num_fails >= 2: 
                return True

        return False

    def evaded(self): 
        """
        indicates if student evaded from university, because of academic reasons
        receives: 
            1. nothing
        returns: 
            True, case student evaded. False otherwise
        """
        if self.way_out in EVASION_WAY_OUT: 
            return True
        return False

    def few_pass(self, pos):
        """
        returns True case for the semester with position pos and the previous one 
        the student didnt pass in four disciplines of the course
        """
        # TODO: can't know what are the disciplines of the course

    def get_course(self, course_lst):
        """
        DEPRECATED
        get the course student is in 
        receives:
            1. course list
        returns:
            the course with curriculum the student is in
        """
        for course in course_lst:
            if course.is_valid(self.course, self.year_in, self.sem_in):
                return course
        exit('could not load course %s for the year %d and semester %d' %
                (self.course, self.year_in, self.sem_in))

    # TODO
    def get_imprv_way_in(self): 
        pass
    def get_imprv_way_out(self): 
        pass

    def get_num_semesters(self):
        """
        get the number of semesters a student was in unb 
        receives: 
            1. a student with correct information regarding the year and semester
                the student left.
        Returns: 
            number of semesters the student was in the university
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

    def get_sem_grade(self, year, semester, course, fp):
        """
        receives a student, the year and semester we are considering, the course
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
                    continue                

                # if the student dropped
                if student_dropped(data[grade_pos]):
                    # if the discipline is mandatory
                    if course.is_mandatory(data[code_pos]):
                        drop_mand_sub += 1
                    else:
                        drop_opt_sub += 1
                    num_sub += 1

                # weight of the grade
                grade_weight = get_grade_weight(data[grade_pos])
                if grade_weight == None: 
                    # dont consider
                    continue
                else:
                    # increment the number of subjects coursed
                    num_sub += 1
                    sum_weights += grade_weight
        
        # there are cases where the number of subjects taken is zero (for instance,
        # when all the student got is CC
        try: 
            penalty_factor = 1 - ((0.6 * drop_mand_sub + 0.4 * drop_opt_sub) / num_sub)
            grade_factor = float(sum_weights) / num_sub
            ira_semester = penalty_factor * grade_factor
            assert (ira_semester >= 0 and ira_semester <= 5.0)
            return ira_semester
        except ZeroDivisionError:
            self.log_info(fp)
            return NOT_KNOWN
        except AssertionError:
            print(penalty_factor)
            print(grade_factor)
            print(ira_semester)
    
    def get_sub_info(self, key, pos, info):
        """
        obtain information of a given student in a given subject
        receives: 
            1. a key to access a given subject
            2. the position in the list of information for that subject
            3. a string describing the info we want - 'code', 'name', 'grade', 'year,
            'sem', 'credits' or 'all'
        return: 
            the information we want
        """
        if info == 'code':
            return self.grades[key][pos][0] # code is the first information
        elif info == 'name':
            return self.grades[key][pos][1] # name is the second information
        elif info == 'grade':
            return self.grades[key][pos][2] # grade is the third information
        elif info == 'year':
            return self.grades[key][pos][3] # year is the fourth information
        elif info == 'sem':
            return self.grades[key][pos][4] # semester is the fifth information
        elif info == 'credits':
            return self.grades[key][pos][5] # credit is the sixth information
        elif info == 'all':
            tup = tuple(self.grades[key][pos])
            return tup # tuple returned in the same order
        else:
            exit('value passed to get_sub_info not valid')

    def graduated(self): 
        """
        indicates if student was able to graduate
        receives: 
            1. nothing
        returns: 
            True, case student was able to form. False otherwise
        """
        if self.way_out.lower() == 'formatura': 
            return True
        return False

    def is_train_inst(self):
        """
        indicates if a student is in the training instance
        receives: 
            nothing
        returns: 
            True, case student is on the training set. False otherwise
        """
        return self.year_in >= YEAR_START_TRA and self.year_in <= YEAR_END_TRA

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

    def migrated(self): 
        """
        indicates if student migrated from the course he was in 
        receives: 
            1. nothing
        returns: 
            True, case student did migrate. False otherwise
        """
        if self.way_out in MIGRATION_WAY_OUT: 
            return True
        return False

    def min_pass(self, pos):
        """
        checks if student was approved in the given semester and in the previous one 
        in the minimum amount of credits for the course
        receives:
            1. the position we are interested
        returns: 
            boolean, indicating student situation
        """
        assert (pos > 0)
        credits_cur_semester = self.get_credit_appr(pos)
        credits_last_semester = self.get_credit_appr(pos - 1)

        # TODO: need to know the minimum number of credits for each course
        
    def pos_2_yearsem(self, pos, year, sem):
        """
        receives a position the student is in, a year and a semester
        returns the year and semester correspondent

        * pos = 0 means the year and semester the student got in unb
        """
        assert (pos >= 0)

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
        set the attributes of student contained in the database correctly 
        receives: 
            1. tuple containing student information (no derived attributes)
        returns:
            nothing
        """
        ## the magic numbers are the position in the row
        # set attributes
        self.reg = tup[0]
        self.sex = tup[1]
        self.age = tup[2]
        self.quota = tup[3]
        self.school_type = tup[4]
        self.race = tup[5]
        self.local = tup[6]
        self.course = tup[7]
        self.year_in = tup[8]
        self.sem_in = tup[9]
        self.year_out = tup[10]
        self.sem_out = tup[11]
        self.way_in = tup[12]
        self.way_out = tup[13]

        # for code consistency reasons, change the name of the courses
        self.set_course_name()

    def set_condition(self):
        """
        fills whether the student is in condition for that semester or not
        receives: 
            nothing
        returns: 
            nothing
        also, fills the list with right information

        fills: 
            NO_CONDITION - case the student is not in condition
            TWICE_FAIL - case the student is in condition because of twice failing in the same
            subject
            FEW_PASS - case the student is in condition because of not being approved in
            four disciplines for the two periods
            CANT_COMPLETE - case the student is in the last semester without
            condition to complete the course
        """
        # avoid magic numbers ;)
        NO_CONDITION = 0
        TWICE_FAIL = 1
        FEW_PASS = 2
        CANT_COMPLETE = 3
        
        # iterate through the semesters, filling whether he is in position or not
        for pos in range(self.get_num_semesters()):

            # no student at the end of the first semester is in condition
            if pos == 0: 
                self.in_condition[pos] = NO_CONDITION

            # if student that is in condition for twice failing a subject is not
            # better
            elif self.in_condition[pos - 1] == TWICE_FAIL:
                # check if there's any reprovation in two subjects 
                if self.check_2repr(pos):
                    self.in_condition[pos] = TWICE_FAIL

            # check if student that was in condition for few approvations is now better
            # this problem can't happen if student is in the first semester 
            elif self.in_condition[pos - 1] == FEW_PASS:
                if not self.min_pass(pos):
                    self.in_condition[pos] = FEW_PASS

            # we need to check if student has two reprovations in the same subject
            elif self.check_2repr(pos):
                self.in_condition[pos] = TWICE_FAIL

            # check if student has not been approved in four disciplines of the course
            # for the past 2 semesters
            elif self.few_pass(pos):
                self.in_condition[pos] = FEW_PASS

            # TODO: evaluate whether the student is in the last semester of the course
            # and has the possibility to finish seems rather hard 
            #elif not self.can_finish(pos):
            #    self.in_condition[pos] = CANT_COMPLETE

            # else, student not in condition
            else: 
                self.in_condition[pos] = NO_CONDITION

    def set_course_name(self):
        """
        the course name the student has may be a variation of the standard one 
        this function ensure that we don't have this distortion
        receives:
            nothing
        returns: 
            nothing
        """
        # if name is in the official name list, nothing to do 
        if self.course in COURSES_OFF_NAME:
            return
        elif 'ciência da computação' in self.course.lower(): 
            self.course = CIC_BACHELOR
        elif 'engenharia de computação' in self.course.lower():
            self.course = COMPUTER_ENGINEERING
        # the other 'computação' is cic non bachelor course. So this code fragment
        # should come after we handle the bachelors of cic and the computer
        # engineering students
        elif 'computação' in self.course.lower() or \
                'informática' in self.course.lower():
            self.course = CIC_NON_BACHELOR
        elif 'engenharia de software' in self.course.lower():
            self.course = SOFTWARE_ENGINEERING
        elif 'engenharia de redes de comunicação' in self.course.lower():
            self.course = NETWORK_ENGINEERING
        elif 'engenharia mecatrônica' in self.course.lower():
            self.course = MECHATRONICS_ENGINEERING
        else: 
            print('case not handled. Course: %s||' % (self.course))
            exit()

    def set_grades(self, row):
        """
        extracts the grades of the student and put it in the student grade attribute
        receives:
            1. a row of the csv file containing student info
        returns:
            nothing

        ** the same discipline may be coursed by one student more than one time, case
        he has failed it
        """
        # rows indices - RIND
        CODE_SUB_RIND = 1
        SEMESTER_RIND = 2
        YEAR_RIND = 3
        GRADE_RIND = 4 
        NAME_RIND = 5
        CREDITS_RIND = 6

        # get subject name, grade, year and semester coursed
        data = []
        data.append(row[CODE_SUB_RIND])
        data.append(row[NAME_RIND])
        data.append(row[GRADE_RIND])
        data.append(row[YEAR_RIND])
        data.append(row[SEMESTER_RIND])
        data.append(row[CREDITS_RIND])

        ## add grade of student to the dictionary
        # if it's the first time the student coursed subject
        if row[NAME_RIND] not in self.grades:
            self.grades[row[NAME_RIND]] = []

        # be sure not to add an info that we already have
        for lst_data in self.grades[row[NAME_RIND]]: 
            if data == lst_data:
                return
        self.grades[row[NAME_RIND]].append(data)
        
    def set_hard_rate(self, subj_dic):
        """
        set the hard rate for the given student, by consulting the subject list
        receives:
            1. subject dict
        returns: 
            nothing
        """
        # obtain list of tuples of the form: 
        # [(grade, appr_rate), ...]
        # this list measure the performance on hard disciplines
        GRADE_POS_IND = 0
        APPR_RATE_IND = 1

        # initially, perf_hard is an empty list with the same length of the hard rate
        # list
        perf_hard = []
        perf_hard_len = len(self.hard_rate)
        for i in range(perf_hard_len):
            perf_hard.append(NOT_KNOWN)

        for key_grades, grades_lst in self.grades.items(): 
            for pos in range(len(grades_lst)):
                # get student information
                code_sub = self.get_sub_info(key_grades, pos, 'code')
                grade_sub = self.get_sub_info(key_grades, pos, 'grade')
                year_sub = self.get_sub_info(key_grades, pos, 'year')
                sem_sub = self.get_sub_info(key_grades, pos, 'sem')
                appr_rate = subj_dic[code_sub].get_appr_rate()

                # need to obtain the index on the list to perform comparison
                index = self.yearsem_2_pos(year_sub, sem_sub)

                # don't account for subjects that were coursed before student entered
                # in his option
                if index == ERROR: 
                    continue
                
                if (perf_hard[index] == NOT_KNOWN or \
                    appr_rate < perf_hard[index][APPR_RATE_IND]):
                    perf_hard[index] = (grade_sub, appr_rate) 

        # get hard rate
        hard_coursed = 0
        hard_apprv = 0

        for sem in range(len(self.hard_rate)):
            # check hard rate for a given subject was indeed calculated
            if type(perf_hard[sem]) == tuple:
                hard_coursed += 1
            if student_passed(perf_hard[sem][GRADE_POS_IND]):
                hard_apprv += 1 
             
            # if it's not possible to calculate hard rate, put as missing value
            # value
            if hard_coursed == 0: 
                self.hard_rate[sem] = NOT_KNOWN
            else:
                self.hard_rate[sem] =  hard_apprv / float(hard_coursed)
                assert (self.hard_rate[sem] < 1.1)

    def set_improvement_rate(self, fp, course_lst):
        """
        calculates the improvement rate for every student
        """
        # iterate through every year, setting position
        cur_year = self.year_in
        cur_semester = self.sem_in
        for pos in range(self.get_num_semesters()):
            self.set_improvement_rate_semester(cur_year, cur_semester, pos, fp)
            # update current year/semester
            if cur_semester == 1: 
                cur_semester = 2 
            else:
                cur_year += 1
                cur_semester = 1

    def set_improvement_rate_semester(self, year, semester, pos, fp):
        """
        calculates the improvement rate for a given year and semester
        receives:
            1. year,
            2. semester, 
            3. position to insert in a list 
            4. file pointer
        returns:
            nothing
        * if it's the first semester, put a missing value. Should be handled later
        """
        # if position equals 0, missing value
        if pos == 0:
            self.improvement_rate[pos] = NOT_KNOWN
            return
        
        # get grades for past semester and for current semester
        past_sem_grade = self.ira_acc[pos - 1]
        cur_sem_grade = self.ira_acc[pos]

        # handle cases where we don't know the grades by imputation 
        if past_sem_grade == NOT_KNOWN or cur_sem_grade == NOT_KNOWN:
            self.improvement_rate[pos] = 1.0
        else:
            # avoid division by zero
            if past_sem_grade > 0.001:
                self.improvement_rate[pos] = cur_sem_grade / past_sem_grade

                # log pathological cases
                if self.improvement_rate[pos] > 5:
                    fp.write('---- imprv rate strange value ----\n')
                    fp.write('(pos, cur_sem_grade, past_sem_grade): ' +\
                            '(%d, %f, %f)\n' % (pos, cur_sem_grade, past_sem_grade))
                    fp.write('(registration, impr_rate): ' +
                            '(%d, %f)\n' % (self.reg, self.improvement_rate[pos]))
                    fp.write('\n\n')
            # handle division by zero
            else:
                #self.log_info(fp)
                self.improvement_rate[pos] = 1.0
            
    def set_ira(self, ira, year, semester):
        """
        ** DEPRECATED - 
        receives a tuple containing student information (no derived attributes) and
        the year and semester of the information. 
        insert in the student the IRA correctly
        """
        # since it's deprecated, exit with error if called
        exit('called deprecated function')

        # does not consider summer school
        if semester == 0: 
            return

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
        DEPRECATED
        receives the course list
        set the mandatory rate for a given student
        """
        num_sub = 0
        mand_sub = 0

        # get course student is in 
        course = self.get_course(course_lst)

        # count all subjects coursed and how many are mandatory
        for (grade, data_list) in self.grades.items():
            # iterate through all the data in the data list
            for pos in range(len(data_list)):
                num_sub += 1
                code_sub = self.get_sub_info(grade, pos, 'code')
                if course.is_mandatory(code_sub):
                    mand_sub += 1
        
        self.mand_credit_rate = float(mand_sub) / num_sub

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
                % (self.reg, self.year_in, self.sem_in))
        print('\tstudent  %d left in year: %d and semester: %d' \
                % (self.reg, self.year_out, self.sem_out))

    def yearsem_2_pos(self, year, sem):
        """
        calculates for the position student is in, from year and semester
        receives: 
            1. year
            2. semester
        returns: 
            the position the student is in 
        * pos = 0 means the year and semester the student got in unb. 
        * pos = 1 means the semester just after pos = 0, and so on
        * if the subject was coursed before student got in the option, an ERROR is
            returned. 
        """
        # summer counts as last semester of the previous year
        if sem == 0:
            sem = 2
            year -= 1

        pos = 0 
        cur_year = self.year_in 
        cur_sem = self.sem_in 

        # return 
        if self.year_in > year or (self.year_in == year and cur_sem > sem):
            # verbose option
            #print('warning: function yearsem_2_pos called with parameters:')
            #print('year: %d, semester: %d' % (year, sem))
            #print('but student entered in year: %d and semester: %d'\
            #        % (self.year_in, self.sem_in))
            return ERROR

        while cur_year != year or cur_sem != sem: 
            pos += 1
            if cur_sem == 1 or cur_sem == 0:
                cur_sem += 1
            else: 
                cur_sem = 1
                cur_year += 1


        # a student should not be 30 semesters or more in unb
        assert (pos <= 30)
        return pos
