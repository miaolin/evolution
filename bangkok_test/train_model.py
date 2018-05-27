import os
from sklearn.preprocessing import OneHotEncoder
from sklearn import neighbors
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from config import categorical_columns
from preprocessing import preprocessing


def encode_fit(train_feature):
    train_cols = train_feature.columns.tolist()
    index_arr = [train_cols.index(col) for col in categorical_columns if col in train_cols]
    print(index_arr)

    enc = OneHotEncoder(categorical_features=index_arr)
    enc.fit(train_feature)
    print(enc.feature_indices_)
    print(enc.n_values_)
    return enc


def transform_feature(feature_df, enc):
    return enc.transform(feature_df).toarray()


def test_linearReg_model(x, y):
    lr = LinearRegression().fit(x, y)
    y_ = lr.predict(x)
    error = mean_squared_error(y, y_)
    print("Linear regression model error {}".format(error))
    print(y[:5])
    print(y_[:5])


def test_knn_model(x, y, n_neighbors):
    knn = neighbors.KNeighborsRegressor(n_neighbors)
    cnn_model = knn.fit(x, y)
    y_ = cnn_model.predict(x)
    error = mean_squared_error(y, y_)
    print([n_neighbors, error])


def model_testing(train_x, train_y):

    # features transformation
    enc = encode_fit(train_x)
    train_x_tran = transform_feature(train_x, enc)

    test_linearReg_model(train_x_tran, train_y)

    test_knn_model(train_x, train_y, 3)


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
    model_testing(train_x, train_y)


if __name__ == "__main__":
    main()
