# Keylogger Script with Email Logging

This project is a Python-based keylogger that captures keystrokes on a system, logs them to a file, and periodically emails the log file content to a specified email address.

## Features

- Captures all keystrokes, including special keys (e.g., Enter, Space, Tab).
- Logs keystrokes to a text file.
- Periodically emails the log file content.
- Automatically clears the log file after sending an email.
- Runs in the background with the ability to hide the console window.

## Requirements

- Python 3.x
- Required Python libraries:
  - `pynput`
  - `logging`
  - `smtplib`
  - `email`
  - `threading`
  - `zipfile`

To install the dependencies, you can use the following command:

```bash
pip install pynput
```

## Configuration

Update the following variables in the script to configure the keylogger:

- **Email Settings**
  - `EMAIL_ADDRESS`: Your email address used to send the logs.
  - `EMAIL_PASSWORD`: Your email password.
  - `TO_EMAIL`: Recipient's email address.
  - `SMTP_SERVER`: SMTP server (default: `smtp.gmail.com`).
  - `SMTP_PORT`: SMTP port (default: `587`).

- **Log File Settings**
  - `LOG_DIR`: Directory to store the log files (default: system's temporary directory).
  - `LOG_FILE`: Log file name.
  - `ZIP_FILE`: Compressed log file name.

- **Email Interval**
  - `EMAIL_INTERVAL`: Interval (in seconds) to send the log file via email (default: `20`).

## Usage

1. Configure the script with the correct email credentials and settings.
2. Run the script:

   ```bash
   python keylogger.py
   ```

3. The keylogger will run in the background and capture keystrokes.
4. Logs will be sent via email at the configured interval.

## How It Works

1. **Key Logging**:
   - The script uses the `pynput` library to capture keystrokes.
   - Keystrokes are logged into a text file.

2. **Email Sending**:
   - A background thread periodically reads the log file.
   - The content is sent as an email body using the `smtplib` library.
   - After sending, the log file is cleared to prevent duplicate logs.

3. **Console Window Hiding**:
   - The script hides the console window on Windows systems using the `ctypes` library.

## Security Warning

This script is for educational purposes only. Unauthorized use of keyloggers is illegal and unethical. Use responsibly and ensure you have explicit permission to monitor any system.

## Disclaimer

The developer is not responsible for any misuse of this script. It is intended solely for learning and authorized use cases.

