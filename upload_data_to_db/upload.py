#!/usr/bin/env python3
"""
Simple MongoDB data upload script for PhishLens
Run this from the project root: python upload_data_to_db/upload.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get MongoDB URL
mongo_url = os.getenv("MONGO_DB_URL")
if not mongo_url:
    print("ERROR: MONGO_DB_URL not found in .env file")
    sys.exit(1)

print(f"Using MongoDB: {mongo_url[:50]}...")

# Import MongoDB connector
try:
    from database_connect import mongo_operation
except ImportError:
    print("ERROR: database_connect module not found")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

# Configuration
database_name = "phising"
datasets_dir = Path(__file__).parent  # Current directory (upload_data_to_db/)

# Find and upload CSV files
print(f"\nSearching for CSV files in: {datasets_dir}")

csv_files = list(datasets_dir.glob("*.csv"))
if not csv_files:
    print("No CSV files found!")
    sys.exit(1)

print(f"Found {len(csv_files)} CSV file(s)")

for csv_file in csv_files:
    file_name = csv_file.stem  # filename without extension
    
    print(f"\nUploading {csv_file.name}...")
    
    try:
        mongo_connection = mongo_operation(
            client_url=mongo_url,
            database_name=database_name,
            collection_name=file_name
        )
        
        mongo_connection.bulk_insert(str(csv_file))
        print(f"✓ {file_name} uploaded successfully to MongoDB")
    
    except Exception as e:
        print(f"✗ Error uploading {file_name}: {str(e)}")
        sys.exit(1)

print("\n✓ All files uploaded successfully!")
