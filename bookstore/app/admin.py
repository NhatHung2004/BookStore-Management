from datetime import datetime

from flask_admin.contrib.sqla import ModelView
from app import db, app, dao
from models import Staff, Book, Category, Author, UserRole, User, Form
from flask_admin import Admin, BaseView, expose
from flask_login import current_user, logout_user
from flask import redirect, request

admin = Admin(app=app, name="Bookstore Admin", template_mode='bootstrap4')

class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class CategoryView(AdminView):
    column_list = ['name', 'books']


class AuthorView(AdminView):
    column_list = ['name', 'books']


class BookView(AdminView):
    column_list = ['id', 'name', 'price', 'inventoryQuantity', 'category']
    can_export = True
    column_searchable_list = ['name']
    page_size = 4
    column_filters = ['id', 'name', 'price']
    column_editable_list = ['name']
    form_excluded_columns = ['bills', 'bookEntryForms', 'onlineOrders']


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class StatsView(BaseView):
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
                           book_frequency_stats =book_frequency_stats, total_revenue=total_revenue)




# admin.add_view(ModelView(Bill, db.session))
# admin.add_view(ModelView(BookEntryForm, db.session))
admin.add_view(CategoryView(Category, db.session))
admin.add_view(AuthorView(Author, db.session))
admin.add_view(BookView(Book, db.session))
admin.add_view(StatsView(name='Thống kê - báo cáo'))

