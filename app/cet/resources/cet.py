from app import db
from app.authentication import verify_token
from flask import Response, json, g
from ..models.models import QueryLog
from app.utils.cet import NeeaCetQuery
from flask_restful import Resource, request


class Cet(Resource):

    def get(self):
        """neea cet查询验证码"""

        data = {}
        staus = 0
        query = NeeaCetQuery()
        get_img = query.get_image(zkzh=request.args.get('zkzh'))  # 该函数只需要准考证号即可
        if get_img:
            data["img_url"], result_cookies = get_img
            resp = Response(json.dumps({'data': {'img_url': data['img_url']},
                                        'msg': "ok"}))
            for key in result_cookies:
                resp.set_cookie(key, result_cookies[key])
        else:
            resp = Response(json.dumps({'data': {}, 'msg': "获取失败"}))
        return resp

    def post(self):
        """neea cet 查询"""

        query = NeeaCetQuery()
        r = query.get_result(str(request.form.get('zkzh')), str(request.form.get('v')), str(request.form.get('name')),
                             request.cookies)
        data = r
        status = r[1]
        msg = "ok" if r[1] else "获取失败"
        try:
            log = QueryLog.query.filter_by(zkzh=data[0]['ID'], means=True).first()
            if not log:
                log = QueryLog(ip=request.remote_addr, zkzh=data[0]['ID'], xm=request.form.get('name'))
            db.session.add(log)
            db.session.commit()
        finally:
            db.session.close()
        return {
            "data": data[0],
            "status": status,
            "msg": msg
        }
    # data:({'ID': '360**********22', 'name': '***', 'school': '南昌大学',
    # 'score': '511.00', 'time': '0', 'listening': '161', 'reading': '203', 'translate': '147',
    # 'oralId': '--', 'oralLevel': '--', 'exam_type': 'CET4'}, 1)


class Zkzh(Resource):
    """查询准考证号"""

    def get(self):
        data = {}
        token = request.headers.get('Authorization')
        if not token:
            return {"msg": "缺少token"}
        elif not verify_token(token):
            return {"msg": "token错误", "status": 0}
        sql = 'SELECT CET.zkzh, USER.xm FROM ***.cetinfo_2019_1 AS CET LEFT JOIN ***.xs_jbxx AS USER ' \
              'ON CET.xh = USER.xh WHERE CET.xh =:XH'
        try:
            data['zkzh'], data['xm'] = db.session.execute(sql, {"XH": g.current_user.username}).first()
            msg = "ok"
            status = 1
        except:
            msg = "查询失败，数据库连接错误"
            status = 0
        finally:
            db.session.close()
        if 'zkzh' not in data:
            msg = "查询失败，信息不存在"
            status = 2
        else:
            log = QueryLog(ip=request.remote_addr, means=True, zkzh=data['zkzh'], xm=data['xm'])
            try:
                db.session.add(log)
                db.session.commit()
            finally:
                db.session.close()
        return {
            "data": data,
            "msg": msg,
            "status": status
        }

    # def post(self):
    #     data = {}
    #     user = User.query.filter_by(username=request.form.get('xh'))
    #     sql = 'SELECT CET.zkzh, USER.xm FROM cetinfo_2019_1 AS CET LEFT JOIN xs_jbxx AS USER ' \
    #           'ON CET.xh = USER.xh WHERE CET.xh =:XH'
    #     try:
    #         data['zkzh'], data['xm'] = db.session.execute(sql, {"XH": user.username}).first()
    #         msg = "ok"
    #         status = 1
    #     except:
    #         msg = "查询失败，数据库连接错误"
    #         status = 0
    #     db.session.close()
    #     if not data:
    #         msg = "查询失败，信息不存在"
    #         status = 2
    #     return {
    #         "data": data,
    #         "msg": msg,
    #         "status": status
    #     }
