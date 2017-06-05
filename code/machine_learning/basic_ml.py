# basic definitions for the module of machine learning

# should we be verbose?
VERB = 0

# indices in a list that correspond to the graduation risk, evasion risk and
# migration risk
GRAD_IND = 0
EVADE_IND = 1
MIGR_IND = 2

# lists of the form (<graduation risk>, <evasion_risk>, <migration_risk>)
GRADUATED = [1, 0, 0]
EVADED = [0, 1, 0]
MIGRATED = [0, 0, 1]

# code for people that didn't graduate - migration or evasion
NOT_GRADUATED = -1

# path and name of the pickle object consisting of the ml model
PCK_ML_MODEL = './data/perf_ml_model'

# path and name of the pickle object consisting of all models
OPT_PCK_ML_MODEL = './data/all_conf_ml_models'

# number of k fold for cross validation
NUM_KFOLD = 10
