import os
import numpy as np


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



def main():
    data_path = "../data/bangkok_test_data"
    train_feature_file = "train_features_2013-03-07.csv"
    train_salary_file = "train_salaries_2013-03-07.csv"
    test_feature_file = "test_features_2013-03-07.csv"

    train_feature = read_feature_data(os.path.join(data_path, train_feature_file))
    print(train_feature.head())

    train_salaries = read_feature_data(os.path.join(data_path, train_salary_file))
    print(train_salaries.head())


    salary_info = company_salary(train_data)
    print(salary_info)

    #company_jobs(train_data)

    print(train_data[train_data["jobType"] == "CEO"][["companyId", "salary"]].groupby("companyId").mean())

    #test_feature = read_feature_data(os.path.join(data_path, test_feature_file))

if __name__ == "__main__":
    main()