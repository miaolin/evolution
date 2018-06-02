import os
import pandas as pd
import numpy as np
from config import categorical_columns, mean_salary_columns, with_none_columns, \
    data_path, train_feature_file, train_salary_file, test_feature_file


def read_data(file_path):
    return pd.read_csv(file_path)


def convert_category_to_int(data, column_name, value_dict={}):
    if column_name not in data.columns:
        return data, _

    if len(value_dict) == 0:
        value_types = data[column_name].unique().tolist()
        value_dict = dict(zip(value_types, range(len(value_types))))
        if column_name == "jobType":
            print(value_dict)
    int_arr = [value_dict[cat] for cat in data[column_name].values]
    data[column_name] = int_arr
    return data, value_dict


def convert_features(train_data, test_data):
    # map string value features to int
    value_dict_dict = {}
    for col in categorical_columns:
        train_data, value_dict = convert_category_to_int(train_data, col)
        test_feature, _ = convert_category_to_int(test_data, col, value_dict)
        value_dict_dict[col] = value_dict
    return train_data, test_data, value_dict_dict


def prepare_model_data(data, data_type, remove_cols=[]):
    # data_type = "train" or "test"
    jobTypes_arr = data["jobType"].values
    if len(remove_cols) > 0:
        for col in remove_cols:
            if col in data.columns:
                data.drop(columns=col, inplace=True)

    jobId_arr = data["jobId"].values
    if data_type == "train":
        data_features = data.drop(columns=["jobId", "salary"])
        return jobId_arr, data_features, data["salary"].values, jobTypes_arr
    elif data_type == "test":
        data_features = data.drop(columns="jobId")
        return jobId_arr, data_features, np.array([]), jobTypes_arr
    else:
        raise Exception("unknown data type!")


def calculate_salary_info(train_data, col_name):
    # mean salary per column
    new_col_name = "mean_salary_" + col_name
    mean_salary = train_data[[col_name, "salary"]].groupby(col_name).mean()
    mean_salary.reset_index(inplace=True)
    mean_salary.rename(columns={"salary": new_col_name}, inplace=True)
    return mean_salary


def add_indicator_features(data_df, column, zero_values="NONE"):
    column_name = column + "_indicator"
    column_values = data_df[column].values
    indicator_values = [0 if value == zero_values else 1 for value in column_values]
    data_df[column_name] = indicator_values
    return data_df


def remove_zero_salary(train_data):
    if not train_data[train_data["salary"] == 0].empty:
        print("before data cleaning the number of rows is {}".format(len(train_data)))
        train_data = train_data[train_data["salary"] > 0]
        train_data.reset_index(drop=True, inplace=True)
        print("after data cleaning the number of rows is {}".format(len(train_data)))
    return train_data


def remove_all_nones(train_data, value_dict_dict):

    all_index = []
    for col in with_none_columns:
        value_dict = value_dict_dict[col]
        none_value = value_dict["NONE"]
        remove_index = train_data[train_data[col] == none_value].index
        if len(all_index) == 0:
            all_index = remove_index
        else:
            all_index = list(set(all_index).intersection(set(remove_index)))

    train_data.drop(all_index, inplace=True)
    print("after removing both none rows, the number of rows is {}".format(len(train_data)))
    train_data.reset_index(drop=True, inplace=True)
    return train_data


def preprocessing(train_data_path, train_label_path, test_data_path, remove_cols=["companyId"], print_flag=False):

    # step 1. load all the data
    train_data = read_data(train_data_path)
    train_labels = read_data(train_label_path)

    # step 2. merge train data with training labels
    train_data = pd.merge(train_data, train_labels, how='left')
    if print_flag:
        print(train_data.columns)

    # step 4. load test data
    test_data = read_data(test_data_path)

    # step 5. add mean salary features
    for col in mean_salary_columns:
        salary_info = calculate_salary_info(train_data, col)
        if print_flag:
            print(salary_info)
        train_data = pd.merge(train_data, salary_info, how="left", on=col)
        test_data = pd.merge(test_data, salary_info, how="left", on=col)

    # step 6. add two indicator features
    # column: with_degree, values={0, 1}
    # column: with_major, values={0, 1}
    for column in with_none_columns:
        train_data = add_indicator_features(train_data, column)
        test_data = add_indicator_features(test_data, column)

    # step 7. convert string-value features to int-value features
    train_data, test_data, value_dict_dict = convert_features(train_data, test_data)

    # step 8. data cleaning
    # remove jobs with zero salary
    train_data = remove_zero_salary(train_data)

    if print_flag:
        correlation_analysis(train_data)

    # step 8
    model_data = dict()
    for data_type in ["train", "test"]:
        if data_type == "train":
            data = train_data
        elif data_type == "test":
            data = test_data
        ids, features, labels, jobType_arr = prepare_model_data(data, data_type, remove_cols)
        model_data[data_type] = {"ids": ids, "features": features, "labels": labels,
                                 "jobTypes": jobType_arr}
    return model_data


def correlation_analysis(train_data):
    numerical_cols = list(set(list(train_data.columns)) - set(categorical_columns + ["jobId"]))

    corr_matrix = train_data[numerical_cols].corr()
    print(corr_matrix.columns)
    for col in numerical_cols:
        print(corr_matrix[col])


def main():

    model_data = preprocessing(os.path.join(data_path, train_feature_file),
                               os.path.join(data_path, train_salary_file),
                               os.path.join(data_path, test_feature_file),
                               remove_cols=["companyId", "jobType"], print_flag=True)


if __name__ == "__main__":
    main()
