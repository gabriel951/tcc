#!/usr/bin/python3.4

# file to get statistic from the database
import itertools
import math
import pandas

# import basic
import sys
sys.path.append('..')
from basic import *

import psycopg2
from subprocess import call

sys.path.append('../core/')
from students_methods import *

# TODO: eliminate local attribute from the analysis

def apply_kendall():
    """
    apply the kendall test for all the students we got 
    receives: 
        nothing
    returns: 
        nothing
    """
    # file pointer
    FILE_NAME = '../logs/kendall.txt'
    fp = open(FILE_NAME, 'w')

    # load student info 
    stu_info = load_students(NAME_STU_STRUCTURE, path = '../core/data/')

    # write student info
    for key, stu in stu_info.items():
         social = '%d,%s,%d,%s,%s,%s,%s,%s,' \
                 % (stu.reg, stu.sex, stu.age, stu.quota, stu.school_type, \
                 stu.course, stu.local, stu.way_in)
         perf = '%f,%f,%f,%f,%f,%f,%f,%f,%f,' \
             % (stu.fail_rate[LAST_ELEM], stu.pass_rate[LAST_ELEM],\
                 stu.drop_rate[LAST_ELEM], stu.ira[LAST_ELEM], \
                 stu.improvement_rate[LAST_ELEM], stu.credit_rate_acc[LAST_ELEM], \
                 stu.hard_rate[LAST_ELEM], stu.in_condition[LAST_ELEM], \
                 stu.position[LAST_ELEM]) 

         way_out = '%s\n' % (stu.way_out)
        
         fp.write(social + perf + way_out)

    fp.close()

    # apply kendal tao test 
    call("Rscript kendall.r " + FILE_NAME, shell = True)

def generate_graphs():
    """
    generate the graphs for the primitive and derived attributes
    saves the graph as .png files in the folder we are in
    receives: 
        nothing
    returns: 
        nothing
    """

    # load student info
    stu_info = load_students(NAME_STU_STRUCTURE, path = '../core/data/')

    ## primitive features
    #TODO: deprecated! 
    #get_graph('local', stu_info, False, data_type = 'discrete')
    #get_graph('sex', stu_info, False, data_type = 'discrete')
    #get_graph('age', stu_info, False, data_type = 'discrete')
    #get_graph('quota', stu_info, False, data_type = 'discrete')
    #get_graph('school_type', stu_info, False, data_type = 'discrete')
    #get_graph('course', stu_info, False, data_type = 'discrete')
    #get_graph('race', stu_info, False, data_type = 'discrete')
    #get_graph('way_in', stu_info, False, data_type = 'discrete')
    #get_graph('way_out', stu_info, False, data_type = 'discrete')
    #get_graph('grades', stu_info, False, data_type = 'discrete')

    ## derived features
    #get_graph('ira', stu_info, False, data_type = 'continuous', index = LAST_ELEM, 
    #        binwidth = 0.2)
    get_graph('improvement_rate', stu_info, False, data_type = 'continuous', 
            index = LAST_ELEM, binwidth = 0.2)
    #get_graph('pass_rate', stu_info, True, data_type = 'continuous', index = LAST_ELEM)
    #get_graph('pass_rate', stu_info, False, data_type = 'continuous', index = LAST_ELEM)
    #get_graph('fail_rate', stu_info, True, data_type = 'continuous', index = LAST_ELEM)
    #get_graph('fail_rate', stu_info, False, data_type = 'continuous', index = LAST_ELEM)
    #get_graph('drop_rate', stu_info, True, data_type = 'continuous', index = LAST_ELEM)
    #get_graph('drop_rate', stu_info, False, data_type = 'continuous', index = LAST_ELEM)
    #get_graph('credit_rate_acc', stu_info, False, data_type = 'continuous', index = 0, 
    #        binwidth = 2)
    #get_graph('hard_rate', stu_info, False, data_type = 'continuous', index =
    #        LAST_ELEM)
    # TODO: 
    #get_graph('in_condition', stu_info, False, data_type = 'discrete', index =
    #        LAST_ELEM)
    #get_graph('in_condition', stu_info, True, data_type = 'discrete', index =
    #        LAST_ELEM)
    get_graph('position', stu_info, False, data_type = 'discrete', index = LAST_ELEM)

