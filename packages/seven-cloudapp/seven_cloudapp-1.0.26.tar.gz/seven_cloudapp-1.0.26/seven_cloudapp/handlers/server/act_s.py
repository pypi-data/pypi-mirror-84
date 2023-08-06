# -*- coding: utf-8 -*-
"""
@Author: CaiYouBin
@Date: 2020-05-12 20:04:54
@LastEditTime: 2020-11-04 14:17:13
@LastEditors: HuangJingCan
@Description: 基础接口
"""
import random
from seven_cloudapp.handlers.seven_base import *
from seven_cloudapp.handlers.top_base import *
from seven_framework.qr_code import *

from seven_cloudapp.models.db_models.machine.machine_info_model import *
from seven_cloudapp.models.db_models.behavior.behavior_orm_model import *
from seven_cloudapp.models.db_models.act.act_prize_model import *
from seven_cloudapp.models.db_models.act.act_info_model import *
from seven_cloudapp.models.db_models.act.act_type_model import *
from seven_cloudapp.models.db_models.app.app_info_model import *
from seven_cloudapp.models.db_models.theme.theme_info_model import *
from seven_cloudapp.models.db_models.skin.skin_info_model import *
from seven_cloudapp.models.db_models.base.base_info_model import *
from seven_cloudapp.models.seven_model import PageInfo
from seven_cloudapp.models.behavior_model import *
from seven_cloudapp.models.enum import *


class ActTypeHandler(SevenBaseHandler):
    """
    @description: 活动类型相关
    """
    def post_async(self):
        """
        @description: 活动类型入库
        @param type_id：类型id
        @param type_name：类型名称
        @param act_title：活动标题
        @param act_img：活动图
        @param experience_img：体验码二维码图
        @param play_process：玩法流程
        @param applicable_behavior：适用行为
        @param market_function：营销功能
        @return: 
        @last_editors: HuangJingCan
        """
        type_id = int(self.get_param("type_id", "0"))
        type_name = self.get_param("type_name")
        act_title = self.get_param("act_title")
        act_img = self.get_param("act_img")
        experience_img = self.get_param("experience_img")
        play_process = self.get_param("play_process")
        applicable_behavior = self.get_param("applicable_behavior")
        market_function = self.get_param("market_function")

        # 数据入库
        act_type_model = ActTypeModel()
        act_type = None
        if type_id > 0:
            act_type = act_type_model.get_entity_by_id(type_id)

        is_add = False
        if not act_type:
            is_add = True
            act_type = ActType()

        act_type.type_name = type_name
        act_type.act_title = act_title
        act_type.act_img = act_img
        act_type.experience_img = experience_img
        act_type.play_process = play_process
        act_type.applicable_behavior = applicable_behavior
        act_type.market_function = market_function
        act_type.modify_date = self.get_now_datetime()

        if is_add:
            act_type.create_date = act_type.modify_date
            act_type_model.add_entity(act_type)
        else:
            act_type_model.update_entity(act_type)

        self.reponse_json_success()

    def get_async(self):
        """
        @description: 活动类型获取
        @param 
        @return: 列表
        @last_editors: HuangJingCan
        """
        act_type_model = ActTypeModel()
        act_type_list = act_type_model.get_list()

        new_list = []

        for info in act_type_list:
            if info.play_process:
                info.play_process = ast.literal_eval(info.play_process)
            if info.applicable_behavior:
                info.applicable_behavior = ast.literal_eval(info.applicable_behavior)
            if info.market_function:
                info.market_function = ast.literal_eval(info.market_function)
            new_list.append(info.__dict__)

        self.reponse_json_success(new_list)


