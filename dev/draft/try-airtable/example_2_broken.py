from dotenv import load_dotenv
from pyairtable import Api
from pyairtable.formulas import match
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from typing import Optional, List
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
    name: str
    description: Optional[str] = None
    quantity: int = Field(gt=0)
    tags: List[str] = []

class AirtableManager:
    def __init__(self):
        self.settings = Settings()
        self.api = Api(self.settings.pat)
        self.base = self.get_or_create_base()
        self.table = self.get_or_create_table()

    def get_or_create_base(self):
        try:
            return self.api.base(self.settings.base_id)
        except Exception as e:
            logging.error(f"Base not found: {e}")
            # Note: Airtable API doesn't allow programmatic base creation
            raise Exception("Base not found. Please create it manually in Airtable.")

    def get_or_create_table(self):
        try:
            return self.base.table(self.settings.table_name)
        except Exception as e:
            logging.info(f"Table not found, creating: {self.settings.table_name}")
            return self.base.create_table(self.settings.table_name, [
                {"name": "name", "type": "singleLineText"},
                {"name": "description", "type": "multilineText"},
                {"name": "quantity", "type": "number"},
                {"name": "tags", "type": "multipleSelects"}
            ])

    def add_item(self, item: SampleItem):
        return self.table.create(item.dict())

    def get_all_records(self):
        return self.table.all()

    def print_metadata(self):
        logging.info(f"Workspace Name: {self.base.name}")
        logging.info(f"Base ID: {self.settings.base_id}")
        logging.info(f"Table Name: {self.table.name}")

def main():
    manager = AirtableManager()
    manager.print_metadata()

    # Add a sample item
    sample_item = SampleItem(
        name="Test Item",
        description="This is a test item",
        quantity=5,
        tags=["test", "sample"]
    )
    new_record = manager.add_item(sample_item)
    logging.info(f"Added new record: {new_record}")

    # Fetch and print all records
    records = manager.get_all_records()
    for record in records:
        logging.info(record)

if __name__ == '__main__':
    main()