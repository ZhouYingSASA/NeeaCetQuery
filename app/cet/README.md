# api/cet/result

## GET  —— 获取验证码图片

地址栏传参 zkzh = 准考证号

返回
```json
{"data":
    {"img_url": 验证码图片地址},
    "msg"： 成功"ok"失败"获取失败"
}
```

## POST  —— 获取结果

传入
```json
{
    "zkzh": 准考证号,
    "name": 姓名,
    "v": 验证码
}
```

返回
```json
{
    "data":{
        'ID': 准考证号,
        'name': 姓名,
        'school': 学校,
        'score': 总分,
        'time': ？,
        'listening': 听力,
        'reading': 阅读,
        'trabslate': 写作和翻译,
        'oralID': 口语考试准考证号,
        'oralLevel': 口语考试等级,
        'exam_type': 考试类别('CET4'或'CET6')
    },
    "status": 1或0,
    "msg": "ok"或"获取失败"
}
```

# api/cet/zkzh

## GET  —— 查询准考证号

header传参 Authorization = 云家园token (无开头 passport)

返回
```json
{
    "data":{
        "zkzh": 准考证号,
        "xm": 姓名
    },
    "msg": 状态信息,
    "status": 状态: 0数据库查询失败，1成功，2四六级数据库内无此人信息
}
```