class ActCreateHandler(TopBaseHandler):
    """
    @description: 创建活动
    """
    @filter_check_params("act_type")
    def get_async(self):
        """
        @description: 创建活动
        @param act_type：活动类型
        @return: 
        @last_editors: CaiYouBin
        """
        user_nick = self.get_taobao_param().user_nick
        if not user_nick:
            return self.reponse_json_error("Error", "对不起，请先授权登录")
        act_name = self.get_param("act_name")

        # 实例化
        description = "购买拆盲盒次数后，直接在线拆盲盒，提前获得盲盒内的惊喜奖品！"
        icon = "https://isv.alibabausercontent.com/010228250372/imgextra/i3/2206353354303/O1CN01CAOKQg1heos6pZTpl_!!2206353354303-2-isvtu-010228250372.png"
        # icon = ""
        name_ending = "拆盲盒"
        app_info = self.instantiate(user_nick, act_name, description, icon, name_ending)

        #查询appInfo表后等到
        if not hasattr(app_info, 'app_id'):
            return self.reponse_json_error("Error", "对不起，实例化失败请重试")
        app_id = app_info.app_id
        act_id = self.get_param("act_id")
        act_type = self.get_param("act_type")
        source_app_id = self.get_taobao_param().source_app_id
        act_model = ActInfoModel()
        machine_info_model = MachineInfoModel()
        theme_info_model = ThemeInfoModel()
        skin_info_model = SkinInfoModel()
        theme_info = theme_info_model.get_entity()
        if not theme_info:
            return self.reponse_json_error("NoTheme", "对管理员先上传主题信息")
        skin_info = skin_info_model.get_entity("theme_id=%s", params=theme_info.id)
        if not skin_info:
            return self.reponse_json_error("NoSkin", "对管理员先上传皮肤信息")

        if not act_id:
            #增加默认活动
            act_info = ActInfo()
            act_info.app_id = app_id
            #商家OpenID 查询appInfo表后等到
            act_info.owner_open_id = "123456"
            act_info.act_name = act_name
            act_info.act_type = act_type
            act_info.sort_index = 1
            #默认主题ID 查询theme表得到
            act_info.theme_id = theme_info.id
            act_info.store_url = ""
            act_info.close_word = "抱歉，程序维护中"
            act_info.share_desc = {"taoword": "", "icon": [{"url": "https://isv.alibabausercontent.com/010229100714/imgextra/i3/2206353354303/O1CN01nmEdhH1heosXANKpT_!!2206353354303-2-isvtu-010229100714.png"}], "title": "", "desc": ""}
            act_info.share_desc = self.json_dumps(act_info.share_desc)
            act_info.rule_desc = [{"ruleName": "什么是盲盒", "ruleDetail": "这是一个拼RP（人品）的游戏，是一种娱乐性的人气购物体验，每个盲盒中都含有惊喜奖品。用户购买对应的拆盒次数，选择盲盒进行拆盒后即为消费完成，用户在背包中可以对抽取到的奖品进行下单确认后即可发货。可能会抽到意料之外的惊喜哦！"}, {"ruleName": "特别说明", "ruleDetail": "1、本产品为在线体验商品，用户购买拆盒次数完成在线拆盲盒后，即为消费完成，仓库根据用户抽取的确认款式直接发货；\n" + "2、盲盒商品完成在线开拆盒后，不支持任何理由的退换货，若出现产品质量问题等，本单品一样享受售后换货流程；\n" + "3、盲盒内的商品都是随机抽取，每个盲盒有对应的奖品池；\n" + "4、盲盒会不定期更新，具体以该盲盒奖品池中显示的奖品为准；\n" + "5、如果您愿意拍下，就是认同我们的活动规则，介意者也不勉强，可以自由选择关闭页面或者浏览我们的其他商品；\n" + "6、本活动最终解释权归本店所有；\n"}]
            act_info.rule_desc = self.json_dumps(act_info.rule_desc)
            act_info.start_date = "2020-02-25 00:00:00"
            act_info.end_date = "2100-02-25 00:00:00"
            act_info.is_black = 0
            act_info.is_release = 1
            act_info.create_date = self.get_now_datetime()
            act_info.modify_date = self.get_now_datetime()
            act_id = act_model.add_entity(act_info)
            #增加默认机台.
            machine_info = MachineInfo()
            machine_info.machine_name = "测试数据"
            machine_info.machine_type = 2
            machine_info.act_id = act_id
            machine_info.app_id = app_id
            machine_info.machine_price = 88
            #SKUid待定
            machine_info.sku_id = 0
            machine_info.skin_id = skin_info.id
            machine_info.sort_index = 1
            machine_info.is_release = 1
            machine_info.single_lottery_price = 100
            machine_info.many_lottery_price = 200
            machine_info.many_lottery_num = 2
            machine_info.is_repeat_prize = 0
            machine_info.create_date = self.get_now_datetime()
            machine_info.modify_date = self.get_now_datetime()
            machine_infoid = machine_info_model.add_entity(machine_info)
            #增加行为映射数据
            orm_infos = []

            for i in range(0, 2):
                behavior_orm = BehaviorOrm()
                if i == 0:
                    behavior_orm.is_repeat = 0
                    behavior_orm.key_value = machine_info.machine_name + "拆开次数"
                    behavior_orm.key_name = "openCount_" + str(machine_infoid)
                else:
                    behavior_orm.is_repeat = 1
                    behavior_orm.key_value = machine_info.machine_name + "拆开人数"
                    behavior_orm.key_name = "openUserCount_" + str(machine_infoid)
                behavior_orm.orm_type = 1
                behavior_orm.group_name = ""
                behavior_orm.is_common = 0
                behavior_orm.sort_index = 1
                behavior_orm.app_id = app_id
                behavior_orm.act_id = act_id
                behavior_orm.create_date = self.get_now_datetime()
                orm_infos.append(behavior_orm)

            BehaviorModel().save_orm(orm_infos, act_id)

            self.save_default_prize(act_id, app_id, source_app_id, machine_infoid)

            self.create_operation_log(OperationType.add.value, act_info.__str__(), "ActCreateHandler", None, self.json_dumps(act_info))

        self.reponse_json_success(act_id)

    def save_default_prize(self, act_id, app_id, source_app_id, machine_info_id):
        act_prize_model = ActPrizeModel()
        act_prize_list = []
        for i in range(0, 2):
            act_prize = ActPrize()
            act_prize.act_id = act_id
            act_prize.app_id = app_id
            act_prize.owner_open_id = source_app_id
            act_prize.machine_id = machine_info_id
            act_prize.prize_name = "奖品测试标题" + str(i + 1)
            act_prize.prize_title = "奖品测试子标题" + str(i + 1)
            act_prize.prize_pic = "https://img.alicdn.com/imgextra/i4/2206353354303/O1CN01q2wHOL1heor4k3qD8_!!2206353354303-2-miniprogram.png"
            act_prize.prize_detail = ["https://img.alicdn.com/imgextra/i4/2206353354303/O1CN01q2wHOL1heor4k3qD8_!!2206353354303-2-miniprogram.png", "https://img.alicdn.com/imgextra/i4/2206353354303/O1CN01q2wHOL1heor4k3qD8_!!2206353354303-2-miniprogram.png"]
            act_prize.prize_detail = self.json_dumps(act_prize.prize_detail)
            act_prize.goods_code = "1111"
            act_prize.prize_type = 1
            act_prize.prize_price = 88
            act_prize.probability = 50
            act_prize.surplus = 100
            act_prize.prize_limit = 0
            act_prize.prize_total = 100
            act_prize.tag_id = 1
            act_prize.hand_out = 0
            act_prize.sort_index = 1
            act_prize.is_release = 1
            act_prize.create_date = self.get_now_datetime()
            act_prize.modify_date = self.get_now_datetime()
            act_prize_list.append(act_prize)
        act_prize_model.add_list(act_prize_list)


