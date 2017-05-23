#!/usr/bin/python3.4

# TODO: add way to pick the target variable to my code

# this file contain the machine learning algorithms code

# imports
import statistics as stat
import random
import itertools

# multioutput
from sklearn.multioutput import *

# decision tree related
from sklearn import tree 
import pydotplus 
import graphviz
import os 

import sys
sys.path.append('..')
from basic import *

from features import *
from ml_models import *

sys.path.append('../core/')
from students_methods import *



def add_student_features(stu, semester, feat_name_lst, data_desc, filter_data):
    """
    add the relevant student features to a list
    receives: 
        1. student database 
        2. semester which we are trying to predict
        3. list with name of the features
        4. description of the data 
        6. boolean indicating whether we should select the features based on the
        data description
    returns: 
        list containing the student features
    """
    # get list of the functions that the given model excludes
    funcs_excl_model = get_exclude_func_lst(data_desc)
    
    stu_features = []

    # apply functions that don't need the semester
    func_apply_nosemester = [add_feature_sex]
    func_apply_nosemester.append(add_feature_age)
    func_apply_nosemester.append(add_feature_quota)
    func_apply_nosemester.append(add_feature_course)
    func_apply_nosemester.append(add_feature_way_in)
    for cur_func in func_apply_nosemester: 
        if filter_data and cur_func in funcs_excl_model:
            continue
        cur_func(stu, stu_features, feat_name_lst)

    # apply functions that need the semester
    func_apply_semester = [add_feature_pass_rate]
    func_apply_semester.append(add_feature_drop_rate)
    func_apply_semester.append(add_feature_ira)
    func_apply_semester.append(add_feature_impr_rate)
    func_apply_semester.append(add_feature_credit_rate_acc)
    func_apply_semester.append(add_feature_hard_rate)
    func_apply_semester.append(add_feature_condition)
    func_apply_semester.append(add_feature_position)
    for cur_func in func_apply_semester:
        if filter_data and cur_func in funcs_excl_model:
            continue
        cur_func(stu, stu_features, semester, feat_name_lst)

    return stu_features

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

    # for each model, print decision tree for the last semester
    for (data, data_desc) in data_coll: 
        print('starting for data %s' %(data_desc))
        (feat_name, feature_lst, result_lst, key_lst) = \
                get_data(data, data_desc, YEAR_START, YEAR_END, 1, last_sem = True, 
                        filter_model = False)

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

def build_run_ml_models_wrapper():
    """
    builds ml models using sklearn and then run it to evaluate performance
    receives: 
        nothing
    returns: 
        nothing
    """
    # we'll change the global variable to indicate if the model should use
    # retroalimentation or not
    global USE_TAIL, WAY_MODEL_TGT

    # get data collection along with the descriptions
    data_coll = get_model_info()

    # list of semesters being studied
    # it should start with 1, dumbass! 0 we'll get you to the last element of the
    # list
    MAX_NUM_SEM = 20
    sem_lst = [sem for sem in range(1, MAX_NUM_SEM)]

    # we should use model with tail or not
    use_tail_lst = [True, False]

    # ways model can choose the target variable
    way_model_tgt_lst = ['absolute', 'relative']

    # iterate through the options of semester and data collection and to whether model
    # should use retroalimentation or not
    for (sem, cur_data) in itertools.product(sem_lst, data_coll):

        (data, data_desc) = cur_data

        #if data_desc != 'young_students_lic_courses': 
        #    continue

        print('\nstarting study for:')
        print('(sem, data): %d %s ' % (sem, data_desc))

        # iterate through options of using retroalimentation and the way the model
        # picks the target variable
        for (use_tail, way_model_tgt) in 
            itertools.product(use_tail_lst, way_model_tgt_lst):

                # regulate global boolean variables 
                USE_TAIL = use_tail
                WAY_MODEL_TGT = way_model_tgt

                # build and run models
                build_run_ml_models(sem, data, data_desc)

