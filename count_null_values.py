import pandas as pd

file_name = "Oracle DB Check n Detail Aug2023.xlsx"


# Load the Excel file into a dictionary of DataFrames
excel_data = pd.read_excel(file_name, sheet_name=None)

# print(excel_data)
# print(excel_data.items())

for sheet_name, df in excel_data.items():
    total_rows = df.shape[0]
    print(f"Sheet Name: {sheet_name}")
    # columns= list(df)
    # print(df.columns)
    for column in df.columns:
        # print(df[column])
        # if column == "menuItemName2":
        #     data = list(df[column])
            # print(df[column])
            # print(data)
        null_count = 0
        """Count null values in each column/attribute"""
        # for value in df[column]:
        #     # print(df[column])
        #     if not value or value == "":
        #         # print(value)
        #         null_count += 1
        null_count = df[column].isnull().sum() + (df[column] == '').sum() + (df[column] == 'NULL').sum() + (df[column] == ' ').sum()
        percentage_of_null = round((null_count / total_rows) * 100, 2)
        print(f"Column: {column}, NullCount: {null_count}, NullPercentage: {percentage_of_null} %")