def get_coef_cor():
    """
    get the coefficient of correlation for the relevant atributes
    * print info 
    receives: 
        nothing
    returns: 
        nothing
    """
    # load student info
    stu_info = load_students(NAME_STU_STRUCTURE, path = '../core/data/')

    # features that we decided not to include
    # get_coef_cor_atr('local', stu_info, False)
    # get_coef_cor_atr('race', stu_info, False)

    # primitive features
    get_coef_cor_atr('sex', stu_info, False)
    get_coef_cor_atr('age', stu_info, False)
    get_coef_cor_atr('quota', stu_info, False)
    get_coef_cor_atr('school_type', stu_info, False)
    get_coef_cor_atr('course', stu_info, False)
    get_coef_cor_atr('way_in', stu_info, False)
    get_coef_cor_atr('way_out', stu_info, False)

    get_coef_cor_atr('ira', stu_info, False, index = LAST_ELEM)
    get_coef_cor_atr('improvement_rate', stu_info, False, index = LAST_ELEM)
    get_coef_cor_atr('pass_rate', stu_info, False, index = LAST_ELEM)
    get_coef_cor_atr('fail_rate', stu_info, False, index = LAST_ELEM)
    get_coef_cor_atr('drop_rate', stu_info, False, index = LAST_ELEM)
    get_coef_cor_atr('credit_rate_acc', stu_info, False, index = LAST_ELEM)
    get_coef_cor_atr('hard_rate', stu_info, False, index = LAST_ELEM)
    get_coef_cor_atr('in_condition', stu_info, False, index = LAST_ELEM)
    get_coef_cor_atr('position', stu_info, False, index = LAST_ELEM)

def get_coef_cor_atr(feature, stu_info, sep_course, index = None):
    """
    get the coefficient of correlation for a given feature, 
    print it on the screen 
    receives:
        1. feature name
        2. dictionary containing student information
        3. boolean to indicate if we should separate courses
        4. Index (optional): if the feature is in a list, the index that we are
        considering. Else, leave it None
    returns: 
        nothing
    """
    assert (sep_course == True or sep_course == False)

    # iterate through every course of interest
    for course in COURSES_OFF_NAME:
        # show course being analysed
        if sep_course == True: 
            print('feature %s and course: %s.' % (feature, course))
        else:
            print('feature %s, all courses.' % (feature))

        # get feature values
        (atr_values, way_out) = get_feature_val(feature, \
                stu_info, sep_course, index, course = course)

        # write query in file, call r program to plot chart 
        write_execute(atr_values, way_out, r_get_coef_cor)

        # if we don't want to separate course, end function
        if sep_course == False: 
            return
    
def get_contigency_table():
    """
    get contingency table for the atributes
    receives: 
        nothing
    returns: 
        nothing
    """
    # load student information
    stu_info = load_students(NAME_STU_STRUCTURE, path = '../core/data/')
    
    # get crosstab for the age
    sep_course = False
    index = None
    (age, way_out) = get_feature_val('age', stu_info, sep_course, index, course =
    'all')
    age_table = pandas.crosstab([age], [way_out], rownames = ['age'], 
            colnames = ['way_out'], margins = True)
    print(age_table)
    #percentage_age_table = age_table.apply(lambda x: x/x.sum(), axis = 1)
    #print(percentage_age_table)

    # get crosstab for the course
    #sep_course = False
    #index = None
    #(course, way_out) = get_feature_val('course', stu_info, sep_course, index, course =
    #'all')
    #course_table = pandas.crosstab([course], [way_out], rownames = ['course'], 
    #        colnames = ['way_out'], margins = True)
    #print(course_table)
    

