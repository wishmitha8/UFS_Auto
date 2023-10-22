from sqlalchemy import create_engine, inspect
import pandas as pd
from datetime import datetime
from urllib.parse import quote_plus
from sqlalchemy.exc import NoSuchTableError

# Define your PostgreSQL connection parameters
username = 'postgres'
password = 'postgres@123'
host = '194.233.89.26'
port = '5432'
database = 'dev'
schema_name = 'dev_sahan'

encoded_password = quote_plus(password)

url_object = f'postgresql://{username}:{encoded_password}@{host}:{port}/{database}'

engine = create_engine(url_object)
inspector = inspect(engine)

# Read the data from your source, e.g., a CSV file
df = pd.read_csv('output/details.csv')
df['insert_date'] = datetime.today()
table_name = 'ldg_ops_usfauto'

try:
    # Check if the table already exists
    inspector.get_table_names(schema=schema_name)
    append_mode = 'append'
except NoSuchTableError:
    append_mode = 'replace'

# Append data to an existing table or create a new table
df.to_sql(name=table_name, con=engine, if_exists=append_mode, index=False, schema=schema_name)
print("Data has been transferred")

# Dispose of the engine
engine.dispose()
