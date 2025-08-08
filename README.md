# Quản lý tiệm sách

Đây là website được xây dựng bằng Flask, sử dụng SQLAlchemy để tương tác với cơ sở dữ liệu và Flask-Admin để tạo giao diện admin. Dự án cũng tích hợp Flask-Login để xử lý xác thực người dùng và Flask-Mail để gửi email.
## Các tính năng nổi bật

- Cơ sở dữ liệu: Sử dụng SQLAlchemy làm ORM (Object-Relational Mapper) để tương tác với cơ sở dữ liệu MySQL (PyMySQL).
- Tác vụ nền: Sử dụng APScheduler để lên lịch và thực hiện các tác vụ nền định kỳ (xoá các đơn hàng đến hạn).
- Lưu trữ cloud: Tích hợp Cloudinary để quản lý và lưu trữ file trên cloud.
- Gửi email: Hỗ trợ gửi email thông qua Flask-Mail.


## Cài đặt

1.Môi trường ảo

```bash
  # Tạo môi trường ảo
  cd app
  python -m venv venv

  # Kích hoạt môi trường ảo
  # Trên Windows
  venv\Scripts\activate
  # Trên macOS/Linux
  source venv/bin/activate
```

2.Cài đặt các thư viện
```bash
  pip install -r requirements.txt
```

3.Đăng ký Cloudinary và VNPay để lưu trữ ảnh và test chức năng thanh toán

```bash
  # Cloudinary
  https://cloudinary.com/users/register_free
  # Đăng ký tài khoản vnpay developer kiểm thử
  https://sandbox.vnpayment.vn/apis/docs/gioi-thieu/
```

4.Chạy dự án
```bash
  # Tạo database storedb trong workbench
  # Tạo dữ liệu mẫu
  python models.py
  # Chạy dự án
  python routes.py
```
    
## Các biến môi trường

Để chạy dự án này, ta cần phải thêm các biến môi trường bên dưới vào file .env

`API_KEY`

`API_SECRET`

`MYSQL_USERNAME`

`MYSQL_PASSWORD`

`CLOUD_NAME`

`MAIL_USERNAME`

`MAIL_PASSWORD`

`SECRET_KEY`

`VNP_TMN_CODE`

`VNP_HASH_SECRET`

`VNP_URL`

