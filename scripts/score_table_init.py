import psycopg2
from psycopg2 import sql
import getpass


# Database connection parameters
host = "hopandzip.com"  # Change if your DB is not on localhost
database = "ninja"
user = "ninja"
password = getpass.getpass()
port = 8888

# Create a connection to the PostgreSQL database
conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password,
    port=port
)
print("Connected to the database successfully")

# Create a cursor object
cursor = conn.cursor()

# Define the table creation query
create_table_query = '''
CREATE TABLE IF NOT EXISTS score (
    name varchar(16),
    score         int,           
    date         date        
);
'''

# Execute the table creation query
cursor.execute(create_table_query)

# Commit the changes
conn.commit()
print("Table created successfully")


# Close the cursor and connection
if cursor:
    cursor.close()
if conn:
    conn.close()
print("Connection closed")