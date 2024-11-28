# AdSense API example

## Overview
Python script to automatically check your daily Google AdSense earnings using the AdSense API. No more manual login to check your revenue!

## Features
- Real-time AdSense earnings check
- OAuth 2.0 authentication
- Automatic token refresh
- JSON formatted output
- Error handling

## Prerequisites
- Python 3.x
- Google AdSense account
- Google Cloud Console project with AdSense API enabled

## Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/adsense-revenue-tracker.git
cd adsense-revenue-tracker
```

2. Install required packages
```bash
pip install google-auth-oauthlib google-api-python-client
```

3. Set up Google Cloud Console
- Create a project at [Google Cloud Console](https://console.cloud.google.com)
- Enable AdSense API
- Create OAuth 2.0 credentials
- Download credentials.json

## Configuration
1. Place your `credentials.json` in the project directory
2. Run the script first time to authorize:
```bash
python main.py
```

## Usage
Simply run:
```bash
python main.py
```

Example output:
```json
{
  "date": "2024-11-28",
  "estimated_earnings": 12.34,
  "currency": "USD"
}
```

## Error Handling
The script handles common errors:
- No AdSense account found
- API authentication errors
- No data available

## Contributing
Feel free to open issues or submit pull requests.

## License
MIT License

## Author
Your Name

## Acknowledgments
- Google AdSense API
- Google Cloud Platform