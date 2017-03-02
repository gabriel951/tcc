# this file contain features function that we'll be used to put features in the right
# format for the machine learning algorithms to work
#TODO: eliminate as outlier students that died!
#TODO: normalize features
#TODO: in original table, students from ENEM did not appear

import sys
sys.path.append('..')
from basic import *

# valid values for some attributes
VALID_SEX_VALUES = ['masculino', 'feminino']
VALID_LOCAL_VALUES = ['df', 'outros', 'indisponível']
VALID_QUOTA_VALUES = ['escola publica alta renda-ppi', 'escola publica baixa renda-ppi', 
        'escola publica alta renda-nao ppi', 'escola publica baixa renda-nao ppi', 
        'negro', 'universal']
VALID_SCHOOL_TYPE_VALUES = ['', 'nao declarado', 'particular', 'publica']
VALID_COURSE_VALUES = COURSES_OFF_NAME
VALID_WAY_IN_VALUES = ['Vestibular', 'Convenio-Int', 'Transferencia Obrigatoria', 
        'Acordo Cultural-PEC',  'Convenio Andifes', 'Matricula Cortesia', 'SISU',
        'Transferencia Facultativa', 'PEC-G Peppfol', 'Portador Diploma Curso Superior', 
        'Vestibular para mesmo Curso', 'PAS', 'ENEM']
    
def add_feature_sex(stu, stu_features):
    """
    append feature sex to the student feature list
    receives:
        1. a student
        2. a list containing all the student features
    returns:
        nothing 
    """
    # assert value is as expected
    assert(stu.sex in VALID_SEX_VALUES)
    if stu.sex == 'masculino':
        stu_features.append(0)
    elif stu.sex == 'feminino':
        stu_features.append(1)
    else:
        exit('error on add feature sex function')

def add_feature_age(stu, stu_features):
    """
    append feature age to the student feature list
    receives:
        1. a student
        2. a list containing all the student features
    returns:
        nothing 
    """
    # assert value is as expected
    assert(stu.age > 0 and stu.age < 100)
    stu_features.append(stu.age)

def add_feature_course(stu, stu_features):
    """
    append feature course to the student feature list
    receives:
        1. a student
        2. a list containing all the student features
    returns:
        nothing 
    """
    # use dummy list
    put_dummy_variables(stu.course, VALID_COURSE_VALUES, stu_features) 

def add_feature_local(stu, stu_features):
    """
    append feature local to the student feature list
    receives:
        1. a student
        2. a list containing all the student features
    returns:
        nothing 
    """
    # use dummy list
    put_dummy_variables(stu.local, VALID_LOCAL_VALUES, stu_features) 

def add_feature_quota(stu, stu_features):
    """
    append feature quota to the student feature list
    receives:
        1. a student
        2. a list containing all the student features
    returns:
        nothing 
    """
    # use dummy list
    put_dummy_variables(stu.quota, VALID_QUOTA_VALUES, stu_features) 

def add_feature_quota_enh(stu, stu_features):
    """
    append feature quota enhanced to the student feature list
    receives:
        1. a student
        2. a list containing all the student features
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
    put_dummy_variables(enh_quota, ENH_QUOTA_VALUES, stu_features) 

def add_feature_pass_rate(stu, stu_features, semester):
    """
    append feature pass_rate to the student feature list
    receives:
        1. a student
        2. a list containing all the student features
        3. the semester we are interested. 
    returns:
        nothing 
    """
    # if student has already graduate, put last value in the list
    if stu.get_num_semesters() < semester: 
        assert(stu.pass_rate[-1] >= -1 and stu.pass_rate[-1] <= 2)
        stu_features.append(stu.pass_rate[-1])
    else:
        assert(stu.pass_rate[semester - 1] >= -1 and stu.pass_rate[semester - 1] <= 2)
        stu_features.append(stu.pass_rate[semester - 1])

def add_feature_school_type(stu, stu_features):
    """
    append feature school_type to the student feature list
    receives:
        1. a student
        2. a list containing all the student features
    returns:
        nothing 
    """
    # use dummy list
    put_dummy_variables(stu.school_type, VALID_SCHOOL_TYPE_VALUES, stu_features) 

def add_feature_way_in_enh(stu, stu_features):
    """
    append feature way in enhance to the student feature list
    receives:
        1. a student
        2. a list containing all the student features
    returns:
        nothing 
    * function should enhance performance of model by considering a different set of
    * categories than the original
    """
    ENH_WAY_IN_VALUES = ['PAS', 'Vestibular', 'Transferencia', 'Outros']
    try:
        assert (stu.way_in in VALID_WAY_IN_VALUES)
    except:
        print(stu.way_in)
        exit()
    if stu.way_in == 'PAS':
        enh_way_in = stu.way_in
    elif stu.way_in == 'Vestibular':
        enh_way_in = stu.way_in
    elif stu.way_in in ['Transferencia Obrigatoria', 'Transferencia Facultativa']:
        enh_way_in = 'Transferencia'
    else:
        enh_way_in = 'Outros'

    # use dummy list
    put_dummy_variables(enh_way_in, ENH_WAY_IN_VALUES, stu_features) 

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
    assert (stu.way_out in WAY_OUT_CONSIDERED)
    if stu.way_out == 'Formatura':
        target_lst.append(0)
    else:
        target_lst.append(1)

def put_dummy_variables(atr_value, lst_values, stu_features):
    """
    put a given atribute as dummy variable
    receives:
        1. atribute value
        2. list of possible values for the attribute
        3. list of students variable that we must append attributes
    returns: 
        nothing
    """
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

