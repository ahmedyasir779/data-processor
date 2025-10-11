import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cleaner import DataCleaner


class TestDataCleaner:

    @pytest.fixture
    def messy_data(self):
        return pd.DataFrame({
            'name': ['  Alice  ', 'Bob', 'Charlie', 'Alice', '  David'],
            'age': [25, 30, None, 25, 150],
            'salary': [50000, 60000, 55000, 50000, 75000],
            'city': ['NYC', '  LA  ', 'NYC', 'NYC', None]
        })
    
    def test_handle_missing_values_drop(self, messy_data):
        cleaner = DataCleaner(messy_data)
        cleaned = cleaner.handle_missing_values(strategy='drop').get_cleaned_data()
        
        assert cleaned.isnull().sum().sum() == 0
        assert len(cleaned) < len(messy_data)
    
    def test_handle_missing_values_fill(self, messy_data):
        cleaner = DataCleaner(messy_data)
        cleaned = cleaner.handle_missing_values(strategy='fill', fill_value=0).get_cleaned_data()
        
        # Numeric columns should have 0, string columns should have '0'
        assert cleaned.isnull().sum().sum() == 0
    
    def test_remove_duplicates(self, messy_data):
        cleaner = DataCleaner(messy_data)
        cleaned = (cleaner
               .clean_strings()  
               .remove_duplicates()
               .get_cleaned_data())
        
        # Alice appears twice, should be reduced to once
        assert len(cleaned) < len(messy_data)
    
    def test_clean_strings(self, messy_data):
        cleaner = DataCleaner(messy_data)
        cleaned = cleaner.clean_strings().get_cleaned_data()
        
        # Check that whitespace is stripped
        assert cleaned['name'].iloc[0] == 'Alice'  # Was '  Alice  '
        assert cleaned['city'].iloc[1] == 'LA'     # Was '  LA  '
    
    def test_remove_outliers(self, messy_data):
        cleaner = DataCleaner(messy_data)
        cleaned = cleaner.remove_outliers('age', method='iqr').get_cleaned_data()
        
        # Age 150 should be removed as outlier
        assert cleaned['age'].max() < 150
    
    def test_method_chaining(self, messy_data):
        cleaner = DataCleaner(messy_data)
        cleaned = (cleaner
                   .handle_missing_values()
                   .remove_duplicates()
                   .clean_strings()
                   .get_cleaned_data())
        
        assert isinstance(cleaned, pd.DataFrame)
        assert len(cleaned) > 0
    
    def test_get_report(self, messy_data):
        cleaner = DataCleaner(messy_data)
        cleaner.handle_missing_values().remove_duplicates()
        report = cleaner.get_report()
        
        assert 'original_rows' in report
        assert 'final_rows' in report
        assert 'steps_applied' in report
        assert len(report['steps_applied']) == 2