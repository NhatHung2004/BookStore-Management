from flask_admin.contrib.sqla import ModelView
from app import db, app, dao
from models import Staff, Book, Category, Author, UserRole, User, Form
from flask_admin import Admin, BaseView, expose
from flask_login import current_user, logout_user
from flask import redirect

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


class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html', stats=dao.revenue_stats())


# admin.add_view(ModelView(Bill, db.session))
# admin.add_view(ModelView(BookEntryForm, db.session))
admin.add_view(CategoryView(Category, db.session))
admin.add_view(AuthorView(Author, db.session))
admin.add_view(BookView(Book, db.session))
admin.add_view(StatsView(name='Thống kê - báo cáo'))

