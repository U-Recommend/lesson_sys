import json
from django.shortcuts import render

from common.utils import common_response, logger
from lessons.models import Exercises, Homework
from lessons.serializers.exercises import exercises_data
from lessons.serializers.homework import stdoutIO, homework_create_or_update


def exercises_detail(request):
    if request.method == "GET":
        exercises_id = request.GET.get('exercises_id')
        user_id = request.GET.get('user_id')
        lesson_id = request.GET.get('lesson_id')
        data = exercises_data(eid=exercises_id, uid=user_id, lesson_id=lesson_id)
        return common_response(result=data)


def homework_code(request):
    if request.method == "POST":
        req = request.POST
        code = req.get('code')
        content = req.get('content')
        user_id = req.get('uid')
        lesson_id = req.get('lid')
        exercises_id = req.get('eid')
        logger.info(code)
        homework = homework_create_or_update(user_id=user_id, lesson_id=lesson_id, exercises_id=exercises_id,
                                             content=content, code=code)
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
