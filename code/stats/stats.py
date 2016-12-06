#!/usr/bin/python3.4

# file to get statistic from the database
# import basic
import sys
sys.path.append('..')
from basic import *

import psycopg2
from subprocess import call

# generate graphs for the database
def generate_graphs():
    """
    generate the database graphs
    """
    # student restriction
    (year_start, year_end) = get_mode_year('all')
    student_restriction = 'where year_in >= %d and year_in <= %d' \
            % (year_start, year_end)

    ## students
    get_graph('student', 'sex', student_restriction)
    get_graph('student', 'age', student_restriction)
    get_graph('student', 'local', student_restriction)
    get_graph('student', 'school_type', student_restriction)
    get_graph('student', 'quota', student_restriction)
    get_graph('student', 'race', student_restriction)
    get_graph('student', 'course', student_restriction)
    get_graph('student', 'way_out', student_restriction)

    # subject example
    get_graph('student_subject', 'grade')

def get_graph(table, column, restriction = '', data_type = 'discrete'):
    """
    receives a table name, a column name, a restriction, a mode name, 
    whether the data is discrete or continuous.
    generate a bar graph (discrete data) or a histogram graph (continuous data) for a
    given table with a given column.
    a restriction can be appended to the query
    """
    # query database
    query = "select %s from %s.%s " % (column, MY_DATABASE, table) \
                + restriction

    print(query)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    
    # convert from list of tuples to list of strings
    rows_list = []
    for row in rows:
        rows_list.append(row[0])
    
    # handle column, if necessary
    rows_list = handle_column(rows_list, column)

    # write query in file, call r program to plot pie chart and delete
    if data_type == 'discrete':
        write_execute_delete(rows_list, r_get_bar_graph, column)
    elif data_type == 'continuous':
        write_execute_delete(rows_list, r_get_hist_graph, column)
    else:
        exit("misinformed value")

def handle_column(rows_list, column):
    """
    if the data of a given column need to be shortened, this function
    does that
    """
    if column == 'quota':
        rows_list = [row.replace('escola publica alta renda-ppi', 'pub_alta_ppi') \
                for row in rows_list] 
        rows_list = [row.replace('escola publica baixa renda-ppi', 'pub_baixa_ppi') \
                for row in rows_list] 
        rows_list = [row.replace('escola publica alta renda-nao ppi', 'pub_alta_n_ppi') \
                for row in rows_list] 
        rows_list = [row.replace('escola publica baixa renda-nao ppi', 'pub_baixa_n_ppi') \
                for row in rows_list] 
        return rows_list
    elif column == 'way_out':
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

def r_get_bar_graph(column_name):
    """
    call r program to plot a bar graph
    """
    call("Rscript stats_bar_graph.r", shell = True)
    call("mv temp.png " + column_name + ".png", shell = True)

def r_get_hist_graph(column_name):
    """
    call r program to plot a bar graph
    """
    call("Rscript stats_hist_graph.r", shell = True)
    call("mv temp.png " + column_name + ".png", shell = True)

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
