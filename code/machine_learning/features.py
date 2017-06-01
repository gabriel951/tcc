# this file contain features function that we'll be used to put features in the right
# format for the machine learning algorithms to work

from basic_ml import *

import sys
sys.path.append('..')
from basic import *

#TODO: simplify the 3 lines of code that append to the feat name list

# valid values for some attributes
VALID_SEX_VALUES = ['m', 'f']
VALID_LOCAL_VALUES = ['df', 'outros', 'indisponível']
VALID_QUOTA_VALUES = ['sim', 'não']
VALID_SCHOOL_TYPE_VALUES = ['não informada', 'particular', 'pública']
VALID_COURSE_VALUES = COURSES_OFF_NAME
VALID_WAY_IN_VALUES = ['Vestibular', 'Convênio-Int', 'Transferência Obrigatória', 
        'Acordo Cultural-PEC-G',  'Convênio - Andifes', 'Matrícula Cortesia', 
        'Sisu-Sistema de Seleção Unificada', 'Transferência Facultativa', 
        'Portador Diplom Curso Superior', 'PEC-Peppfol-Graduação', 
        'Vestibular para mesmo Curso', 'Programa de Avaliação Seriada', 'Enem']
    

def add_feature_sex(stu, stu_features, feat_name_lst):
    """
    append feature sex to the student feature list
    append atribute to the name list, if not already in there
    receives:
        1. a student
        2. a list containing all the student features
        3. list with the name of the features considered so far
    returns:
        nothing 
    """
    name_feature = 'sex'
    if not (name_feature in feat_name_lst):
        feat_name_lst.append(name_feature)

    # assert value is as expected
    assert(stu.sex in VALID_SEX_VALUES)
    if stu.sex == 'm':
        stu_features.append(0)
    elif stu.sex == 'f':
        stu_features.append(1)
    else:
        exit('error on add feature sex function')

def add_feature_age(stu, stu_features, feat_name_lst):
    """
    append feature age to the student feature list
    append atribute to the name list, if not already in there
    receives:
        1. a student
        2. a list containing all the student features
        3. list with the name of the features considered so far
    returns:
        nothing 
    """
    name_feature = 'age'
    if not (name_feature in feat_name_lst):
        feat_name_lst.append(name_feature)

    # assert value is as expected
    assert(stu.age > 0 and stu.age < 100)
    stu_features.append(stu.age)

def add_feature_condition(stu, stu_features, semester, feat_name_lst):
    """
    append feature condition to the student feature list
    append atribute to the name list, if not already in there
    receives:
        1. a student
        2. a list containing all the student features
        3. the semester we are interested. 
        4. list with the name of the features considered so far
    returns:
        nothing 
    """
    name_feature = 'condition'
    if not (name_feature in feat_name_lst):
        feat_name_lst.append(name_feature)

    assert(type(stu.in_condition[semester - 1]) == int)
    if stu.in_condition[semester - 1] == 0: 
        stu_features.append(0)
    else: 
        stu_features.append(1)

def add_feature_course(stu, stu_features, feat_name_lst):
    """
    append feature course to the student feature list
    append atribute to the name list, if not already in there
    receives:
        1. a student
        2. a list containing all the student features
        3. list with the name of the features considered so far
    returns:
        nothing 
    """
    # use dummy list
    name_feature = 'course'
    put_dummy_variables(stu.course, VALID_COURSE_VALUES, stu_features, name_feature,\
            feat_name_lst) 

def add_feature_credit_rate_acc(stu, stu_features, semester, feat_name_lst):
    """
    append feature credit_rate_acc to the student feature list
    append atribute to the name list, if not already in there
    receives:
        1. a student
        2. a list containing all the student features
        3. the semester we are interested. 
        4. list with the name of the features considered so far
    returns:
        nothing 
    """
    name_feature = 'credit_rate_acc'
    if not (name_feature in feat_name_lst):
        feat_name_lst.append(name_feature)

    # if student has already graduate, put last value in the list
    assert(stu.credit_rate_acc[semester - 1] >= 0)
    stu_features.append(stu.credit_rate_acc[semester - 1])

