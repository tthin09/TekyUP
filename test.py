import pandas as pd

df = pd.read_excel("student.xlsx")
print(df.to_dict(orient='records'))