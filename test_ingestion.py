#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv

load_dotenv()

try:
    print("Testing data ingestion...")
    
    from src.components.data_ingestion import DataIngestion
    
    print("\n1. Creating DataIngestion...")
    ingestion = DataIngestion()
    raw_dir = ingestion.data_ingestion_config.data_ingestion_dir
    print(f"✓ Raw data ingestion dir: {raw_dir}")
    
    print("\n2. Exporting data to raw dir...")
    try:
        ingestion.export_data_into_raw_data_dir()
        print("✓ Data export completed")
    except Exception as e:
        print(f"✗ Export error: {e}")
        raise
    
    print("\n3. Checking raw data dir...")
    os.makedirs(raw_dir, exist_ok=True)
    
    files = os.listdir(raw_dir)
    print(f"Files in {raw_dir}:")
    for f in files:
        fpath = os.path.join(raw_dir, f)
        if os.path.isfile(fpath):
            size = os.path.getsize(fpath)
            print(f"  ✓ {f} ({size} bytes)")
        else:
            print(f"  - {f}/ (directory)")
    
    if len(files) == 0:
        print("  (empty - this is the problem!)")
        
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

