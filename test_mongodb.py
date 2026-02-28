#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_url = os.getenv("MONGO_DB_URL")
if not mongo_url:
    print("ERROR: MONGO_DB_URL not set in .env")
    exit(1)

try:
    print("Connecting to MongoDB...")
    client = MongoClient(mongo_url)
    print("✓ Connected to MongoDB")
    
    # List databases
    databases = client.list_database_names()
    print(f"\nDatabases: {databases}")
    
    # Check phising database
    db = client["phising"]
    collections = db.list_collection_names()
    print(f"\nCollections in 'phising' DB: {collections}")
    
    # Check data in each collection
    for collection_name in collections:
        col = db[collection_name]
        count = col.count_documents({})
        print(f"\n{collection_name}: {count} documents")
        
        if count > 0:
            sample = col.find_one()
            if sample:
                print(f"  Sample fields: {list(sample.keys())}")
                print(f"  Expected: 31 columns + _id")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
