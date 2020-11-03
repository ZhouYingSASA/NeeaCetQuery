# coding: utf-8
from functools import wraps

from flask import g

from app.user.models.user_model import User
from . import auth, inner_auth


@inner_auth.verify_password
def verify_password(username, password):
    if username == '......' and password == '***':
        return True
    elif username == '...' and password == '***':
        return True
    else:
        return False


@auth.verify_token
def verify_token(token):
    if token == '':
        return False
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.current_user = user
    return True


def require_admin(func):
    """
    验证用户是否是管理员
    :param func: 被装饰的resources函数
    :user: 目标用户
    :return:
    """

    @wraps(func)
    def _verify(self):
        # verify role and permission
        # only admin can create, delete
        ...
        return func(self)

    return _verify
