#!/usr/bin/python3.4

# this file contain the machine learning algorithms code

# imports
import statistics as stat

from sklearn.neural_network import *
from sklearn.svm import SVR

import sys
sys.path.append('..')
from basic import *

from features import *

sys.path.append('../core/')
from students_methods import *

# TODO: were quotes institutionalized too recently? is this a problem?
# TODO: test instances refer primarily to students that dropped out, while training
# is not 

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
    sem_lst = [1]

    # iterate through the semesters
    for semester in sem_lst:
        print('starting study for semester: %d' % (semester))
        print('started getting data necessary for training and test')

        for enh in [False, True]:
            print('\nstarting training with enh = %s' % (str(enh)))

            # get training data in the correct form to work with 
            (training_feature, training_result) = get_data(stu_info, YEAR_START_TRA, \
                                                    YEAR_END_TRA, semester, enh)
            # get test data
            (test_feature, test_result) = get_data(stu_info, YEAR_START_TEST, \
                                                    YEAR_END_TEST, semester, enh)

            #print('training feature follow:\n')
            #print(training_feature)
            #print('\n\ntraining result follow:\n')
            #print(training_result)
            #print('\n\ntest feature follow:\n')
            #print(test_feature)
            #print('\n\ntest result follow:\n')
            #print(test_result)

            # train multilayer perceptron model 
            regressor = MLPRegressor()
            print('started training ANN')
            regressor.fit(training_feature, training_result)

            # train svr
            svr = SVR()
            print('started training SVR')
            svr.fit(training_feature, training_result)

            evaluate_performance(test_feature, test_result, regressor, 'ANN')
            evaluate_performance(test_feature, test_result, svr, 'SVR')

def evaluate_performance(test_feature, test_result, model, model_desc):
    """
    evaluates the performance of a model, by showing how many test instances the
    model was able to get right
    """
    # predict
    print('started evaluating performance of %s' % (model_desc))
    prediction_lst = model.predict(test_feature)
    assert(len(prediction_lst) == len(test_result))

    # evaluate performance
    num_misses = 0
    num_rights = 0
    for i in range(len(prediction_lst)):
        # discretize prediction
        if prediction_lst[i] < 0.5: 
            prediction = 0
        else:
            prediction = 1

        # evaluate performance
        if prediction == test_result[i]:
            num_rights += 1
        else:
            num_misses += 1

    # show performance
    rate = num_rights / float((num_rights + num_misses))
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

    if enh: 
        normalize_values(stu_info, semester)

    # iterate through every student
    for key, stu in stu_info.items():
        # if student entered in a year we're not interessed, skip
        if stu.year_in < year_inf or stu.year_in > year_sup: 
            continue

        # build student features list and append to student features list
        # TODO: could be helpful if we normalize it?
        stu_features = []
        if not enh: 
            add_feature_quota(stu, stu_features)
        else: 
            add_feature_quota_enh(stu, stu_features)
        add_feature_sex(stu, stu_features)
        add_feature_age(stu, stu_features)
        add_feature_age(stu, stu_features)
        add_feature_local(stu, stu_features)
        add_feature_school_type(stu, stu_features)
        add_feature_course(stu, stu_features)
        add_feature_way_in_enh(stu, stu_features)
        add_feature_pass_rate(stu, stu_features, semester)
        #add_feature_drop_rate(stu, stu_features)
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
