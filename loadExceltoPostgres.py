from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy.types import VARCHAR, BIGINT, TIMESTAMP, DECIMAL, BINARY
import pandas as pd
# import mysql.connector
# import sqlalchemy as db
# from pandas.io.json._table_schema import build_table_schema
from sqlalchemy import text
import psycopg2

data_type_mapping = {
    'bigint': 'bigint',
    'bit': 'bit',
    'datetime': 'timestamp',
    'decimal': 'decimal',
    'nvarchar': 'varchar',
    'varbinary': 'bytea',
    'varchar': 'varchar'
}

reserved_keywords = [
    "all", "analyse", "analyze", "and", "any", "array", "as", "asc", "asymmetric",
    "both", "case", "cast", "check", "collate", "column", "constraint", "create",
    "current_catalog", "current_date", "current_role", "current_time", "current_timestamp",
    "current_user", "default", "deferrable", "desc", "distinct", "do", "else", "end",
    "except", "false", "fetch", "for", "foreign", "from", "grant", "group", "having",
    "in", "initially", "intersect", "into", "lateral", "leading", "limit", "localtime",
    "localtimestamp", "new", "not", "null", "of", "off", "offset", "old", "on", "only",
    "or", "order", "placing", "primary", "references", "returning", "select", "session_user",
    "similar", "some", "symmetric", "table", "then", "to", "trailing", "true", "union",
    "unique", "user", "using", "variadic", "when", "where", "window", "with"
]

def map_data_type(data_type):
    return data_type_mapping.get(data_type, 'VARCHAR(255)')


filepath = "Simphony_Table_Schema.xlsx"


database_connection = create_engine("postgresql://factadmin:Weavers#456@172.210.3.233:5432/test_potgres_database", ISOLATION_LEVEL="AUTOCOMMIT")


def generate_sql_for_schema():
    df = pd.read_excel(filepath)

    try:
        table_names = df['TABLE_NAME'].tolist()
        field_names = df['COLUMN_NAME'].tolist()
        data_types = df['DATA_TYPE'].tolist()

    except:
        print("Invalid column name")

    table_fields = {}

    for table_name, field_name, data_type in zip(table_names, field_names, data_types) :
        if table_name not in table_fields:
            table_fields[table_name] = []

        table_fields[table_name].append((field_name, data_type))

    for table_name, fields in table_fields.items():

        sql_statement = f"CREATE TABLE {table_name} ("

        for i, (field_name, data_type) in enumerate(fields):
            postgres_data_type = map_data_type(data_type)
            if field_name.lower() in reserved_keywords:
                field_name = f'"{field_name}"'
            sql_statement += f"{field_name} {postgres_data_type}"
            if i < len(fields) -1:
                sql_statement += ","
        sql_statement += ")"

        print(sql_statement)
        executable_object = text(sql_statement)

        with database_connection.connect() as connection:
            connection.execute(executable_object)


generate_sql_for_schema()






# df.to_sql(con=database_connection, name=table_name, if_exists='replace')

