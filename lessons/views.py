import json
from django.shortcuts import render

from common.utils import common_response, logger
from lessons.models import HomeworkSubject, Homework


def homework_code(request):
    if request.method == "POST":
        req = request.POST
        # req = json.loads(request.body)
        code = req.get('code')
        uid = req.get('uid')
        sid = req.get('sid')
        logger.info(code)
        homework = Homework.objects.filter(user_id=uid, homework_subject_id=sid).first()
        if homework:
            homework.code = code
        else:
            homework = Homework(user_id=uid, homework_subject_id=sid, code=code)
            homework.save()
    return common_response(message="保存成功")
