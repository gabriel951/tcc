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

# number of k fold for cross validation - not needed anymore
# NUM_KFOLD = 10

# year to start and year to end the training for the validation step
YEAR_START_TRA_VAL = 2000
YEAR_END_TRA_VAL = 2006
YEAR_START_VAL = 2007
YEAR_END_VAL = 2009

# maximum number of iterations for our ml model
MAX_ITER = 100

# confidence interval we are interested in 
CONF_INT = 0.95
