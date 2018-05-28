import os
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn import neighbors
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from xgboost import XGBClassifier

from config import categorical_columns
from preprocessing import preprocessing

VALUE_MODEL_LR = "linearReg"
VALUE_MODEL_XGBOOST = "xgbc"
VALUE_MODEL_GNB = "GaussianNB"


def encode_fit(train_feature):
    train_cols = train_feature.columns.tolist()
    index_arr = [train_cols.index(col) for col in categorical_columns if col in train_cols]
    numerical_cols = list(set(train_cols) - set(categorical_columns))

    print("categorical columns: ")
    print([train_cols[id] for id in index_arr])
    print("numerical columns: ")
    print(numerical_cols)

    enc = OneHotEncoder(categorical_features=index_arr)
    enc.fit(train_feature)
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

    #for col in numerical_cols:
    #    feature_df = feature_normalization(feature_df, col)
    #print(feature_df[numerical_cols].head())

    feature_array = encode_transform_feature(feature_df, enc)
    return feature_array


def test_linearReg_model(x, y):
    lr = LinearRegression().fit(x, y)
    y_ = lr.predict(x)
    error = mean_squared_error(y, y_)
    print("Linear regression model error {}".format(error))
    return y_, error


def test_models(x_tran, y, model_name):

    if model_name == VALUE_MODEL_LR:
        clf = LinearRegression()
    elif model_name == VALUE_MODEL_GNB:
        clf = GaussianNB()
    elif model_name == VALUE_MODEL_XGBOOST:
        clf = XGBClassifier()
    scores = cross_val_score(clf, x_tran, y, scoring="neg_mean_squared_error", cv=5)
    return np.mean(-scores)


# def test_knn_model(x, y, n_neighbors):
#     knn = neighbors.KNeighborsRegressor(n_neighbors)
#     cnn_model = knn.fit(x, y)
#     y_ = cnn_model.predict(x)
#     error = mean_squared_error(y, y_)
#     print([n_neighbors, error])
#     return y_, error


# def model_testing(train_x, train_y):
#     # model testing based on one single model
#     enc = encode_fit(train_x)
#     train_x_tran = transform_feature(train_x, enc)
#     test_linearReg_model(train_x_tran, train_y)
#     test_knn_model(train_x, train_y, 3)
#
#     # build jobType-based models
#     pred_y = []
#     act_y = []
#     jobId_list = train_x["jobType"].unique().tolist()
#     for jobId in jobId_list:
#         cur_index = train_x[train_x["jobType"] == jobId].index
#         cur_train_x = train_x.loc[cur_index]
#         cur_train_y = train_y[cur_index]
#         act_y.extend(cur_train_y)
#         print([jobId, len(cur_index)])
#
#         cur_enc = encode_fit(cur_train_x)
#         cur_train_x_tran = transform_feature(cur_train_x, cur_enc)
#         cur_pred, error = test_linearReg_model(cur_train_x_tran, cur_train_y)
#         pred_y.extend(cur_pred)
#     overall_error = mean_squared_error(act_y, pred_y)
#     print(overall_error)


def main():

    data_path = "../data/bangkok_test_data"
    train_feature_file = "train_features_2013-03-07.csv"
    train_salary_file = "train_salaries_2013-03-07.csv"
    test_feature_file = "test_features_2013-03-07.csv"

    model_data = preprocessing(os.path.join(data_path, train_feature_file),
                               os.path.join(data_path, train_salary_file),
                               os.path.join(data_path, test_feature_file),
                               remove_cols=["companyId"])

    train_x = model_data["train"]["features"]
    train_y = model_data["train"]["labels"]
    print(train_x.head())

    train_x_tran = feature_transformation(train_x)
    print(train_x_tran.shape)
    print(train_x_tran[0, -3:])
    for model_name in [VALUE_MODEL_LR]:
        print("running model {}".format(model_name))
        #error = test_models(train_x_tran, train_y, model_name)

        _, error = test_linearReg_model(train_x_tran, train_y)
        print([model_name, error])


if __name__ == "__main__":
    main()
