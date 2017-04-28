#!/usr/bin/python3.4

# this file contain the machine learning algorithms code

# imports
import statistics as stat
import random

# regressors
from sklearn.neural_network import *
from sklearn.svm import SVR
from sklearn import linear_model

# decision tree related
from sklearn import tree 
import pydotplus 
import graphviz
import os # TODO

import sys
sys.path.append('..')
from basic import *

from features import *

sys.path.append('../core/')
from students_methods import *

# TODO: were quotes institutionalized too recently? is this a problem? - apparently
# not

# TODO: test instances refer primarily to students that dropped out, while training
# is not 
    # -> Train proportion: 0.5 app
    # -> Test proportion: 0.18 app

def apply_oversampling(test_feature, test_result): 
    """
    apply oversampling so that the percentage of student able to graduate remains the
    same on the training data and on the test data
    receives: 
        1. test features list
        2. test result list
    returns: 
        nothing
    * please be sure that the training proportion is correct
    * the training proportion should be greater that the test proportion in order to
        this function make any sense
    """
    print('started oversampling')

    GRADUATED = 0
    NOT_GRADUATED = 1

    # copy features to the oversample list
    oversample_result = test_result[:]
    oversample_feature = test_feature[:]

    # training data proportion of students able to graduate 
    TRAIN_PROP_STU_GRA = 0.55
    TRAIN_PROP_STU_NOT_GRA = 1 - TRAIN_PROP_STU_GRA
    #TEST_PROP_STU_GRA = 0.18 # wont be used, put here just if u want to know

    # get amount of students on test feature not able to graduate and able to
    # graduate
    stu_not_able_grad = 0
    for i in range(len(test_result)):
        if test_result[i] != GRADUATED: 
            stu_not_able_grad += 1
    stu_able_grad = len(test_result) - stu_not_able_grad

    # calculate number of test features to be oversampled so that the proportion can be
    # equal to the training proportion
    features_graduate = round(stu_not_able_grad * 
                        (TRAIN_PROP_STU_GRA / TRAIN_PROP_STU_NOT_GRA))
    num_oversamples = features_graduate - stu_able_grad

    # add samples to the oversample feature and oversample result list
    added_samples = 0
    while added_samples < num_oversamples:

        # get random sample 
        ind = random.randrange(len(test_feature))

        # be sure sample is of a student that graduated and add it 
        if test_result[ind] == GRADUATED: 
            oversample_feature.append(test_feature[ind])
            oversample_result.append(test_result[ind])
            added_samples += 1

    print('new test size: %d' % (len(oversample_result)))
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
    # load student information
    stu_info = load_students(NAME_STU_STRUCTURE, path = '../core/data/')

    # list of semesters being studied
    sem_lst = [1, 2, 3]

    # iterate through the semesters
    for semester in sem_lst:
        print('\n\nstarting study for semester: %d' % (semester))
        print('started getting data necessary for training and test')

        # get training data in the correct form to work with 
        (training_feature, training_result) = get_data(stu_info, YEAR_START_TRA, \
                                                YEAR_END_TRA, semester)
        # get test data
        (test_feature, test_result) = get_data(stu_info, YEAR_START_TEST, \
                                                YEAR_END_TEST, semester)

        print('(train_size, test_size): (%d, %d)' \
                % (len(training_result), len(test_result)))
        print('number of features: %d', len(training_feature[0]))

        # decision tree
        dc_tree = tree.DecisionTreeRegressor()
        dc_tree.fit(training_feature, training_result)
        # show
        dot_data = tree.export_graphviz(dc_tree, out_file=None) 
        graph = pydotplus.graph_from_dot_data(dot_data) 
        graph.write_pdf("iris.pdf") 
        #with open("iris.dot", 'w') as f:
        #    f = tree.export_graphviz(dc_tree, out_file=f)
        exit()
        # train multilayer perceptron model 
        #regressor = MLPRegressor()
        #print('started training ANN')
        #regressor.fit(training_feature, training_result)

        ## train svr
        #svr = SVR()
        #print('started training SVR')
        #svr.fit(training_feature, training_result)

        ## train linear model 
        #linear_regressor = linear_model.LinearRegression()
        #print('started training linear regressor')
        #linear_regressor.fit(training_feature, training_result)

        # evaluate performance of the models
        oversample = True
        evaluate_performance(test_feature, test_result, regressor, 'ANN', oversample)
        evaluate_performance(test_feature, test_result, svr, 'SVR', oversample)
        evaluate_performance(test_feature, test_result, svr, 'L. Regressor', oversample)

