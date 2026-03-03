import pandas as pd

df = pd.read_csv("data.csv")
val = df.head()
#print(val)


val_2 = df.tail()
#print(val_2)


info = df.info()
#print(df.info())


desc = df.describe()
#print(desc)

score_column = df["score"]
#print("single column(score):")
#print(score_column)

selected_columns = df[[ "name","score"]]

#print("Multiple Columns (name and score):")
#print(selected_columns)

filtered_rows = df[["name","score"]]

print("Flitered rows (Score > 80):")
print(filtered_rows)

