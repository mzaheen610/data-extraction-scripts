import pandas as pd
import mysql.connector
import sqlalchemy as db
from pandas.io.json._table_schema import build_table_schema
from sqlalchemy import text


data_type_mapping = {
    'integer': 'INT',
    'string': 'VARCHAR(255)',
    'number': 'NUMERIC',
    'datetime': 'DATETIME',
    'int64': 'INT',
    'float64': 'FLOAT',
    'object': 'VARCHAR(255)',
    'bool': 'BOOLEAN',
    'datetime64': 'DATETIME',
    'timedelta64': 'TIME',
    'category': 'VARCHAR(255)',
}

def map_data_type(data_type):
    return data_type_mapping.get(data_type, 'VARCHAR(255)')


filepath = "Simphony_Table_Schema.xlsx"
df = pd.read_excel(filepath)

# Extract schema from DataFrame
schema = {
    'fields': [{'name': col, 'type': str(df[col].dtype)} for col in df.columns],
    'primaryKey': ['index'],
}
# schema = build_table_schema(df)
print(schema)

table_name = 'simphony_tableee'

sql_statement = f"CREATE TABLE {table_name} ("

for i, field in enumerate(schema['fields']):
    name = field['name']
    data_type = field['type']
    mysql_data_type = map_data_type(data_type)

    sql_statement += f"{name} {mysql_data_type}"
    if i < len(schema['fields']) - 1:
        sql_statement += ","

sql_statement += ")"
print(sql_statement)

# database_connection = db.create_engine("mysql+mysqlconnector://root:password@localhost:3306/testdb")
# executable_object = text(sql_statement)

# with database_connection.connect() as connection:
#     connection.execute(executable_object)

# df.to_sql(con=database_connection, name=table_name, if_exists='replace')

