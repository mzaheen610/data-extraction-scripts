"""
Generating DBML code for generating relation between entities from excel data.
"""

import pandas as pd


filepath = r"Outsystems Entity-Field Data Model_V2.xlsx"


file = pd.ExcelFile(filepath)
sheet_names = file.sheet_names

print(sheet_names)


def getDataFromSheets():
    sheet_name = 'Table Summary'
    df = pd.read_excel(filepath, sheet_name)
    # print(df)
    # sheet_name = sheet_names[2]
    columns = df.columns.tolist()
    print(columns)

    # field_names = df['Field label'].tolist()
    # data_types = df['DataType'].tolist()

    table_names = df['OS Table'].tolist()
    primary_key_fields = df['OS Primary Key'].tolist()

    print(len(table_names))
    print(len(primary_key_fields))

    mapping_list = []

    for table, field in zip(table_names, primary_key_fields):
        statement = f"{table}" + "." + f"{field}"
        mapping_list.append(statement)
    # generateDBMLcode(field_names, data_types, sheet)

    print(mapping_list)

getDataFromSheets()
