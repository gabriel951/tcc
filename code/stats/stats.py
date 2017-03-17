#!/usr/bin/python3.4

# file to get statistic from the database
# import basic
import sys
sys.path.append('..')
from basic import *

import psycopg2
from subprocess import call

sys.path.append('../core/')
from students_methods import *

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
         perf = '%f,%f,%f,' \
                 % (stu.fail_rate[LAST_ELEM], stu.pass_rate[LAST_ELEM],\
                         stu.drop_rate[LAST_ELEM]) 
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
    #get_graph('sex', stu_info, False, data_type = 'discrete')
    #get_graph('age', stu_info, False, data_type = 'discrete')
    #get_graph('local', stu_info, False, data_type = 'discrete')
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
    #get_graph('improvement_rate', stu_info, False, data_type = 'continuous', 
    #        index = LAST_ELEM, binwidth = 0.2)
    #get_graph('pass_rate', stu_info, True, data_type = 'continuous', index = LAST_ELEM)
    #get_graph('pass_rate', stu_info, False, data_type = 'continuous', index = LAST_ELEM)
    #get_graph('fail_rate', stu_info, True, data_type = 'continuous', index = LAST_ELEM)
    #get_graph('fail_rate', stu_info, False, data_type = 'continuous', index = LAST_ELEM)
    #get_graph('drop_rate', stu_info, True, data_type = 'continuous', index = LAST_ELEM)
    #get_graph('drop_rate', stu_info, False, data_type = 'continuous', index = LAST_ELEM)
    #get_graph('mand_rate', stu_info, data_type = 'continuous')
    #get_graph('credit_rate_acc', stu_info, False, data_type = 'continuous', index = 0, 
    #        binwidth = 2)
    #get_graph('hard_rate', stu_info, False, data_type = 'continuous', index =
    #        LAST_ELEM)
    # TODO: 
    #get_graph('in_condition', stu_info, False, data_type = 'continuous', index =
    #        LAST_ELEM)
    #get_graph('position', stu_info, False, data_type = 'discrete', index = LAST_ELEM)

def get_graph(feature, stu_info, sep_course, data_type, index = None, binwidth = 0.05):
    """
    generate a bar graph (discrete data) or a histogram graph (continuous data) for 
    the feature distribution. No separation by course
    receives:
        1. a feature name
        2. a dictionary of students. 
        3. a boolean to indicate if we need to separate the courses or not
        3. whether the datatype is discrete or continuous.
        4. (optional) an index. If passed its because the feature is a list (one for
        each semester) and its the position for the list
        5. (optional) the binwidth, case the feature is continuous 
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

        # iterate through every student - keeping record of feature value
        rows_list = []
        for key, cur_stu in stu_info.items(): 

            # it may be necessary to skip the student
            if sep_course == True and cur_stu.course != course:
                continue

            # keep record
            for attr, value in cur_stu.__dict__.items():
                if attr == feature: 
                    if index == None:
                        rows_list.append(value)
                    else:
                        rows_list.append(value[index])

        # handle feature, if necessary
        rows_list = handle_feature(stu_info, rows_list, feature)

        # write query in file, call r program to plot chart and delete
        if data_type == 'discrete':
            write_execute_delete(rows_list, r_get_bar_graph, name)
        elif data_type == 'continuous':
            write_execute_delete(rows_list, r_get_hist_graph, name, binwidth)
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
        rows_list = [row.replace('Deslig - Nao Cumpriu condicao', 'deslg') \
                for row in rows_list] 
        rows_list = [row.replace('Rep 3 vezes na mesma Disc Obrig', 'deslg') \
                for row in rows_list] 
        rows_list = [row.replace('Novo Vestibular', 'vest') \
                for row in rows_list] 
        rows_list = [row.replace('Vestibular p/outra Habilitacao', 'vest') \
                for row in rows_list] 
        rows_list = [row.replace('Desligamento Forca de Convenio', 'deslg') \
                for row in rows_list] 
        rows_list = [row.replace('Desligamento Voluntario', 'deslg') \
                for row in rows_list] 
        rows_list = [row.replace('Desligamento Falta Documentacao', 'deslg') \
                for row in rows_list] 
        rows_list = [row.replace('Desligamento Decisao Judicial', 'deslg') \
                for row in rows_list] 
        rows_list = [row.replace('Anulacao de Registro', 'null') \
                for row in rows_list] 
        rows_list = [row.replace('Ex-Aluno (Decreto 477)', 'dec') \
                for row in rows_list] 
        rows_list = [row.replace('Transferencia', 'trnsf') \
                for row in rows_list] 
        rows_list = [row.replace('Formatura', 'form') \
                for row in rows_list] 
        rows_list = [row.replace('Falecimento', 'mrr') \
                for row in rows_list] 
        return rows_list
    elif feature == 'race':
        rows_list = [row.replace('0', '000') for row in rows_list] 
        rows_list = [row.replace('nao cadastrada', '000') for row in rows_list] 
        rows_list = [row.replace('nao dispoe de informacao', '000') for row in rows_list] 
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

        rows_list = [row.replace('Convenio-Int', 'ci') \
                for row in rows_list] 
        print('substituting Convenio-Int for ci')

        rows_list = [row.replace('Transferencia Obrigatoria', 'to') \
                for row in rows_list] 
        print('substituting Transferencia Obrigatoria for to')

        rows_list = [row.replace('Acordo Cultural-PEC', 'ac') \
                for row in rows_list] 
        print('substituting Acordo Cultural-PEC for ac')

        rows_list = [row.replace('Convenio Andifes', 'ca') \
                for row in rows_list] 
        print('substituting Convenio Andifes for ca')

        rows_list = [row.replace('Matricula Cortesia', 'mc') \
                for row in rows_list] 
        print('substituting Matricula Cortesia for mc')

        rows_list = [row.replace('Transferencia Facultativa', 'tf') \
                for row in rows_list] 
        print('substituting Transferencia Facultativa for tf')

        rows_list = [row.replace('PEC-G Peppfol', 'ppp') \
                for row in rows_list] 
        print('substituting PEC-G Peppfol for ppp')

        rows_list = [row.replace('Portador Diploma Curso Superior', 'pdcs') \
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
                new_row_lst.append('nao declarado')
            else: 
                new_row_lst.append(row)
        return new_row_lst
    else:
        return rows_list

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

def write_execute_delete(rows, function, *args):
    """
    write each entry of the row on a temporary file, execute function given (for all
    courses together or for each of them separately) and delete the temporary file
    receives:
        1. a row
        2. function to execute 
        3. additional arguments to the function
    returns: 
        nothing
    """
    # write to temp file
    with open('temp.txt', 'w') as temp_file:
        for row in rows:
            temp_file.write(str(row))
            temp_file.write(",\n")

    # execute function
    function(*args)

    # exclude temp file - useful as log
    #call('rm temp.txt', shell = True)

if __name__ == "__main__":
    generate_graphs()
    #apply_kendall()
    #study_attr()
    #study_train_test_division()
