# coding: utf-8
from app import db

UsersRoles = db.Table()

RolesApps = db.Table()

RolesPermissions = db.Table()


class ModelBase:
    """base class for to_json function"""
    ...


class App(db.Model):
    """for app permission system, mainly in passport"""
    __tablename__ = '***'
    id = ...
    something = ...
    roles = ...

    def __repr__(self):
        return '<{} {} {}>'.format(self.__class__.__name__,
                                   self.something, self.something)

    def to_json(self):
        return {
            'id': self.id
        }

    def to_json_with_roles(self):
        dic = self.to_json()
        dic['roles'] = [role.id for role in self.roles]
        return dic


class Permission(db.Model):
    """for single permission system, mainly in ncuhome_cn"""
    __tablename__ = '***'
    pass


class Role(ModelBase, db.Model):
    __tablename__ = '***'
    pass


class User(ModelBase, db.Model):
    __tablename__ = '***'

    id = db.Column()

    username = db.Column()  # student id or teacher id

    # 用户名经加密后的唯一标识, 已使用MySQL触发器为每个用户生成,无需手动设置
    user_code = db.Column()

    roles = db.relationship()

    def __repr__(self):
        return '<{} {} {}>'.format(self.__class__.__name__,
                                   self.id, self.username)

    def __init__(self, username, name='',
                 nickname: str = None, password='123',
                 about_me='', roles: list = None, is_teacher=False):
        if roles is None:
            roles = []
        self.id = 123
        self.username = username
        self.name = name
        self.nickname = nickname
        self.password = password
        self.about_me = about_me
        self.roles = roles
        self.is_teacher = is_teacher

    def generate_id(self):
        """generate a unique id with 10 charaters"""
        ...

    @property
    def password(self):
        """password is a readable property"""
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """Set password_hash via password."""
        ...

    def change_password(self, oldpassword, newpassword):
        """change password"""
        ...

    def reset_password(self):
        ...

    def verify_password(self, password):
        """verify password"""
        ...

    def set_verify_code_time(self):
        """set verify_code in use for 10 minutes"""
        ...

    def verify_verify_code(self, code):
        """
        verify the verify_code
        return True/False 'message'
        """
        ...

    def modify_phone_num(self, phone_num):
        """修改电话号码"""
        ...

    def generate_auth_token(self, expiration=3000):
        """gernerate auth token, default expire time is 5 minutes"""
        ...

    @staticmethod
    def verify_auth_token(token):
        ...

    def ping(self):
        """refresh last_login when the user login"""
        ...

    def generate_verify_code(self):
        ...

    def get_phone_num(self):
        ...

    def get_profile(self):
        ...

    def get_model(self):
        ...

    def to_json(self):
        ...


class AppType(db.Model):
    __tablename__ = '***'
    ...


class YH_TXGL(db.Model):
    u"""头像管理."""

    __tablename__ = '***'
    ...


class BlackListUsername(db.Model):
    """黑名单"""

    __tablename__ = "***"
    ...
