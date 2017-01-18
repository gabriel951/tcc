#!/usr/bin/python3.4

# file to get statistic from the database
# import basic
import sys
sys.path.append('..')
from basic import *

import psycopg2
from subprocess import call

sys.path.append('../students/')
from students import *

# generate graphs for the database
def generate_graphs():
    """
    generate the graphs for the primitive and derived attributes
    """
    # load student info
    stu_info = load_students(NAME_STU_STRUCTURE, path = '../students/data/')

    ## students
    #get_graph('sex', stu_info)
    #get_graph('age')

    #get_graph('student', 'age', student_restriction)
    #get_graph('student', 'local', student_restriction)
    #get_graph('student', 'school_type', student_restriction)
    #get_graph('student', 'quota', student_restriction)
    #get_graph('student', 'race', student_restriction)
    #get_graph('student', 'course', student_restriction)
    #get_graph('student', 'way_out', student_restriction)
    #get_graph('ira', stu_info, data_type = 'continuous')

    #get_graph('pass_rate', stu_info, 'continuous')
    #get_graph('fail_rate', stu_info, 'continuous')
    get_graph('drop_rate', stu_info, 'continuous')

    # subject grades
    #get_graph('student_subject', 'grade')

def get_graph(feature, stu_info, data_type = 'discrete'):
    """
    receives a feature name and a dictionary of students. 
    Optionally receives whether the datatype is discrete or continuous.
    generate a bar graph (discrete data) or a histogram graph (continuous data) for 
    the feature distribution
    """
    rows_list = []

    # iterate through every student
    for key in stu_info: 
        cur_stu = stu_info[key]
        # iterate through the students attributes, printing them
        for attr, value in cur_stu.__dict__.items():
            if attr == feature: 
                rows_list.append(value)

    # handle feature, if necessary
    rows_list = handle_feature(rows_list, feature)

    # write query in file, call r program to plot pie chart and delete
    if data_type == 'discrete':
        write_execute_delete(rows_list, r_get_bar_graph, feature)
    elif data_type == 'continuous':
        write_execute_delete(rows_list, r_get_hist_graph, feature)
    else:
        exit("misinformed value")

def handle_feature(rows_list, feature):
    """
    if the data of a given feature need to be shortened, this function
    does that
    """
    if feature == 'quota':
        rows_list = [row.replace('escola publica alta renda-ppi', 'pub_alta_ppi') \
                for row in rows_list] 
        rows_list = [row.replace('escola publica baixa renda-ppi', 'pub_baixa_ppi') \
                for row in rows_list] 
        rows_list = [row.replace('escola publica alta renda-nao ppi', 'pub_alta_n_ppi') \
                for row in rows_list] 
        rows_list = [row.replace('escola publica baixa renda-nao ppi', 'pub_baixa_n_ppi') \
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
    else:
        return rows_list

def r_get_bar_graph(feature):
    """
    call r program to plot a bar graph
    """
    call("Rscript stats_bar_graph.r", shell = True)
    call("mv temp.png " + feature + ".png", shell = True)

def r_get_hist_graph(feature):
    """
    call r program to plot a bar graph
    """
    call("Rscript stats_hist_graph.r", shell = True)
    call("mv temp.png " + feature + ".png", shell = True)

def write_execute_delete(rows, function, *args):
    """
    receives a row, function to execute and arguments to the function
    write each entry of the row on a temporary file, execute function given and delete
    the temporary file
    """
    # write to temp file
    with open('temp.txt', 'w') as temp_file:
        for row in rows:
            temp_file.write(str(row))
            temp_file.write(",\n")

    # execute function
    function(*args)

    # exclude temp file
    #call('rm temp.txt', shell = True)

generate_graphs()
