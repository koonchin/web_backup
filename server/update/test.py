import pandas as pd

df = pd.read_excel('Order_2021-12-12_20211220141943.xlsx')
for i in df.columns:
    print(i)
