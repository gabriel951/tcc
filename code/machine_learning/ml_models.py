#!/usr/bin/python3.4

import sys

from basic_ml import *
from basic import * 
import global_ml as gml

sys.path.append('../core/')
from students_methods import *

# regressors
from sklearn.neural_network import *
from sklearn.svm import SVR
from sklearn import linear_model
from sklearn.ensemble import *
from sklearn.naive_bayes import GaussianNB

# multioutput regressor
from sklearn.multioutput import *

def add_evasion_chance(sem, data, ml_model_desc, feature_lst, key_lst):
    """
    append feature evasion chance to the feature list (train or test)
    receives:
        1. semester we are in
        2. dictionary containing the data we have
        3. ml_model description 
        4. feature list 
        5. list with the key for each student on the feature list
    returns:
        nothing 
    """
    # first semester students don't have previous evasion chance calculated
    if sem == 1: 
        return
    
    # train feature list and key list should have same length
    assert(len(feature_lst) == len(key_lst))

    # get base value 
    (amount, grad_base_val, evade_base_val, migr_base_val) = \
            get_tot_grad_evd_migr(data)

    # iterate through the list with the keys
    for index in range(len(key_lst)):

        # get key and student for that particular info 
        key = key_lst[index]
        stu = data[key]

        # if the student left before the semester we are considering
        if sem > stu.get_num_semesters():

            # if the student stayed for one semester, use the base as value
            if stu.get_num_semesters() == 1: 
                pred_lst = [grad_base_val, evade_base_val, migr_base_val]

            # else
            else: 
                # put last semester as the evasion chance
                pred_lst = [grad_base_val, evade_base_val, migr_base_val]
                #pred_lst = stu.evasion_chance[(stu.get_num_semesters(), ml_model_desc)]

        # else, it's a normal case
        else: 
            pred_lst = [grad_base_val, evade_base_val, migr_base_val]
            #pred_lst = stu.evasion_chance[(sem - 1, ml_model_desc)]
        
        assert(len(pred_lst) == 3)

        # add it to the training feature instance
        feature_lst[index].append(pred_lst[GRAD_IND])
        feature_lst[index].append(pred_lst[EVADE_IND])
        feature_lst[index].append(pred_lst[MIGR_IND])
    
def add_evasion_chance_all_models(ml_models, sem, data, key_train_lst, key_test_lst):
    """
    Add evasion chances to all models
    receives: 
        1. list containing model info
        2. semester we are interested
        3. data we have 
        4. list containing the key of the training students
        5. list containing the key of the test students
    returns: 
        nothing
    """
    # iterate through each model 
    for [model_name, model, model_train_feat, model_test_feat] in ml_models: 
        # add evasion chance to that model feature list
        add_evasion_chance(sem, data, model_name, model_train_feat, key_train_lst)
        add_evasion_chance(sem, data, model_name, model_test_feat, key_test_lst)

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
    if gml.USE_TAIL: 
        suffix += '_use_tail'
    else: 
        suffix += '_no_tail'

    # consider the way of picking target variable for the model
    if gml.WAY_MODEL_TGT == 'absolute':
        suffix += '_absolute'
    elif gml.WAY_MODEL_TGT == 'relative':
        suffix += '_relative'
    else: 
        exit('error on the function that gets suffix')

    return suffix

def get_tot_grad_evd_migr(data):
    """
    get the total of students on the data, and the proportion that graduated, evaded
    and migrated
    receives: 
        1. data
    returns: 
        tuple of the form (total_amount, graduate proportion, evasion proportion,
        migration proportion)
    """
    (amount, grad_base_val) = get_grad_evd_migr_info(data, 
            lambda stu: stu.is_train_inst(), 'grad')
    (amount, evade_base_val) = get_grad_evd_migr_info(data, 
            lambda stu: stu.is_train_inst(), 'evade')
    (amount, migr_base_val) = get_grad_evd_migr_info(data, 
            lambda stu: stu.is_train_inst(), 'migr')
    amount = len(data)
    return (amount, grad_base_val, evade_base_val, migr_base_val)

def get_untrained_ann(bool_var, ml_models, training_feature, test_feature):
    """
    if bool_var is set to true, append to the model an untrained ann
    receives: 
        1. list of the models we are considering
        2. training feature list
        3. test feature list
    returns: 
        nothing
    """
    if bool_var:
        ann_name = 'ANN' + get_suffix_ml_model()
        ann = MLPRegressor()
        multi_ann = MultiOutputRegressor(ann)
        ann_train_feat = list(training_feature)
        ann_test_feat = list(test_feature)
        ml_models.append([ann_name, multi_ann, ann_train_feat, ann_test_feat])

