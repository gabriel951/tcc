#!/usr/bin/python3.4

# file to get statistic from the database
import itertools
import math
import pandas
from scipy import stats

# import basic
import sys
sys.path.append('..')
from basic import *

import psycopg2
from subprocess import call

sys.path.append('../core/')
from students_methods import *

from stats import *

def generate_graphs():
    """
    generate the graphs for the primitive and derived attributes
    saves the graph as .png files in the folder we are in
    receives: 
        nothing
    returns: 
        nothing
    """
    # get model information
    models_lst = get_model_info()
 
    # for every model info, make the graph
    for (model, model_desc) in models_lst: 
        if model_desc != 'old_students':
            continue
        print('starting for %s' % (model_desc))

        # deprecated features: local and race
        ## primitive features
        prim_feat_lst = ['sex', 'age', 'quota', 'school_type', 'course', \
                'race', 'way_in', 'way_out', 'grades']
        sep_course = False
        for prim_feat in prim_feat_lst: 
            get_graph(model_desc, prim_feat, model, sep_course, data_type = 'discrete')

        ## derived features - continuous
        # list of tuples of the form: [(<attr_name, sep_course, index, binwidth>)]
        derv_feat_lst = []
        derv_feat_lst.append(('ira', False, LAST_ELEM, 0.2))
        derv_feat_lst.append(('improvement_rate', False, LAST_ELEM, 0.2))
        #derv_feat_lst.append(('pass_rate', True, LAST_ELEM, 0.05))
        derv_feat_lst.append(('pass_rate', False, LAST_ELEM, 0.05))
        #derv_feat_lst.append(('fail_rate', True, LAST_ELEM, 0.05))
        derv_feat_lst.append(('fail_rate', False, LAST_ELEM, 0.05))
        #derv_feat_lst.append(('drop_rate', True, LAST_ELEM, 0.05))
        derv_feat_lst.append(('drop_rate', False, LAST_ELEM, 0.05))
        derv_feat_lst.append(('credit_rate_acc', False, 0, 2))
        derv_feat_lst.append(('hard_rate', False, LAST_ELEM, 0.05))
        for (feat_name, sep_course, index, binwidth) in derv_feat_lst: 
            get_graph(model_desc, feat_name, model, sep_course, \
                    data_type = 'continuous', index = LAST_ELEM, binwidth = binwidth)

        ## derived features - discrete
        derv_feat_lst = []
        derv_feat_lst.append(('in_condition', False, LAST_ELEM))
        #derv_feat_lst.append(('in_condition', True, LAST_ELEM))
        derv_feat_lst.append(('position', False, LAST_ELEM))
        for (feat_name, sep_course, index) in derv_feat_lst: 
            get_graph(model_desc, feat_name, model, sep_course, data_type = 'discrete', \
                    index = LAST_ELEM)

def get_graph(model_desc, feature, stu_info, sep_course, data_type, index = None, binwidth =
        0.05):
    """
    generate a bar graph (discrete data) or a histogram graph (continuous data) for 
    the feature distribution. No separation by course
    receives:
        1. the model description
        2. a feature name
        3. a dictionary of students. 
        4. a boolean to indicate if we need to separate the courses or not
        5. whether the datatype is discrete or continuous.
        6. (optional) an index. If passed its because the feature is a list (one for
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
            write_execute(atr_values, way_out, r_get_bar_graph, name, model_desc)
        elif data_type == 'continuous':
            write_execute(atr_values, way_out, r_get_hist_graph, name, model_desc, \
                    binwidth)
        else:
            exit("misinformed value")

        # if we don't want to separate course, end function
        if sep_course == False: 
            return

def r_get_bar_graph(name, folder):
    """
    call r program to plot a bar graph
    receives: 
        1. the name for the graph
        2. the folder the graph we'll be saved
    returns:
        nothing
    """
    call("Rscript stats_bar_graph.r", shell = True)
    call("mv temp.png " + folder + "/" + name, shell = True)

def r_get_hist_graph(name, folder, binwidth):
    """
    call r program to plot a histogram graph
    receives: 
        1. the name for the graph
        2. the folder the graph we'll be saved
        3. the binwidth for the histogram graph
    returns: 
        nothing
    """
    call("Rscript stats_hist_graph.r " + str(binwidth), shell = True)
    call("mv temp.png " + folder + "/" + name, shell = True)

if __name__ == "__main__":

    # histograms
    generate_graphs()
