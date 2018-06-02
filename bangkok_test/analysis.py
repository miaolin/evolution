import os
import pandas as pd
import numpy as np
from preprocessing import read_data
from config import data_path, train_feature_file, train_salary_file


def company_salary(train_data):
    company_list = train_data["companyId"].unique().tolist()
    salary_info = {}
    for company in company_list:
        salary_arr = train_data[train_data["companyId"] == company]["salary"].values
        info = [np.mean(salary_arr), np.std(salary_arr)]
        salary_info[company] = info
    return salary_info


def company_jobs(train_data):
    company_list = train_data["companyId"].unique().tolist()
    for company in company_list:
        job_type_arr = train_data[train_data["companyId"] == company]["jobType"].values
        print(company)
        print(np.unique(job_type_arr, return_counts=True))


def salary_by_types(train_data, column):

    with_degree_mean = train_data[train_data[column] != "NONE"]["salary"].mean()
    with_degree_std = train_data[train_data[column] != "NONE"]["salary"].std()

    none_degree_mean = train_data[train_data[column] == "NONE"]["salary"].mean()
    none_degree_std = train_data[train_data[column] == "NONE"]["salary"].std()
    print("with {} mean salary {} and std salary {}".format(column, with_degree_mean, with_degree_std))
    print("without {} mean salary {} and std salary {}".format(column, none_degree_mean, none_degree_std))


def main():

    train_feature = read_data(os.path.join(data_path, train_feature_file))
    print(train_feature.head())

    train_salaries = read_data(os.path.join(data_path, train_salary_file))
    print(train_salaries.head())

    train_data = pd.merge(train_feature, train_salaries, how="left", on="jobId")
    print(train_data.head())

    salary_info = company_salary(train_data)
    print(salary_info)

    salary_by_types(train_data, "degree")

    salary_by_types(train_data, "major")
    company_jobs(train_data)


if __name__ == "__main__":
    main()