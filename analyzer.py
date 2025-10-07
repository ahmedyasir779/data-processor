
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)


class DataAnalyzer:
    
    def __init__(self, df: pd.DataFrame):
    
        self.df = df
        self.numeric_cols = self._get_numeric_columns()
        self.categorical_cols = self._get_categorical_columns()
    
    def _get_numeric_columns(self) -> List[str]:
        return self.df.select_dtypes(include=[np.number]).columns.tolist()
    
    def _get_categorical_columns(self) -> List[str]:
        return self.df.select_dtypes(include=['object']).columns.tolist()
    
    def get_summary_statistics(self) -> Dict:
        summary = {}
        
        for col in self.numeric_cols:
            summary[col] = {
                'count': int(self.df[col].count()),
                'mean': float(self.df[col].mean()),
                'median': float(self.df[col].median()),
                'std': float(self.df[col].std()),
                'min': float(self.df[col].min()),
                'max': float(self.df[col].max()),
                'q25': float(self.df[col].quantile(0.25)),  # 25th percentile
                'q75': float(self.df[col].quantile(0.75))   # 75th percentile
            }
        
        return summary
    
    def get_correlation_matrix(self) -> pd.DataFrame:

        if len(self.numeric_cols) < 2:
            print("Warning: Need at least 2 numeric columns for correlation")
            return pd.DataFrame()
        
        return self.df[self.numeric_cols].corr()
    
    def get_value_counts(self, column: str, top_n: int = 10) -> pd.Series:

        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found")
        
        return self.df[column].value_counts().head(top_n)
    
    def plot_distribution(self, column: str, bins: int = 30, save_path: Optional[str] = None):
        
        if column not in self.numeric_cols:
            raise ValueError(f"Column '{column}' is not numeric")
        
        plt.figure(figsize=(10, 6))
        
        # Create histogram
        plt.hist(self.df[column].dropna(), bins=bins, color='skyblue', edgecolor='black', alpha=0.7)
        
        # Add mean and median lines
        mean_val = self.df[column].mean()
        median_val = self.df[column].median()
        
        plt.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
        plt.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Median: {median_val:.2f}')
        
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.title(f'Distribution of {column}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Plot saved to {save_path}")
        
        plt.show()
    
    def plot_correlation_heatmap(self, save_path: Optional[str] = None):

        if len(self.numeric_cols) < 2:
            print("Warning: Need at least 2 numeric columns for correlation heatmap")
            return
        
        plt.figure(figsize=(10, 8))
        
        corr_matrix = self.get_correlation_matrix()
        
        # Create heatmap
        sns.heatmap(
            corr_matrix,
            annot=True,      # Show numbers in cells
            cmap='coolwarm', # Color scheme: blue (negative) to red (positive)
            center=0,        # Center color scale at 0
            fmt='.2f',       # Format numbers to 2 decimal places
            square=True,     # Make cells square
            linewidths=1
        )
        
        plt.title('Correlation Heatmap')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Heatmap saved to {save_path}")
        
        plt.show()
    
    def plot_categorical_counts(self, column: str, top_n: int = 10, save_path: Optional[str] = None):

        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found")
        
        plt.figure(figsize=(10, 6))
        
        value_counts = self.get_value_counts(column, top_n)
        
        # Create bar chart
        value_counts.plot(kind='bar', color='steelblue', edgecolor='black')
        
        plt.xlabel(column)
        plt.ylabel('Count')
        plt.title(f'Top {top_n} Values in {column}')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Plot saved to {save_path}")
        
        plt.show()
    
    def generate_report(self) -> str:

        report = []
        report.append("=" * 60)
        report.append("DATA ANALYSIS REPORT")
        report.append("=" * 60)
        
        # Basic info
        report.append(f"\n📊 DATASET OVERVIEW:")
        report.append(f"   Rows: {len(self.df)}")
        report.append(f"   Columns: {len(self.df.columns)}")
        report.append(f"   Numeric columns: {len(self.numeric_cols)}")
        report.append(f"   Categorical columns: {len(self.categorical_cols)}")
        
        # Summary statistics
        if self.numeric_cols:
            report.append(f"\n📈 SUMMARY STATISTICS:")
            summary = self.get_summary_statistics()
            
            for col, stats in summary.items():
                report.append(f"\n   {col}:")
                report.append(f"      Mean: {stats['mean']:.2f}")
                report.append(f"      Median: {stats['median']:.2f}")
                report.append(f"      Std Dev: {stats['std']:.2f}")
                report.append(f"      Range: [{stats['min']:.2f}, {stats['max']:.2f}]")
        
        # Categorical summaries
        if self.categorical_cols:
            report.append(f"\n📋 CATEGORICAL COLUMNS:")
            for col in self.categorical_cols:
                unique_count = self.df[col].nunique()
                most_common = self.df[col].mode()[0] if len(self.df[col].mode()) > 0 else 'N/A'
                report.append(f"\n   {col}:")
                report.append(f"      Unique values: {unique_count}")
                report.append(f"      Most common: {most_common}")
        
        # Correlations (if applicable)
        if len(self.numeric_cols) >= 2:
            report.append(f"\n🔗 CORRELATIONS:")
            corr_matrix = self.get_correlation_matrix()
            
            # Find strongest correlations
            corr_pairs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    col1 = corr_matrix.columns[i]
                    col2 = corr_matrix.columns[j]
                    corr_val = corr_matrix.iloc[i, j]
                    corr_pairs.append((col1, col2, corr_val))
            
            # Sort by absolute correlation value
            corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
            
            report.append("\n   Strongest correlations:")
            for col1, col2, corr_val in corr_pairs[:3]:  # Top 3
                report.append(f"      {col1} ↔ {col2}: {corr_val:.2f}")
        
        report.append("\n" + "=" * 60)
        
        return "\n".join(report)
    
    def export_report(self, filepath: str = 'output/analysis_report.txt'):

        import os
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        report = self.generate_report()
        
        with open(filepath, 'w') as f:
            f.write(report)
        
        print(f"✓ Report exported to {filepath}")
