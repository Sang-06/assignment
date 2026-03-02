import pandas as pd

df = pd.read_csv("data.csv")
val = df.head()
#print(val)


val_2 = df.tail()
#print(val_2)


info = df.info()
#print(df.info())


desc = df.describe()
print(desc)
