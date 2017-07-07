#!/usr/bin/python3.4

import itertools
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
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB

# multioutput regressor
from sklearn.multioutput import *

# crossvalidation
from sklearn.model_selection import cross_val_score

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

def do_cross_val(sem, data_desc, perf_ml_model, ml_model_desc, ml_model, train_feature,
        train_result):
    """
    DEPRECATED - We are using the validation set
    apply cross validation and saves the result
    receives: 
        1. semester we are in 
        2. description of the data we are working with 
        3. dictionary containing the performance of the ml model
        4. description of the ml model 
        5. ml model object we are working with 
        6. train feature list
        7. train result list
    """
    scores = cross_val_score(ml_model, train_feature, train_result, cv = NUM_KFOLD,
            scoring = 'neg_mean_absolute_error')
    if VERB: 
        print("model: %s - score: %f" % (ml_model_desc, statistics.mean(scores)))
    perf_ml_model[(sem, data_desc, ml_model_desc)] = statistics.mean(scores)

def get_optimal_param(data_desc, ml_model_desc):
    """
    get the optimal parameters, according to the ml model passed and the data we are
    working with
    receives: 
        1. description of the data we are working with
        2. description of the model we are working with
    returns: 
        list containing the optimal parameters
    """
    if ml_model_desc == 'ANN': 
        # return [<num_layers>, <momentum>, <learn rate>]
        if data_desc == 'young_students_ti_courses':
            return [100, 0.5, 0.001]
        elif data_desc == 'young_students_lic_courses':
            return [36, 0.9, 1.0]
        elif data_desc == 'young_students_comp_courses':
            return [36, 0.6, 0.001]
        elif data_desc == 'old_students':
            return [24, 0.5, 0.7]
        else:
            exit('can not get optimal parameters for the combination passed!')
    elif ml_model_desc == 'naive_bayes':
        if data_desc == 'young_students_ti_courses':
            return [GaussianNB()]
        elif data_desc == 'young_students_lic_courses':
            return [BernoulliNB()]
        elif data_desc == 'young_students_comp_courses':
            return [MultinomialNB()]
        elif data_desc == 'old_students':
            return [GaussianNB()]
        else:
            exit('can not get optimal parameters for the combination passed!')
    elif ml_model_desc == 'SVR': 
        if data_desc == 'young_students_ti_courses':
            return ['linear', 1.0]
        elif data_desc == 'young_students_lic_courses':
            return ['linear', 1.0]
        elif data_desc == 'young_students_comp_courses':
            return ['rbf', 1.0]
        elif data_desc == 'old_students':
            return ['linear', 1.0]
        else:
            exit('can not get optimal parameters for the combination passed!')
    else: 
        exit('can not get optimal parameters for the combination passed!')

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

def get_suffix_configuration(lst):
    """
    get suffix configuration for the parameters passed on the lst of parameters
    receives: 
        1. list containing the parameters
    returns: 
        suffix configuration
    """
    suffix_conf = ''
    for elem in lst: 
        suffix_conf += '_'
        if type(elem) != str: 
            elem = str(elem)
        suffix_conf += elem
    return suffix_conf

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

