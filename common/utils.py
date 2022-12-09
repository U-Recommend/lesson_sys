import os.path
import re
import jwt
import time
import qrcode
import requests
import base64
import random
import string
import socket
import datetime
from hashlib import md5
from io import BytesIO
from decimal import Decimal
from contextlib import contextmanager
from django.conf import settings
from django.http import JsonResponse
from difflib import SequenceMatcher  # 导入库
from functools import lru_cache
import logging

logger = logging.getLogger("django")


@contextmanager
def ignored(exception):
    '''
    忽略代码块错误
    :param exception:
    :return:
    '''
    try:
        yield
    except exception:
        pass


# 接口通用返回方法
def common_response(code=0, message="success", result=None, **kwargs):
    res = {"code": code, "msg": message, "result": result}
    res.update(**kwargs)
    logger.info(res)
    return JsonResponse(res)


def get_page_data_info(data, current_page=1, page_size=20):
    """ 获取分页数据
    :param data:
    :param current_page:
    :param page_size:
    :return: cut_data, current_page, total_page: 分页数据,  当前页, 总页数
    """
    current_page = int(current_page)
    page_size = int(page_size)
    start_num = (current_page - 1) * page_size
    end_num = current_page * page_size
    # total_page = math.ceil(len(data) / page_size)
    total_data = len(data)
    return data[start_num: end_num], current_page, total_data, page_size


def page_calculate(request_data, data=None):
    '''分页'''
    try:
        draw = int(request_data.get('draw', 1))
        logger.info(draw)
    except:
        draw = 1
    try:
        length = int(request_data.get('length', 10))
    except:
        length = 20
    start = int((draw - 1) * length)
    data = data[int(start): int(start) + int(length)]
    data_dict = {
        'draw': draw,
        'total': 0,
        'rows': [],
        'code': 0,
    }
    return data_dict, data


def timestamp_str():
    '''时间戳'''
    return str(int(time.time()))


def timedelta_to_time(timedelta=None):
    '''
    时间戳格式化
    :param timedelta:
    :return:
    '''
    try:
        t = time.localtime(int(timedelta))
        res = time.strftime("%Y-%m-%d %H:%M:%S", t)
    except:
        res = ""
    return res


def datetime_to_timedelta(stime=None):
    '''时间转换时间戳'''
    if isinstance(stime, datetime.datetime):
        stime = stime.strftime("%Y-%m-%d %H:%M:%S")
    s_t = time.strptime(stime, "%Y-%m-%d %H:%M:%S")
    mkt = int(time.mktime(s_t))
    return mkt


def datetime_strftime(the_time=None):
    '''datetime的strftime方法'''
    try:
        return the_time.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return ""


def similarity(a, b):
    '''匹配两个字符串的相似度'''
    return SequenceMatcher(None, a, b).ratio()


def re_text_format(text):
    '''去掉文本中括号及内容'''
    text = re.sub("\\（.*?）|\\{.*?}|\\[.*?]|\\【.*?】", "", text)
    text = re.sub("\\(.*?\\)|\\{.*?}|\\[.*?]", "", text)
    return text


def md5_encrypt(data):
    '''md5加密'''
    return md5(data.encode()).hexdigest()


def tencent_location_sign(path=None, params=None):
    ks = sorted(params.keys())
    ps = "&".join([f"{k}={params[k]}" for k in ks])
    string_sign_temp = f"{path}?{ps}{settings.TENCENT_LOCATION_SECRET}"
    return md5(string_sign_temp.encode()).hexdigest()


def city_location(latitude: float, longitude: float) -> dict:
    """
    用户城市定位
    :param latitude:
    :param longitude:
    :return:
    """
    params = {
        'location': f'{latitude},{longitude}',
        'key': settings.TENCENT_LOCATION_KEY
    }
    params["sig"] = tencent_location_sign(path=settings.TENCENT_LOCATION_PATH, params=params)
    result = requests.get(url=settings.TENCENT_LOCATION_URL, params=params)
    result = result.json().get('result')
    return result


