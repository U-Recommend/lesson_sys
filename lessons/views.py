import json
from django.shortcuts import render
from django.http import JsonResponse
from common.utils import common_response, logger, admin_page_calculate_result
from common.models import User, Grade
from lessons.models import Exercises, Homework, Lesson
from lessons.serializers.exercises import exercises_data
from lessons.serializers.homework import stdoutIO, homework_create_or_update
from lessons.serializers.lesson import lesson_filter
from lessons.serializers.attendance import attendance_data


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


# 考勤列表页面
def attendance_list_page(request):
    if request.method == "GET":
        user = request.user
        lessons = [{"id": l.id, "name": l.course.title} for l in Lesson.objects.filter(user=user, is_deleted=0)]
        users = None
        grades = None
        if user.is_superuser:
            users = [{'id': u.id, 'name': u.name} for u in User.objects.filter(is_active=True, is_superuser=False)]
            grades = [{'id': g.id, 'name': g.name} for g in Grade.objects.filter(is_deleted=0)]
        datas = {
            'user': user,
            'lessons': lessons,
            'users': users,
            'grades': grades
        }
        return render(request, "attendance_list.html", datas)


# 考勤列表
def attendance_list(request):
    if request.method == "GET":
        user = request.user
        logger.info(request.GET)
        filter_lesson = request.GET.get("filter_lesson")
        filter_grade = request.GET.get("filter_grade")
        filter_user = request.GET.get("filter_user")
        date__gte = request.GET.get('date__gte')
        date__lte = request.GET.get('date__lte')
        if user.is_superuser:
            query = lesson_filter()
        else:
            query = lesson_filter(user=user)
        if filter_lesson:
            query = query.filter(id=filter_lesson)
        if filter_grade:
            query = query.filter(user__grade_id=filter_grade)
        if filter_user:
            query = query.filter(user=filter_user)
        if date__gte:
            query = query.filter(lesson_date__gte=date__gte)
        if date__lte:
            query = query.filter(lesson_date__lte=date__lte)
        data_dict = {}
        try:
            logger.info(query.count())
            data_dict, datas = admin_page_calculate_result(request_data=request, data=query)
            result = []
            for data in datas:
                logger.info(data.id)
                res = attendance_data(lesson=data, user=user)
                result.append(res)
            data_dict['rows'] = result
        except Exception as ex:
            logger.exception(ex)
        return JsonResponse(data_dict)
