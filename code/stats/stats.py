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
    #     perf = '%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t' \
    #             % (stu.ira, stu.improvement_rate, stu.fail_rate, stu.pass_rate, \
    #             stu.drop_rate, stu.credit_rate, stu.mand_credit_rate, stu.hard_rate, \
    #                stu.in_condition, stu.position)
         way_out = '%s\n' % (stu.way_out)
        
         #fp.write(social + perf + way_out)
         # TODO: code above should be the one
         fp.write(social + way_out)

    fp.close()

    # apply kendal tao test 
    call("Rscript kendall.r " + FILE_NAME, shell = True)

def generate_graphs():
    """
    generate the graphs for the primitive and derived attributes
    """
    # avoid magic number - last element on a list
    LAST_ELEM = -1

    # load student info
    stu_info = load_students(NAME_STU_STRUCTURE, path = '../core/data/')

    ## primitive features
    #get_graph('sex', stu_info)
    #get_graph('age', stu_info)
    #get_graph('local', stu_info)
    #get_graph('quota', stu_info)
    #get_graph('school_type', stu_info)
    #get_graph('race', stu_info)
    #get_graph('course', stu_info)
    #get_graph('way_in', stu_info)
    #get_graph('grades', stu_info)
    #get_graph('way_out', stu_info)

    ## derived features
    #get_graph('ira', stu_info, True, data_type = 'continuous')
    #get_graph('improvement_rate', stu_info, data_type = 'continuous')
    #get_graph('pass_rate', stu_info, True, data_type = 'continuous', index = LAST_ELEM)
    get_graph('pass_rate', stu_info, False, data_type = 'continuous', index = LAST_ELEM)
    #get_graph('fail_rate', stu_info, True, data_type = 'continuous', index = LAST_ELEM)
    ##get_graph('fail_rate', stu_info, False, data_type = 'continuous', index = LAST_ELEM)
    #get_graph('drop_rate', stu_info, True, data_type = 'continuous', index = LAST_ELEM)
    #get_graph('drop_rate', stu_info, False, data_type = 'continuous', index = LAST_ELEM)
    #get_graph('mand_rate', stu_info, data_type = 'continuous')

def get_graph(feature, stu_info, sep_course, data_type = 'discrete', index = None):
    """
    generate a bar graph (discrete data) or a histogram graph (continuous data) for 
    the feature distribution. No separation by course
    receives:
        1. a feature name
        2. a dictionary of students. 
        3. a boolean to indicate if we need to separate the courses or not
        3. (optional) whether the datatype is discrete or continuous.
        4. (optional) an index. If passed its because the feature is a list (one for
        each semester) and its the position for the list
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
            write_execute_delete(rows_list, r_get_hist_graph, name)
        else:
            exit("misinformed value")

        # if we don't want to separate course, end function
        if sep_course == False: 
            return

def handle_feature(stu_info, rows_list, feature):
    """
    if the data of a given feature need to be shortened, this function
    does that, according to the feature
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

def r_get_hist_graph(name):
    """
    call r program to plot a histogram graph
    receives: 
        1. the name for the graph
    returns: 
        nothing
    """
    call("Rscript stats_hist_graph.r", shell = True)
    call("mv temp.png " + name, shell = True)

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

generate_graphs()

#apply_kendall()