def get_wechat_openid(code: str) -> dict:
    """
    获取openid
    :param code:
    :return:
    """
    params = {
        'appid': settings.WECHAT_APP_ID,
        'secret': settings.WECHAT_APP_SECRET,
        'js_code': code
    }
    result = requests.get(url=settings.CODE_TO_SESSION_URL, params=params).json()
    return result


# 制作二维码
def make_qrcode(data):
    if not data:
        return ''
    qr = qrcode.QRCode()
    qr.make(fit=True)
    qr.add_data(data)
    img = qr.make_image()
    buf = BytesIO()
    img.save(buf, format='PNG')
    image_stream = buf.getvalue()
    heximage = base64.b64encode(image_stream)
    return 'data:image/png;base64,' + heximage.decode()


def set_token(jwt_params=None):
    '''创建新token'''
    token = jwt.encode(jwt_params, settings.SECRET_KEY, algorithm="HS256")
    return token


def get_token(token=None):
    '''解码token'''
    with ignored(Exception):
        res = jwt.decode(token.encode("utf-8"), settings.SECRET_KEY, algorithms="HS256")
        return res


def create_nonce_str(length=16):
    '''获取noncestr（随机字符串）'''
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def new_order_num():
    '''新建订单号'''
    now_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    none_str = create_nonce_str(length=8)
    return f'RED{now_datetime}{none_str}'


def format_file_url(path=None):
    '''格式化文件请求地址'''
    try:
        if path.startswith("http"):
            return path
        path = path.lstrip("/")
        if "redpack" in path:
            return f"https://{path}"
        return f"{settings.HOST_URL}/{path}"
    except:
        return ""


def check_number(data=None):
    if not data:
        return 0.00
    if isinstance(data, str):
        try:
            data = float(data)
        except:
            pass
    if isinstance(data, (Decimal, float)):
        return round(float(data), 2)
    return data


def get_host_ip():
    '''获取服务器IP'''
    return socket.gethostbyname(socket.gethostname())


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in settings.ALLOWED_FILE_EXTENSIONS


def allowed_img_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in settings.ALLOWED_IMAGE_EXTENSIONS


@lru_cache(maxsize=None)
def check_mobile(mobile):
    '''
    检查是否是手机号码
    :param mobile:
    :return:
    '''
    if not mobile:
        return False, '无效号码'
    try:
        if isinstance(mobile, str):
            mobile = str(mobile).strip()
            mobile = int(float(mobile))
        else:
            mobile = int(float(mobile))
    except Exception as ex:
        logger.exception(ex)
        return False, '非手机号码'
    mobile = str(mobile)
    if len(mobile) != 11:
        return False, '手机号码长度错误'
    phone_reg = re.compile('^1(3[0-9]|4[5,7]|5[0,1,2,3,5,6,7,8,9]|6[2,5,6,7]|7[0,1,7,8]|8[0-9]|9[1,8,9])\d{8}$')

    # phone_reg = re.compile(r"^1[3,4,5,6,7,8,9]{1}[0-9]{9}$")
    if not phone_reg.search(mobile):
        return False, "手机号码错误"
    return True, mobile


def str_strip(data=None):
    if not data:
        return ''
    return str(data).strip()


def set_captcha():
    # 设置验证码
    code = str(time.time())[-6:].replace(".", "0")
    return code


def check_email(email=None):
    '''邮箱格式验证'''
    reg = "\w+[@][a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)+"
    result = re.findall(reg, email)
    if result:
        return True  # 邮箱合法
    else:
        return False


def get_client_ip(request):
    '''请求IP'''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def download_img(file_url=None):
    r = requests.get(file_url)
    filename = create_nonce_str(length=5)
    ext = file_url.rsplit('.', 1)[1]
    filename = f'{filename}.{ext}'
    filename = os.path.join(settings.MEDIA_ROOT, filename)
    with open(filename, 'wb') as f:
        f.write(r.content)
    return filename
