import json
from django.shortcuts import render
from common.utils import common_response, logger
from projects.models import PythonTrain


def train_code(request):
    if request.method == "POST":
        req = request.POST
        logger.info(req)
        code = req.get("code")
        uid = req.get('uid')
        sid = req.get('sid')
        logger.info(code)

        train = PythonTrain.objects.filter(id=sid).first() if sid else None
        if train:
            train.code = code
            train.save()
        else:
            train = PythonTrain(user_id=uid, code=code)
            train.save()
        return common_response(message="保存成功")
