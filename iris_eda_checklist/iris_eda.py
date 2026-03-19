import pandas as pd
import plotly.express as px

#have loaded dataset copied from the link and created a folder iris.csv

df = pd.read_csv("iris.csv")

#1 have inspected data structure

#print("first 5 rows:")
#print(df.head())

#print("\nshapr of dataset:")
#print(df.shape)

#print("\ncolumn names:")
#print(df.columns)

#observed Dataset has 150 rows and 5 columns including species

#2 now check column info and missing values

#print("\ndataset info:")
#print(df.info())

#print("\nmissing values:")
#print(df.isnull().sum())

#print("\nstatistical summary:")
#print(df.describe())

#observed no missing values found dataset is clean

#3 analysis of one feature petal length

#fig1 = px.histogram(df, x="petal_length", color="species",
                    #title="Distribution of Petal Length")
#fig1.show()

#observed setosa has very small petal length compared to others

#4 outlier detection

#fig2 = px.box(df, y="petal_length", color="species", title="Boxplot for Petal Length")
#fig2.show()

#observed virginica shows wider variation, few extreme values

#5 relation between variables

#fig3 = px.scatter(df, x="petal_length", y="petal_width",
                  #color="species",
                  #title="Petal Length vs Petal Width")
#fig3.show()

#observed strong positive correlation and clear separation of species

#6 correlation analysis

corr = df.corr(numeric_only=True)
print("\nCoreelation Matrix:")
print(corr)