def add_feature_hard_rate(stu, stu_features, semester, feat_name_lst):
    """
    append feature hard_rate to the student feature list
    append atribute to the name list, if not already in there
    receives:
        1. a student
        2. a list containing all the student features
        3. the semester we are interested. 
        4. list with the name of the features considered so far
    returns:
        nothing 
    """
    name_feature = 'hard_rate'
    if not (name_feature in feat_name_lst):
        feat_name_lst.append(name_feature)

    # if student has already graduate, put last value in the list
    assert(stu.hard_rate[semester - 1] >= 0 and stu.hard_rate[semester - 1] <= 1.0)
    stu_features.append(stu.hard_rate[semester - 1])

def add_feature_drop_rate(stu, stu_features, semester, feat_name_lst):
    """
    append feature drop_rate to the student feature list
    append atribute to the name list, if not already in there
    receives:
        1. a student
        2. a list containing all the student features
        3. the semester we are interested. 
        4. list with the name of the features considered so far
    returns:
        nothing 
    """
    name_feature = 'drop_rate'
    if not (name_feature in feat_name_lst):
        feat_name_lst.append(name_feature)

    assert(stu.drop_rate[semester - 1] >= -1 and stu.drop_rate[semester - 1] <= 2)
    stu_features.append(stu.drop_rate[semester - 1])

def add_feature_impr_rate(stu, stu_features, semester, feat_name_lst):
    """
    append feature improvement_rate to the student feature list
    append atribute to the name list, if not already in there
    receives:
        1. a student
        2. a list containing all the student features
        3. the semester we are interested. 
        4. list with the name of the features considered so far
    returns:
        nothing 
    """
    name_feature = 'impr_rate'
    if not (name_feature in feat_name_lst):
        feat_name_lst.append(name_feature)

    # if student has already graduate, put last value in the list
    stu_features.append(stu.improvement_rate[semester - 1])

def add_feature_ira(stu, stu_features, semester, feat_name_lst):
    """
    append feature ira to the student feature list
    append atribute to the name list, if not already in there
    receives:
        1. a student
        2. a list containing all the student features
        3. the semester we are interested. 
        4. list with the name of the features considered so far
    returns:
        nothing 
    """
    name_feature = 'ira'
    if not (name_feature in feat_name_lst):
        feat_name_lst.append(name_feature)

    # if student has already graduate, put last value in the list
    assert(stu.ira[semester - 1] >= 0.0 and stu.ira[semester - 1] <= 5.0)
    stu_features.append(stu.ira[semester - 1])

def add_feature_local(stu, stu_features, feat_name_lst):
    """
    NOTE: this function should not be used anymore
    append feature local to the student feature list
    append atribute to the name list, if not already in there
    receives:
        1. a student
        2. a list containing all the student features
        3. list with the name of the features considered so far
    returns:
        nothing 
    """
    exit('add feature local is not to be used')
    # use dummy list
    #name_feature = 'local'
    #put_dummy_variables(stu.local, VALID_LOCAL_VALUES, stu_features, name_feature,
    #        feat_name_lst) 

def add_feature_quota(stu, stu_features, feat_name_lst):
    """
    append feature quota to the student feature list
    append atribute to the name list, if not already in there
    receives:
        1. a student
        2. a list containing all the student features
        3. list with the name of the features considered so far
    returns:
        nothing 
    """
    # use dummy list
    name_feature = 'quota'
    put_dummy_variables(stu.quota, VALID_QUOTA_VALUES, stu_features, name_feature, 
            feat_name_lst) 

def add_feature_quota_enh(stu, stu_features, feat_name_lst):
    """
    append feature quota enhanced to the student feature list
    append atribute to the name list, if not already in there
    receives:
        1. a student
        2. a list containing all the student features
        3. list with the name of the features considered so far
    returns:
        nothing 
    * function should enhance performance of model by considering a different set of
    * categories than the original
    """

    ENH_QUOTA_VALUES = ['negro', 'universal', 'outros']
    assert (stu.quota in VALID_QUOTA_VALUES)
    if stu.quota == 'negro':
        enh_quota = stu.quota
    elif stu.quota == 'universal':
        enh_quota = stu.quota
    else:
        enh_quota = 'outros'

    # use dummy list
    name_feature = 'enh_quota'
    put_dummy_variables(enh_quota, ENH_QUOTA_VALUES, stu_features, name_feature, 
            feat_name_lst) 

