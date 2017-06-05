# file containing functions to evaluate the performance of all ml models

import pickle
import statistics

from basic_ml import *
from subprocess import call
import global_ml as gml

def get_all_data_desc():
    """
    get a list containing the data description we are considering
    receives:
        1. nothing
    returns: 
        nothing
    """
    data_desc_lst = ["young_students_ti_courses", "young_students_lic_courses", \
            "young_students_comp_courses", "old_students"]
    return data_desc_lst
    #return ["old_students"] # to facilitate test, only old students

def plot_ml_model_perf():
    """
    DEPRECATED
    plot a graph showing the performance of each ml model for the various semesters
    we are considering
    receives: 
        1. nothing
    returns:
        nothing
    """
    # load pickle object 
    try: 
        perf_ml_model = pickle.load(open(PCK_ML_MODEL, 'rb'))
    except FileNotFoundError:
        exit('performance of the ml model pickle object not found')

    # get the different data we are working with 
    data_desc_lst = []
    for key, val in perf_ml_model.items():
        (sem, data_desc, model_desc) = key
        if not (data_desc in data_desc_lst):
            data_desc_lst.append(data_desc)

    # for each data description
    for data_desc in data_desc_lst:

        # open file for writing 
        arq = open('ml_graph.txt', 'w')

        # iterate through performance dictionary
        for key, val in perf_ml_model.items():

            # if current entrie is about the data description we are interested in
            if data_desc in key: 

                # write in the file
                (sem, data_desc, model_desc) = key
                arq.write(data_desc + "     ")
                arq.write(str(sem) + "     ")
                arq.write(model_desc + "     ")
                arq.write(str(val) + "     ")
                arq.write("\n")


        arq.close()

        # call r program to plot graph
        call("Rscript r_plot_ml_graph.r", shell = True)
        call("mv temp.png ./graphs/" + data_desc + ".png", shell = True)

def report_best_model_conf(conf_path):
    """
    report which configuration is better for every model
    receives: 
        nothing
    returns: 
        nothing
    """
    # open dictionary of model performance
    try: 
        perf_ml_model = pickle.load(open(conf_path, 'rb'))
    except FileNotFoundError:
        exit('performance of the ml model pickle object not found')

    # get all data descriptions
    data_desc_lst = get_all_data_desc()

    # for every data desc, report best configuration
    for data_desc in data_desc_lst: 
        if gml.USE_ANN:
            report_best_conf_wrap(perf_ml_model, data_desc, 'ANN')
        if gml.USE_SVR: 
            report_best_conf_wrap(perf_ml_model, data_desc, 'SVR')
        if gml.USE_NB:
            report_best_conf_wrap(perf_ml_model, data_desc, 'naive_bayes')

def report_best_conf_wrap(ml_models, data_desc_2_consider, name_rest):
    """
    report which configuration is better for every model
    receives: 
        1. dictionary containing the performance for the ml models
        2. data description to consider. Only get the data that is from this data
        desc
        2. a name restriction. We'll only consider ml models which contain this name
        restriction. 
    returns: 
        nothing
    * prints results on the screen
    """
    # only consider models that have the name restriction passed and the data we are
    # considering
    restricted_ml_models = {}
    for key, val in ml_models.items():
        (sem, data_desc, ml_model_desc) = key
        score = val
        if (name_rest in ml_model_desc) and (data_desc == data_desc_2_consider):
            restricted_ml_models[key] = val
    assert(len(restricted_ml_models) != 0)

    # get dictionary containing for every model a list of scores
    score_per_model = {}
    for key, val in restricted_ml_models.items():
        (sem, data_desc, ml_model_desc) = key
        score = val
        if not (ml_model_desc in score_per_model): 
            score_per_model[ml_model_desc] = [score]
        else: 
            score_per_model[ml_model_desc].append(score)

    # make list of performance by models - and print the one with best performance
    perf_model_lst = []
    for model, score_lst in score_per_model.items():
        mean_perf = statistics.mean(score_lst)
        perf_model_lst.append((model, mean_perf))
    perf_model_lst.sort(key = lambda tup: tup[1], reverse = True)
    print("performance - ml model: %s - data: %s" % (name_rest, data_desc_2_consider))
    for (model, mean_perf) in perf_model_lst:
        print("\t" + model + ": " + str(mean_perf))
    print("")