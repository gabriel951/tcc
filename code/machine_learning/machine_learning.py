#!/usr/bin/python3.4

# this file contain the machine learning algorithms code

# imports
import statistics as stat
import random

# multioutput
from sklearn.multioutput import *

# regressors
from sklearn.neural_network import *
from sklearn.svm import SVR
from sklearn import linear_model

# decision tree related
from sklearn import tree 
import pydotplus 
import graphviz
import os 

import sys
sys.path.append('..')
from basic import *

from features import *

sys.path.append('../core/')
from students_methods import *

# verbose flag
VERB = 1

def analyse_decision_tree():
    """
    obtain a decision tree of relevant attributes to be analysed
    receives: 
        nothing
    returns: 
        nothing
    * saves the information on a pdf file <dec_tree> + <model_name>.pdf
    """
    # obtain data collections
    data_coll = get_model_info()

    # for each model, print decision tree for a given semester
    for (data, data_desc) in data_coll: 
        print('starting for data %s' %(data_desc))
        (feat_name, feature_lst, result_lst, key_lst) = \
                get_data(data, YEAR_START, YEAR_END, 1, last_sem = True)

        # decision tree
        dc_tree = tree.DecisionTreeRegressor()
        dc_tree.fit(feature_lst, result_lst)
        # save decision tree - why dot data? no idea!
        dot_data = tree.export_graphviz(dc_tree, out_file=None) 
        graph = pydotplus.graph_from_dot_data(dot_data) 
        graph.write_pdf("decision_tree_" + data_desc + ".pdf") 

def apply_oversampling(test_feature, test_result, model): 
    """
    apply oversampling so that the percentage of student able to graduate remains the
    same on the training data and on the test data
    receives: 
        1. test feature list
        2. test result list
        3. key list of students on test set
        3. model description 
        4. boolean to indicate whether we should be verbose or not
    returns: 
        oversampled list of test features and test results

    * function apply oversampling, assuming that the proportion of students able to
    graduate on train set is bigger than on the test set. So, function oversamples
    students on test set able to graduate. The number of students on test set unable
    to graduate stay the same
    """
    if VERB: 
        print('started oversampling')

    # get training and test list of graduation, or not
    ntrain_grad = 0
    train_dict = filter_dict_by(lambda stu: stu.year_in >= YEAR_START_TRA and \
            stu.year_in <= YEAR_END_TRA, model)
    for key, stu in train_dict.items():
        if stu.graduated():
            ntrain_grad += 1

    assert (test_result.count(GRADUATED) <= ntrain_grad)

    # training data proportion of students able to graduate and test data proportion
    TRAIN_PROP_STU_GRA = ntrain_grad / len(train_dict)
    TRAIN_PROP_STU_NOT_GRA = 1 - TRAIN_PROP_STU_GRA

    # calculate number of test features to be oversampled so that the proportion can be
    # equal to the training proportion
    correct_num_test_feat = get_num_non_grad(test_result) / TRAIN_PROP_STU_NOT_GRA
    num_oversamples = correct_num_test_feat - len(test_result)

    try: 
        assert (num_oversamples >= 0)
    except: 
        print(correct_num_test_feat, len(test_result))
        exit ('error on oversampling')

    # add samples to the oversample feature and oversample result list
    oversample_feature = list(test_feature)
    oversample_result = list(test_result)
    added_samples = 0
    while added_samples < num_oversamples:

        # get random sample 
        ind = random.randrange(len(test_feature))

        # be sure sample is of a student that graduated and add it 
        if test_result[ind] == GRADUATED: 
            oversample_feature.append(test_feature[ind])
            oversample_result.append(test_result[ind])
            added_samples += 1

    if VERB: 
        print('\t new test size: %d' % (len(oversample_result)))
        print('\t train proportion of students that graduated: %f' %
                (TRAIN_PROP_STU_GRA))

        OLD_TEST_PROP_STU_GRA = test_result.count(GRADUATED) / \
                                    len(test_result)
        print('\t old test proportion of students that graduated: %f' %
                (OLD_TEST_PROP_STU_GRA))

        NEW_TEST_PROP_STU_GRA = oversample_result.count(GRADUATED) / \
                                    len(oversample_result)
        print('\t new test proportion of students that graduated: %f' %
                (NEW_TEST_PROP_STU_GRA))

        print('finished oversampling')

    return (oversample_feature, oversample_result)

