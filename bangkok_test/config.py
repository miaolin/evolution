
data_path = "../data/bangkok_test_data"
train_feature_file = "train_features_2013-03-07.csv"
train_salary_file = "train_salaries_2013-03-07.csv"
test_feature_file = "test_features_2013-03-07.csv"

categorical_columns = ["companyId", "jobType", "degree", "major", "industry"]
with_none_columns = ["degree", "major"]

# all the columns
## Exclude column: mean_salary_yearsExperience
# this one has high correlation with yearsExperience: 0.99
## Exclude column: mean_salary_major
# has high correlation with mean_salary_degree: 0.85
# mean_salary_columns = ["jobType", "degree", "major", "industry", "yearsExperience"]
mean_salary_columns = ["jobType", "degree", "industry"]


VALUE_MODEL_LR = "linearReg"
VALUE_MODEL_XGBOOST = "xgbc"
VALUE_MODEL_KNN = "knn"
VALUE_MODEL_LOGREG = "logisticReg"
VALUE_MODEL_RF = "randomforest"


model_info_list = [(VALUE_MODEL_LR, []),
                   (VALUE_MODEL_XGBOOST, [100, 3]),
                   (VALUE_MODEL_XGBOOST, [100, 4]),
                   (VALUE_MODEL_XGBOOST, [100, 5]),
                   (VALUE_MODEL_XGBOOST, [100, 3]),
                   (VALUE_MODEL_XGBOOST, [200, 4]),
                   (VALUE_MODEL_XGBOOST, [200, 5]),
                   (VALUE_MODEL_XGBOOST, [100, 3]),
                   (VALUE_MODEL_XGBOOST, [300, 4]),
                   (VALUE_MODEL_XGBOOST, [300, 5])]

best_model_info = (VALUE_MODEL_XGBOOST, [300, 3])

