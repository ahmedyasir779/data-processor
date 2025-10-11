import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from analyzer import DataAnalyzer


class TestDataAnalyzer:
    
    @pytest.fixture
    def sample_data(self):
        np.random.seed(42)
        return pd.DataFrame({
            'age': np.random.randint(20, 60, 100),
            'salary': np.random.randint(30000, 100000, 100),
            'experience': np.random.randint(0, 20, 100),
            'city': np.random.choice(['NYC', 'LA', 'Chicago'], 100),
            'department': np.random.choice(['Sales', 'Engineering'], 100)
        })
    
    def test_initialization(self, sample_data):
        analyzer = DataAnalyzer(sample_data)
        
        assert analyzer.df is not None
        assert len(analyzer.numeric_cols) > 0
        assert len(analyzer.categorical_cols) > 0
    
    def test_get_summary_statistics(self, sample_data):
        analyzer = DataAnalyzer(sample_data)
        summary = analyzer.get_summary_statistics()
        
        assert isinstance(summary, dict)
        assert 'age' in summary
        assert 'mean' in summary['age']
        assert 'median' in summary['age']
        assert 'std' in summary['age']
    
    def test_get_correlation_matrix(self, sample_data):
        analyzer = DataAnalyzer(sample_data)
        corr = analyzer.get_correlation_matrix()
        
        assert isinstance(corr, pd.DataFrame)
        assert len(corr) > 0
        # Correlation matrix should be square
        assert corr.shape[0] == corr.shape[1]
    
    def test_get_value_counts(self, sample_data):
        analyzer = DataAnalyzer(sample_data)
        counts = analyzer.get_value_counts('city')
        
        assert isinstance(counts, pd.Series)
        assert len(counts) > 0
        assert counts.sum() == len(sample_data)
    
    def test_generate_report(self, sample_data):
        analyzer = DataAnalyzer(sample_data)
        report = analyzer.generate_report()
        
        assert isinstance(report, str)
        assert 'DATASET OVERVIEW' in report
        assert 'SUMMARY STATISTICS' in report
        assert len(report) > 100
    
    def test_invalid_column(self, sample_data):
        analyzer = DataAnalyzer(sample_data)
        
        with pytest.raises(ValueError):
            analyzer.get_value_counts('nonexistent_column')