def build_run_models():
    """
    builds ml models using sklearn and then run it to evaluate performance
    receives: 
        nothing
    returns: 
        nothing
    """
    # get data collection along with the descriptions
    data_coll = get_model_info()

    # list of semesters being studied
    # it should start with 1, dumbass! 0 we'll get you to the last element of the
    # list
    sem_lst = [1, 2, 3, 4]

    # iterate through the semesters
    for semester in sem_lst:
        print('\n\n**starting study for semester: %d' % (semester))

        # iterate through the data collection
        for (data, data_desc) in data_coll: 
            print('\n**starting for the data %s' % (data_desc))

            if VERB:
                print('**started getting data necessary for training and test')

            # get training data in the correct form to work with 
            (feat_name, training_feature, training_result, key_train) = \
                    get_data(data, YEAR_START_TRA, YEAR_END_TRA, semester)
            # get test data
            (feat_name, test_feature, test_result, key_test) = \
                    get_data(data, YEAR_START_TEST, YEAR_END_TEST, semester)

            if VERB: 
                print('**(train_size, test_size): (%d, %d)' \
                    % (len(training_result), len(test_result)))
                show_class_proportion(training_result, 'training result:')
                #print('**number of features: %d' %(len(training_feature[0])))

            # train multilayer perceptron model 
            #regressor = MLPRegressor()
            #if VERB:
            #    print('**started training ANN')
            #multiregressor = MultiOutputRegressor(regressor)
            #multiregressor.fit(training_feature, training_result)

            ## train svr
            #svr = SVR()
            #if VERB:
            #    print('**started training SVR')
            #svr.fit(training_feature, training_result)

            ## train linear model 
            linear_regressor = linear_model.LinearRegression()
            if VERB:
                print('**started training linear regressor')
            linear_regressor.fit(training_feature, training_result)
            multi_linear_regressor = MultiOutputRegressor(linear_regressor)
            multi_linear_regressor.fit(training_feature, training_result)
            assert(len(feat_name) == len(training_feature[0]))
            print(feat_name)
            #exit()

            # evaluate performance of the ml techniques
            oversample = True
            #evaluate_performance(data, semester, test_feature, test_result,\
            #        regressor, 'ANN', oversample, key_test)
            #evaluate_performance(data, semester, test_feature, test_result,\
            #        svr, 'SVR', oversample, key_test)
            evaluate_performance(data, semester, test_feature, test_result, \
                    linear_regressor, 'L. Regressor', oversample, key_test)

            #print('\n\n\n####### WARNING - training start ######')
            #oversample = False
            #evaluate_performance(data, semester, training_feature, training_result,\
            #        regressor, 'ANN', oversample, key_train)
            #evaluate_performance(data, semester, training_feature, training_result,\
            #        svr, 'SVR', oversample, key_train)
            #evaluate_performance(data, semester, training_feature, training_result, \
            #        linear_regressor, 'L. Regressor', oversample, key_train)
            #print('####### WARNING - training end ######\n\n\n')


            # TODO - just analyse all students
            break

def evaluate_performance(data, cur_sem, test_feature, test_result, model, \
        model_desc, oversample, key_lst):
    """
    evaluates the performance of a model, by showing how many test instances the
    model was able to get right
    receives: 
        1. the dictionary of the data we are working with
        2. current semester we are in
        3. list containing all the test features
        4. list containing the test results
        5. model to apply
        6. a description of the model 
        7. boolean to indicate if we should oversample
        8. list of the keys of the students on the test set passed
    returns:
        nothing
    """
    # predict
    print('\n\nstarted evaluating performance of %s' % (model_desc))

    # apply oversampling if we should
    if oversample: 
        (final_test_feature, final_test_result) = \
                apply_oversampling(test_feature, test_result, data)
    else: 
        (final_test_feature, final_test_result) = \
                (test_feature, test_result)

    prediction_lst = model.predict(final_test_feature)

    # set the evasion chance for the model
    for ind in range(len(key_lst)): 
        key = key_lst[ind]
        cur_stu = data[key]
        if cur_sem < cur_stu.get_num_semesters(): # needed because student may have
                                                    #left
            cur_stu.evasion_chance[cur_sem] = prediction_lst[ind]

    assert(len(prediction_lst) == len(final_test_result))

    # discretize prediction 
    disc_prediction_lst = get_discrete_prediction(prediction_lst)

    # show stats of how many evasions for the test result and the prediction list
    show_class_proportion(final_test_result, 'final test result: ')
    show_class_proportion(disc_prediction_lst, 'discrete prediction result: ')
    
    # evaluate performance 
    show_model_perf(final_test_result, disc_prediction_lst)

