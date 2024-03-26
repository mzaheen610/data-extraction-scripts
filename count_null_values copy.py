from sqlalchemy import create_engine, MetaData, Table, Column

# from sqlalchemy.types import VARCHAR, BIGINT, TIMESTAMP, DECIMAL, BINARY
from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Float,
    Integer,
    Numeric,
    String,
    Text,
    VARBINARY,
    Time,
    LargeBinary,
)

import pandas as pd

# import mysql.connector
# import sqlalchemy as db
# from pandas.io.json._table_schema import build_table_schema
from sqlalchemy import text
import psycopg2


data_type_mapping = {
    "bigint": BigInteger,
    "bit": Integer,
    "datetime": DateTime,
    "decimal": Numeric,
    "nvarchar": String(256),
    "varbinary": LargeBinary,
    "varchar": String(256),
    "integer": Integer,
    "string": String(256),
    "number": Numeric,
    "int64": BigInteger,
    "float64": Float,
    "object": Text,
    "bool": Boolean,
    "datetime64": DateTime,
    "timedelta64": Time,
    "category": String(256),
}

# reserved_keywords = [
#     "all", "analyse", "analyze", "and", "any", "array", "as", "asc", "asymmetric",
#     "both", "case", "cast", "check", "collate", "column", "constraint", "create",
#     "current_catalog", "current_date", "current_role", "current_time", "current_timestamp",
#     "current_user", "default", "deferrable", "desc", "distinct", "do", "else", "end",
#     "except", "false", "fetch", "for", "foreign", "from", "grant", "group", "having",
#     "in", "initially", "intersect", "into", "lateral", "leading", "limit", "localtime",
#     "localtimestamp", "new", "not", "null", "of", "off", "offset", "old", "on", "only",
#     "or", "order", "placing", "primary", "references", "returning", "select", "session_user",
#     "similar", "some", "symmetric", "table", "then", "to", "trailing", "true", "union",
#     "unique", "user", "using", "variadic", "when", "where", "window", "with"
# ]



def map_data_type(data_type):
    return data_type_mapping.get(data_type, "VARCHAR(255)")

filepath_schema = "Simphony_Table_Schema.xlsx"
filepath_data = "Oracle DB Check n Detail Aug2023 (1).xlsx"

file = pd.ExcelFile(filepath_data)
sheet_names = file.sheet_names

print(sheet_names)



def create_table(engine, table_name, fields):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    columns = []

    # Define columns
    for field_name, data_type in fields:
        postgres_data_type = map_data_type(data_type)
        column = Column(field_name, postgres_data_type)
        columns.append(column)

    # Create table

    table = Table(table_name, metadata, *columns, extend_existing=True)
    # table.drop(engine, checkfirst=True)
    metadata.create_all(bind=engine)
    print(f"Table '{table_name}' created successfully.")

    """Load data into corresponding tables."""

    try:
        df = pd.read_excel(filepath_data, sheet_name=table_name)
        print(df)
        df.to_sql(con=engine, name=table_name, if_exists='append', index=False)
    except Exception as e:
        print(f"Error loading data into table {table_name}. {e}")



def generate_tables_from_schema():
    df = pd.read_excel(filepath_schema)

    try:
        table_names = df["TABLE_NAME"].tolist()
        field_names = df["COLUMN_NAME"].tolist()
        data_types = df["DATA_TYPE"].tolist()
    except:
        print("Invalid column name")

    table_fields = {}

    for table_name, field_name, data_type in zip(table_names, field_names, data_types):
        if table_name not in table_fields:
            table_fields[table_name] = []

        table_fields[table_name].append((field_name, data_type))

    engine = create_engine(
        "postgresql://factadmin:Weavers#456@172.210.3.233:5432/test_potgres_database"
    )

    for table_name, fields in table_fields.items():
        if table_name in ['PosMenuItemClass']:
        # if table_name in sheet_names and table_name not in ['PosCheckHeader', 'PosCheckMenuItemDetail', 'PosMenuItem']:
            create_table(engine, table_name, fields)


generate_tables_from_schema()