def get_feature_val(feature, stu_info, sep_course, index, course = 'all'):
    """
    get a list of the feature value we are interested and the way out
    receives:
        1. feature name 
        2. dictionary containing student info
        3. boolean to indicate if we should separate course
        4. index, case we are talking about 
    returns: 
        tuple of lists: (<atr_value_lst, way_out_lst>
    """
    # iterate through every student - keeping record of atribute value and way
    # out
    atr_values = []
    way_out = []
    for key, cur_stu in stu_info.items(): 

        # it may be necessary to skip the student
        if sep_course == True and cur_stu.course != course:
            continue

        # keep record
        for attr, value in cur_stu.__dict__.items():
            if attr == feature: 
                if index == None:
                    atr_values.append(value)
                else:
                    atr_values.append(value[index])

        way_out.append(cur_stu.way_out)

    # handle feature, if necessary
    atr_values = handle_feature(stu_info, atr_values, feature)
    way_out = handle_target(way_out)
    
    # pathological atributes that don't have the way out list with the same size
    # of the atribute list are handled below
    exceptions = ['grades']
    if feature in exceptions: 
        print('way out list will be incorrect, but its not needed for the feature')
        way_out = atr_values[:]

    # return correct value
    return (atr_values, way_out)

def get_graph(feature, stu_info, sep_course, data_type, index = None, binwidth =
        0.05):
    """
    generate a bar graph (discrete data) or a histogram graph (continuous data) for 
    the feature distribution. No separation by course
    receives:
        1. a feature name
        2. a dictionary of students. 
        3. a boolean to indicate if we need to separate the courses or not
        4. whether the datatype is discrete or continuous.
        5. (optional) an index. If passed its because the feature is a list (one for
        each semester) and its the position for the list
        6. (optional) the binwidth, case the feature is continuous 
    returns: 
        nothing
    """
    assert (sep_course == True or sep_course == False)

    # iterate through every course of interest
    for course in COURSES_OFF_NAME:
        # inform user whats going on and set name of graph
        if sep_course == False:
            print('getting graph for feature %s' % (feature))
            name = feature + '.png'
        else:
            print('getting graph for feature %s and course %s' % (feature, course))
            name = feature + '_' + course + '.png'

        # get feature values
        (atr_values, way_out) = get_feature_val(feature, \
                stu_info, sep_course, index, course = course)

        # write query in file, call r program to plot chart 
        if data_type == 'discrete':
            write_execute(atr_values, way_out, r_get_bar_graph, name)
        elif data_type == 'continuous':
            write_execute(atr_values, way_out, r_get_hist_graph, name, binwidth)
        else:
            exit("misinformed value")

        # if we don't want to separate course, end function
        if sep_course == False: 
            return

