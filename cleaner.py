
import pandas as pd
import numpy as np
from typing import Dict, List, Optional


class DataCleaner:
    def __init__(self, df: pd.DataFrame):

        self.df = df.copy()  
        self.cleaning_report = {
            'original_rows': len(df),
            'original_columns': len(df.columns),
            'steps_applied': []
        }
    
    def handle_missing_values(self, strategy: str = 'drop', fill_value=None) -> 'DataCleaner':

        missing_before = self.df.isnull().sum().sum()
        
        if strategy == 'drop':
            self.df = self.df.dropna()
        elif strategy == 'fill':
            self.df = self.df.fillna(fill_value if fill_value is not None else 0)
        elif strategy == 'forward_fill':
            self.df = self.df.fillna(method='ffill')
        
        missing_after = self.df.isnull().sum().sum()
        
        self.cleaning_report['steps_applied'].append({
            'step': 'handle_missing_values',
            'strategy': strategy,
            'missing_before': int(missing_before),
            'missing_after': int(missing_after)
        })
        
        return self
    
    def remove_duplicates(self, subset: Optional[List[str]] = None) -> 'DataCleaner':

        rows_before = len(self.df)
        self.df = self.df.drop_duplicates(subset=subset, keep='first')
        rows_after = len(self.df)
        
        self.cleaning_report['steps_applied'].append({
            'step': 'remove_duplicates',
            'rows_removed': rows_before - rows_after
        })
        
        return self
    
    def clean_strings(self, columns: Optional[List[str]] = None) -> 'DataCleaner':

        if columns is None:
            columns = self.df.select_dtypes(include=['object']).columns.tolist()
        
        for col in columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str).str.strip()
        
        self.cleaning_report['steps_applied'].append({
            'step': 'clean_strings',
            'columns_cleaned': columns
        })
        
        return self
    
    def convert_types(self, type_map: Dict[str, str]) -> 'DataCleaner':

        for col, dtype in type_map.items():
            if col in self.df.columns:
                try:
                    self.df[col] = self.df[col].astype(dtype)
                except ValueError as e:
                    print(f"Warning: Could not convert {col} to {dtype}: {e}")
        
        self.cleaning_report['steps_applied'].append({
            'step': 'convert_types',
            'conversions': type_map
        })
        
        return self
    
    def remove_outliers(self, column: str, method: str = 'iqr') -> 'DataCleaner':

        rows_before = len(self.df)
        # Ensure numeric type
        self.df[column] = pd.to_numeric(self.df[column], errors='coerce')

        if method == 'iqr':
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            self.df = self.df[
                (self.df[column] >= lower_bound) & 
                (self.df[column] <= upper_bound)
            ]
        
        rows_after = len(self.df)
        
        self.cleaning_report['steps_applied'].append({
            'step': 'remove_outliers',
            'column': column,
            'method': method,
            'rows_removed': rows_before - rows_after
        })
        
        return self
    
    def get_cleaned_data(self) -> pd.DataFrame:

        self.cleaning_report['final_rows'] = len(self.df)
        self.cleaning_report['final_columns'] = len(self.df.columns)
        return self.df
    
    def get_report(self) -> Dict:

        return self.cleaning_report


