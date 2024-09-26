from dotenv import load_dotenv
from pyairtable import Api
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Optional
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
    Name: str
    Notes: Optional[str] = None
    Status: Optional[str] = None

class AirtableManager:
    def __init__(self):
        self.settings = Settings()
        self.api = Api(self.settings.pat)
        self.base = self.api.base(self.settings.base_id)
        self.table = self.base.table(self.settings.table_name)

    def add_item(self, item: SampleItem):
        try:
            return self.table.create(item.dict(exclude_none=True))
        except Exception as e:
            logging.error(f"Error adding item: {e}")
            raise

    def get_all_items(self):
        return self.table.all()

    def print_metadata(self):
        logging.info(f"Base ID: {self.settings.base_id}")
        logging.info(f"Table Name: {self.settings.table_name}")

def main():
    manager = AirtableManager()
    manager.print_metadata()

    # Add a sample item
    sample_item = SampleItem(
        Name="New Task from Python",
        Notes="This task was added using our corrected Python script",
        Status="Todo"
    )

    try:
        new_record = manager.add_item(sample_item)
        logging.info(f"Added new item: {new_record}")
    except Exception as e:
        logging.error(f"Failed to add new item: {e}")

    # Fetch and print all items
    items = manager.get_all_items()
    logging.info("All items:")
    for item in items:
        logging.info(f"Item ID: {item['id']}")
        logging.info(f"Item Name: {item['fields'].get('Name', 'N/A')}")
        logging.info(f"Item Status: {item['fields'].get('Status', 'N/A')}")
        logging.info(f"Item Notes: {item['fields'].get('Notes', 'N/A')}")
        logging.info("---")

if __name__ == '__main__':
    main()