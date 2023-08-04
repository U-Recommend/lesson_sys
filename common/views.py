import json
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from common.utils import common_response, logger, page_calculate
from common.handle.dirty_word_of_filter.handle import DFAFilter
from common.models import Feedback
from common.serializers.feedback import feedback_filter, feedback_data
from common.serializers.weather import get_weather, get_weather_json


def feedback_list_page(request):
    if request.method == "GET":
        user = request.user
        datas = {
            'user': user,
        }
        return render(request, "feedback/feedback_list.html", datas)


def feedback_list(request):
    user = request.user
    if request.method == "GET":
        filter_content = request.GET.get("filter_content")
        is_private = request.GET.get("is_private")
        is_feedback = request.GET.get("is_feedback")
        date__gte = request.GET.get('date__gte')
        date__lte = request.GET.get('date__lte')
        query = feedback_filter()
        if not user.is_superuser:
            query = query.filter(Q(user_id=user.id) | Q(is_private=0)).filter(status=1)
        if filter_content:
            query = query.filter(content__icontains=filter_content)
        if str(is_private) in ['0', '1']:
            query = query.filter(is_private=is_private)
        if str(is_feedback) == '0':
            query = query.filter(feedback__isnull=True)
        if str(is_feedback) == '1':
            query = query.filter(feedback_isnull=False)
        if date__gte:
            query = query.filter(created__gte=date__gte)
        if date__lte:
            query = query.filter(created__lte=date__lte)
        query = query.order_by('-id')
        data_dict = {}
        try:
            logger.info(query.count())
            data_dict, datas = page_calculate(request_data=request.GET, data=query)
            result = []
            for data in datas:
                logger.info(data.id)
                res = feedback_data(feedback=data)
                result.append(res)
            data_dict['rows'] = result
        except Exception as ex:
            logger.exception(ex)
        return JsonResponse(data_dict)
    if request.method == "POST":
        req = json.loads(request.body)
        id = req.get('id')
        content = req.get('content')
        is_private = req.get('is_private')
        if not content or len(content.strip()) == 0:
            return common_response(code=20000, message="内容为必填")
        # 脏词过滤
        dirty_word_status = DFAFilter().filter(content)
        if not dirty_word_status:
            return common_response(code=20000, message="请重新提交")

        if id:
            feedback = feedback_filter(id=id).first()
            if not user.is_superuser:
                if not feedback or feedback.feedback:
                    return common_response(code=20000, message="操作失败，请重试")
            feedback.content = content
            feedback.is_private = is_private
            feedback.save()
        else:
            feedback = Feedback(user_id=user.id, content=content, is_private=is_private)
            feedback.save()
        return common_response(message="提交成功，我们会尽快回复")


def feedback_detail(request):
    user = request.user
    if request.method == "GET":
        id = request.GET.get('id')
        data = feedback_data(feedback_id=id)
        return common_response(result=data)
    if request.method == "POST":
        req = json.loads(request.body)
        id = req.get('id')
        status = req.get('status')
        feedback = req.get('feedback')
        if str(status) in ['0', '1']:
            feedback_filter(id=id).update(status=status)
            return common_response(message="修改成功")
        if feedback:
            feedback_filter(id=id).update(feedback=feedback)
            return common_response(message="修改成功")
        return common_response(code=20000, message="操作失败")


def feedback_delete(request):
    user = request.user
    if request.method == "POST":
        req = request.POST
        id = req.get('id')
        feedback = feedback_filter(id=id).first()
        if not feedback:
            return common_response(code=20000, message="操作失败，请重试")
        if not user.is_superuser:
            if feedback.user_id != user.id:
                return common_response(code=20000, message="无操作权限")
        feedback.delete()
        return common_response()


def get_weather_data(request):
    if request.method == "GET":
        wtype = request.GET.get('wtype')
        data = get_weather(wtype=wtype)
        return common_response(result=str(data))


def weather_data(request):
    if request.method == "GET":
        data = get_weather_json()
        return JsonResponse(data)
