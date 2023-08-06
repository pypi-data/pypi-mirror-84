# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-05-19 11:33:16
@LastEditTime: 2020-11-04 10:37:35
@LastEditors: HuangJingCan
@Description: 用户处理
"""
import decimal
from seven_cloudapp.handlers.seven_base import *
from seven_cloudapp.handlers.top_base import *

from seven_cloudapp.models.db_models.user.user_info_model import *
from seven_cloudapp.models.db_models.act.act_info_model import *
from seven_cloudapp.models.db_models.machine.machine_info_model import *
from seven_cloudapp.models.db_models.pay.pay_order_model import *
from seven_cloudapp.models.db_models.machine.machine_value_model import *
from seven_cloudapp.models.db_models.prize.prize_roster_model import *
from seven_cloudapp.models.db_models.prize.prize_order_model import *
from seven_cloudapp.models.db_models.behavior.behavior_orm_model import *
from seven_cloudapp.models.db_models.behavior.behavior_log_model import *
from seven_cloudapp.models.db_models.behavior.behavior_report_model import *
from seven_cloudapp.models.db_models.coin.coin_order_model import *
from seven_cloudapp.models.db_models.act.act_prize_model import *
from seven_cloudapp.models.db_models.app.app_info_model import *
from seven_cloudapp.models.behavior_model import *

from seven_cloudapp.models.seven_model import PageInfo

from seven_cloudapp.libs.customize.seven import *


class LoginHandler(SevenBaseHandler):
    """
    @description: 登录处理
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 登录日志入库
        @param avatar：头像
        @param is_auth：是否授权（1是0否）
        @param owner_open_id：应用拥有者唯一标识
        @param login_token：登录令牌
        @param signin：签到信息
        @param act_id：活动id
        @return: 
        @last_editors: HuangJingCan
        """
        open_id = self.get_taobao_param().open_id
        user_nick = self.get_taobao_param().user_nick
        app_id = self.get_taobao_param().source_app_id
        avatar = self.get_param("avatar")
        is_auth = int(self.get_param("is_auth", 0))
        owner_open_id = self.get_param("owner_open_id")
        login_token = self.get_param("login_token")
        signin = self.get_param("signin")
        act_id = int(self.get_param("act_id", 0))

        # request_params = str(self.request_params)

        user_info_model = UserInfoModel()
        user_info = user_info_model.get_entity("app_id=%s and act_id=%s and open_id=%s", params=[app_id, act_id, open_id])

        act_info_model = ActInfoModel()
        act_info = act_info_model.get_entity("id=%s", params=act_id)
        if not act_info:
            return self.reponse_json_error("NoAct", "对不起，活动不存在")

        machine_info_model = MachineInfoModel()
        machine_info_list = machine_info_model.get_list("app_id=%s and act_id=%s", params=[app_id, act_id])
        if not machine_info_list:
            return self.reponse_json_error("NoMachine", "对不起，盲盒不存在")

        is_add = False
        if not user_info:
            is_add = True
        if is_add:
            user_info = self.get_default_user(act_id)
            user_info.login_token = SevenHelper.get_random(16, 1)
            user_info.id = user_info_model.add_entity(user_info)
        else:
            user_info.modify_date = self.get_now_datetime()
            user_info.login_token = SevenHelper.get_random(16, 1)
            user_info.is_new = 0
            user_info_model.update_entity(user_info)

        machine_value_model = MachineValueModel()
        machine_value_list = machine_value_model.get_dict_list("open_id=%s", params=open_id)
        user_info_dict = user_info.__dict__
        user_info_dict["machine_value_list"] = machine_value_list

        behavior_model = BehaviorModel()
        # 访问次数
        behavior_model.report_behavior(app_id, act_id, open_id, owner_open_id, 'VisitCountEveryDay', 1)
        # 访问人数
        behavior_model.report_behavior(app_id, act_id, open_id, owner_open_id, 'VisitManCountEveryDay', 1)
        if user_info.is_new == 1:
            # 新增用户数
            behavior_model.report_behavior(app_id, act_id, open_id, owner_open_id, 'VisitManCountEveryDayIncrease', 1)

        self.reponse_json_success(user_info_dict)


class UserHandler(SevenBaseHandler):
    """
    @description: 更新用户信息
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 更新用户信息
        @param avatar：头像
        @param act_id：活动id
        @return: 
        @last_editors: CaiYouBin
        """
        try:
            open_id = self.get_taobao_param().open_id
            user_nick = self.get_taobao_param().user_nick
            source_app_id = self.get_taobao_param().source_app_id
            avatar = self.get_param("avatar")
            act_id = int(self.get_param("act_id", 0))

            user_info_model = UserInfoModel()
            user_info = user_info_model.get_entity("open_id=%s and app_id=%s and act_id=%s", params=[open_id, source_app_id, act_id])
            if not user_info:
                return self.reponse_json_error("NoUser", "对不起，用户不存在")
            user_info.user_nick = user_nick
            user_info.avatar = avatar
            user_info.is_auth = 1
            user_info.modify_date = self.get_now_datetime()
            user_info_model.update_entity(user_info)

            self.reponse_json_success("更新成功")
        except Exception as ex:
            self.reponse_json_error("Error", "更新失败")


class SyncPayOrderHandler(TopBaseHandler):
    """
    @description: 用户支付订单提交（业务各自实现）
    """
    def get_async(self):
        """
        @description: 用户支付订单提交（业务各自实现）
        @param {*}
        @return {*}
        @last_editors: HuangJingCan
        """
        pass


class UserPrizeListHandler(SevenBaseHandler):
    """
    @description: 获取用户奖品列表
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 获取用户奖品列表
        @param act_id：活动id
        @return status：状态
        @param page_index：页索引
        @param page_size：页大小
        @return: 
        @last_editors: HuangJingCan
        """
        app_id = self.get_taobao_param().source_app_id
        open_id = self.get_taobao_param().open_id

        act_id = int(self.get_param("act_id", 0))
        status = int(self.get_param("status", 0))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 20))

        prize_roster_model = PrizeRosterModel()
        if status == 0:
            condition = "open_id=%s and act_id=%s and prize_order_id=0"
        else:
            condition = "open_id=%s and act_id=%s and prize_order_id>0"

        page_list, total = prize_roster_model.get_dict_page_list("*", page_index, page_size, condition, "", "create_date desc", [open_id, act_id])

        page_info = PageInfo(page_index, page_size, total, page_list)

        self.reponse_json_success(page_info)


class SubmitPrizeOrder(SevenBaseHandler):
    """
    @description: 奖品订单提交
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 奖品订单提交
        @param act_id：活动id
        @param login_token：登录令牌
        @param real_name：用户名
        @param telephone：联系电话
        @param province：所在省
        @param city：所在市
        @param county：所在区
        @param street：所在街道
        @param address：收货地址
        @return 
        @last_editors: HuangJingCan
        """
        app_id = self.get_taobao_param().source_app_id
        open_id = self.get_taobao_param().open_id

        act_id = int(self.get_param("act_id", 0))
        login_token = self.get_param("login_token")
        real_name = self.get_param("real_name")
        telephone = self.get_param("telephone")
        province = self.get_param("province")
        city = self.get_param("city")
        county = self.get_param("county")
        street = self.get_param("street")
        address = self.get_param("address")

        user_info_model = UserInfoModel()
        user_info = user_info_model.get_entity("open_id=%s and app_id=%s and act_id=%s", params=[open_id, app_id, act_id])
        if not user_info:
            return self.reponse_json_error("NoUser", "对不起，用户不存在")
        if user_info.user_state == 1:
            return self.reponse_json_error("UserBlock", "对不起，你是黑名单用户,无法提交订单")
        if user_info.login_token != login_token:
            return self.reponse_json_error("ErrorLoginToken", "对不起，帐号已在另一台设备登录,当前无法提交订单")

        act_info_model = ActInfoModel()
        act_info = act_info_model.get_entity("id=%s and is_del=0 and is_release=1", params=act_id)
        if not act_info:
            return self.reponse_json_error("NoAct", "对不起，活动不存在")

        prize_roster_model = PrizeRosterModel()
        prize_roster_count = prize_roster_model.get_total("act_id=%s and open_id=%s and prize_order_id=0", params=[act_id, open_id])
        if prize_roster_count == 0:
            return self.reponse_json_error("NoNeedSubmitPrize", "当前没有未提交订单的奖品")

        prize_order_model = PrizeOrderModel()
        prize_order = PrizeOrder()
        prize_order.app_id = app_id
        prize_order.open_id = open_id
        prize_order.act_id = act_id
        prize_order.user_nick = user_info.user_nick
        prize_order.real_name = real_name
        prize_order.telephone = telephone
        prize_order.province = province
        prize_order.city = city
        prize_order.county = county
        prize_order.street = street
        prize_order.adress = address
        prize_order.create_date = self.get_now_datetime()
        prize_order.modify_date = self.get_now_datetime()
        prize_order.order_no = self.create_order_id()

        prize_order.id = prize_order_model.add_entity(prize_order)

        prize_roster_model.update_table("prize_order_id=%s,prize_order_no=%s", "act_id=%s and open_id=%s and prize_order_id=0", params=[prize_order.id, prize_order.order_no, act_id, open_id])

        self.reponse_json_success()


class PrizeOrderHandler(SevenBaseHandler):
    """
    @description: 用户订单列表
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 用户订单列表
        @param act_id：活动id
        @param page_index：页索引
        @param page_size：页大小
        @return: 
        @last_editors: HuangJingCan
        """
        app_id = self.get_taobao_param().source_app_id
        open_id = self.get_taobao_param().open_id

        act_id = int(self.get_param("act_id", 0))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 20))

        prize_order_model = PrizeOrderModel()
        prize_roster_model = PrizeRosterModel()
        prize_order_list_dict, total = prize_order_model.get_dict_page_list("*", page_index, page_size, "open_id=%s and act_id=%s ", "", "create_date desc", [open_id, act_id])
        if prize_order_list_dict:
            prize_order_id_list = [i["id"] for i in prize_order_list_dict]
            prize_order_ids = str(prize_order_id_list).strip('[').strip(']')
            prize_roster_list_dict = prize_roster_model.get_dict_list("prize_order_id in (" + prize_order_ids + ")")
            for i in range(len(prize_order_list_dict)):
                prize_order_list_dict[i]["prize_order_list"] = [prize_roster for prize_roster in prize_roster_list_dict if prize_order_list_dict[i]["id"] == prize_roster["prize_order_id"]]

        page_info = PageInfo(page_index, page_size, total, prize_order_list_dict)

        self.reponse_json_success(page_info)


class RosterNoticeHandler(SevenBaseHandler):
    """
    @description: 中奖通告
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 中奖通告
        @param act_id：活动id
        @return 列表
        @last_editors: HuangJingCan
        """
        act_id = int(self.get_param("act_id", 0))

        prize_roster_list_dict = PrizeRosterModel().get_dict_list("act_id=%s", order_by="create_date desc", limit="20", params=act_id)

        self.reponse_json_success(prize_roster_list_dict)