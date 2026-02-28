#!/usr/bin/env python3
import os
from dotenv import load_dotenv

load_dotenv()

try:
    print("Testing data export from MongoDB...")
    
    from src.data_access.phising_data import PhisingData
    
    phising_data = PhisingData(database_name="phising")
    
    print("\n1. Getting collection names...")
    collections = phising_data.get_collection_names()
    print(f"✓ Collections found: {collections}")
    
    print("\n2. Exporting collection data...")
    for collection_name, df in phising_data.export_collections_as_dataframe():
        print(f"\n✓ {collection_name}:")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {list(df.columns)[:5]}... ({len(df.columns)} total)")
        
        # Save to CSV for testing
        csv_path = f"test_{collection_name}.csv"
        df.to_csv(csv_path, index=False)
        print(f"  Saved to: {csv_path}")
        
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
