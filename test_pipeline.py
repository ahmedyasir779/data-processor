
from loader import DataLoader
from cleaner import DataCleaner
import pandas as pd

# Step 1: Load
print("\n LOADING DATA...")
loader = DataLoader('data/messy_data.csv')
raw_data = loader.load()
loader.preview(10)

# Step 2: Clean
print("\n CLEANING DATA...")
cleaner = DataCleaner(raw_data)
clean_data = (cleaner
              .handle_missing_values(strategy='drop')
              .remove_duplicates()
              .clean_strings()
              .remove_outliers('age')
              .get_cleaned_data())

print("\nFINAL RESULT:")
print(clean_data)

# Step 3: Report
print("\nREPORT:")
report = cleaner.get_report()
print(f"Started: {report['original_rows']} rows")
print(f"Ended: {report['final_rows']} rows")
print(f"Removed: {report['original_rows'] - report['final_rows']} problematic rows")

print("\n" + "=" * 60)
print(" PIPELINE COMPLETE!")