def get_untrained_ann(bool_var, data_desc, ml_models, train_feature, train_result,
        test_feature, option):
    """
    if bool_var is set to true, append to the model an untrained ann
    receives: 
        1. boolean variable indicating if we should append
        2. data description we are working with
        3. list of the models we are considering
        4. training feature list
        5. train result list
        6. test feature list
        7. option - whether we are just looking for the right optimization parameters
        or we are running the model for good
    returns: 
        nothing
    """
    # just return case we dont want any ann
    if not bool_var: 
        return
    
    # if we want just an optimal configuration, append to it
    if option != 'optimization':
        [num_layers, momentum, learn_rate] = get_optimal_param(data_desc, 'ANN')
        ann_name = 'ANN' + get_suffix_ml_model()
        ann = MLPRegressor(hidden_layer_sizes = num_layers, solver = 'lbfgs', momentum =
                momentum, learning_rate_init = learn_rate)
        multi_ann = MultiOutputRegressor(ann)
        ml_models.append([ann_name, multi_ann, list(train_feature), 
            list(test_feature)]) # it should be copies of the lists, not the lists
                                 # itselves, because we'll add to this lists 
    
    # try all configurations
    else: 
        # list in which we'll try the configurations
        [num_layers, NOT_momentum, NOT_learn_rate] = \
            get_optimal_param(data_desc, 'ANN')
        #num_layers_lst = [12, 24, 36, 100]
        #momentum = 0.9
        #learn_rate = 0.001
        momentum_lst = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        learn_rate_lst = [0.001, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

        # iterate through configurations
        for (momentum, learn_rate) in itertools.product(momentum_lst,
                learn_rate_lst):

            # get ann name  - consider parameters
            ann_name = 'ANN' + get_suffix_ml_model()
            ann_name += get_suffix_configuration((num_layers, momentum, learn_rate))
            
            # get model and append to the list
            ann = MLPRegressor(hidden_layer_sizes = num_layers, solver = 'lbfgs',
                    momentum = momentum, learning_rate_init = learn_rate, max_iter =
                    MAX_ITER)
            multi_ann = MultiOutputRegressor(ann)
            ml_models.append([ann_name, multi_ann, list(train_feature), 
                list(test_feature)]) 
            
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

def get_untrained_ml_models(data_desc, train_feature, train_result, test_feature, 
        option):
    """
    get a list containing the untrained linear models, along with the description for
    each one and the training/test feature list for each one
    receives: 
        1. data description that we are working with
        2. training feature list
        3. training result list
        4. test feature list
        5. option - whether it's to do optimization or just run the models
    returns: 
        a list of lists. Each nested list contain: 
        1. the model name 
        2. the model object (untrained)
        3. the model training feature list
        4. the model test feature list
    """
    ml_models = []

    # bools indicate which model we are considering. Set just one to True, so it's easy
    # to test ;)
    use_lreg = gml.USE_LREG
    use_ann = gml.USE_ANN
    use_svr = gml.USE_SVR
    use_rand_for = gml.USE_RAND_FOR
    use_nb = gml.USE_NB
    
    # get untrained models
    get_untrained_linear_regressor(use_lreg, ml_models, train_feature, test_feature)
    get_untrained_ann(use_ann, data_desc, ml_models, train_feature, train_result, 
            test_feature, option)
    get_untrained_svr(use_svr, data_desc, ml_models, train_feature, train_result,
            test_feature, option) 
    get_untrained_rand_for(use_rand_for, ml_models, train_feature, test_feature)
    get_untrained_naive_bayes(use_nb, data_desc, ml_models, train_feature,
            train_result, test_feature, option)

    return ml_models

def get_untrained_naive_bayes(bool_var, data_desc, ml_models, train_feature, train_result, 
        test_feature, option):
    """
    if bool_var is set to true, append to the model an untrained ann
    receives: 
        1. boolean variable indicating if we should append
        2. data description 
        4. list of the models we are considering
        5. training feature list
        6. train result list
        7. test feature list
        8. option - whether we are just looking for the right optimization parameters
        or we are running the model for good
    returns: 
        nothing
    """
    # just return case we dont want any naive bayes
    if not bool_var: 
        return

    if option != 'optimization':
        nb_name = 'naive_bayes' + get_suffix_ml_model()
        [nb] = get_optimal_param(data_desc, 'naive_bayes') 
        multi_nb = MultiOutputRegressor(nb)
        nb_train_feat = list(train_feature)
        nb_test_feat = list(test_feature)
        ml_models.append([nb_name, multi_nb, nb_train_feat, nb_test_feat])

    # try all configuration
    else:
        nb_name_lst = ['gaussian', 'multinomial', 'multi_bernoulli']
        nb_obj_lst = [GaussianNB(), MultinomialNB(), BernoulliNB()]
        for i in range(len(nb_name_lst)):
            nb_name = 'naive_bayes' + get_suffix_ml_model()
            nb_name += get_suffix_configuration([nb_name_lst[i]])
            nb = nb_obj_lst[i]
            multi_nb = MultiOutputRegressor(nb)
            ml_models.append([nb_name, multi_nb, list(train_feature),
                list(test_feature)])

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

def get_untrained_svr(bool_var, data_desc, ml_models, train_feature, train_result, 
        test_feature, option):
    """
    if bool_var is set to true, append to the model an untrained svr
    receives: 
        1. boolean variable indicating if we should append
        2. data description that we are working with
        3. list of the models we are considering
        4. training feature list
        5. train result list
        6. test feature list
        7. option - whether we are just looking for the right optimization parameters
        or we are running the model for good
    returns: 
        nothing
    """
    # just return case we dont want any svr
    if not bool_var: 
        return

    # if we want just the optimal configuration, append
    if option != 'optimization':
        [kernel, penalty_factor] = get_optimal_param(data_desc, 'SVR')
        svr_name = 'SVR' + get_suffix_ml_model()
        svr = SVR(kernel = kernel, C = penalty_factor, max_iter = MAX_ITER * 1000)
        multi_svr = MultiOutputRegressor(svr)
        ml_models.append([svr_name, multi_svr, list(train_feature), 
            list(test_feature)]) # it should be copies of the lists, not the lists

    # try all configuration
    else:
        [kernel, NOT_penalty_factor] = get_optimal_param(data_desc, 'SVR')
        penalty_factor_lst = [0.5, 1.0, 2.0]
        for penalty_factor in penalty_factor_lst:
            svr_name = 'SVR' + get_suffix_ml_model()
            svr_name += get_suffix_configuration([kernel, penalty_factor])
            svr = SVR(kernel = kernel, C = penalty_factor, max_iter = MAX_ITER * 1000)
            multi_svr = MultiOutputRegressor(svr)
            ml_models.append([svr_name, multi_svr, list(train_feature), 
                list(test_feature)]) 
            
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
