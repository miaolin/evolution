import os
import pandas as pd
from config import categorical_columns


def read_data(file_path):
    return pd.read_csv(file_path)


def convert_category_to_int(data, column_name, value_dict={}):
    if column_name not in data.columns:
        return data, _

    if len(value_dict) == 0:
        value_types = data[column_name].unique().tolist()
        value_dict = dict(zip(value_types, range(len(value_types))))
        print(value_dict)
    int_arr = [value_dict[cat] for cat in data[column_name].values]
    data[column_name] = int_arr
    return data, value_dict


def convert_features(train_data, test_data):
    # map string value features to int
    for col in categorical_columns:
        train_data, value_dict = convert_category_to_int(train_data, col)
        test_feature, _ = convert_category_to_int(test_data, col, value_dict)
    return train_data, test_data


def prepare_model_data(data, data_type, remove_cols=[]):
    # data_type = "train" or "test"
    # "companyId"
    if len(remove_cols) > 0:
        for col in remove_cols:
            if col in data.columns:
                data.drop(columns=col, inplace=True)

    jobId_arr = data["jobId"].values
    if data_type == "train":
        data_features = data.drop(columns=["jobId", "salary"])
        return jobId_arr, data_features, data["salary"].values
    elif data_type == "test":
        data_features = data.drop(columns="jobId")
        return jobId_arr, data_features, []
    else:
        raise Exception("unknown data type!")


def preprocessing(train_data_path, train_label_path, test_data_path, remove_cols=["companyId"]):

    # step 1. load all the data
    train_data = read_data(train_data_path)
    train_labels = read_data(train_label_path)

    # step 2. merge train data with training labels
    train_data = pd.merge(train_data, train_labels, how='left')
    print(train_data.columns)

    # step 3. load test data
    test_data = read_data(test_data_path)

    # step 4. convert string-value features to int-value features
    train_data, test_data = convert_features(train_data, test_data)
    correlation_analysis(train_data)

    # step 5
    model_data = dict()
    for data_type in ["train", "test"]:
        if data_type == "train":
            data = train_data
        elif data_type == "test":
            data = test_data
        print(data_type)
        print(data.columns)
        ids, features, labels = prepare_model_data(data, data_type, remove_cols)
        model_data[data_type] = {"ids": ids, "features": features, "labels": labels}
    return model_data


def correlation_analysis(train_data):
    for col in train_data.columns:
        if col in ["jobId", "salary"]:
            continue
        cor = train_data[col].corr(train_data["salary"])
        print([col, cor])


def main():

    data_path = "indeed_data_science_exercise_data"
    train_feature_file = "train_features_2013-03-07.csv"
    train_salary_file = "train_salaries_2013-03-07.csv"
    test_feature_file = "test_features_2013-03-07.csv"

    model_data = preprocessing(os.path.join(data_path, train_feature_file),
                               os.path.join(data_path, train_salary_file),
                               os.path.join(data_path, test_feature_file),
                               remove_cols=["companyId"])


if __name__ == "__main__":
    main()
