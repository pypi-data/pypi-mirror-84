"""
# 模块管理
## 模块分类管理
## 模块管理
"""
import requests
from loguru import logger
from .base import base


class appModCat(base):
    """
    模块分类管理
    """

    def __init__(self, token) -> None:
        super().__init__(token)

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


class appMod(base):
    """
    app模块管理
    """

    def __init__(self, token) -> None:
        super().__init__(token)

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


def testcase1():
    tk = "84d09f73a6f9965d3f4ddf131c2f3303_csb_web"
    m = appModCat(tk)
    response = m.create(
        "任秋锴的测试模块分类2",
        3,
    )
    print(response)


def testcase11():
    tk = "84d09f73a6f9965d3f4ddf131c2f3303_csb_web"
    m = appModCat(tk)
    response = m.get_last_one_mod_id()
    print(response)


def testcase2():
    img_url = "http://supershoper.xxynet.com/csb1604498917482"
    tk = "84d09f73a6f9965d3f4ddf131c2f3303_csb_web"
    m = appMod(tk)
    response = m.create(
        module_name="任秋锴的测试3",
        module_code="Rqk005",
        cate_id=169,
        img_url=img_url,
        disp_order=3,
    )
    print(response)


def testcase21():
    tk = "84d09f73a6f9965d3f4ddf131c2f3303_csb_web"
    m = appMod(tk)
    response = m.get_last_one_mod_id()
    print(response)


def testcase3():
    tk = "84d09f73a6f9965d3f4ddf131c2f3303_csb_web"
    img_url = "http://supershoper.xxynet.com/csb1604498917482"
    m = appMod(tk)
    c = appModCat(tk)
    cate_id = c.create(
        "自动添加001",
        3,
    )
    response = m.create(
        module_name="自动添加模块",
        module_code="Rqk005",
        cate_id=cate_id,
        img_url=img_url,
        disp_order=3,
    )
    print(response)


def testcase4():
    tk = "4be768e606ca3e349df2a9b626061186_moban004_web"
    m = appMod(tk)
    response = m.delete_all()
    print(response)


if __name__ == "__main__":
    testcase4()
