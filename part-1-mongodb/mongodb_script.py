import os
from datetime import datetime
import logging
import json

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.database import Database


load_dotenv(".env")
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = "brewery"
BEERS_COLLECTION = "beers"
EMPLOYEES_COLLECTION = "employees"
PATRONS_COLLECTION = "patrons"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )


class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.database = None

    def connect(self) -> Database | None:
        try:
            self.client = MongoClient(self.uri)
            self.database = self.client[self.db_name]
            logging.info("Successfully connected to MongoDB and Database")
            return self.database
        except PyMongoError as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            return None

    def disconnect(self):
        if self.client:
            self.client.close()
            logging.info("Disconnected from MongoDB")


def get_all_customers(db: Database) -> list[dict]:
    try:
        patrons_collection = db[PATRONS_COLLECTION]
        all_customers = patrons_collection.find()
        customer_list = [customer for customer in all_customers]
        logging.info(f"Retrieved all customers: {len(customer_list)}")
        return customer_list
    except PyMongoError as e:
        logging.error(f"Failed to retrieve all customers: {e}")
        return []

def get_customer_emails(db: Database) -> list[str]:
    try:
        patrons_collection = db[PATRONS_COLLECTION]
        query = {"email": {"$exists": True, "$nin": [None, ""]}}
        projection = {"_id": 0, "email": 1}
        customers_by_only_email = patrons_collection.find(query, projection)
        email_list = [customer["email"] for customer in customers_by_only_email]
        logging.info(f"Retrieved customers with only email: {len(email_list)}")
        return email_list
    except PyMongoError as e:
        logging.error(f"Failed to retrieve customers with only email: {e}")
        return []

def get_customer_emails_by_beer_types(db: Database, beer_types: list[str]) -> list[str]:
    try:
        email_list = []
        patrons_collection = db[PATRONS_COLLECTION]
        beer_ids = get_beers_by_types(db, beer_types)
        query = {"email": {"$exists": True, "$nin": [None, ""]}, "favorite_beer": {"$in": beer_ids}}
        customers_with_email_and_beer_type = patrons_collection.find(query)
        email_list = [customer["email"] for customer in customers_with_email_and_beer_type]
        logging.info(f"Retrieved customers with email and IPA: {len(email_list)}")
        return email_list
    except PyMongoError as e:
        logging.error(f"Failed to retrieve customers with only email: {e}")
        return []

def get_beers_by_types(db: Database, beer_types: list[str]) -> list[str]:
    try:
        beers_collection = db[BEERS_COLLECTION]
        all_beers = beers_collection.find()
        beer_ids = [beer["_id"] for beer in all_beers if beer.get("type", "") in beer_types]
        return beer_ids
    except PyMongoError as e:
        logging.error(f"Failed to retrieve IPA type beers: {e}")
        return []

def get_beers_map(db: Database) -> dict:
    try:
        beers_collection = db[BEERS_COLLECTION]
        all_beers = beers_collection.find()
        beers_map = {beer["_id"]: {"name": beer["name"], "type": beer["type"]} for beer in all_beers}
        return beers_map
    except PyMongoError as e:
        logging.error(f"Failed to retrieve beers map: {e}")
        return {}

def get_location_frequency(db: Database, start_date: datetime, end_date: datetime) -> list[dict]:
    try:
        patrons_collection = db[PATRONS_COLLECTION]
        match_filter = {"$match": {"last_checkin": {"$lte": end_date, "$gte": start_date}}}
        group_by_filter = {"$group": {"_id": "$location", "count": {"$sum": 1}}}
        project_filter = {"$project": {"_id": 0, "location": "$_id", "count": 1}}
        sort_by_filter = {"$sort": {"count": -1}}
        location_frequency = patrons_collection.aggregate([match_filter, group_by_filter, project_filter, sort_by_filter])
        location_frequency_list = list(location_frequency)
        logging.info(f"Retrieved frequency for {len(location_frequency_list)} locations.")
        return location_frequency_list
    except PyMongoError as e:
        logging.error(f"Failed to retrieve location frequency: {e}")
        return []

def favorite_beers_by_customers(db: Database) -> list[dict]:
    try:
        beers_map = get_beers_map(db)
        all_customers = get_all_customers(db)
        favorite_beers = filter_customers_by_favorite_beer(all_customers, beers_map)
        return favorite_beers
    except PyMongoError as e:
        logging.error(f"Failed to retrieve favorite beers by customers: {e}")
        return []

def filter_customers_by_favorite_beer(customers: list[dict], beers_map: dict) -> list[dict]:
    favorite_beers = []
    for customer in customers:
        favorite_beer_id = customer.get("favorite_beer")
        if favorite_beer_id and favorite_beer_id in beers_map:
            if "count" in beers_map[favorite_beer_id]:
                beers_map[favorite_beer_id]["count"] += 1
            else:
                beers_map[favorite_beer_id]["count"] = 1
    favorite_beers = [beer for beer in beers_map.values()]
    return sorted(favorite_beers, key=lambda beer: beer["count"], reverse=True)

def create_json_output_file(all_customers_with_only_email, all_customers_with_email_and_ipa, location_frequency, favorite_beers):
    output_data = {
        "all_customers_with_only_email": all_customers_with_only_email,
        "all_customers_with_email_and_ipa": all_customers_with_email_and_ipa,
        "location_frequency": location_frequency,
        "favorite_beers": favorite_beers
    }
    output_file_path = os.path.join(os.path.dirname(__file__), 'output.json')
    try:
        with open(output_file_path, 'w') as output_file:
            json.dump(output_data, output_file, indent=4)
        logging.info(f"Output JSON file created at: {output_file_path}")
    except Exception as e:
        logging.error(f"Failed to create output JSON file: {e}")

if __name__ == '__main__':
    mongodb_client = MongoDB(MONGO_URI, DATABASE_NAME)
    client = mongodb_client.connect()
    if client is None:
        logging.error("MongoDB connection failed.")
        exit(1)

    beer_types = ["IPA"] # Also there is a type named Hazy IPA.
    all_customers_with_only_email = get_customer_emails(client)
    all_customers_with_email_and_ipa = get_customer_emails_by_beer_types(client, beer_types)

    start_date = datetime(2024, 1, 1, 0, 0, 0)  # 2024/01/01 00:00:00
    end_date = datetime(2024, 4, 1, 0, 0, 0)  # 2024/04/01 00:00:00
    location_frequency = get_location_frequency(client, start_date, end_date)

    favorite_beers = favorite_beers_by_customers(client)

    create_json_output_file(all_customers_with_only_email, all_customers_with_email_and_ipa, location_frequency, favorite_beers)

    logging.info(f"All customer emails with only email: {all_customers_with_only_email}")
    logging.info(f"All customer emails with email and IPA: {all_customers_with_email_and_ipa}")
    logging.info(f"Location frequency: {location_frequency}")
    logging.info(f"Favorite beers by customers: {favorite_beers}")

    mongodb_client.disconnect()
