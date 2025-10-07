"""
Complete Data Pipeline: Load → Clean → Analyze
"""

from loader import DataLoader
from cleaner import DataCleaner
from analyzer import DataAnalyzer
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

cleaning_report = cleaner.get_report()
print(f"Cleaned: {cleaning_report['original_rows']} → {cleaning_report['final_rows']} rows")

# Step 3: Analyze Data
print("\n📊 STEP 3: Analyzing data...")
analyzer = DataAnalyzer(clean_data)

# Generate report
report = analyzer.generate_report()
print(report)

# Export report
analyzer.export_report('output/analysis_report.txt')

# Create visualizations
if len(analyzer.numeric_cols) > 0:
    print("\n📈 Generating visualizations...")
    
    # Plot first numeric column
    first_numeric = analyzer.numeric_cols[0]
    analyzer.plot_distribution(first_numeric, save_path=f'output/{first_numeric}_distribution.png')
    
    # Correlation heatmap if we have multiple numeric columns
    if len(analyzer.numeric_cols) >= 2:
        analyzer.plot_correlation_heatmap(save_path='output/correlation_heatmap.png')

print("\n" + "=" * 60)
print("Check the 'output/' folder for saved files")
print("=" * 60)