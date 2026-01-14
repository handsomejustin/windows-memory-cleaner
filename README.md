# Windows Memory Cleaner

A system tray application for Windows that monitors and cleans system memory cache to improve system performance.

## Overview

Windows Memory Cleaner is a lightweight utility that runs in the system tray and provides real-time monitoring of memory usage. It allows users to manually clean memory caches or configure automatic cleaning based on memory usage thresholds.

## Features

- Real-time memory usage monitoring in the system tray
- Manual memory cache cleaning with a single click
- Configurable warning thresholds for memory usage
- Optional automatic memory cleaning when usage exceeds threshold
- Customizable refresh intervals for memory monitoring
- Visual indicators for memory usage levels
- Logging system for tracking cleaning operations

## Installation

### Prerequisites

- Windows 10 or later
- Python 3.8 or higher

### Setup

1. Clone or download this repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

- `pystray` (>=0.19.5) - System tray icon functionality
- `psutil` (>=5.9.5) - System and process utilities
- `pywin32` (>=305) - Windows-specific API access

## Usage

### Starting the Application

Run the application using Python:
```bash
python -m src
```

The application will appear in the system tray with a memory usage indicator.

### System Tray Menu

Right-click the system tray icon to access the following options:

- **Show Memory Info** - Display current memory usage statistics
- **Clean Memory** - Manually trigger memory cache cleaning
- **Settings** - Configure warning thresholds, auto-clean settings, and refresh intervals
- **Exit** - Close the application

## Configuration

The application can be configured through the `config.json` file:

```json
{
  "warning_threshold": 85,
  "auto_clean": false,
  "auto_clean_threshold": 80,
  "refresh_interval": 5
}
```

### Configuration Options

- `warning_threshold` (integer, 0-100): Memory usage percentage that triggers a warning (default: 85)
- `auto_clean` (boolean): Enable automatic memory cleaning (default: false)
- `auto_clean_threshold` (integer, 0-100): Memory usage percentage that triggers auto-cleaning (default: 80)
- `refresh_interval` (integer): Seconds between memory usage updates (default: 5)

## Project Structure

```
clear_mem/
├── src/              # Application source code
├── icons/            # Application icons
├── logs/             # Application logs (runtime)
├── docs/             # Documentation
├── config.json       # Configuration file
└── requirements.txt  # Python dependencies
```

## Security Considerations

Memory cleaning operations require appropriate system permissions. The application uses Windows API functions through `pywin32` to perform memory operations safely.

## License

This project is provided as-is for educational and utility purposes.

## Version

Current version: 0.1.0
