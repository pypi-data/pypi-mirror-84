# 开放平台接口基类
from loguru import logger
import requests


def get_up_token(cjdg_access_token):
    """
    七牛上传令牌
    """
    url = "http://bms.chaojidaogou.com/shopguide/api/file/qiniu/getUpToken"
    params = {
        "accessToken": cjdg_access_token
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    params["response"] = response
    params["response_raw"] = response.content
    logger.error(params)


def request_accesstoken(acc: str, pwd: str) -> str:
    # 请求accesstooke函数
    url = "http://bms.microc.cn/shopguide/api/auth/logon"
    data = {}
    data["loginName"] = acc
    data["password"] = pwd
    data["version"] = "1"
    response = requests.get(url, data)
    if response.status_code == 200:
        accessToken = response.json().get("accessToken")
        return accessToken


class base:
    def __init__(self, token, app_secret=None):
        self.token = token
        self.app_secret = app_secret

    def request(self, api_name=None, params={}, data={}, method="GET",
                url=None, json={}, headers={}, api_prefix="api/"):
        host_name = "http://bms.microc.cn/shopguide/"
        # host_name = "http://test.xxynet.com/shopguide/api/"
        if not url:
            if host_name not in api_name:
                url = f"{host_name}{api_prefix}{api_name}"
        if "accessToken" not in params:
            # 没有token自动添加
            params["accessToken"] = self.token
        if "appSecret" not in params:
            # 没有token自动添加
            params["appSecret"] = self.app_secret

        if method == "GET":
            params.update(data)
            response = requests.get(url, params=params, headers=headers)
        elif method == "POST":
            if data:
                response = requests.post(
                    url, params=params, data=data, headers=headers)
            elif json:
                response = requests.post(
                    url, params=params, json=json, headers=headers)
            else:
                logger.warning({
                    "msg": "网络请求数据格式错误。",
                    "method": "POST",
                    "data": "没有任何数据请求，为什么不用GET？",
                })
                response = requests.post(url, params=params, headers=headers)

        else:
            raise ValueError("请求方法错误。")
        if response.status_code == 200:
            # logger.debug({
            #     "url": url,
            #     "headers": headers,
            #     "response": response.text,
            # })
            return self.response(response.json())

    def response(self, response_raw):

        return response_raw
