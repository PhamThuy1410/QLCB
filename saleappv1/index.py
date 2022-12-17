from flask import render_template, request, redirect, session, jsonify
from saleappv1 import dao, app, login, admin, controller
from flask_login import login_user, logout_user, current_user, login_required
from saleappv1.decorator import annonymous_user
import cloudinary.uploader


app.add_url_rule("/", 'index', controller.index)
app.add_url_rule('/chuyenbay/<int:macb>', 'detail', controller.detail)
app.add_url_rule('/login-admin', 'login-admin', controller.admin_login, methods=['post'])
app.add_url_rule('/register', 'register', controller.register, methods=['get', 'post'])

#
#     return render_template('register.html', err_msg=err_msg)
#
#
app.add_url_rule('/login', 'login-user', controller.login_my_user, methods=['get', 'post'])
app.add_url_rule('/logout', 'logout', controller.logout_my_user)


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)
