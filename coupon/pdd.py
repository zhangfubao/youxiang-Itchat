import time
import json
import itchat
import random
from untils.common import save_pic, del_pic
from untils.pdd_api import PddApiClient
from chat.itchatHelper import set_system_notice


def pdd_share_text(group_name: str, group_material_id: str, app_key: str, secret_key: str, p_id: str, access_token: str,
                   refresh_token: str):
    '''
    :param group_name:
    :param material_id:
    :return:
    '''
    try:
        offset = str(random.randint(0, 200))  # top.goods.list.query 好像只有300个商品
        limit = "1"  #

        client = PddApiClient(app_key=app_key, secret_key=secret_key, access_token=access_token,
                              refresh_token=refresh_token)
        resp = client.call("pdd.ddk.goods.recommend.get",
                           {"offset": offset,
                            "limit": limit,
                            "p_id": p_id
                            })
        # print("type:pdd.ddk.goods.recommend.get come in===")
    except Exception as e:
        print(e)
        set_system_notice(f'''offset: {offset},\nlimit:{limit}\n\n发现问题''')
        pdd_share_text(group_name, group_material_id, app_key, secret_key, secret_key, p_id)

    for data in json.loads(resp.text)['goods_basic_detail_response']['list']:
        goods_sign = data['goods_sign']
        goods_name = data['goods_name']
        search_id = data['search_id']
        goods_thumbnail_url = data['goods_thumbnail_url']
        min_normal_price = int(data['min_normal_price'])  # 原价
        min_group_price = int(data['min_group_price'])  # 折扣价
        coupon_discount = int(data['coupon_discount'])  # 券价
        if min_group_price < min_normal_price:
            cal_price = min_group_price
        else:
            cal_price = min_normal_price
        cal_price_str = str(cal_price)[:len(str(cal_price)) - 2] if len(
            str(cal_price)[:len(str(cal_price)) - 2]) > 0 else '0' + '.' + str(cal_price)[len(str(cal_price)) - 2:]
        price = str(cal_price - coupon_discount)[:len(str(cal_price - coupon_discount)) - 2] \
            if len(str(cal_price - coupon_discount)[:len(str(cal_price - coupon_discount)) - 2]) > 0 else '0' + '.' \
                                                                                                          + str(
            cal_price - coupon_discount)[len(str(cal_price - coupon_discount)) - 2:]
        short_url = promotion_url_generate(app_key=app_key, secret_key=secret_key, p_id=p_id,
                                           goods_sign=goods_sign, search_id=search_id,
                                           access_token=access_token, refresh_token=refresh_token)

        groups = itchat.search_chatrooms(name=f'''{group_name}''')
        for room in groups:
            room_name = room['UserName']
            time.sleep(random.randint(1, 5))
            filename = save_pic(goods_thumbnail_url, goods_sign)
            # 发送图片
            itchat.send('@img@%s' % (f'''{filename}'''), room_name)
            time.sleep(random.randint(1, 3))
            itchat.send(
                f''' {goods_name} \n【现价】¥{cal_price_str}\n【内部价】¥{price}\n-----------------\n抢购地址:\n{short_url}''',
                room_name)
            del_pic(filename)


def promotion_url_generate(app_key: str, secret_key: str, p_id: str, goods_sign: str, search_id: str,
                           access_token: str, refresh_token: str):
    client = PddApiClient(app_key=app_key, secret_key=secret_key, access_token=access_token,
                          refresh_token=refresh_token)
    resp = client.call("pdd.ddk.goods.promotion.url.generate",
                       {"goods_sign": f'''{goods_sign}''',
                        "search_id": search_id,
                        "p_id": p_id
                        })
    # print("type:pdd.ddk.goods.promotion.url.generate come in===")
    # print("resp===", str(resp.text))
    try:
        short_url = json.loads(resp.text)['goods_promotion_url_generate_response']['goods_promotion_url_list'][0][
            'mobile_short_url']
    except Exception as e:
        print(e)
        set_system_notice(f'''goods_sign: {goods_sign},\nsearch_id:{search_id}\np_id:{p_id}\n\n无法获取连接''')
        short_url = ""
    return short_url
