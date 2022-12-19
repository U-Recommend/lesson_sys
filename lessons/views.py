import json
from django.shortcuts import render
from django.http import JsonResponse
from common.utils import common_response, logger, page_calculate
from common.models import User, Grade, STATUS
from lessons.models import Exercises, Homework, Lesson
from lessons.serializers.exercises import exercises_filter, exercises_data, student_exercises_data
from lessons.serializers.homework import stdoutIO, homework_create_or_update
from lessons.serializers.lesson import lesson_filter, lesson_data
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


# 课程页面
def lesson_list_page(request):
    if request.method == "GET":
        user = request.user
        if user.is_superuser:
            lessons = lesson_filter()
        else:
            logger.info(dir(user))
            lessons = lesson_filter().filter(grade_id=user.grade_id)
        grades = Grade.objects.filter(is_deleted=0).values_list('id', 'name')
        grades = [{'id': i[0], 'name': i[1]} for i in grades]
        nums = list(set(list(lessons.values_list('num', flat=True))))
        nums.sort()
        logger.info(nums)
        status = [{'id': i, 'name': v} for i, v in STATUS]
        datas = {
            'nums': nums,
            'grades': grades,
            'statuss': status,
            'lessons_notice': ''
        }
        return render(request, "lessons/change_list.html", datas)


def lesson_list(request):
    if request.method == "GET":
        user = request.user
        logger.info(request.GET)
        logger.info(request.GET.get('draw'))
        filter_name = request.GET.get("filter_name")
        filter_num = request.GET.get("filter_num")
        filter_grade = request.GET.get("filter_grade")
        filter_status = request.GET.get("filter_status")
        date__gte = request.GET.get('date__gte')
        date__lte = request.GET.get('date__lte')
        query = lesson_filter()
        if not user.is_superuser:
            logger.info(dir(user))
            query = query.filter(grade_id=user.grade_id, status=1)
        if filter_name:
            query = query.filter(course__title__icontains=filter_name)
        if filter_num:
            query = query.filter(num=filter_num)
        if filter_grade:
            query = query.filter(grade_id=filter_grade)
        if filter_status:
            query = query.filter(status=filter_status)
        if date__gte:
            query = query.filter(lesson_date__gte=date__gte)
        if date__lte:
            query = query.filter(lesson_date__lte=date__lte)
        query = query.order_by("-num")
        data_dict = {}
        try:
            logger.info(query.count())
            data_dict, datas = page_calculate(request_data=request.GET, data=query)
            result = []
            for data in datas:
                logger.info(data.id)
                res = lesson_data(lesson=data)
                result.append(res)
            data_dict['rows'] = result
        except Exception as ex:
            logger.exception(ex)
        return JsonResponse(data_dict)


# 修改状态
def lesson_status_change(request):
    if request.method == "POST":
        req = json.loads(request.body)
        lesson_id = req.get('lesson_id')
        status = req.get('status', 0)
        lesson_filter(id=lesson_id).update(status=status)
        return common_response()


# 删除状态
def lesson_delete(request):
    if request.method == "POST":
        req = json.loads(request.body)
        lesson_id = req.get('lesson_id')
        lesson_filter(id=lesson_id).delete()
        return common_response()


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
        logger.info(request.GET.get('draw'))
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
        query = query.filter(is_attendance=1)
        query = query.order_by('-num')
        data_dict = {}
        try:
            logger.info(query.count())
            data_dict, datas = page_calculate(request_data=request.GET, data=query)
            result = []
            for data in datas:
                logger.info(data.id)
                res = attendance_data(lesson=data, user=user)
                result.append(res)
            data_dict['rows'] = result
        except Exception as ex:
            logger.exception(ex)
        return JsonResponse(data_dict)


# 学生端作业列表页面
def student_homework_list_page(request):
    if request.method == "GET":
        user = request.user
        datas = {
            'user': user
        }
        return render(request, "homework/student_list.html", datas)


# 学生端作业列表
def student_homework_list(request):
    if request.method == "GET":
        user = request.user
        logger.info(request.GET)
        logger.info(request.GET.get('draw'))
        filter_name = request.GET.get("filter_name")
        date__gte = request.GET.get('date__gte')
        date__lte = request.GET.get('date__lte')
        query = exercises_filter().filter(is_alone=1)
        if filter_name:
            query = query.filter(title__icontains=filter_name)
        if date__gte:
            query = query.filter(created__gte=date__gte)
        if date__lte:
            query = query.filter(created__lte=date__lte)
        query = query.order_by('-sort')
        data_dict = {}
        try:
            logger.info(query.count())
            data_dict, datas = page_calculate(request_data=request.GET, data=query)
            result = []
            for data in datas:
                logger.info(data.id)
                res = student_exercises_data(exercises=data, uid=user.id)
                result.append(res)
            data_dict['rows'] = result
        except Exception as ex:
            logger.exception(ex)
        return JsonResponse(data_dict)


# 评语提交
def homework_comment(request):
    if request.method == "POST":
        # req = json.loads(request.body)
        req = request.POST
        comment = req.get("comment")
        hid = req.get("hid")
        homework = Homework.objects.filter(id=hid).first()
        if not homework:
            return common_response(code=20000, message="作业不存在")
        homework.comment = comment
        homework.save()
        return common_response(message="评语保存成功")
