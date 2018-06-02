import os
import numpy as np
import itertools
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from xgboost import XGBRegressor
from config import categorical_columns, VALUE_MODEL_KNN, VALUE_MODEL_XGBOOST, VALUE_MODEL_LR, \
    VALUE_MODEL_RF, VALUE_MODEL_LOGREG, model_info_list, train_feature_file, train_salary_file, \
    test_feature_file, data_path
from preprocessing import preprocessing


def encode_fit(train_feature):
    print("before encoding the feature columns are:")
    print(train_feature.columns)
    train_cols = train_feature.columns.tolist()
    index_arr = [train_cols.index(col) for col in categorical_columns if col in train_cols]
    numerical_cols = list(set(train_cols) - set(categorical_columns))

    enc = OneHotEncoder(categorical_features=index_arr)
    enc.fit(train_feature)
    print(enc.feature_indices_)
    return enc, numerical_cols


def encode_transform_feature(feature_df, enc):
    return enc.transform(feature_df).toarray()


def feature_normalization(feature_df, col, min_value=-1, max_value=-1):
    if col not in feature_df.columns:
        raise Exception("{} column does not exist in the input dataframe!".format(col))

    value_arr = feature_df[col].values
    if max_value < 0:
        min_value = np.min(value_arr)
        max_value = np.max(value_arr)

    norm_value_arr = (value_arr - min_value) / (max_value - min_value)
    feature_df[col] = norm_value_arr
    return feature_df


def feature_transformation(feature_df, enc=None, numerical_cols=[]):
    if enc is None:
        enc, numerical_cols = encode_fit(feature_df)

    for col in numerical_cols:
        feature_df = feature_normalization(feature_df, col)
    feature_array = encode_transform_feature(feature_df, enc)
    return feature_array, enc, numerical_cols


def train_model(x_train, y_train, model_info):
    if model_info[0] == VALUE_MODEL_LR:
        clf = LinearRegression().fit(x_train, y_train)
    elif model_info[0] == VALUE_MODEL_XGBOOST:
        n_estimator = model_info[1][0]
        max_depth = model_info[1][1]
        clf = XGBRegressor(n_estimators=n_estimator, max_depth=max_depth).fit(x_train, y_train)
    elif model_info[0] == VALUE_MODEL_KNN:
        n_neighbors = model_info[1]
        clf = KNeighborsRegressor(n_neighbors).fit(x_train, y_train)
    elif model_info[0] == VALUE_MODEL_RF:
        n_estimator = model_info[1][0]
        max_depth = model_info[1][1]
        clf = RandomForestRegressor(n_estimators=n_estimator, max_depth=max_depth).fit(x_train, y_train)
    elif model_info[0] == VALUE_MODEL_LOGREG:
        clf = LogisticRegression().fit(x_train, y_train)
    return clf


def test_single_model(x, y, model_info, cv_num=5):
    kf = KFold(cv_num)
    true_y = []
    pred_y = []
    for train_index, test_index in kf.split(x):
        x_train, x_test = x[train_index], x[test_index]
        y_train, y_test = y[train_index], y[test_index]
        clf = train_model(x_train, y_train, model_info)
        y_pred = clf.predict(x_test)
        true_y.extend(y_test)
        pred_y.extend(y_pred)
    return true_y, pred_y


def group_data(train_jobTypes):
    # group by jobType
    train_data_dict = dict()
    jobType_list = np.unique(train_jobTypes)
    for jobType in jobType_list:
        index = np.where(train_jobTypes == jobType)[0]
        train_data_dict[jobType] = index
    return train_data_dict


def model_evaluation(train_x_tran, train_y, train_data_dict, model_info_list):
    # jobType-based modelling
    for model_info in model_info_list:
        pred_y = []
        true_y = []
        print("Evaluation for model {}".format(model_info[0]))
        print(model_info[1])
        for jobType, index in train_data_dict.items():
            cur_train_x_tran = train_x_tran[index]
            cur_train_y = train_y[index]
            cur_true_y, cur_pred_y = test_single_model(cur_train_x_tran, cur_train_y, model_info)
            pred_y.extend(cur_pred_y)
            true_y.extend(cur_true_y)
            cur_error = mean_squared_error(cur_true_y, cur_pred_y)
            print("-- MSE for jobType {} is {}".format(jobType, cur_error))
        error = mean_squared_error(true_y, pred_y)
        print("Overall MSE is {}".format(error))


def generate_xgboost_parameters():
    tree_num_list = range(500, 0, -200)
    depth_list = range(5, 2, -1)
    tree_depth_list = list(itertools.product(tree_num_list, depth_list))
    xgboost_model_info = []
    for param in tree_depth_list:
        xgboost_model_info.append((VALUE_MODEL_XGBOOST, list(param)))
    return xgboost_model_info


def main():

    model_data = preprocessing(os.path.join(data_path, train_feature_file),
                               os.path.join(data_path, train_salary_file),
                               os.path.join(data_path, test_feature_file),
                               remove_cols=["companyId", "jobType"])

    train_x = model_data["train"]["features"]
    train_y = np.array(model_data["train"]["labels"])
    train_jobTypes = model_data["train"]["jobTypes"]
    train_data_dict = group_data(train_jobTypes)
    print(train_x.head())

    train_x_tran, _, _ = feature_transformation(train_x)
    print(train_x_tran.shape)

    model_evaluation(train_x_tran, train_y, train_data_dict, model_info_list)


if __name__ == "__main__":
    main()
