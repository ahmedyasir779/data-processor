# 📊 Data Processing Pipeline

A professional, production-ready data processing toolkit for loading, cleaning, analyzing, and visualizing data.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

## ✨ Features

- 🔄 **Multi-format Data Loading** - Load CSV, JSON, and Excel files
- 🧹 **Intelligent Data Cleaning** - Handle missing values, duplicates, outliers
- 📊 **Statistical Analysis** - Generate comprehensive statistics and insights
- 📈 **Beautiful Visualizations** - Create professional dashboards automatically
- 🖥️ **Command-Line Interface** - Easy-to-use CLI with colored output
- 📝 **Comprehensive Logging** - Track all operations with detailed logs
- ✅ **Fully Tested** - Unit and integration tests included

## Features in Detail
Data Loading

✅ CSV files (.csv)
✅ JSON files (.json)
✅ Excel files (.xlsx, .xls)
✅ Automatic format detection
✅ Error handling for corrupted files

Data Cleaning

✅ Handle missing values (drop, fill, forward-fill)
✅ Remove duplicates
✅ Clean string columns (strip whitespace)
✅ Remove outliers (IQR method)
✅ Data type conversion
✅ Generates cleaning report

Statistical Analysis

✅ Summary statistics (mean, median, std, etc.)
✅ Correlation analysis
✅ Value counts for categorical data
✅ Distribution analysis
✅ Exportable reports

Visualizations

✅ Overview dashboard (2x2 grid)
✅ Distribution plots (histograms)
✅ Correlation heatmaps
✅ Categorical bar charts
✅ Comparison plots (scatter + box)
✅ High-resolution exports (300 DPI)


## CLI Options
Options:
  --file, -f          Input file path (required)
  --clean, -c         Clean the data
  --clean-strategy    Strategy: drop, fill, forward_fill (default: drop)
  --analyze, -a       Generate analysis report
  --dashboard, -d     Create visualization dashboard
  --all               Run complete pipeline (clean + analyze + dashboard)
  --output, -o        Output directory (default: output/)
  --title, -t         Custom dashboard title
  --interactive, -i   Run in interactive mode
  --help, -h          Show help message

  
## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/ahmedyasir779/data-processor
cd data-processor

# Create virtual environment
python -m venv venv

# Install dependencies
pip install -r requirements.txt
```

Author
Ahmed Yasir

GitHub: @Yahmedyasir779 
LinkedIn: www.linkedin.com/in/ahmed-yasir-907561206