def get_untrained_linear_regressor(bool_var, ml_models, training_feature, test_feature):
    """
    if bool_var is set to true, append to the model an untrained linear regressor
    receives: 
        1. list of the models we are considering
        2. training feature list
        3. test feature list
    returns: 
        nothing
    """
    if bool_var:
        lreg_name = 'linear_regressor' + get_suffix_ml_model()
        linear_regressor = linear_model.LinearRegression()
        multi_linear_regressor = MultiOutputRegressor(linear_regressor)
        lreg_train_feat = list(training_feature)
        lreg_test_feat = list(test_feature)
        ml_models.append([lreg_name, multi_linear_regressor, lreg_train_feat,
            lreg_test_feat])

def get_untrained_ml_models(training_feature, test_feature):
    """
    get a list containing the untrained linear models, along with the description for
    each one and the training/test feature list for each one
    receives: 
        1. training feature list
        2. test feature 
    returns: 
        a list of lists. Each nested list contain: 
        1. the model name 
        2. the model object (untrained)
        3. the model training feature list
        4. the model test feature list
    """
    ml_models = []

    # bools indicate which model we are consider. Set just one to True, so it's easy
    # to test ;)
    use_lreg = True
    use_ann = True
    use_svr = True
    use_rand_for = True
    use_nb = True
    
    # get untrained models
    get_untrained_linear_regressor(use_lreg, ml_models, training_feature, test_feature)
    get_untrained_ann(use_ann, ml_models, training_feature, test_feature)
    get_untrained_svr(use_svr, ml_models, training_feature, test_feature)
    get_untrained_rand_for(use_rand_for, ml_models, training_feature, test_feature)
    get_untrained_naive_bayes(use_nb, ml_models, training_feature, test_feature)

    return ml_models

def get_untrained_naive_bayes(bool_var, ml_models, training_feature, test_feature):
    """
    if bool_var is set to true, append to the model an untrained naive bayes model
    receives: 
        1. list of the models we are considering
        2. training feature list
        3. test feature list
    returns: 
        nothing
    """
    if bool_var:
        nb_name = 'naive_bayes' + get_suffix_ml_model()
        nb = GaussianNB()
        multi_nb = MultiOutputRegressor(nb)
        nb_train_feat = list(training_feature)
        nb_test_feat = list(test_feature)
        ml_models.append([nb_name, multi_nb, nb_train_feat, nb_test_feat])

def get_untrained_rand_for(bool_var, ml_models, training_feature, test_feature):
    """
    if bool_var is set to true, append to the model an untrained random forest
    receives: 
        1. list of the models we are considering
        2. training feature list
        3. test feature list
    returns: 
        nothing
    """
    if bool_var:
        rand_for_name = 'random_forest' + get_suffix_ml_model()
        rand_for = RandomForestRegressor()
        multi_rand_for = MultiOutputRegressor(rand_for)
        rand_for_train_feat = list(training_feature)
        rand_for_test_feat = list(test_feature)
        ml_models.append([rand_for_name, multi_rand_for, rand_for_train_feat,
            rand_for_test_feat])

def get_untrained_svr(bool_var, ml_models, training_feature, test_feature):
    """
    if bool_var is set to true, append to the model an untrained svr
    receives: 
        1. list of the models we are considering
        2. training feature list
        3. test feature list
    returns: 
        nothing
    """
    if bool_var:
        svr_name = 'SVR' + get_suffix_ml_model()
        svr = SVR()
        multisvr = MultiOutputRegressor(svr)
        svr_train_feat = list(training_feature)
        svr_test_feat = list(test_feature)
        ml_models.append([svr_name, multisvr, svr_train_feat, svr_test_feat])

def normalize_values(stu_info, semester):
    """
    not being used
    normalize the pass rate of students
    receive: 
        1. a student dictionary containing all relevant information
        2. a given semester that we should normalize
    returns:
        nothing
    """
    # list of values to normalize
    values_normalize = []
    for key, stu in stu_info.items():
        values_normalize.append(stu.pass_rate[semester - 1])

    # normalize
    mean = stat.mean(values_normalize)
    for key, stu in stu_info.items():
        stu.pass_rate[semester - 1] = stu.pass_rate[semester - 1] - mean

def train_ml_models(ml_models, train_result):
    """
    train ml models
    receives: 
        1. ml models list
        2. list with training results
    returns: 
        nothing
    """
    for [model_name, model, model_train_feat, model_test_feat] in ml_models: 
        if 'linear_regressor' in model_name: 
            model.fit(model_train_feat, train_result)
        elif 'ANN' in model_name: 
            model.fit(model_train_feat, train_result)
        elif 'SVR' in model_name: 
            model.fit(model_train_feat, train_result)
        elif 'random_forest' in model_name:
            model.fit(model_train_feat, train_result)
        elif 'naive_bayes' in model_name: 
            model.fit(model_train_feat, train_result)
        else: 
            exit('not prepared to handle model: %s' % (model_name))
