import pandas as pd
import json
import os
from pathlib import Path


class DataLoader:
    """Load data from various file formats"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = None
        self.file_type = self._get_file_type()
    


    def _get_file_type(self) -> str:
        """
        Determine file type from extension
        """
        return Path(self.file_path).suffix.lower().replace('.', '')
    

    
    def load(self) -> pd.DataFrame:
        """
        Load the file based on its type
        """
        # Check if file exists
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        print(f"Loading {self.file_type.upper()} file: {self.file_path}")
        
        # Load based on file type
        if self.file_type == 'csv':
            self.data = self._load_csv()
        elif self.file_type == 'json':
            self.data = self._load_json()
        elif self.file_type == 'xlsx':
            self.data = self._load_excel()
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")
        
        print(f"Loaded {len(self.data)} rows and {len(self.data.columns)} columns")
        return self.data
    


    def _load_csv(self) -> pd.DataFrame:
        try:
            return pd.read_csv(self.file_path)
        except Exception as e:
            raise Exception(f"Error loading CSV: {e}")
        

    
    def _load_json(self) -> pd.DataFrame:
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                return pd.DataFrame(data)
            elif isinstance(data, dict):
                # JSON is object with nested data
                # Try to find the array (common pattern)
                for key, value in data.items():
                    if isinstance(value, list):
                        return pd.DataFrame(value)
                # If no array found, try to convert dict directly
                return pd.DataFrame([data])
            
        except Exception as e:
            raise Exception(f"Error loading JSON: {e}")
        


    
    def _load_excel(self) -> pd.DataFrame:
        try:
            return pd.read_excel(self.file_path)
        except Exception as e:
            raise Exception(f"Error loading Excel: {e}")
        

    
    def get_info(self) -> dict:
        if self.data is None:
            raise ValueError("No data loaded. Call load() first.")
        
        return {
            'rows': len(self.data),
            'columns': len(self.data.columns),
            'column_names': self.data.columns.tolist(),
            'memory_usage': f"{self.data.memory_usage(deep=True).sum() / 1024:.2f} KB",
            'missing_values': self.data.isnull().sum().to_dict()
        }
    


    def preview(self, n: int = 5):
        if self.data is None:
            raise ValueError("No data loaded. Call load() first.")
        
        print(f"\n{'='*60}")
        print(f"DATA PREVIEW (First {n} rows):")
        print('='*60)
        print(self.data.head(n))
        print('='*60)


    

def test_loader():
    print("\n" + "="*60)
    print("TESTING DATA LOADER")
    print("="*60)
    
    # Test CSV loading
    print("\n1. Testing CSV Loader:")
    print("-" * 60)
    csv_loader = DataLoader('data/sample.csv')
    csv_data = csv_loader.load()
    csv_loader.preview(3)
    
    print("\nData Info:")
    info = csv_loader.get_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # Test JSON loading
    print("\n2. Testing JSON Loader:")
    print("-" * 60)
    json_loader = DataLoader('data/sample.json')
    json_data = json_loader.load()
    json_loader.preview(3)
    
    print("\nData Info:")
    info = json_loader.get_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED!")
    print("="*60)


if __name__ == "__main__":
    test_loader()