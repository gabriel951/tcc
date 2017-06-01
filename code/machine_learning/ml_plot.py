# file containing functions to plot interesting graphs about the model
# performance

import pickle
from basic_ml import *
from subprocess import call

def plot_ml_model_perf():
    """
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

