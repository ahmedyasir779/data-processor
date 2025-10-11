import pytest
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from loader import DataLoader

class TestDataLoader:

    def test_load_csv(self):
        loader = DataLoader('data/sample.csv')
        df = loader.load()
        
        assert df is not None
        assert len(df) > 0
        assert len(df.columns) > 0
    
    def test_load_json(self):
        loader = DataLoader('data/sample.json')
        df = loader.load()
        
        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
    
    def test_file_not_found(self):
        loader = DataLoader('nonexistent.csv')
        
        with pytest.raises(FileNotFoundError):
            loader.load()
    
    def test_unsupported_file_type(self):
        import tempfile
        import os
        
        # Create a temporary file with unsupported extension
        with tempfile.NamedTemporaryFile(suffix='.xyz', delete=False, mode='w') as f:
            f.write('test content')
            temp_path = f.name
        
        try:
            loader = DataLoader(temp_path)
            with pytest.raises(ValueError):
                loader.load()
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_get_info(self):
        loader = DataLoader('data/sample.csv')
        df = loader.load()
        info = loader.get_info()
        
        assert 'rows' in info
        assert 'columns' in info
        assert 'column_names' in info
        assert info['rows'] == len(df)
        assert info['columns'] == len(df.columns)