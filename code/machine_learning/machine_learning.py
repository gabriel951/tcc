#!/usr/bin/python3.4

# this file contain the machine learning algorithms code

# imports
import statistics as stat
import random

from sklearn.neural_network import *
from sklearn.svm import SVR
from sklearn import linear_model

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

    # training data proportion of students able to graduate 
    TRAIN_PROP_STU_GRA = 0.55
    TEST_PROP_STU_GRA = 0.18

    # get amount of students on test feature able to graduate and amount that was not
    # able to graduate
    stu_able_grad = 0
    for i in range(len(test_result)):
        if test_result[i] == GRADUATED: 
            stu_able_grad += 1

    # calculate number of test features to be oversampled so that the proportion can be
    # equal to the training proportion
    features_graduate = round(len(test_result) * (1 - TRAIN_PROP_STU_GRA))
    oversamples = features_graduate - stu_able_grad

    # list of indexes to add 
    samples_to_add = []

    # add samples to the test feature and test result list
    while len(samples_to_add) < oversamples:

        # get random sample 
        ind = random.randrange(len(test_feature))

        # be sure sample is of a student that graduated and add it 
        if test_result[ind] == GRADUATED: 
            samples_to_add.append(ind)

    # append the samples to add
    for i in samples_to_add:
        test_feature.append(test_feature[i])
        test_result.append(test_result[i])

    print('new test size: %d' % (len(test_result)))
    print('finished oversampling')

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

        # get training data in the correct form to work with 
        (training_feature, training_result) = get_data(stu_info, YEAR_START_TRA, \
                                                YEAR_END_TRA, semester)
        # get test data
        (test_feature, test_result) = get_data(stu_info, YEAR_START_TEST, \
                                                YEAR_END_TEST, semester)

        print('(train_size, test_size): (%d, %d)' \
                % (len(training_result), len(test_result)))

        # train multilayer perceptron model 
        regressor = MLPRegressor()
        print('started training ANN')
        regressor.fit(training_feature, training_result)

        # train svr
        svr = SVR()
        print('started training SVR')
        svr.fit(training_feature, training_result)

        # train linear model 
        linear_regressor = linear_model.LinearRegression()
        print('started training linear regressor')
        linear_regressor.fit(training_feature, training_result)

        evaluate_performance(test_feature, test_result, regressor, 'ANN')
        evaluate_performance(test_feature, test_result, svr, 'SVR')
        evaluate_performance(test_feature, test_result, svr, 'Linear Regressor')

def evaluate_performance(test_feature, test_result, model, model_desc):
    """
    evaluates the performance of a model, by showing how many test instances the
    model was able to get right
    receives: 
        1. list containing all the test features
        2. list containing the test results
        3. model to apply
        4. a description of the model 
    returns:
        nothing
    """
    # predict
    print('\nstarted evaluating performance of %s' % (model_desc))

    # apply oversampling 
    (oversampled_feature, oversample_result) = apply_oversampling(test_feature, test_result)

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
        #add_feature_sex(stu, stu_features)
        #add_feature_age(stu, stu_features)
        #add_feature_local(stu, stu_features)
        #add_feature_quota(stu, stu_features)
        #add_feature_school_type(stu, stu_features)
        #add_feature_course(stu, stu_features)
        #add_feature_way_in_enh(stu, stu_features)
        #add_feature_pass_rate(stu, stu_features, semester)
        #add_feature_drop_rate(stu, stu_features, semester)
        #add_feature_ira(stu, stu_features, semester)
        #add_feature_impr_rate(stu, stu_features, semester)
        add_feature_credit_rate_acc(stu, stu_features, semester)
        #add_feature_hard_rate(stu, stu_features, semester)
        #add_feature_condition(stu, stu_features, semester)
        #add_feature_position(stu, stu_features, semester)
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
