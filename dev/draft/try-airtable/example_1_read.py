from dotenv import load_dotenv
from pyairtable import Api
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    pat: str
    base_id: str
    table_name: str

    class Config:
        env_prefix = "airtable_"
        env_file = ".env"

# Initialize settings
settings = Settings()

# Initialize Airtable API
api = Api(settings.pat)

# Fetch base details
base = api.base(settings.base_id)

# base_details = api.get_base(settings.base_id)
# workspace_name = base_details['name']
workspace_name = base.name

# Fetch table details
# table_details = api.get_table(settings.base_id, settings.table_name)
table = base.table(settings.table_name)

table_name = table.name

if __name__ == '__main__':
    # Print workspace and table name
    print(f"Workspace Name: {workspace_name}")


    print("Base Metadata:")
    print(base)


    print(f"Table Name: {table_name}")

    print("Table Metadata:")
    print(table)


    # # Initialize Airtable table
    # table = Table(settings.pat, settings.base_id, settings.table_name)

    # Fetch all records from the table
    records = table.all()

    # Print all records
    for record in records:
        print(record)