def build_run_ml_models(sem, data, data_desc):
    """
    build and run ml models for a specific semester, data and data description
    receives: 
        1. semester we are in 
        2. data we have
        3. description of the data
    returns:
        nothing
    * prints the performance for each model
    """
    if VERB:
        print('**started getting data necessary for training and test')

    # get training data in the correct form to work with 
    (feat_name, training_feature, training_result, key_train) = \
            get_data(data, data_desc, YEAR_START_TRA, YEAR_END_TRA, sem)

    # get test data
    (feat_name, test_feature, test_result, key_test) = \
            get_data(data, data_desc, YEAR_START_TEST, YEAR_END_TEST, sem)

    # train models
    ml_models = get_ml_models(sem, data, training_feature, training_result, 
            key_train)

    if VERB: 
        print('**(train_size, test_size): (%d, %d)' \
                % (len(training_result), len(test_result)))
        show_class_proportion(training_result, 'training result:')
        #print('**number of features: %d' %(len(training_feature[0])))

    set_evasion_chance(ml_models, key_train, data, training_feature, sem)
    set_evasion_chance(ml_models, key_test, data, test_feature, sem)

    # evaluate performance of the ml techniques - test
    oversample = True
    for (model, model_desc) in ml_models: 
        result = evaluate_performance(data, sem, test_feature, test_result,
                model, model_desc, oversample, key_test)
        print('performance %s: %f' % (model_desc, result))

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
        percentage the model got right
    """
    # semester count should start at 1
    assert(cur_sem >= 1)

    # apply oversampling if we should
    if oversample: 
        (final_test_feature, final_test_result) = \
                apply_oversampling(test_feature, test_result, data)
    else: 
        (final_test_feature, final_test_result) = \
                (test_feature, test_result)

    # predict
    if VERB: 
        print('\nstarted evaluating performance of %s' % (model_desc))
    prediction_lst = model.predict(final_test_feature)
    #print(prediction_lst[0])
    #print(final_test_result[0])
    #exit()

    assert(len(prediction_lst) == len(final_test_result))

    # discretize prediction 
    disc_prediction_lst = get_discrete_prediction(prediction_lst)

    # show stats of how many evasions for the test result and the prediction list
    show_class_proportion(final_test_result, 'final test result: ')
    show_class_proportion(disc_prediction_lst, 'discrete prediction result: ')
    
    # evaluate performance and get percentage of rights 
    right_pct = show_model_perf(final_test_result, disc_prediction_lst)
    
    # return percentage of rights the model got
    return right_pct

def get_data(data, data_desc, year_inf, year_sup, semester, enh = False, 
        last_sem = False, filter_data = True):
    """
    organizes student information in order to feed machine learning model of scikit
    receives:
        1. Student dictionary containing student info
        2. Description of the data we are working with
        3. Inferior limit for the year student entered university
        4. Superior limit for the year student entered university
        5. Semester the student is in 
        6. (optional) boolean to indicate whether we should use the enhanced
        functions or not
        7. (optional) boolean to indicate if we should get the last semester (instead
        of the semester passed as a parameter) or not
        8. (optional) boolean that indicates if we should filter the attributes
        according to the data we are passing
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
    #    normalize_values(data, semester)

    # iterate through every student
    for key, stu in data.items():
        # if student entered in a year we're not interessed, skip
        if stu.year_in < year_inf or stu.year_in > year_sup: 
            continue

        # if the student has already graduated, fill the data with the last semester
        # information. If we should select the last semester, select it!
        if last_sem or semester > stu.get_num_semesters():
            semester = stu.get_num_semesters()

        # build student features list and append to student features list
        stu_features = add_student_features(stu, semester, feat_name_lst, 
                data_desc, filter_data)
        features_lst.append(stu_features)

        # add outcome
        add_outcome(stu, target_lst)

        # add key
        key_lst.append(key)

    # lists should have equal length
    assert(len(features_lst) == len(target_lst) == len(key_lst))

    # return 
    return (feat_name_lst, features_lst, target_lst, key_lst)

def get_ml_models(sem, data, training_feature, training_result, key_train_lst): 
    """
    get a list of the ml models we'll be using. All of them already trained
    receives: 
        1. semester we are interested in 
        2. dictionary containing the student information
        3. list of training features
        4. list of training results
        5. list with the keys of the students in the training features
    returns: 
        list of tuples containing the model and a description of the model. List is
        of the form: [(model, model_description)]
    """
    model_lst = []

    # train models
    get_trained_linear_regressor(model_lst, sem, data, training_feature, training_result,
            key_train_lst)
    get_trained_ann(model_lst, sem, data, training_feature, training_result, 
            key_train_lst)
    get_trained_svr(model_lst, sem, data, training_feature, training_result, 
            key_train_lst)
    #get_trained_random_forest(model_lst, training_feature, training_result)
    #get_trained_naive_bayes(model_lst, training_feature, training_result)

    return model_lst

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

def get_exclude_func_lst(data_desc):
    """
    get the functions that add features function should not consider 
    receives: 
        1. data description we are working with
    returns: 
        list containing the data we are working with 
    """
    POSSIBLE_MODEL_DESC = ['all_students', 'young_students_ti_courses', 
            'young_students_lic_courses', 'young_students_comp_courses', 
            'old_students']
    assert(data_desc in POSSIBLE_MODEL_DESC)

    if data_desc == 'all_students':
        return []
    elif data_desc == 'young_students_ti_courses':
        return []
    elif data_desc == 'young_students_lic_courses':
        return [add_feature_course]
    elif data_desc == 'young_students_comp_courses':
        return []
    elif data_desc == 'old_students':
        return [add_feature_quota, add_feature_course, add_feature_drop_rate]
    else: 
        exit("error on get exclude func lst")

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

def set_evasion_chance(ml_models, key_lst, data, features_lst, sem):
    """
    set the evasion chance for the students on the prediction list
    receives: 
        1. list of tuples containing ml model and description [(ml_model, model_desc)]
        2. list with the key to access the student we are in 
        3. data we currently have 
        4. list of features 
        5. semester we are considering 
    returns: 
        nothing
    """
    # iterate through models
    for (ml_model, model_desc) in ml_models: 

        # get prediction list
        prediction_lst = ml_model.predict(features_lst)

        # set evasion chance
        for ind in range(len(key_lst)): 
            key = key_lst[ind]
            cur_stu = data[key]
            if sem < cur_stu.get_num_semesters(): # needed because student may have
                                                        #left
                cur_stu.evasion_chance[(sem, model_desc)] = prediction_lst[ind]

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
    if VERB: 
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
        percentage of rights the model got
    """
    assert(len(correct_lst) == len(model_lst))
    
    trues, falses = 0, 0
    for cur_pred in range(len(correct_lst)):
        if model_lst[cur_pred] == correct_lst[cur_pred]:
            trues += 1
        else: 
            falses += 1
    total = trues + falses

    if VERB: 
        print('right predictions: %d, wrong predictions: %d' % (trues, falses))
        print('right percentage: %f, wrong percentage: %f' % (trues/total, falses/total))

    return trues/total

def report_best_model_conf():
    """
    report which configuration is better for every model
    receives: 
        nothing
    returns: 
        nothing
    """
    report_best_conf_ann()
    report_best_conf_svr()
    report_best_conf_nb()

# execute case this is the main file
if __name__ == "__main__":

    # get decision tree information
    #analyse_decision_tree()

    # build and run machine learning models
    #build_run_ml_models_wrapper()

    # get report on which parametrization is better for each model 
    #report_best_model_conf()
