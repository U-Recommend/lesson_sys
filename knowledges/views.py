import json
from django.shortcuts import render
from django.http import JsonResponse
from common.utils import common_response, logger, page_calculate
from common.models import User, Grade
from knowledges.models import Knowledge
from knowledges.serializers.knowledge import knowledge_filter, knowledge_data


# 教程列表页面
def knowledge_list_page(request):
    if request.method == "GET":
        knowledges = [{"id": k.id, "name": k.title} for k in knowledge_filter()]
        datas = {
            "knowledges": knowledges
        }
        return render(request, "knowledge/knowledge_list.html", datas)


# 教程列表
def knowledge_list(request):
    if request.method == "GET":
        user = request.user
        filter_name = request.GET.get('filter_name')
        filter_knowledge = request.GET.get('filter_knowledge')
        query = knowledge_filter()
        if filter_knowledge:
            query = query.filter(id=filter_knowledge)
        if filter_name:
            query = query.filter(title__icontains=filter_name)
        data_dict = {}
        try:
            logger.info(query.count())
            data_dict, datas = page_calculate(request_data=request.GET, data=query)
            result = []
            for data in datas:
                logger.info(data.id)
                res = knowledge_data(knowledge=data)
                result.append(res)
            data_dict['rows'] = result
        except Exception as ex:
            logger.exception(ex)
        return JsonResponse(data_dict)


# 教程删除
def knowledge_delete(request):
    req = json.loads(request.body)
    knowledge_id = req.get('id')
    knowledge_filter(id=knowledge_id).delete()
    return common_response()
