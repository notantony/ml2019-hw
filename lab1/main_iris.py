# %%
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

import kernels
import knn

# %%
data = pd.read_csv("https://www.openml.org/data/get_csv/21756804/iris.arff")
data.head()

# %%
data["class"] = pd.factorize(data["class"])[0]

n_classes = 3
data.head()

# %%
x_train, x_test, y_train, y_test = \
    train_test_split(data.drop("class", axis=1), data["class"], test_size=0.33, random_state=1)

print("train: {} samples, test: {} samples".format(len(x_train), len(x_test)))

# %%
dist_fs = [kernels.euclidean]
kernel_fs = [kernels.uniform, kernels.gaussian, kernels.cosine, kernels.logistic, kernels.sigmoid]

# %%
LEARN = False

if LEARN:
    ks = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12]
    for k in ks:
        for dist_f in dist_fs:
            for kernel_f in kernel_fs:
                result = np.zeros((n_classes, n_classes))
                margins = []
                for i, sample in x_train.iterrows():
                    model = knn.KNN(x_train.drop(i), y_train.drop(i), k=k, dist_f=dist_f, kernel_f=kernel_f)
                    predict_y, margin = model.run(sample, y_train[i])
                    margins.append(margin)
                    result[predict_y][y_train[i]] += 1
                print("{:6} : k={:3}, dist={:8}, kernel={:8}".format(kernels.f_score(result)[0], k, dist_f.__name__, kernel_f.__name__))

if LEARN:
    ds = [0.01, 0.1, 0.5, 1.0, 2.0, 4.0, 6.0, 8.0, 12.0]
    for d in ds:
        for dist_f in dist_fs:
            for kernel_f in kernel_fs:
                result = np.zeros((n_classes, n_classes))
                margins = []
                for i, sample in x_train.iterrows():
                    model = knn.KNN(x_train.drop(i), y_train.drop(i), d=d, dist_f=dist_f, kernel_f=kernel_f)
                    predict_y, margin = model.run(sample, y_train[i])
                    margins.append(margin)
                    result[predict_y][y_train[i]] += 1
                print("{:6} : d={:5}, dist={:8}, kernel={:8}".format(kernels.f_score(result)[0], d, dist_f.__name__, kernel_f.__name__))

# %%
k = 8
dist_f = kernels.chebyshev
kernel_f = kernels.cosine

result = np.zeros((n_classes, n_classes))
margins = []

model = knn.KNN(x_test, y_test, k=k, dist_f=dist_f, kernel_f=kernel_f)

for i, sample in x_test.iterrows():
    predict_y, margin = model.run(sample, y_test[i])
    result[predict_y][y_test[i]] += 1
    margins.append(margin)
print("{} : k={}, dist={}, kernel={}".format(kernels.f_score(result)[0], k, dist_f.__name__, kernel_f.__name__))
sns.kdeplot(margins)

# %%
train_margins = pd.Series(margins)

def get_filtered(border):
    x_filtered = x_train[(train_margins > border).values]
    y_filtered = y_train[(train_margins > border).values]
    return x_filtered, y_filtered

x_filtered0, y_filtered0 = get_filtered(0)
x_filtered3, y_filtered3 = get_filtered(-3)
x_filtered5, y_filtered5 = get_filtered(-5)
x_filtered7, y_filtered7 = get_filtered(-7)
x_filtered9, y_filtered9 = get_filtered(-9)


# %%
def run_test(k, dist_f, kernel_f, x_train, y_train, name):
    result = np.zeros((n_classes, n_classes))
    margins = []
    model = knn.KNN(x_train, y_train, k=k, dist_f=dist_f, kernel_f=kernel_f)
    for i, sample in x_test.iterrows():
        predict_y, margin = model.run(sample, y_test[i])
        result[predict_y][y_test[i]] += 1
        margins.append(margin)
    print(result)
    print("{} : k={}, dist={}, kernel={}, name={}".format(kernels.f_score(result)[0], k, dist_f.__name__, kernel_f.__name__, name))
    sns.kdeplot(margins)


run_test(4, kernels.euclidean, kernels.logistic, x_train, y_train, "train")
run_test(4, kernels.euclidean, kernels.logistic, x_filtered0, y_filtered0, "filtered0")
run_test(4, kernels.euclidean, kernels.logistic, x_filtered3, y_filtered3, "filtered3")
run_test(4, kernels.euclidean, kernels.logistic, x_filtered5, y_filtered5, "filtered5")
run_test(4, kernels.euclidean, kernels.logistic, x_filtered7, y_filtered7, "filtered7")
run_test(4, kernels.euclidean, kernels.logistic, x_filtered9, y_filtered9, "filtered9")



# %%
