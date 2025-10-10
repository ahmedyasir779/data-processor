from loader import DataLoader
from cleaner import DataCleaner
from analyzer import DataAnalyzer
from dashboard import DashboardGenerator
import pandas as pd
import os

# Create output directory
os.makedirs('output', exist_ok=True)


# Step 1: Load Data
loader = DataLoader('data/messy_data.csv')
raw_data = loader.load()
print(f"Loaded {len(raw_data)} rows")

# Step 2: Clean Data
cleaner = DataCleaner(raw_data)
clean_data = (cleaner
              .handle_missing_values(strategy='drop')
              .remove_duplicates()
              .clean_strings()
              .get_cleaned_data())

print(f"Cleaned: {cleaner.get_report()['original_rows']} → {len(clean_data)} rows")

# Step 3: Analyze Data
analyzer = DataAnalyzer(clean_data)
report = analyzer.generate_report()
print(report)

# Export text report
analyzer.export_report('output/analysis_report.txt')

# Step 4: Create Dashboard
dashboard = DashboardGenerator(clean_data, title="Data Analysis Dashboard")

# Create overview dashboard
dashboard.create_overview_dashboard(save_path='output/final_dashboard.png')

# Create comparison plots
# dashboard.create_interactive_dashboard("final_dashboard")

print("\n" + "=" * 60)
print("✓ PIPELINE COMPLETE!")