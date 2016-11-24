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
    ## students
    #get_graph('student', 'sex')
    #get_graph('student', 'age')
    #get_graph('student', 'local')
    #get_graph('student', 'course')

    # TODO: buggy columns
    #get_graph('student', 'school_type')
    #get_graph('student', 'quota')
    #get_graph('student', 'race')
    
    ## 
def get_graph(table, column):
    """
    generate a pizza graph for a given table with a given column
    four modes are possible: small (only year 2000 considered), training (only
    training years are considered), testing (similar) and all (all years considered)
    """
    (year_start, year_end) = get_mode_year('small')

    # query database
    query = "select %s from %s.%s where year_in >= %d and year_end <= %d" 
                % (column, MY_DATABASE, table, year_start, year_end)
    print(query)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    
    # convert from list of tuples to list of strings
    rows_list = []
    for row in rows:
        rows_list.append(row[0])
    
    # handle problematic cases - TODO
    #handle_cases(column)

    # write query in file, call r program to plot pie chart and delete
    write_execute_delete(rows_list, r_get_graph, column)

def r_get_graph(column_name):
    """
    call r program to plot a bar graph
    """
    call("Rscript stats.r", shell = True)
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
