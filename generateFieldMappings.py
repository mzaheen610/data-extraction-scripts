import pandas as pd


filepath = "Outsystems Entity-Field Data Model_V2 (2).xlsx"


file = pd.ExcelFile(filepath)
sheet_names = file.sheet_names

# print(sheet_names)


data_type_mapping = {
    'Number': 'numeric',
    'Name': 'string',
    'Picklist': 'string',
    'Record Type': 'string',
    'Hierarchy': 'string',
    'Address': 'string',
    'Phone': 'string',
    'Fax': 'string',
    'Text': 'string',
    'URL': 'string',
    'Currency': 'numeric',
    'Long Text Area': 'string',
    'Content': 'string',
    'Lookup': 'string',
    'Date/Time': 'datetime',
    'Date': 'date',
    'Lookup': 'string',
    'Checkbox': 'boolean',
    'External Lookup': 'string',
}

def map_data_type(data_type):
    return data_type_mapping.get(data_type, 'string')


field_names = []
data_types = []

references_code = ""

def getDataFromSheets(sheet_names):
    for sheet in sheet_names[1::]:
        df = pd.read_excel(filepath, sheet_name=sheet)
        # print(sheet)
        # sheet_name = sheet_names[2]
        columns = df.columns.tolist()
        # print(columns)
        try:
            field_names = df['Field label'].tolist()
            data_types = df['DataType'].tolist()
        except:
            continue
        # print(field_names)
        # print(data_types)
        generateDBMLcode(field_names, data_types, sheet)


def generateDBMLcode(field_names, data_types, sheet_name):
    dbml_code = "Table "+ f"{sheet_name}" + " {"

    for i, (field_name, data_type) in enumerate(zip(field_names, data_types)):
        try:
            mysql_data_type = map_data_type(data_type.split("(")[0])
            if data_type.split("(")[0] == "Lookup":
                lookup_table = data_type.split("(")[1].split(")")[0]
                mapping_statement = "Ref: " + f"{sheet_name}" + f".{field_name}" + " > " + f"{lookup_table}" + "." + f"{field_name}"
                print(mapping_statement)
                references_code += mapping_statement
                # print(data_type.split("(")[1].split(")")[0])
        except:
            mysql_data_type = map_data_type(data_type)
        dbml_code += f"\n  {field_name} {mysql_data_type}"

    dbml_code += "\n}"

    # print(dbml_code)
getDataFromSheets(sheet_names)

print(references_code)