class ActHandler(SevenBaseHandler):
    """
    @description: 活动信息保存（业务各自实现）
    """
    @filter_check_params("act_id,act_name")
    def post_async(self):
        """
        @description: 活动信息保存（业务各自实现）
        @param 
        @return 
        @last_editors: HuangJingCan
        """
        pass


class ActListHandler(SevenBaseHandler):
    """
    @description: 获取活动列表（业务各自实现）
    """
    def get_async(self):
        """
        @description: 获取活动列表（业务各自实现）
        @param act_name：活动名称
        @param is_del：是否删除
        @param page_index：页索引
        @param page_size：页大小
        @return: 列表
        @last_editors: HuangJingCan
        """
        pass


class ActInfoHandler(SevenBaseHandler):
    """
    @description: 活动信息获取（业务各自实现）
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 活动信息获取（业务各自实现）
        @param act_id：活动id
        @return: 活动信息
        @last_editors: HuangJingCan
        """
        pass


class ActDelHandler(SevenBaseHandler):
    """
    @description: 删除或者还原活动
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 删除或者还原活动
        @param act_id：活动id
        @param is_del：0-还原，1-删除
        @return: 
        @last_editors: HuangJingCan
        """
        act_id = int(self.get_param("act_id", "0"))
        is_del = int(self.get_param("is_del", "1"))
        modify_date = self.get_now_datetime()

        if act_id <= 0:
            return self.reponse_json_error_params()
        if is_del == 1:
            ActInfoModel().update_table("is_del=%s,modify_date=%s,is_release=0", "id=%s", [is_del, modify_date, act_id])
        else:
            ActInfoModel().update_table("is_del=%s,modify_date=%s,is_release=1", "id=%s", [is_del, modify_date, act_id])

        self.reponse_json_success()