def evaluate_performance(test_feature, test_result, model, model_desc, oversample):
    """
    evaluates the performance of a model, by showing how many test instances the
    model was able to get right
    receives: 
        1. list containing all the test features
        2. list containing the test results
        3. model to apply
        4. a description of the model 
        5. boolean to indicate if we should oversample
    returns:
        nothing
    """
    # predict
    print('\nstarted evaluating performance of %s' % (model_desc))

    # apply oversampling if we should
    if oversample: 
        (final_test_feature, final_test_result) = apply_oversampling(test_feature, test_result)
    else: 
        (final_test_feature, final_test_result) = (test_feature, test_result)

    prediction_lst = model.predict(final_test_feature)
    assert(len(prediction_lst) == len(final_test_result))

    # discretize prediction
    disc_prediction_lst = []
    for i in range(len(prediction_lst)):
        if prediction_lst[i] < 0.5: 
            disc_prediction_lst.append(0)
        else:
            disc_prediction_lst.append(1)

    # show stats of how many evasions for the test result and the prediction list
    print('test result: ')
    print('\t will evade instances: %d, will not evade: %d' \
            % (final_test_result.count(1), final_test_result.count(0)))
    print('discrete prediction result: ')
    print('\t will evade instances: %d, will not evade: %d' \
            % (disc_prediction_lst.count(1), disc_prediction_lst.count(0)))
    
    # evaluate performance - positive for "will evade"
    true_pos = 0
    true_neg = 0
    false_pos = 0
    false_neg = 0

    for i in range(len(disc_prediction_lst)): 
        # evaluate performance
        if disc_prediction_lst[i] == 0 and final_test_result[i] == 0:
            true_neg += 1
        elif disc_prediction_lst[i] == 1 and final_test_result[i] == 1:
            true_pos += 1
        elif disc_prediction_lst[i] == 0 and final_test_result[i] == 1:
            false_neg += 1
        elif disc_prediction_lst[i] == 1 and final_test_result[i] == 0: 
            false_pos += 1
        else:
            print('error')
            exit()

    # show performance
    print('(true_neg, true_pos, false_neg, false_pos): (%d, %d, %d, %d)' 
            % (true_neg, true_pos, false_neg, false_pos))
    rate = (true_neg + true_pos) / float(true_neg + true_pos + false_neg + false_pos)
    print('the model was right in %f of the cases' % (rate))   

def get_data(stu_info, year_inf, year_sup, semester, enh = False):
    """
    organizes student information in order to feed machine learning model of scikit
    receives:
        1. Student dictionary containing student info
        2. Inferior limit for the year student entered university
        3. Superior limit for the year student entered university
        4. Semester the student is in 
        5. (optional) boolean to indicate whether we should use the enhanced
        functions or not
    returns:
        tuple containing:
            first entrie - list of (list of features). One list of features per student
            second entrie - list of results. One result per student 
    """
    # tuple of outcomes
    features_lst = []
    target_lst = []

    # TODO: could be helpful if we normalize it?
    #if enh: 
    #    normalize_values(stu_info, semester)

    # iterate through every student
    for key, stu in stu_info.items():
        # if student entered in a year we're not interessed, skip
        if stu.year_in < year_inf or stu.year_in > year_sup: 
            continue

        # build student features list and append to student features list
        stu_features = []
        add_feature_sex(stu, stu_features)
        add_feature_age(stu, stu_features)
        add_feature_local(stu, stu_features)
        add_feature_quota(stu, stu_features)
        add_feature_school_type(stu, stu_features)
        add_feature_course(stu, stu_features)
        add_feature_way_in_enh(stu, stu_features)

        add_feature_pass_rate(stu, stu_features, semester)
        add_feature_drop_rate(stu, stu_features, semester)
        add_feature_ira(stu, stu_features, semester)
        add_feature_impr_rate(stu, stu_features, semester)
        add_feature_credit_rate_acc(stu, stu_features, semester)
        add_feature_hard_rate(stu, stu_features, semester)
        #add_feature_condition(stu, stu_features, semester)
        add_feature_position(stu, stu_features, semester)
        features_lst.append(stu_features)

        # add outcome
        add_outcome(stu, target_lst)

    # lists should have equal length
    assert(len(features_lst) == len(target_lst))

    # return 
    return (features_lst, target_lst)

def normalize_values(stu_info, semester):
    """
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

# execute case this is the main file
if __name__ == "__main__":

    # build and run machine learning models
    build_run_models()
