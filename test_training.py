#!/usr/bin/env python3
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Test the training pipeline directly
try:
    print("=" * 60)
    print("Testing PhishLens Training Pipeline")
    print("=" * 60)
    
    print("\n1. Importing modules...")
    from src.pipeline.train_pipeline import TrainingPipeline
    print("✓ TrainingPipeline imported")
    
    print("\n2. Creating training pipeline...")
    pipeline = TrainingPipeline()
    print("✓ TrainingPipeline created")
    
    print("\n3. Running pipeline...")
    pipeline.run_pipeline()
    print("✓ Pipeline completed successfully!")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    print("\nFull Traceback:")
    print("=" * 60)
    traceback.print_exc()
    sys.exit(1)
