#!/usr/bin/python3.4

import sys

from basic import * 

sys.path.append('../core/')
from students_methods import *

# regressors
from sklearn.neural_network import *
from sklearn.svm import SVR
from sklearn import linear_model

# multioutput regressor
from sklearn.multioutput import *

# indices in a list that correspond to the graduation risk, evasion risk and
# migration risk
GRAD_IND = 0
EVADE_IND = 1
MIGR_IND = 2

def add_evasion_chance(sem, data, ml_model_desc, training_feature, key_lst):
    """
    append feature evasion chance to the training feature list
    receives:
        1. semester we are in
        2. dictionary containing the data we have
        3. ml_model description 
        4. training feature list 
        5. list with the key for each entrie on the training feature list
    returns:
        nothing 
    """
    # first semester students don't have previous evasion chance calculated
    if sem == 1: 
        return

    # train feature list and key list should have same length
    assert(len(training_feature) == len(key_lst))

    # iterate through the list with the keys
    for index in range(len(key_lst)):

        # get key and student for that particular info 
        key = key_lst[index]
        stu = data[key]

        # get prediction list for that student
        pred_lst = stu.evasion_chance[(sem - 1, ml_model_desc)]

        # add it to the training feature instance
        training_feature[index].append(pred_lst[GRAD_IND])
        training_feature[index].append(pred_lst[EVADE_IND])
        training_feature[index].append(pred_lst[MIGR_IND])
    
    # train feature list and key list should have same length
    assert(len(training_feature) == len(key_lst))

def get_suffix_ml_model():
    """
    get the right suffix an ml model should have, according to the use (or not) of
    retroalimentation and the use model way of picking the target variable
    receives:
        nothing
    returns: 
        string containing the suffix
    """
    suffix = ''
    
    # consider if the model uses tail or not
    if USE_TAIL: 
        suffix += '_use_tail'
    else: 
        suffix += '_no_tail'

    # consider the way of picking target variable for the model
    if WAY_MODEL_TGT == 'absolute':
        suffix += '_absolute'
    else if WAY_MODEL_TGT == 'relative':
        suffix += '_relative'
    else: 
        exit('error on the function that gets suffix')

    return suffix

def get_trained_linear_regressor(model_lst, sem, data, training_feature, training_result, 
        key_lst): 
    """
    append to the models a trained linear regressor and it's description
    receives: 
        1. list containing the models so far
        2. semester we are interested in 
        3. dictionary containing student info
        4. list of training features
        5. list of training results
        6. list that, for each training feature, has the key (stu.reg) for the
        correspondent student  
    returns: 
        nothing
    * modifies the models_lst list
    """
    # if it's to use retroalimentation, modify the features list to include the
    # variable
    if USE_TAIL: 
        add_evasion_chance(sem, data, 'linear_regressor', training_feature, key_lst)

    # train linear regressor
    linear_regressor = linear_model.LinearRegression()
    if VERB:
        print('**started training linear regressor')
    linear_regressor.fit(training_feature, training_result)
    multi_linear_regressor = MultiOutputRegressor(linear_regressor)
    multi_linear_regressor.fit(training_feature, training_result)

    # name the linear regressor and append it to the list
    suffix = get_suffix_ml_model() 
    model_lst.append((multi_linear_regressor, 'linear_regressor' + suffix))
    
def get_trained_ann(model_lst, sem, data, training_feature, training_result, 
        key_lst): 
    """
    append to the models a trained ann regressor and it's description
    receives: 
        1. list containing the models so far
        2. semester we are interested in 
        3. dictionary containing student info
        4. list of training features
        5. list of training results
        6. list that, for each training feature, has the key (stu.reg) for the
        correspondent student 
    returns: 
        nothing
    * modifies the models_lst list
    """
    # if it's to use retroalimentation, modify the features list to include the
    # variable
    if USE_TAIL: 
        add_evasion_chance(sem, data, 'ANN', training_feature, key_lst)

    # train and append ann
    regressor = MLPRegressor()
    if VERB:
        print('**started training ANN')
    multiregressor = MultiOutputRegressor(regressor)
    multiregressor.fit(training_feature, training_result)
    model_lst.append((multiregressor, 'ANN'))

def get_trained_svr(model_lst, sem, data, training_feature, training_result, 
        key_lst): 
    """
    append to the models a trained svr and it's description
    receives: 
        1. list containing the models so far
        2. semester we are interested in 
        3. dictionary containing student info
        4. list of training features
        5. list of training results
        6. list that, for each training feature, has the key (stu.reg) for the
        correspondent student 
    returns: 
        nothing
    * modifies the models_lst list
    """
    # if it's to use retroalimentation, modify the features list to include the
    # variable
    if USE_TAIL: 
        add_evasion_chance(sem, data, 'SVR', training_feature, key_lst)

    # train and append SVR
    svr = SVR()
    if VERB:
        print('**started training SVR')
    #svr.fit(training_feature, training_result)
    multisvr = MultiOutputRegressor(svr)
    multisvr.fit(training_feature, training_result)
    model_lst.append((multisvr, 'SVR'))
