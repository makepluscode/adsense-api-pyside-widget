# AdSense API example

## Overview
Python script to automatically check your daily Google AdSense earnings using the AdSense API. No more manual login to check your revenue!

## Features
- Real-time AdSense earnings check
- OAuth 2.0 authentication 
- Automatic token refresh
- Desktop widget display
- Error handling

## Prerequisites
- Python 3.x
- Google AdSense account
- Google Cloud Console project with AdSense API enabled
- PySide6

## Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/adsense-revenue-tracker.git
cd adsense-revenue-tracker
```

2. Run install.bat to set up the environment
```bash
install.bat
```

## Configuration
1. Create a project at [Google Cloud Console](https://console.cloud.google.com)
2. Enable AdSense API
3. Create OAuth 2.0 credentials (Desktop app)
4. Download and rename credentials as `credentials.json`
5. Place `credentials.json` in the `config` directory
6. Create `.env` file in `config` directory with following content:
```
CREDENTIALS_FILE=config/credentials.json
TOKEN_FILE=config/token.pickle
REFRESH_INTERVAL=600000
WIDGET_WIDTH=400
WIDGET_HEIGHT=100
```

## Environment Variables
- `CREDENTIALS_FILE`: Path to Google OAuth credentials file
- `TOKEN_FILE`: Path to store OAuth token
- `REFRESH_INTERVAL`: Data refresh interval in milliseconds (default: 600000 = 10 minutes)
- `WIDGET_WIDTH`: Widget window width in pixels
- `WIDGET_HEIGHT`: Widget window height in pixels

## Usage
Run the application:
```bash
python main.py
```

The widget will appear in the top-right corner of your screen showing:
- Today's earnings
- Yesterday's earnings
- Last 7 days earnings
- This month's earnings

To close the widget, select it and press ESC or Q.

## License
MIT License

## Acknowledgments
- Google AdSense API
- Google Cloud Platform
- PySide6