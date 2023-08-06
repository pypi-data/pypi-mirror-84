"""
# 模块管理
## 模块分类管理
## 模块管理
"""
import requests
from loguru import logger
from .base import base


class appMod(base):
    """
    app模块管理
    """

    def __init__(self, token) -> None:
        super().__init__(token)

    def request(self, **kwarg):
        api_prefix = ""
        return super().request(api_prefix=api_prefix, **kwarg)

    def list(self, mod_name=None):
        data = dict(
            page=1,
            rows=100
        )
        if mod_name:
            data["param.modName"] = mod_name
        return self.request(api_name="appModlist.jhtml",
                            data=data,
                            method="POST")

    def get_last_one(self):
        rows = self.list().get("rows")
        if rows:
            return rows[0]

    def get_last_one_mod_id(self):
        return self.get_last_one().get("appModuleId")

    def create(self, module_name, module_code, cate_id, img_url, disp_order):
        """
        增加模块
        """
        data = {
            "appModules.moduleName": module_name,
            "appModules.moduleCode": module_code,
            "appModules.type": 20,
            "appModules.cate": cate_id,
            "appModules.img": img_url,
            "appModules.moduleFlag": 1,
            "appModules.isShowNew": 1,
            "appModules.dispOrder": disp_order,
        }
        response = self.request(api_name="appModadd.jhtml",
                                data=data,
                                method="POST"
                                )
        return self.get_last_one_mod_id()

    def delete_all(self):
        rows = self.list().get("rows")
        for row in rows:
            module_id = row.get("appModuleId")
            data = {
                "moduleId": module_id,
            }
            response = self.request(api_name="appModdel.jhtml",
                                    data=data,
                                    method="POST"
                                    )
            data["response"] = response
            logger.debug(data)


class appModCat(base):
    """
    模块分类管理
    """

    def __init__(self, token) -> None:
        super().__init__(token)

    def request(self, **kwarg):
        api_prefix = ""
        headers = {
            "Cookie": f"accessToken={self.token}"
        }
        return super().request(api_prefix=api_prefix,
                               headers=headers,
                               ** kwarg)

    def list(self):
        data = dict(
            page=1,
            rows=100
        )
        return self.request(api_name="appModmoduleCateList.jhtml",
                            data=data,
                            method="POST")

    def get_last_one(self):
        rows = self.list().get("rows")
        if rows:
            return rows[-1]

    def get_last_one_mod_id(self):
        return self.get_last_one().get("id")

    def create(self, cate_name, cate_order):
        """
        增加模块分类

        """
        data = {
            "cateName": cate_name,
            "cateOrder": cate_order,
        }
        response = self.request(api_name="appModmodfiModuleCate.jhtml",
                                data=data,
                                method="POST"
                                )
        info = response.get("info")
        if info == "ok":
            return self.get_last_one_mod_id()
        else:
            data["msg"] = "添加失败"
            data["response"] = response
            logger.error(data)
