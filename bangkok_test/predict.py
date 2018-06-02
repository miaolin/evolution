import os
import numpy as np
import pandas as pd
from preprocessing import preprocessing
from train_model import group_data, feature_transformation, train_model
from config import best_model_info, data_path, train_feature_file, train_salary_file, test_feature_file


def prediction(train_x_tran, train_y, train_data_dict, test_x_tran, test_data_dict):
    # jobType-based modelling
    pred_y_list = []
    print("Prediction based on model {}".format(best_model_info[0]))
    print(best_model_info[1])
    for jobType, index in train_data_dict.items():
        print("jobType is {}".format(jobType))
        cur_train_x_tran = train_x_tran[index]
        cur_train_y = train_y[index]

        cur_test_index = test_data_dict[jobType]
        cur_test_x_tran = test_x_tran[cur_test_index]
        cur_clf = train_model(cur_train_x_tran, cur_train_y, best_model_info)
        print(cur_clf.feature_importances_)
        cur_pred = cur_clf.predict(cur_test_x_tran)
        pred_df = pd.DataFrame({"index": cur_test_index, "predict_salary": cur_pred})
        pred_df["predict_salary"] = pred_df["predict_salary"].astype(int)
        pred_y_list.append(pred_df)
    return pd.concat(pred_y_list).reset_index(drop=True)


def generate_results(model_data, result_file_path):

    # prepare training data
    train_x = model_data["train"]["features"]
    train_y = np.array(model_data["train"]["labels"])
    train_jobTypes = model_data["train"]["jobTypes"]

    train_data_dict = group_data(train_jobTypes)
    train_x_tran, enc, numerical_cols = feature_transformation(train_x)
    print(train_x_tran.shape)

    # prepare test data
    test_x = model_data["test"]["features"]
    test_jobTypes = model_data["test"]["jobTypes"]
    test_data_dict = group_data(test_jobTypes)
    test_x_tran, _, _ = feature_transformation(test_x, enc, numerical_cols)

    pred_df = prediction(train_x_tran, train_y, train_data_dict, test_x_tran, test_data_dict)

    # merge results with jobId
    result_df = pd.DataFrame({"jobId": model_data["test"]["ids"], "salary": -1})
    pred_index = pred_df["index"].values
    pred_salary = pred_df["predict_salary"].values
    result_df.loc[pred_index, "salary"] = pred_salary
    result_df.to_csv(result_file_path, index=False)


def main():

    result_file = "test_salaries.csv"

    model_data = preprocessing(os.path.join(data_path, train_feature_file),
                               os.path.join(data_path, train_salary_file),
                               os.path.join(data_path, test_feature_file),
                               remove_cols=["companyId", "jobType"])

    generate_results(model_data, result_file)


if __name__ == "__main__":
    main()