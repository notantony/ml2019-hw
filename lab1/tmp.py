import numpy as np
import pandas as pd


# qwe = pd.DataFrame()
# qwe.iterrows()
# qwe.columns

# asd = np.ndarray()

# np.asarray

a = pd.Series([3, 0, 0])
b = pd.Series([0, 4, 0])

x = pd.DataFrame([[6, 5, 6], [1, 2, 4]], columns=["a", "b", "c"])
# print(x)
# print(x.iloc[0, 1])

print(x["a"])
print(type(x["a"]))
print(a[0]) 


