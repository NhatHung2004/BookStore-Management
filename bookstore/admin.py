from flask_admin.contrib.sqla import ModelView
from models import Staff
from bookstore import db, admin


# class StaffView(ModelView):
#     column_display_pk = False
#     can_create = True
#     can_edit = True
#     can_delete = True
#     create_modal = True


admin.add_view(ModelView(Staff, db.session))