class ActQrCodeHandler(SevenBaseHandler):
    """
    @description: 活动二维码获取
    """
    @filter_check_params("url")
    def get_async(self):
        """
        @description: 活动二维码获取
        @param act_id：活动id
        @return: 活动二维码图片
        @last_editors: HuangJingCan
        """
        url = self.get_param("url")

        img, img_bytes = QRCodeHelper.create_qr_code(url, fill_color="black")
        img_base64 = base64.b64encode(img_bytes).decode()

        self.reponse_json_success(f"data:image/jpeg;base64,{img_base64}")


class ActReviewHandler(SevenBaseHandler):
    """
    @description: 还原活动
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 还原活动
        @param act_id：活动id
        @return 
        @last_editors: HuangJingCan
        """
        act_id = self.get_param("act_id")
        modify_date = self.get_now_datetime()
        user_nick = self.get_taobao_param().user_nick
        store_user_nick = user_nick.split(':')[0]
        dict_app_id = AppInfoModel().get_dict("store_user_nick=%s", field="app_id", params=store_user_nick)
        if not dict_app_id:
            return self.reponse_json_error("NoAppId", "对不起，app_id不存在")

        act_info_model = ActInfoModel()
        act_info_total = act_info_model.get_total("app_id=%s and is_del=0", params=dict_app_id["app_id"])
        if act_info_total > 9:
            return self.reponse_json_error("OverAct", "对不起，活动不可超过10个")
        act_info_model.update_table("is_del=0,modify_date=%s,is_release=1", "id=%s", [modify_date, act_id])

        self.reponse_json_success()


class NextProgressHandler(SevenBaseHandler):
    """
    @description: 下一步
    """
    def get_async(self):
        """
        @description: 下一步
        @param act_id：活动id
        @param finish_key：finish_key
        @return 
        @last_editors: HuangJingCan
        """
        act_id = int(self.get_param("act_id"))
        finish_key = self.get_param("finish_key")
        base_info = BaseInfoModel().get_entity()
        if not base_info:
            return self.reponse_json_error("Error", "对不起，请与管理员联系")

        act_info_model = ActInfoModel()
        act_info = act_info_model.get_entity("id=%s", params=act_id)

        if not act_info:
            return self.reponse_json_error("NoAct", "对不起，找不到当前活动")

        menu_config = json.loads(base_info.menu_config)
        menu = [menu for menu in menu_config if menu["key"] == finish_key]
        if len(menu) == 0:
            return self.reponse_json_error("Error", "对不起，无此菜单")

        if act_info.menu_configed != "" and finish_key in act_info.menu_configed:
            return self.reponse_json_success()

        if act_info.menu_configed == "":
            act_info.menu_configed = "[]"

        menu_configed = json.loads(act_info.menu_configed)
        menu_configed.append(finish_key)

        result_menu_configed = []
        for item in menu_configed:
            is_exist = [item2 for item2 in menu_config if item2["key"] == item]
            if len(is_exist) > 0:
                result_menu_configed.append(item)
        if len(result_menu_configed) == len(menu_config) and act_info.finish_progress == 0:
            act_info.finish_progress = 1

        act_info.menu_configed = json.dumps(result_menu_configed)

        act_info_model.update_entity(act_info)

        self.reponse_json_success()