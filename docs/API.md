# API Reference

Complete reference for using Data Processor as a Python library.

## DataLoader

### Class: `DataLoader(file_path: str)`

Load data from various file formats.

**Parameters:**
- `file_path` (str): Path to the data file

**Methods:**

#### `load() -> pd.DataFrame`
Load the file and return a DataFrame.

**Returns:**
- pandas DataFrame containing the loaded data

**Raises:**
- `FileNotFoundError`: If file doesn't exist
- `ValueError`: If file format is unsupported

**Example:**
```python
loader = DataLoader('data.csv')
df = loader.load()
print(f"Loaded {len(df)} rows")

get_info() -> dict
Get information about the loaded data.
Returns:

Dictionary with keys: 'rows', 'columns', 'column_names', 'memory_usage', 'missing_values'

