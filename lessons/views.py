import json
from django.shortcuts import render

from common.utils import common_response, logger
from lessons.models import HomeworkSubject, Homework
from lessons.serializers.homework import stdoutIO


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


def compile_code(request):
    if request.method == "POST":
        req = request.POST
        code = req.get('code')
        try:
            with stdoutIO() as s:
                exec(code)
            res = s.getvalue()
            logger.info(res)
            return common_response(result=res)
        except Exception as ex:
            logger.exception(ex)
            return common_response(code=20000, message="运行失败", result=str(ex))
