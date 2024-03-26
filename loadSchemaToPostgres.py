import pandas as pd
import sqlalchemy as db
from sqlalchemy import text
from sqlalchemy import MetaData


data_type_mapping = {
    "bigint": "bigint",
    "bit": "bit",
    "datetime": "timestamp",
    "decimal": "decimal",
    "nvarchar": "varchar",
    "varbinary": "bytea",
    "varchar": "varchar",
}


def map_data_type(data_type):
    return data_type_mapping.get(data_type, "VARCHAR(255)")


filepath = "Simphony_Table_Schema.xlsx"


def generate_sql_for_schema():
    df = pd.read_excel(filepath)
    table_names = df["TABLE_NAME"].tolist()
    field_names = df["COLUMN_NAME"].tolist()
    data_types = df["DATA_TYPE"].tolist()

    table_fields = {}

    for table_name, field_name, data_type in zip(table_names, field_names, data_types):
        if table_name not in table_fields:
            table_fields[table_name] = []

        table_fields[table_name].append((field_name, data_type))

    # Establish connection to PostgreSQL database
    engine = db.create_engine(
        "postgresql://factadmin:Weavers#456@172.210.3.233:5432/test_potgres_database"
    )

    print(len(table_fields))
    with engine.connect() as connection:
        for table_name, fields in table_fields.items():
            sql_statement = f"CREATE TABLE IF NOT EXISTS {table_name} ("

            for i, (field_name, data_type) in enumerate(fields):
                postgres_data_type = map_data_type(data_type)
                sql_statement += f'"{field_name}" {postgres_data_type}'
                if i < len(fields) - 1:
                    sql_statement += ","
            sql_statement += ")"

            # print(sql_statement)

            try:
                connection.execute(text(sql_statement))
                print(f"Table '{table_name}' created successfully.")
            except Exception as e:
                print(f"Error creating table '{table_name}': {str(e)}")

    metadata = MetaData()
    metadata.reflect(bind=engine)
    print(metadata.tables)


generate_sql_for_schema()
