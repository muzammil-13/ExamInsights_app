# Logging Configuration

## Overview
The `app.py` has been configured with comprehensive logging that writes to both console and log files.

## Log File Location
Log files are stored in the `logs/` directory with the naming convention:
```
app_YYYYMMDD_HHMMSS.log
```

Each application run creates a new timestamped log file to prevent log rotation issues.

## Log Levels

### Console Output
- **Level**: INFO
- **Format**: `TIMESTAMP NAME LEVEL MESSAGE`
- **Purpose**: Real-time monitoring during development

### File Output
- **Level**: DEBUG (more detailed than console)
- **Format**: `TIMESTAMP [LEVEL] NAME: MESSAGE`
- **Purpose**: Detailed troubleshooting and debugging

## What Gets Logged

### Initialization
- Application startup and log file location
- Configuration loading
- LLM model initialization
- Embedding model initialization
- Server configuration

### Data Sources
- Source loading progress
- Source type (local, Google Drive, SharePoint)
- Success/failure of each source

### Runtime
- Server startup
- Error conditions with full stack traces

## Example Log Output

**Console:**
```
2026-05-21 11:26:01 root INFO Application started. Log file: logs/app_20260521_112601.log
2026-05-21 11:26:02 root INFO Loading configuration from: config.yaml
2026-05-21 11:26:02 root INFO Configuration loaded successfully
```

**File (logs/app_20260521_112601.log):**
```
2026-05-21 11:26:01 [INFO] root: Application started. Log file: logs/app_20260521_112601.log
2026-05-21 11:26:02 [INFO] root: Loading configuration from: config.yaml
2026-05-21 11:26:02 [INFO] root: Configuration loaded successfully
```

## Usage

No additional configuration needed! Logging is automatically enabled when you run:
```bash
python app.py
```

Or with a custom config file:
```bash
python app.py --config_file custom_config.yaml
```

## Viewing Logs

### Latest Log
```bash
# On Linux/Mac
tail -f logs/app_*.log

# On Windows PowerShell
Get-Content logs/app_*.log -Tail 20 -Wait
```

### All Logs
```bash
# List all log files
ls logs/
```

## .gitignore
Log files are excluded from git via `.gitignore` entries:
- `logs/` directory
- `*.log` files

This prevents large log files from being committed to the repository.