def handle_feature(stu_info, rows_list, feature):
    """
    if the data of a given feature need to be shortened, this function
    does that, according to the feature
    receives: 
        1. dictionary containing all student information
        2. list containing the data that may need to be shortened
        3. feature name we are interested
    returns: 
        1. the row list, with information shortened
    """
    if feature == 'quota':
        rows_list = [row.replace('escola publica alta renda-ppi', 'p_alta_ppi') \
                for row in rows_list] 
        rows_list = [row.replace('escola publica baixa renda-ppi', 'p_baixa_ppi') \
                for row in rows_list] 
        rows_list = [row.replace('escola publica alta renda-nao ppi', 'p_alta_nppi') \
                for row in rows_list] 
        rows_list = [row.replace('escola publica baixa renda-nao ppi', 'p_baixa_nppi') \
                for row in rows_list] 
        return rows_list
    elif feature == 'sex':
        rows_list = [row.replace('m', 'masculino') for row in rows_list]
        rows_list = [row.replace('f', 'feminino') for row in rows_list]
        return rows_list
    elif feature == 'way_out':
        rows_list = [row.replace('Desligamento - Abandono', 'deslg') \
                for row in rows_list] 
        rows_list = [row.replace('Mudança de Curso', 'mdc') \
                for row in rows_list] 
        rows_list = [row.replace('Mudança de Turno', 'mdt') \
                for row in rows_list] 
        rows_list = [row.replace('Deslig - não cumpriu condição', 'deslg') \
                for row in rows_list] 
        rows_list = [row.replace('Repr 3 vezes na mesma disc obr', 'deslg') \
                for row in rows_list] 
        rows_list = [row.replace('Novo Vestibular', 'vest') \
                for row in rows_list] 
        rows_list = [row.replace('Vestibular p/outra Habilitação', 'vest') \
                for row in rows_list] 
        rows_list = [row.replace('Desligamento-Força de Convênio', 'deslg') \
                for row in rows_list] 
        rows_list = [row.replace('Desligamento Voluntário', 'deslg') \
                for row in rows_list] 
        rows_list = [row.replace('Desligamento Falt Documentação', 'deslg') \
                for row in rows_list] 
        rows_list = [row.replace('Desligamento Decisão  Judicial', 'deslg') \
                for row in rows_list] 
        rows_list = [row.replace('Desligamento Jubilamento', 'deslg') \
                for row in rows_list] 
        rows_list = [row.replace('Desligamento por Força de Intercãmbio', 'deslg') \
                for row in rows_list] 
        rows_list = [row.replace('Anulação de Registro', 'null') \
                for row in rows_list] 
        rows_list = [row.replace('Ex-Aluno (Decreto 477)', 'dec') \
                for row in rows_list] 
        rows_list = [row.replace('Transferência', 'trnsf') \
                for row in rows_list] 
        rows_list = [row.replace('Formatura', 'form') \
                for row in rows_list] 
        rows_list = [row.replace('Falecimento', 'mrr') \
                for row in rows_list] 
        return rows_list
    elif feature == 'race':
        rows_list = [row.replace('0', '000') for row in rows_list] 
        rows_list = [row.replace('não cadastrada', '000') for row in rows_list] 
        rows_list = [row.replace('não dispõe da informação', '000') for row in rows_list] 
        rows_list = [row.replace('não informado', '000') for row in rows_list] 
        rows_list = [row.replace('000000000', '000') for row in rows_list] 
        rows_list = [row.replace('000', 'indisponivel') for row in rows_list] 
        return rows_list
    elif feature == 'course':
        rows_list = [row.replace(CIC_BACHELOR, 'cic_b') \
                for row in rows_list] 
        rows_list = [row.replace(CIC_NON_BACHELOR, 'cic_lic') \
                for row in rows_list] 
        rows_list = [row.replace(COMPUTER_ENGINEERING, 'eng_comp') \
                for row in rows_list] 
        rows_list = [row.replace(MECHATRONICS_ENGINEERING, 'eng_mec') \
                for row in rows_list] 
        rows_list = [row.replace(NETWORK_ENGINEERING, 'eng_redes') \
                for row in rows_list] 
        rows_list = [row.replace(SOFTWARE_ENGINEERING, 'eng_softw') \
                for row in rows_list] 
        return rows_list
    elif feature == 'way_in':
        rows_list = [row.replace('Vestibular', 'vest') \
                for row in rows_list] 
        print('substituting Vestibular for vest')

        rows_list = [row.replace('Convênio-Int', 'ci') \
                for row in rows_list] 
        print('substituting Convenio-Int for ci')

        rows_list = [row.replace('Transferência Obrigatória', 'to') \
                for row in rows_list] 
        print('substituting Transferencia Obrigatoria for to')

        rows_list = [row.replace('Acordo Cultural-PEC-G', 'ac') \
                for row in rows_list] 
        print('substituting Acordo Cultural-PEC for ac')

        rows_list = [row.replace('Sisu-Sistema de Seleção Unificada', 'sisu') \
                for row in rows_list] 
        print('substituting Sisu-Sistema de Seleção Unificada for sisu')

        rows_list = [row.replace('Programa de Avaliação Seriada', 'PAS') \
                for row in rows_list] 
        print('substituting Programa de Avaliação Seriada for PAS')

        rows_list = [row.replace('Convênio - Andifes', 'ca') \
                for row in rows_list] 
        print('substituting Convenio Andifes for ca')

        rows_list = [row.replace('Matrícula Cortesia', 'mc') \
                for row in rows_list] 
        print('substituting Matricula Cortesia for mc')

        rows_list = [row.replace('Transferência Facultativa', 'tf') \
                for row in rows_list] 
        print('substituting Transferencia Facultativa for tf')

        rows_list = [row.replace('PEC-Peppfol-Graduação', 'ppp') \
                for row in rows_list] 
        print('substituting PEC-G Peppfol for ppp')

        rows_list = [row.replace('Portador Diplom Curso Superior', 'pdcs') \
                for row in rows_list] 
        print('substituting Portador Diploma Curso Superior for pdcs')
        
        rows_list = [row.replace('vest para mesmo Curso', 'vmc') \
                for row in rows_list] 
        print('substituting vest para mesmo Curso for vmc')
        
        return rows_list
    elif feature == 'grades':
        rows_list = handle_grade(stu_info)
        return rows_list
    elif feature == 'school_type':
        new_row_lst = []
        for row in rows_list:
            if row == '':
                new_row_lst.append('nao_declarado')
            else: 
                new_row_lst.append(row)
        new_row_lst = [row.replace('não informada', 'nao_informada') 
                for row in new_row_lst]
        return new_row_lst
    elif feature == 'in_condition':
        new_row_lst = []
        for row in rows_list: 
            if row == 0: 
                new_row_lst.append('nao_condicao')
            elif row in [1, 2, 3]:
                new_row_lst.append('condicao')
            else:
                exit('error')
        return new_row_lst
    else:
        return rows_list

