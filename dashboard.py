import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from typing import Optional, List
import warnings

warnings.filterwarnings('ignore')

class DashboardGenerator:
    def __init__(self, df: pd.DataFrame, title: str = "Data Analysis Dashboard"):
        self.df = df
        self.title = title
        self.numeric_cols = self._get_numeric_columns()
        self.categorical_cols = self._get_categorical_columns()
        
        # Set default style
        sns.set_style('whitegrid')
        sns.set_palette('husl')


    def _get_numeric_columns(self) -> List[str]:
        return self.df.select_dtypes(include=[np.number]).columns.tolist()
    
    def _get_categorical_columns(self) -> List[str]:
        return self.df.select_dtypes(include=['object']).columns.tolist()
    
    def create_overview_dashboard(self, save_path: Optional[str] = None):

        # Determine layout based on available data
        if len(self.numeric_cols) >= 2 and len(self.categorical_cols) >= 1:
            # Full dashboard: 2x2 grid
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle(self.title, fontsize=20, fontweight='bold', y=0.98)
            
            # 1. Summary Statistics Table (top-left)
            self._plot_summary_table(axes[0, 0])
            
            # 2. Distribution Plot (top-right)
            if len(self.numeric_cols) > 0:
                self._plot_distribution(axes[0, 1], self.numeric_cols[0])
            
            # 3. Correlation Heatmap (bottom-left)
            if len(self.numeric_cols) >= 2:
                self._plot_correlation(axes[1, 0])
            
            # 4. Categorical Counts (bottom-right)
            if len(self.categorical_cols) > 0:
                self._plot_categorical(axes[1, 1], self.categorical_cols[0])
        
        else:
            # Simplified dashboard
            fig, axes = plt.subplots(1, 2, figsize=(16, 6))
            fig.suptitle(self.title, fontsize=20, fontweight='bold')
            
            if len(self.numeric_cols) > 0:
                self._plot_distribution(axes[0], self.numeric_cols[0])
            
            if len(self.categorical_cols) > 0:
                self._plot_categorical(axes[1], self.categorical_cols[0])
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Dashboard saved to {save_path}")
        
        plt.show()
    
    def _plot_summary_table(self, ax):
        ax.axis('tight')
        ax.axis('off')
        
        # Create summary data
        summary_data = []
        summary_data.append(['Dataset Overview', ''])
        summary_data.append(['Total Rows', f"{len(self.df):,}"])
        summary_data.append(['Total Columns', f"{len(self.df.columns)}"])
        summary_data.append(['Numeric Columns', f"{len(self.numeric_cols)}"])
        summary_data.append(['Categorical Columns', f"{len(self.categorical_cols)}"])
        summary_data.append(['Missing Values', f"{self.df.isnull().sum().sum()}"])
        summary_data.append(['', ''])
        
        # Add numeric column stats
        if self.numeric_cols:
            summary_data.append(['Numeric Statistics', ''])
            for col in self.numeric_cols[:3]:  # Show first 3
                mean_val = self.df[col].mean()
                summary_data.append([f"{col} (mean)", f"{mean_val:.2f}"])
        
        # Create table
        table = ax.table(
            cellText=summary_data,
            cellLoc='left',
            loc='center',
            colWidths=[0.6, 0.4]
        )
        
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        
        # Style header rows
        for i in [0, 7]:
            if i < len(summary_data):
                table[(i, 0)].set_facecolor('#4CAF50')
                table[(i, 0)].set_text_props(weight='bold', color='white')
                table[(i, 1)].set_facecolor('#4CAF50')
        
        ax.set_title('Summary Statistics', fontsize=14, fontweight='bold', pad=20)
    
    def _plot_distribution(self, ax, column: str):
        data = self.df[column].dropna()
        
        # Create histogram
        ax.hist(data, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
        
        # Add mean and median lines
        mean_val = data.mean()
        median_val = data.median()
        
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, 
                   label=f'Mean: {mean_val:.2f}')
        ax.axvline(median_val, color='green', linestyle='--', linewidth=2, 
                   label=f'Median: {median_val:.2f}')
        
        ax.set_xlabel(column, fontsize=11)
        ax.set_ylabel('Frequency', fontsize=11)
        ax.set_title(f'Distribution of {column}', fontsize=14, fontweight='bold', pad=20)
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_correlation(self, ax):
        if len(self.numeric_cols) < 2:
            ax.text(0.5, 0.5, 'Insufficient numeric\ncolumns for correlation', 
                   ha='center', va='center', fontsize=12)
            ax.axis('off')
            return
        
        corr_matrix = self.df[self.numeric_cols].corr()
        
        # Create heatmap
        sns.heatmap(
            corr_matrix,
            annot=True,
            cmap='coolwarm',
            center=0,
            fmt='.2f',
            square=True,
            linewidths=1,
            cbar_kws={"shrink": 0.8},
            ax=ax
        )
        
        ax.set_title('Correlation Heatmap', fontsize=14, fontweight='bold', pad=20)
    

    def _plot_categorical(self, ax, column: str, top_n: int = 10):
        value_counts = self.df[column].value_counts().head(top_n)
        
        # Create bar chart
        colors = sns.color_palette('husl', len(value_counts))
        value_counts.plot(kind='barh', ax=ax, color=colors, edgecolor='black')
        
        ax.set_xlabel('Count', fontsize=11)
        ax.set_ylabel(column, fontsize=11)
        ax.set_title(f'Top {len(value_counts)} Values in {column}', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='x')
    
    def create_numeric_dashboard(self, save_path: Optional[str] = None):
        if len(self.numeric_cols) == 0:
            print("No numeric columns to visualize")
            return
        
        # Calculate grid size
        n_cols = len(self.numeric_cols)
        n_rows = (n_cols + 1) // 2  # Ceiling division
        
        fig, axes = plt.subplots(n_rows, 2, figsize=(16, 5 * n_rows))
        fig.suptitle(f'{self.title} - Numeric Analysis', 
                    fontsize=20, fontweight='bold', y=0.995)
        
        # Flatten axes for easier iteration
        if n_rows == 1:
            axes = axes.reshape(1, -1)
        
        for idx, col in enumerate(self.numeric_cols):
            row = idx // 2
            col_idx = idx % 2
            ax = axes[row, col_idx]
            
            self._plot_distribution(ax, col)
        
        # Hide empty subplots
        for idx in range(n_cols, n_rows * 2):
            row = idx // 2
            col_idx = idx % 2
            axes[row, col_idx].axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Numeric dashboard saved to {save_path}")
        
        plt.show()
    
    def create_categorical_dashboard(self, save_path: Optional[str] = None):
        if len(self.categorical_cols) == 0:
            print("No categorical columns to visualize")
            return
        
        n_cols = len(self.categorical_cols)
        n_rows = (n_cols + 1) // 2
        
        fig, axes = plt.subplots(n_rows, 2, figsize=(16, 5 * n_rows))
        fig.suptitle(f'{self.title} - Categorical Analysis', 
                    fontsize=20, fontweight='bold', y=0.995)
        
        if n_rows == 1:
            axes = axes.reshape(1, -1)
        
        for idx, col in enumerate(self.categorical_cols):
            row = idx // 2
            col_idx = idx % 2
            ax = axes[row, col_idx]
            
            self._plot_categorical(ax, col)
        
        # Hide empty subplots
        for idx in range(n_cols, n_rows * 2):
            row = idx // 2
            col_idx = idx % 2
            axes[row, col_idx].axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Categorical dashboard saved to {save_path}")
        
        plt.show()
    
    def create_comparison_plots(self, x_col: str, y_col: str, 
                                hue_col: Optional[str] = None,
                                save_path: Optional[str] = None):
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle(f'{self.title} - {x_col} vs {y_col}', 
                    fontsize=18, fontweight='bold')
        
        # Scatter plot
        if hue_col:
            for category in self.df[hue_col].unique():
                mask = self.df[hue_col] == category
                axes[0].scatter(self.df[mask][x_col], self.df[mask][y_col], 
                              label=category, alpha=0.6, s=50)
            axes[0].legend()
        else:
            axes[0].scatter(self.df[x_col], self.df[y_col], 
                          alpha=0.6, s=50, color='steelblue')
        
        axes[0].set_xlabel(x_col, fontsize=11)
        axes[0].set_ylabel(y_col, fontsize=11)
        axes[0].set_title('Scatter Plot', fontsize=14, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        
        # Box plot
        if hue_col and hue_col in self.categorical_cols:
            self.df.boxplot(column=y_col, by=hue_col, ax=axes[1])
            axes[1].set_xlabel(hue_col, fontsize=11)
            axes[1].set_title(f'{y_col} by {hue_col}', fontsize=14, fontweight='bold')
        else:
            self.df.boxplot(column=y_col, ax=axes[1])
            axes[1].set_title(f'{y_col} Distribution', fontsize=14, fontweight='bold')
        
        axes[1].set_ylabel(y_col, fontsize=11)
        plt.suptitle('')  # Remove the auto-generated title from boxplot
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Comparison plots saved to {save_path}")
        
        plt.show()

    def create_interactive_dashboard(self, dashboard_title: str = 'interactive_dashboard'):
        fig = px.scatter(self.df, x='age', y='salary', color='city')
        
        fig.write_html(f'output/{dashboard_title}.html')

# ============================================
# TESTING CODE

if __name__ == "__main__":
    # Create sample data
    np.random.seed(42)
    
    test_data = pd.DataFrame({
        'age': np.random.randint(20, 60, 200),
        'salary': np.random.randint(30000, 120000, 200),
        'experience': np.random.randint(0, 25, 200),
        'satisfaction': np.random.randint(1, 11, 200),
        'city': np.random.choice(['NYC', 'LA', 'Chicago', 'Boston', 'Austin'], 200),
        'department': np.random.choice(['Sales', 'Engineering', 'Marketing', 'HR'], 200)
    })
    
    test_data['salary'] = test_data['salary'] + (test_data['experience'] * 1500)
    test_data['satisfaction'] = test_data['satisfaction'] + (test_data['salary'] / 15000).astype(int)
    test_data['satisfaction'] = test_data['satisfaction'].clip(1, 10)
    
    print("=" * 60)
    print("DASHBOARD GENERATOR - TEST")
    
    # Initialize dashboard
    dashboard = DashboardGenerator(test_data, title="Employee Analytics Dashboard")
    
    print("\n📊 Creating Overview Dashboard...")
    print("(Close plot window to continue)")
    dashboard.create_overview_dashboard(save_path='output/overview_dashboard.png')
    
    print("\n📈 Creating Numeric Dashboard...")
    print("(Close plot window to continue)")
    dashboard.create_numeric_dashboard(save_path='output/numeric_dashboard.png')
    
    print("\n📋 Creating Categorical Dashboard...")
    print("(Close plot window to continue)")
    dashboard.create_categorical_dashboard(save_path='output/categorical_dashboard.png')
    
    print("\n🔍 Creating Comparison Plots...")
    print("(Close plot window to continue)")
    dashboard.create_comparison_plots('experience', 'salary', hue_col='department',
                                     save_path='output/comparison_plots.png')
    
    print("\n🌐 Creating Interactive Dashboard...")
    dashboard.create_interactive_dashboard()


    print("\n" + "=" * 60)
    print("✓ ALL DASHBOARDS CREATED!")