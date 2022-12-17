from saleappv1.models import SanBay, ChuyenBay, TramDung, Ve, User, TuyenBay, HangVe
from saleappv1 import db, app, dao
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea

class VeView(ModelView):
    can_view_details = True

    def is_accessible(self):
        return current_user.is_authenticated

class StatsView(BaseView):
    @expose('/')
    def index(self):
        sanbay = dao.load_sanbay()
        doanhthu = dao.thongke()

        return self.render('admin/stats.html', sanbay=sanbay, doanhthu=doanhthu)
    def is_accessible(self):
        return current_user.is_authenticated



admin = Admin(app=app, name='Quản trị chuyến bay', template_mode='bootstrap4')

admin.add_view(VeView(Ve, db.session, name='Bán Vé'))
admin.add_view(VeView(ChuyenBay, db.session, name='Tạo Lịch'))
admin.add_view(VeView(TramDung, db.session, name='Trạm Dừng'))
admin.add_view(VeView(TuyenBay, db.session, name='Tuyến Bay'))
admin.add_view(VeView(SanBay, db.session, name='Sân Bay'))
admin.add_view(VeView(User, db.session, name='Quản lý User'))
admin.add_view(StatsView(name='Thống kê'))