def handle_target(way_out):
    """
    the way out target variable that we want to predict is put in correct form for
    the graph. That's a binary form, that says if a student has graduated or has
    evaded
    receives: 
        1. the way out list
    returns: 
        way out list modified
    """
    new_way_out = []
    for elem in way_out: 
        assert (elem in WAY_OUT_CONSIDERED)
        if elem.lower() == 'formatura':
            new_way_out.append(elem.lower())
        else: 
            new_way_out.append('desligamento')

    return new_way_out

def handle_grade(stu_info):
    """
    receives a student dictionary
    returns a list contaning all the grades of all the students
    """
    print('handling grade situation')
    rows_list = []

    for (key_stu, stu) in stu_info.items():
        grades = stu.grades
        for (key_grades, data_lst) in grades.items():
            for pos in range(len(data_lst)): 
                grade = stu.get_sub_info(key_grades, pos, 'grade')
                rows_list.append(grade)

    return rows_list

def record_stats_atr(stu_info, atr):
    """
    put in student attribute dictionary statistics related to a given attribute
    receives:
        1. student dictionary
        2. atribute name 
    returns:
        nothing
    """
    print('starting analysis for attribute %s' % (atr))
    NUM_STU_IND = 0
    NUM_TRA_IND = 1
    NUM_TEST_IND = 2
    GRA_STU_IND = 3

    # empty dictionary
    atr_info = {}

    # iterate through each student 
    for key, stu in stu_info.items():

        # find attribute we care about 
        for stu_atr_name, stu_atr_value in stu.__dict__.items():
            if stu_atr_name != atr:
                continue
            
            # if the attribute is not on dictionary, add it
            if not (stu_atr_value in atr_info):
                atr_info[stu_atr_value] = [0, 0, 0, 0]


            # update the count
            data = atr_info[stu_atr_value]
            data[NUM_STU_IND] = data[NUM_STU_IND] + 1
            if stu.year_in < YEAR_START_TRA or stu.year_in > YEAR_END_TRA:
                data[NUM_TRA_IND] = data[NUM_TRA_IND] + 1
            if stu.year_in < YEAR_START_TEST or stu.year_in > YEAR_END_TEST:
                data[NUM_TEST_IND] = data[NUM_TEST_IND] + 1
            if stu.way_out == 'Formatura':
                data[GRA_STU_IND] = data[GRA_STU_IND] + 1

            # since we found attribute, no reason to keep on loop
            break
    
    return atr_info

