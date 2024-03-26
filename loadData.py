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
}

def map_data_type(data_type):
    return data_type_mapping.get(data_type, 'VARCHAR(255)')  # Default to VARCHAR(255) if no mapping found

filepath = "Simphony_Table_Schema.xlsx"
df = pd.read_excel(filepath)

schema = build_table_schema(df)
# print(schema)


# Define the table name
table_name = 'simphony_table'

# Construct the CREATE TABLE SQL statement
sql_statement = f"CREATE TABLE {table_name} ("

# Add columns to the SQL statement
for field in schema['fields']:
    name = field['name']
    data_type = field['type']
    mysql_data_type = map_data_type(data_type)

    sql_statement += f"{name} {mysql_data_type}, "

# Add primary key constraint
sql_statement += f"PRIMARY KEY ({', '.join(schema['primaryKey'])})"

# Close the SQL statement
sql_statement += ")"

# Print the SQL statement
# print(sql_statement)


# schema = pd.io.sql.get_schema(df, 'simphony_table')
# clean_sql_statement = schema.strip().replace('\n', '')

# print(clean_sql_statement)
# print(df.dtypes)


executable_object = text(sql_statement)
database_connection = db.create_engine("mysql+mysqlconnector://root:password@localhost:3306/testdb")

with database_connection.connect() as connection:
    connection.execute(executable_object)

# df.to_sql(con=database_connection,schema=schema, name="simphony_table", if_exists='replace')

