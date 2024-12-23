from flask_admin.contrib.sqla import ModelView
from app import db, app, dao
from models import Staff, Book, Category, Author, UserRole, User, Form, ImportRule, Customer
from flask_admin import Admin, BaseView, expose
from flask_login import current_user, logout_user
from flask import redirect, request
from datetime import datetime
from flask_admin.form import rules

admin = Admin(app=app, name="Bookstore Admin", template_mode='bootstrap4')

class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class MyView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class RuleView(AdminView):
    column_list = ['min_quantity', 'max_quantity']


class UserView(AdminView):
    column_list = ['username', 'user_role']

    # Hàm xử lý trước khi lưu vào database
    def on_model_change(self, form, model, is_created):
        if form.password.data:  # Nếu có mật khẩu được nhập
            model.set_password(form.password.data)  # Băm mật khẩu trước khi lưu

        super().on_model_change(form, model, is_created)

        if is_created and model.user_role == UserRole.CUSTOMER:

            # Tạo bản ghi Customer với customerID = userID
            customer = Customer(user=model, phone="0123456789", address="Nhà Bè")
            db.session.add(customer)
            db.session.commit()  # Lưu Customer vào database



        return model

    # Ẩn mật khẩu băm khỏi danh sách người dùng
    column_exclude_list = ['password']

    # Đặt quy tắc hiển thị form
    form_edit_rules = [
        rules.Field('username'),
        rules.Field('password')
    ]

class LogoutView(MyView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class StatsView(MyView):
    @expose('/')
    def index(self):
        # Lấy giá trị tháng và năm từ sự kiện click của button
        month = request.args.get('month', type=int)
        year = request.args.get('year', type=int)

        # Gọi hàm DAO để lấy dữ liệu thống kê
        month_revenue_stats = dao.month_revenue_stats(month, year)
        book_frequency_stats = dao.book_frequency_stats(month, year)

        total_revenue = sum([s[2] for s in month_revenue_stats])

        # Trả về dữ liệu thống kê
        return self.render('admin/stats.html', month_revenue_stats=month_revenue_stats,
                           book_frequency_stats=book_frequency_stats, total_revenue=total_revenue)

admin.add_view(RuleView(ImportRule, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(StatsView(name='Thống kê - Báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))