def r_get_bar_graph(name):
    """
    call r program to plot a bar graph
    receives: 
        1. the name for the graph
    returns:
        nothing
    """
    call("Rscript stats_bar_graph.r", shell = True)
    call("mv temp.png " + name, shell = True)

def r_get_coef_cor():
    """
    call R program that calculates the coefficient of correlation
    receives: 
        nothing
    returns: 
        nothing
    """
    call("Rscript r_get_coef_cor.r", shell = True)

def r_get_hist_graph(name, binwidth):
    """
    call r program to plot a histogram graph
    receives: 
        1. the name for the graph
        2. the binwidth for the histogram graph
    returns: 
        nothing
    """
    call("Rscript stats_hist_graph.r " + str(binwidth), shell = True)
    call("mv temp.png " + name, shell = True)

def study_attr():
    """
    divides each student according to some atributes of interest. 
    for each atribute there will be some categories. For each category, print the
    amount of students in each, how many of them were able to graduate and the
    percentage this represents
    * attributes analysed: 
        1. quota
        2. way_in
    receives:
        nothing
    returns: 
        nothing
    """
    # load student dictionary
    stu_info = load_students(NAME_STU_STRUCTURE, path = '../core/data/')

    # attributes that we'll be analysed
    analysed_attributes = ['way_in', 'quota']

    # dictionary containing info for attribute being analysed- initially empty
    # key: way in 
    # value: list [<num_students>, <num_students on training sample>, 
    #               <num_students_test_sample>, <num_students_able_graduate>]
    NUM_STU_IND = 0
    NUM_TRA_IND = 1
    NUM_TEST_IND = 2
    GRA_STU_IND = 3

    # iterate through attributes
    for cur_atr in analysed_attributes: 
        atr_info = record_stats_atr(stu_info, cur_atr)
        show_stats_atr(stu_info, cur_atr, atr_info)

def show_stats_atr(stu_info, atr, atr_info):
    """
    print stats related to a given student attribute
    receives:
        1. student dictionary
        2. atribute name 
        3. atribute dictionary, where stats will be saved
    returns:
        nothing
    """
    NUM_STU_IND = 0
    NUM_TRA_IND = 1
    NUM_TEST_IND = 2
    GRA_STU_IND = 3

    for atr_name, data in atr_info.items():
        print('information regarding atribute: %s' % (atr_name))
        print('\t amount of students: %d' % (data[NUM_STU_IND]))
        print('\t amount of students in training: %d' % (data[NUM_TRA_IND]))
        print('\t amount of students in test: %d' % (data[NUM_TEST_IND]))
        print('\t amount of students able to graduate: %d' % (data[GRA_STU_IND]))

        percentage = float(data[GRA_STU_IND]) / data[NUM_STU_IND]
        print('\t percentage: %f' % (percentage))

