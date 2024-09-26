from dotenv import load_dotenv
from pyairtable import Api
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from typing import Optional, List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    pat: str
    base_id: str
    table_name: str

    class Config:
        env_prefix = "airtable_"
        env_file = ".env"

class SampleItem(BaseModel):
    # Define fields based on your actual Airtable structure
    # For example:
    field1: str
    field2: Optional[str] = None
    field3: int = Field(gt=0)
    field4: List[str] = []

class AirtableManager:
    def __init__(self):
        self.settings = Settings()
        self.api = Api(self.settings.pat)
        self.base = self.get_base()
        self.table = self.get_table()

    def get_base(self):
        try:
            return self.api.base(self.settings.base_id)
        except Exception as e:
            logging.error(f"Base not found: {e}")
            raise

    def get_table(self):
        try:
            return self.base.table(self.settings.table_name)
        except Exception as e:
            logging.error(f"Table not found: {e}")
            raise

    def add_item(self, item: Dict[str, Any]):
        try:
            return self.table.create(item)
        except Exception as e:
            logging.error(f"Error adding item: {e}")
            raise

    def get_all_records(self):
        return self.table.all()

    def print_metadata(self):
        logging.info(f"Base ID: {self.settings.base_id}")
        logging.info(f"Table Name: {self.settings.table_name}")

    def get_table_schema(self):
        try:
            # This method might not be available in all versions of pyairtable
            schema = self.table.schema()
            logging.info("Table Schema:")
            for field in schema['fields']:
                logging.info(f"Field Name: {field['name']}, Type: {field['type']}")
        except AttributeError:
            logging.warning("Unable to fetch table schema. Your pyairtable version might not support this feature.")
        except Exception as e:
            logging.error(f"Error fetching table schema: {e}")

def main():
    manager = AirtableManager()
    manager.print_metadata()
    manager.get_table_schema()

    # Add a sample item
    # Adjust these fields to match your actual Airtable structure
    sample_item = {
        "field1": "Test Item",
        "field2": "This is a test item",
        "field3": 5,
        "field4": ["test", "sample"]
    }

    try:
        new_record = manager.add_item(sample_item)
        logging.info(f"Added new record: {new_record}")
    except Exception as e:
        logging.error(f"Failed to add new record: {e}")

    # Fetch and print all records
    records = manager.get_all_records()
    for record in records:
        logging.info(record)

if __name__ == '__main__':
    main()