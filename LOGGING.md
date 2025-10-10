# Logging Guide

## Log Files

The pipeline creates log files in the `logs/` directory:

- **`pipeline_YYYYMMDD.log`** - All logs (DEBUG level and above)
- **`errors_YYYYMMDD.log`** - Only errors and critical issues

## Log Levels

- **DEBUG** - Detailed diagnostic information
- **INFO** - General informational messages
- **WARNING** - Warning messages (potential issues)
- **ERROR** - Error messages (failures)
- **CRITICAL** - Critical failures

## Viewing Logs

### View latest pipeline log:
```bash


tail -f logs/pipeline_*.log