def study_dist_dpf_rate():
    """
    study the distribution for the drop/pass/fail rate
    receives: 
        1. nothing
    returns: 
        nothing
    """
    # load student dictionary 
    stu_info = load_students(NAME_STU_STRUCTURE, path = '../core/data/')

    # index in which we'll consider the student variables
    index = LAST_ELEM

    # min, max value for feature, spacing and size of list of occurrences
    min_value = 0
    max_value = 1
    spacing = 0.1
    occur_lst = list(itertools.repeat(0, int(max_value/spacing)))
    print(int(max_value/spacing))

    # get dictionary in which we'll count occurrences
    # the key from the dictionary is a tuple (<drop/pass/fail>, <course_name>)
    # the value is a list of occurrences
    occur = {}
    rates = ['drop', 'pass', 'fail']
    courses_lst = COURSES_OFF_NAME[:]
    courses_lst.append('all_courses')
    for tup in itertools.product(rates, courses_lst):
        occur[tup] = occur_lst[:]

    # iterate through student filling info
    for key, stu in stu_info.items():
        # add info correctly to the course
        # the try except handle the only potential problem of a value of 1, which
        # we'll cause an Index Error

        # drop
        try:
            occur[('drop', stu.course)][int(stu.drop_rate[index]/spacing)] += 1
            occur[('drop', 'all_courses')][int(stu.drop_rate[index]/spacing)] += 1
        except IndexError: 
            occur[('drop', stu.course)][LAST_ELEM] += 1
            occur[('drop', 'all_courses')][LAST_ELEM] += 1
        
        # pass 
        try: 
            occur[('pass', stu.course)][int(stu.pass_rate[index]/spacing)] += 1
            occur[('pass', 'all_courses')][int(stu.pass_rate[index]/spacing)] += 1
        except IndexError: 
            occur[('pass', stu.course)][LAST_ELEM] += 1
            occur[('pass', 'all_courses')][LAST_ELEM] += 1

        # fail
        try: 
            occur[('fail', stu.course)][int(stu.fail_rate[index]/spacing)] += 1
            occur[('fail', 'all_courses')][int(stu.fail_rate[index]/spacing)] += 1
        except IndexError: 
            occur[('fail', stu.course)][LAST_ELEM] += 1
            occur[('fail', 'all_courses')][LAST_ELEM] += 1

    # print all info
    for tup in itertools.product(rates, courses_lst):
        print('\nstarting printing info for tup:   ' + str(tup))

        # print amount
        total = 0.0
        for elem in occur[tup]: 
            print('%d   ' % (elem), end='')
            total += elem
        print('total: %d\n' % (total), end = '')

        # print percentage
        for elem in occur[tup]:
            print('%f   ' % (elem/total), end='')
        print('')

def study_train_test_division():
    """
    shows the proportion of students in each category (train vs test)
    according to the year we decide to split.
    receives: 
        nothing
    returns:
        nothing
    """
    # load students
    stu_info = load_students(NAME_STU_STRUCTURE, path = '../core/data/')

    # iterate through years
    for year_split in range(YEAR_START, YEAR_END):
        print('\n\nstarting analysis for year split: %d' % (year_split))
        print('this means the last year for training was: %d' % (year_split))

        # analyse ratio of train and test and number of approvations in each
        train_inst = 0
        train_grad_stu = 0
        train_drop_stu = 0
        test_inst = 0
        test_grad_stu = 0
        test_drop_stu = 0
        for key, stu in stu_info.items():
            if stu.year_in <= year_split:
                train_inst += 1
                if 'Formatura' in stu.way_out:
                   train_grad_stu += 1 
                else:
                    train_drop_stu += 1
            else:
                test_inst += 1
                if 'Formatura' in stu.way_out:
                   test_grad_stu += 1 
                else:
                    test_drop_stu += 1

        print('training instances: %d' % (train_inst))
        print('test instances: %d' % (test_inst))
        ratio = train_inst / float(train_inst + test_inst)
        print('train ratio: %f' % (ratio))

        scs_rate_train = train_grad_stu / float(train_grad_stu + train_drop_stu)
        print('students able to graduate on training set: %f' % (scs_rate_train))

        scs_rate_test = test_grad_stu / float(test_grad_stu + test_drop_stu)
        print('students able to graduate on test set: %f' % (scs_rate_test))
        
def write_execute(feat_lst, target_lst, function, *args):
    """
    write each entry of the row on a temporary file, execute function given (for all
    courses together or for each of them separately) and delete the temporary file
    receives:
        1. a list containing the feature list we are analysing
        2. 
        2. function to execute 
        3. additional arguments to the function
    returns: 
        nothing
    """
    assert (len(feat_lst) == len(target_lst))

    # write to stats file
    with open('stats.txt', 'w') as temp_file:
        for i in range(len(feat_lst)):
            temp_file.write(str(feat_lst[i]))
            temp_file.write("     ")
            temp_file.write(str(target_lst[i]))
            temp_file.write("\n")

    # execute function
    function(*args)


if __name__ == "__main__":

    # histograms
    #generate_graphs()

    # contingency table 
    #get_contigency_table()

    # kendall and coefficient of correlation
    apply_kendall()
    #get_coef_cor()

    # particular atributes
    #study_attr()
    #study_dist_dpf_rate()

    # train and test division
    #study_train_test_division()

