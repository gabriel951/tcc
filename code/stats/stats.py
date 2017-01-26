#!/usr/bin/python3.4

# file to get statistic from the database
# import basic
import sys
sys.path.append('..')
from basic import *

import psycopg2
from subprocess import call

sys.path.append('../core/')
from students import *

# generate graphs for the database
def generate_graphs():
    """
    generate the graphs for the primitive and derived attributes
    """
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
    #get_graph('ira', stu_info, data_type = 'continuous')
    get_graph('improvement_rate', stu_info, data_type = 'continuous')
    #get_graph('pass_rate', stu_info, data_type = 'continuous')
    #get_graph('fail_rate', stu_info, data_type = 'continuous')
    #get_graph('drop_rate', stu_info, data_type = 'continuous')
    #get_graph('mand_rate', stu_info, data_type = 'continuous')

def get_graph(feature, stu_info, data_type = 'discrete'):
    """
    receives a feature name and a dictionary of students. 
    Optionally receives whether the datatype is discrete or continuous.
    generate a bar graph (discrete data) or a histogram graph (continuous data) for 
    the feature distribution
    """
    print('getting graph for feature %s' % (feature))
    rows_list = []

    # iterate through every student
    for key in stu_info: 
        cur_stu = stu_info[key]
        # iterate through the students attributes, printing them
        for attr, value in cur_stu.__dict__.items():
            if attr == feature: 
                rows_list.append(value)

    # handle feature, if necessary
    rows_list = handle_feature(stu_info, rows_list, feature)

    # handle feature, case feature is grade
    if feature == 'grades':
        rows_list = handle_grade(stu_info)

    # write query in file, call r program to plot pie chart and delete
    if data_type == 'discrete':
        write_execute_delete(rows_list, r_get_bar_graph, feature)
    elif data_type == 'continuous':
        write_execute_delete(rows_list, r_get_hist_graph, feature)
    else:
        exit("misinformed value")

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
