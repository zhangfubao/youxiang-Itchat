# coding=utf-8
"""
首先要感谢下这篇文章：
https://www.jianshu.com/p/f9b5e3020789

值得看的一篇文章：
http://g.alicdn.com/tmapp/tida-doc/docs/top/00API%E8%B0%83%E7%94%A8%E8%AF%B4%E6%98%8E.html

"""
import hashlib
import json
import random
import time
import urllib
import urllib.parse
import urllib.request

TB_API_ROOT = 'http://gw.api.taobao.com/router/rest?'

class TbApiClient(object):

    def __init__(self, app_key, secret_key, adzone_id):
        self.app_key = app_key
        self.secret_key = secret_key
        self.adzone_id = adzone_id

    #排序
    def ksort(self, d):
        return [(k, d[k]) for k in sorted(d.keys())]

    #MD5加密
    def md5(self, s, raw_output=False):
        """Calculates the md5 hash of a given string"""
        res = hashlib.md5(s.encode())
        if raw_output:
            return res.digest()
        return res.hexdigest()

    #计算sign
    def createSign(self, paramArr):
        sign = self.secret_key
        paramArr = self.ksort(paramArr)
        paramArr = dict(paramArr)
        for k, v in paramArr.items():
            if k != '' and v != '':
                sign += k + v
        sign += self.secret_key
        sign = self.md5(sign).upper()
        return sign

    #参数排序
    def createStrParam(self, paramArr):
        strParam = ''
        for k, v in paramArr.items():
            if k != '' and v != '':
                strParam += k + '=' + urllib.parse.quote_plus(v) + '&'
        return strParam

    #高效API调用示例
    def taobao_tbk_dg_optimus_material(self, material_id: str):
        '''
        通用物料推荐，传入官方公布的物料id，可获取指定物料
        淘宝接口文档：
        http://bigdata.taobao.com/api.htm?spm=a219a.7386797.0.0.4ad5669aWaaQFi&source=search&docId=33947&docType=2

        :param material_id:  详见https://market.m.taobao.com/app/qn/toutiao-new/index-pc.html#/detail/10628875?_k=gpov9a
        :param adzone_id:  广告位
        :return:
        '''
        # 请求参数，根据API文档修改
        # TODO
        # 把分页现在这里随机有一定考虑
        # 原因是：1. 不同 material_id 得到的数据不一，且刷新周期不一
        #                    2. 微信发送不可太频繁，我仅是怕被封，决定取很小一部分数据
        page_no = str(random.choices(['1','2','3','4', '5', '6', '7', '8', '9'])[0])
        page_size = str(random.randint(8, 10))

        postparm = {
                    'page_no': page_no,
                    'page_size': page_size,
                    'adzone_id': self.adzone_id,
                    'material_id': material_id,
                    'method': 'taobao.tbk.dg.optimus.material'
                    }
        # 公共参数，一般不需要修改
        paramArr = {'app_key': self.app_key,
                    'v': '2.0',
                    'sign_method': 'md5',
                    'format': 'json',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                    }

        paramArr = {**paramArr, **postparm}
        sign = self.createSign(paramArr)
        strParam = self.createStrParam(paramArr)
        strParam += 'sign=' + sign
        url = TB_API_ROOT + strParam
        print(url)
        res = urllib.request.urlopen(url).read()
        return res

    #高效API调用示例 淘宝客-推广者-物料搜索升级版-(适用于自己推广的媒体)
    def taobao_tbk_dg_material_recommend(self, material_id: str, relation_id="", device_type="", device_encrypt="", device_value="",
                                         favorites_id="", promotion_type=""):
        '''
        通用物料推荐，传入官方公布的物料id，可获取指定物料
        淘宝接口文档：
        http://bigdata.taobao.com/api.htm?spm=a219a.7386797.0.0.4ad5669aWaaQFi&source=search&docId=33947&docType=2

        :param material_id:  详见https://market.m.taobao.com/app/qn/toutiao-new/index-pc.html#/detail/10628875?_k=gpov9a
        :param adzone_id:  广告位
        :return:
        '''
        # 请求参数，根据API文档修改
        # 把分页现在这里随机有一定考虑
        # 原因是：1. 不同 material_id 得到的数据不一，且刷新周期不一
        #                    2. 微信发送不可太频繁，我仅是怕被封，决定取很小一部分数据
        page_no = str(random.choices(['1','3','5','7', '9', '11', '13', '15', '17','19','21','23','25','27','29','31','33','35','37','39','41','43','45','47','49','51','53','55','57','59'])[0])
        print("page_no===", int(page_no))
        page_size = '1'
        print("page_size===", page_size)
        postparm = {
                    'page_no': page_no,
                    'page_size': page_size,
                    'adzone_id': self.adzone_id,
                    'material_id': material_id,
                    'method': 'taobao.tbk.dg.material.recommend',
                    'relation_id': relation_id,  # 渠道关系ID，仅适用于渠道推广场景
                    'device_type': device_type,  # 智能匹配-设备号类型：IMEI，或者IDFA，或者UTDID（UTDID不支持MD5加密），或者OAID；使用智能推荐请先签署协议https://pub.alimama.com/fourth/protocol/common.htm?key=hangye_laxin
                    'device_encrypt': device_encrypt, # 智能匹配-设备号加密类型：MD5；使用智能推荐请先签署协议https://pub.alimama.com/fourth/protocol/common.htm?key=hangye_laxin
                    'device_value': device_value, # 智能匹配-设备号加密后的值（MD5加密需32位小写）；使用智能推荐请先签署协议https://pub.alimama.com/fourth/protocol/common.htm?key=hangye_laxin
                    'favorites_id': favorites_id, # 选品库收藏夹id，获取收藏夹id参考文档：https://mos.m.taobao.com/union/page_20230109_175050_176?spm=a219t._portal_v2_pages_promo_goods_index_htm.0.0.7c2a75a5H2ER3N
                    'promotion_type': promotion_type, #1-自购省，2-推广赚（代理模式专属ID，代理模式必填，非代理模式不用填写该字段）
                    }
        # 公共参数，一般不需要修改
        paramArr = {'app_key': self.app_key,
                    'v': '2.0',
                    'sign_method': 'md5',
                    'format': 'json',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                    }

        paramArr = {**paramArr, **postparm}
        sign = self.createSign(paramArr)
        strParam = self.createStrParam(paramArr)
        strParam += 'sign=' + sign
        url = TB_API_ROOT + strParam
        print(url)
        res = urllib.request.urlopen(url).read()
        return res

    #高效API调用示例 淘宝客-推广者-物料搜索升级版-(适用于工具服务商)
    def taobao_tbk_dg_material_optional_upgrade(self, material_id: str, start_dsr="2000", start_tk_rate="0300", end_tk_rate="", start_price="",
                                                end_price="", is_overseas="", is_tmall="", sort="tk_rate_des", itemloc="", cat="", q="", has_coupon="",
                                                ip="", need_free_shipment="true", need_prepay="", include_pay_rate_30="", include_good_rate="",
                                                include_rfd_rate="", npx_level="", device_encrypt="", device_value="", device_type="",
                                                special_id="", relation_id="", get_topn_rate="", biz_scene_id="", promotion_type="",
                                                mgc_start_time="", mgc_end_time="", mgc_status="", ucrowd_id="", ucrowd_rank_items=""):
        '''
        通用物料推荐，传入官方公布的物料id，可获取指定物料
        淘宝接口文档：
        http://bigdata.taobao.com/api.htm?spm=a219a.7386797.0.0.4ad5669aWaaQFi&source=search&docId=33947&docType=2

        :param material_id:  详见https://market.m.taobao.com/app/qn/toutiao-new/index-pc.html#/detail/10628875?_k=gpov9a
        :param adzone_id:  广告位
        :return:
        '''
        # 请求参数，根据API文档修改
        # 把分页现在这里随机有一定考虑
        # 原因是：1. 不同 material_id 得到的数据不一，且刷新周期不一
        #                    2. 微信发送不可太频繁，我仅是怕被封，决定取很小一部分数据
        page_no = str(random.choices(['1','2','3','4', '5', '6', '7', '8', '9'])[0])
        page_size = str(random.randint(8, 10))

        postparm = {
                    'page_no': page_no,
                    'page_size': page_size,
                    'adzone_id': self.adzone_id,
                    'material_id': material_id,
                    'method': 'taobao.tbk.dg.material.optional.upgrade',
                    'start_dsr': start_dsr, #商品筛选-店铺dsr评分。筛选大于等于当前设置的店铺dsr评分的商品0-50000之间
                    'start_tk_rate': start_tk_rate, #商品筛选-淘客收入比率下限(商品佣金比率+补贴比率)。如：1234表示12.34%
                    'end_tk_rate': end_tk_rate, #商品筛选-淘客收入比率上限(商品佣金比率+补贴比率)。如：1234表示12.34%
                    'start_price': start_price, #商品筛选-预估到手价范围下限。单位：元
                    'end_price': end_price, #商品筛选-预估到手价范围上限。单位：元
                    'is_overseas': is_overseas, #商品筛选-是否海外商品。true表示属于海外商品，false或不设置表示不限
                    'is_tmall': is_tmall, #商品筛选-是否天猫商品。true表示属于天猫商品，false或不设置表示不限
                    'sort': sort, #排序_des（降序），排序_asc（升序），销量（total_sales），淘客收入比率（tk_rate），营销计划佣金（tk_mkt_rate）， 累计推广量（tk_total_sales），总支出佣金（tk_total_commi），预估到价格（final_promotion_price），匹配分（match）
                    'itemloc': itemloc, #商品筛选-所在地
                    'cat': cat, #(必填)商品筛选-后台类目ID。用,分割，最大10个
                    'q': q, #(必填)商品筛选-查询词；注意：用标题精准搜索时，若无消费者比价场景ID2权限，当搜索结果只有一个商品时则出参不再提供商品推广链接和商品id字段，若搜索结果仍有多个商品，则正常出参。同时无消费者比价场景ID2权限，q参数也不再支持入参淘宝复制的商品链接进行搜索查询，仅支持入参含新商品id的淘宝客推广链接如uland链接进行搜索查询(场景id使用说明参考《淘宝客新商品ID升级》白皮书：https://www.yuque.com/taobaolianmengguanfangxiaoer/zmig94/tfyt0pahmlpzu2ud)
                    'has_coupon': has_coupon, #优惠券筛选-是否有优惠券。true表示该商品有优惠券，false或不设置表示不限
                    'ip': ip, #ip参数影响邮费获取，如果不传或者传入不准确，邮费无法精准提供
                    'need_free_shipment': need_free_shipment, #商品筛选-是否包邮。true表示包邮，false或不设置表示不限
                    'need_prepay': need_prepay, #商品筛选-是否加入消费者保障。true表示加入，false或不设置表示不限
                    'include_pay_rate_30': include_pay_rate_30, #商品筛选-成交转化是否高于行业均值。True表示大于等于，false或不设置表示不限
                    'include_good_rate': include_good_rate, #商品筛选-好评率是否高于行业均值。True表示大于等于，false或不设置表示不限
                    'include_rfd_rate': include_rfd_rate, #商品筛选-退款率是否低于行业均值。True表示大于等于，false或不设置表示不限
                    'npx_level': npx_level, #商品筛选-牛皮癣程度。取值：1不限，2无，3轻微
                    'device_encrypt': device_encrypt, #智能匹配-设备号加密类型：MD5；使用智能推荐请先签署协议https://pub.alimama.com/fourth/protocol/common.htm?key=hangye_laxin
                    'device_value': device_value, #智能匹配-设备号加密后的值（MD5加密需32位小写）；使用智能推荐请先签署协议https://pub.alimama.com/fourth/protocol/common.htm?key=hangye_laxin
                    'device_type': device_type, #智能匹配-设备号类型：IMEI，或者IDFA，或者UTDID（UTDID不支持MD5加密），或者OAID；使用智能推荐请先签署协议https://pub.alimama.com/fourth/protocol/common.htm?key=hangye_laxin
                    'special_id': special_id, #会员运营ID
                    'relation_id': relation_id, #渠道关系ID，仅适用于渠道推广场景
                    'get_topn_rate': get_topn_rate, #是否获取前N件佣金信息 0否，1是，其他值否
                    'biz_scene_id': biz_scene_id, #1-动态ID转链场景，2-消费者比价场景（不填默认为1）；场景id使用说明参考《淘宝客新商品ID升级》白皮书：https://www.yuque.com/taobaolianmengguanfangxiaoer/zmig94/tfyt0pahmlpzu2ud
                    'promotion_type': promotion_type, #1-自购省，2-推广赚（代理模式专属ID，代理模式必填，非代理模式不用填写该字段）
                    'mgc_start_time': mgc_start_time, #线报内容筛选—内容生产开始时间，13毫秒时间戳
                    'mgc_end_time': mgc_end_time, #线报内容筛选—内容生产截止时间，13毫秒时间戳
                    'mgc_status': mgc_status, #线报状态筛选，0-全部 1-过期 2-实时生效 3-未来生效 不传默认过滤有效
                    'ucrowd_id': ucrowd_id, #人群ID，仅适用于物料评估场景material_id=41377
                    'ucrowd_rank_items': ucrowd_rank_items # 物料评估-商品列表
                    }
        # 公共参数，一般不需要修改
        paramArr = {'app_key': self.app_key,
                    'v': '2.0',
                    'sign_method': 'md5',
                    'format': 'json',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                    }

        paramArr = {**paramArr, **postparm}
        sign = self.createSign(paramArr)
        strParam = self.createStrParam(paramArr)
        strParam += 'sign=' + sign
        url = TB_API_ROOT + strParam
        print(url)
        res = urllib.request.urlopen(url).read()
        return res

    def taobao_tbk_tpwd_create(self, text: str, url: str):
        '''
        提供淘客生成淘口令接口，淘客提交口令内容、logo、url等参数，生成淘口令关键key如：￥SADadW￥，后续进行文案包装组装用于传播
        淘宝接口文档：
        http://bigdata.taobao.com/api.htm?spm=a219a.7386797.0.0.494b669atcwg9a&source=search&docId=31127&docType=2

        :param text: 口令弹框内容
        :param url: 口令跳转目标页
        :return: 返回淘口令，如<￥SADadW￥>
        '''

        postparm = {
                    'text': text,
                    'url': url,
                    'method': 'taobao.tbk.tpwd.create'
                    }
        # 公共参数，一般不需要修改
        paramArr = {'app_key': self.app_key,
                    'v': '2.0',
                    'sign_method': 'md5',
                    'format': 'json',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                    }

        paramArr = {**paramArr, **postparm}
        sign = self.createSign(paramArr)
        strParam = self.createStrParam(paramArr)
        strParam += 'sign=' + sign
        url = TB_API_ROOT + strParam
        # print("tbk_tpwd_create", url)
        res = urllib.request.urlopen(url).read()
        # print("tb_top_res===", res)
        if str(res).find("error_response") > -1:
            res = "{'tbk_tpwd_create_response': {'data': {'model': ''}}}"
        tao_command = json.loads(res)['tbk_tpwd_create_response']['data']['model']
        return tao_command

    def tkl_parser(self, tkl):
        '''
        :param tkl: str 淘口令，例如 ￥ABCDEFG￥
        :return: str  返回自己的淘口令
        '''
        # 取值地址，接口地址
        url = f'''http://www.taofake.com/index/tools/gettkljm.html?tkl={urllib.parse.quote(tkl)}'''
        # 伪装定义浏览器header
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request)
        data = response.read()
        return self.taobao_tbk_tpwd_create(json.loads(data)['data']['content'], json.loads(data)['data']['url'])