def get_data(model, year_inf, year_sup, semester, enh = False, last_sem = False):
    """
    organizes student information in order to feed machine learning model of scikit
    receives:
        1. Student dictionary containing student info
        2. Inferior limit for the year student entered university
        3. Superior limit for the year student entered university
        4. Semester the student is in 
        5. (optional) boolean to indicate whether we should use the enhanced
        functions or not
        6. (optional) boolean to indicate if we should get the last semester (instead
        of the semester passed as a parameter) or not
    returns:
        tuple containing:
            first entrie - feature name
            second entrie - list of (list of features). One list of features per student
            third entrie - list of results. One result per student 
            fourth entrie - list of keys for the students
    """
    # tuple of outcomes
    feat_name_lst = []
    features_lst = []
    target_lst = []
    key_lst = []

    # TODO: could be helpful if we normalize it?
    #if enh: 
    #    normalize_values(model, semester)

    # iterate through every student
    for key, stu in model.items():
        # if student entered in a year we're not interessed, skip
        if stu.year_in < year_inf or stu.year_in > year_sup: 
            continue

        # if the student has already graduated, fill the data with the last semester
        # information. If we should select the last semester, select it!
        if last_sem or semester > stu.get_num_semesters():
            semester = stu.get_num_semesters()

        # build student features list and append to student features list
        stu_features = []
        add_feature_sex(stu, stu_features, feat_name_lst)
        add_feature_age(stu, stu_features, feat_name_lst)
        add_feature_local(stu, stu_features, feat_name_lst)
        add_feature_quota(stu, stu_features, feat_name_lst)
        add_feature_course(stu, stu_features, feat_name_lst)
        add_feature_way_in(stu, stu_features, feat_name_lst)
        add_feature_pass_rate(stu, stu_features, semester, feat_name_lst)
        add_feature_drop_rate(stu, stu_features, semester, feat_name_lst)
        add_feature_ira(stu, stu_features, semester, feat_name_lst)
        add_feature_impr_rate(stu, stu_features, semester, feat_name_lst)
        add_feature_credit_rate_acc(stu, stu_features, semester, feat_name_lst)
        add_feature_hard_rate(stu, stu_features, semester, feat_name_lst)
        #add_feature_condition(stu, stu_features, semester, feat_name_lst)
        add_feature_position(stu, stu_features, semester, feat_name_lst)
        #add_feature_evasion_chance(stu, stu_features, semester, feat_name_lst)
        features_lst.append(stu_features)

        # add outcome
        add_outcome(stu, target_lst)

        # add key
        key_lst.append(key)

    # lists should have equal length
    assert(len(features_lst) == len(target_lst) == len(key_lst))

    # return 
    return (feat_name_lst, features_lst, target_lst, key_lst)

def get_num_non_grad(result_lst):
    """
    calculates the number of students that didn't graduate, in a list of students
    output (so, values on the list should be GRADUATED, EVADED, MIGRATED)
    receives:   
        1. result list
    returns: 
        number of students that didn't graduate
    """
    return result_lst.count(EVADED) + result_lst.count(MIGRATED)

def get_discrete_prediction(prediction_lst):
    """
    build and return a list of what will be the way out of the student, from the 
    prediction list of continuous variables
    receives: 
        1. list of continuous variables, representing the prediction given by some
        model to some student
    returns: 
        discrete prediction list
    """
    disc_prediction_lst = []
    for pred in prediction_lst:
        max_value = max(pred)
        max_index = list(pred).index(max_value)
        if max_index == 0: 
            disc_prediction_lst.append(GRADUATED)
        elif max_index == 1:
            disc_prediction_lst.append(EVADED)
        elif max_index == 2: 
            disc_prediction_lst.append(MIGRATED)
        else: 
            exit('error')
    return disc_prediction_lst

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

def show_class_proportion(result_lst, description): 
    """
    reports the amount and the proportion of students that graduated, evaded or
    migrated
    receives: 
        1. list containing the results
        2. description of the list
    returns: 
        nothing
    * print on the screen 
    """
    print('\t' + description)
    print('\t\t graduate amount: %d, evade amount: %d, migrate amount: %d' %
        (result_lst.count(GRADUATED), result_lst.count(EVADED), 
            result_lst.count(MIGRATED)))

def show_model_perf(correct_lst, model_lst):
    """
    show how many positives and negatives the model got
    receives: 
        1. list of correct results
        2. list of results predicted by the model
    returns: 
        nothing
    """
    assert(len(correct_lst) == len(model_lst))
    
    trues, falses = 0, 0
    for cur_pred in range(len(correct_lst)):
        if model_lst[cur_pred] == correct_lst[cur_pred]:
            trues += 1
        else: 
            falses += 1
    total = trues + falses

    print('right predictions: %d, wrong predictions: %d', trues, falses)
    print('right percentage: %f, wrong percentage: %f', trues/total, falses/total)

# execute case this is the main file
if __name__ == "__main__":

    # get decision tree information
    #analyse_decision_tree()

    # build and run machine learning models
    build_run_models()
