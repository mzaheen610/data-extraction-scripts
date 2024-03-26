from sqlalchemy import create_engine, text

def terminate_all_connections(engine):
    # Get a database connection
    connection = engine.connect()

    try:
        # Execute the SQL query to terminate connections
        query = """
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = 'your_database_name'
        AND pid <> pg_backend_pid();
        """
        connection.execute(text(query))
        print("All connections terminated successfully.")
    finally:
        # Close the database connection
        connection.close()

engine = create_engine(
        "postgresql://user:pass@host:5432/database"
    )

terminate_all_connections(engine)
