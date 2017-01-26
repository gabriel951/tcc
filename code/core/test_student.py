#!/usr/bin/python3.4
# student test file. Needed to perform checks. 
from students import *

def perform_checks():
    """
    performs the necessary checks, to ensure that all students have data as expected
    """
    # load student info
    stu_info = load_students(NAME_STU_STRUCTURE)
    print('loaded student info')

    # check if all student has grades
    #check_grades(stu_info)

    # check if student ira is as expected
    check_ira_consistency(stu_info)

def check_ira_consistency(stu_info):
    """
    checks include:
        1 - check if all iras have value different than None
        2 - check that all entries in the ira list are numbers 
    """
    print('started checking ira consistency')
    
    # part 1 
    errors = 0
    entries = 0
    for key, stu in stu_info.items():
        entries += 1
        if stu.ira == None:
            errors += 1
    print('%d None values in ira, for %d students' % (errors, entries))

    # part 2 
    errors2 = 0
    entries = 0 
    for key, stu in stu_info.items():
        entries += 1
        for ira in stu.ira: 
            if type(ira) != float:
                errors2 += 1
                break
    print('%d students with ira not know, of a total of %d students' % \
            (errors2, entries))
    

perform_checks()