def add_feature_pass_rate(stu, stu_features, semester, feat_name_lst):
    """
    append feature pass_rate to the student feature list
    append atribute to the name list, if not already in there
    receives:
        1. a student
        2. a list containing all the student features
        3. the semester we are interested. 
        4. list with the name of the features considered so far
    returns:
        nothing 
    """
    name_feature = 'pass_rate'
    if not (name_feature in feat_name_lst):
        feat_name_lst.append(name_feature)

    # if student has already graduate, put last value in the list
    assert(stu.pass_rate[semester - 1] >= -1 and stu.pass_rate[semester - 1] <= 2)
    stu_features.append(stu.pass_rate[semester - 1])

def add_feature_position(stu, stu_features, semester, feat_name_lst):
    """
    append feature position to the student feature list
    append atribute to the name list, if not already in there
    receives:
        1. a student
        2. a list containing all the student features
        3. the semester we are interested. 
        4. list with the name of the features considered so far
    returns:
        nothing 
    """
    name_feature = 'position'
    if not (name_feature in feat_name_lst):
        feat_name_lst.append(name_feature)

    # if student has already graduate, put last value in the list
    assert(stu.position[semester - 1] >= -1)
    stu_features.append(stu.position[semester - 1])

def add_feature_school_type(stu, stu_features, feat_name_lst):
    """
    NOT TO USE
        -> please don't use this atribute, because there are a lot of missing 
        values. 
    append feature school_type to the student feature list
    append atribute to the name list, if not already in there
    receives:
        1. a student
        2. a list containing all the student features
        3. list with the name of the features considered so far
    returns:
        nothing 
    """
    exit('too much missing values here')
    # use dummy list
    name_feature = 'school_type'
    put_dummy_variables(stu.school_type, VALID_SCHOOL_TYPE_VALUES, stu_features,
            name_feature, feat_name_lst) 

def add_feature_way_in(stu, stu_features, feat_name_lst):
    """
    append feature way in enhance to the student feature list
    append atribute to the name list, if not already in there
    receives:
        1. a student
        2. a list containing all the student features
        3. list with the name of the features considered so far
    returns:
        nothing 
    """
    ENH_WAY_IN_VALUES = ['PAS', 'Vestibular', 'Outros']
    assert (stu.way_in in VALID_WAY_IN_VALUES)
    if stu.way_in == 'PAS':
        enh_way_in = stu.way_in
    elif stu.way_in == 'Vestibular':
        enh_way_in = stu.way_in
    else:
        enh_way_in = 'Outros'

    # use dummy list
    name_feature = 'way_in'
    put_dummy_variables(enh_way_in, ENH_WAY_IN_VALUES, stu_features, name_feature, 
            feat_name_lst) 

def add_outcome(stu, target_lst):
    """
    append student outcome (whether student was able to graduate or not)
    to a target list containing this students results
    receives:
        1. a student
        2. the target list
    returns: 
        nothing
    """
    # assert value is as expected
    assert(stu.graduated() or stu.migrated() or stu.evaded())

    if stu.graduated():
        target_lst.append(GRADUATED)
    elif stu.migrated():
        target_lst.append(MIGRATED)
    else: 
        target_lst.append(EVADED)

def put_dummy_variables(atr_value, lst_values, stu_features, feat_name, \
        feat_name_lst):
    """
    put a given atribute as dummy variable
    make sure the feature name list remain correct
    receives:
        1. atribute value
        2. list of possible values for the attribute
        3. list of students variable that we must append attributes
        4. atribute name
        5. list of features name
    returns: 
        nothing
    """
    if not (feat_name in feat_name_lst):
        # repeat as long as there we'll be dummy variables
        for i in range(len(lst_values)):
            feat_name_lst.append(feat_name)

    # make sure dummy variable is correct
    try:
        assert(atr_value in lst_values)
    except:
        print(atr_value)
        exit()

    # build list of dummy variables
    dummy_lst = []
    for i in range(len(lst_values)):
        dummy_lst.append(0)

    # change dummy variable for the list the student is in 
    ind = lst_values.index(atr_value)
    dummy_lst[ind] = 1

    # append to student features list
    for elem in dummy_lst:
        stu_features.append(elem)
