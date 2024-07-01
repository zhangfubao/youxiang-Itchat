import time
import json
import itchat
import random
from untils.common import save_pic, del_pic
from untils.tb_top_api import TbApiClient


def tb_share_text(group_name: str, material_id: str, app_key, app_secret, adzone_id):
    '''

    :param group_name:
    :param material_id:
    :return:
    '''
    try:
        material_id = str(random.choices(material_id.split(','))[0])
        # print("material_id===", material_id)
        # print("group_name.f===", f'''{group_name}''')
        # print("group_name===", group_name)
        groups = itchat.search_chatrooms(name=f'''{group_name}''')
        # itchat.send("1234567890",
        #             "@a135f48e0d511adcec2fd48dd80f34c9ebf51d66f138ceee94b22f9d26a85e4e")
        # print("groups===", groups)
        print("开始时间", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        for room in groups:
            # print("room===", room)
            group_uuid = room['UserName']
            print("group_uuid===", group_uuid)
            time.sleep(random.randint(1, 5))
            tb_client = TbApiClient(app_key=app_key, secret_key=app_secret, adzone_id=adzone_id)
            # print("tb_client===", tb_client)
            # res = tb_client.taobao_tbk_dg_optimus_material(material_id)
            res = tb_client.taobao_tbk_dg_material_recommend(material_id)
            # res = res.replace("\n", "")
            # print("res===", res)
            if str(res).find("error_response") > -1:
                continue
            json_data = json.loads(res)['tbk_dg_material_recommend_response']['result_list']['map_data']
            # print("json_data===", json_data)
            count = 0
            for item in json_data:
                count += 1
                coupon_amount = 0
                share_url = ""
                title = ""
                click_url = ""

                basicInfo = item['item_basic_info']
                publishInfo = item['publish_info']
                pricePromotionInfo = item['price_promotion_info']

                pict_url = "https:" + str(basicInfo['pict_url'])
                item_id = item['item_id']
                filename = save_pic(pict_url, item_id)

                if str(item).find("coupon_share_url") > -1:
                    share_url = "https:" + publishInfo['coupon_share_url']
                else:
                    share_url = "https:" + publishInfo['click_url']

                # coupon_amount = item['coupon_amount']
                title = basicInfo['title']
                zk_final_price = pricePromotionInfo['zk_final_price']
                final_promotion_price = ""
                if str(pricePromotionInfo).find("final_promotion_price") > -1:
                    final_promotion_price = pricePromotionInfo['final_promotion_price']

                send_msg = ""
                if final_promotion_price:
                    if final_promotion_price == zk_final_price:
                        send_msg = f'''{title}\n【预估到手】¥{final_promotion_price}'''
                    else:
                        send_msg = f'''{title}\n【在售价】¥{zk_final_price}\n【预估到手】¥{final_promotion_price}'''
                else:
                    send_msg = f'''{title}\n【预估到手】¥{zk_final_price}'''
                # itchat.send(send_msg, group_uuid)
                time.sleep(random.randint(1, 3))
                text = f'''{tb_client.taobao_tbk_tpwd_create(title, share_url)}'''
                if not text:
                    return

                print("pict_url1===", pict_url)
                # print("img2===", '@img@%s' % (f'''{filename}'''))
                # 发送图片
                itchat.send('@img@%s' % f'''{filename}''', group_uuid)
                time.sleep(2)

                start_index = text.find('￥')
                # itchat.send(f'''({text[start_index: 13+start_index]})''', group_uuid)
                text1 = text.replace(title, "")
                # print('text1===', text1)
                itchat.send(f'''{send_msg}\n(奍码：{text1})\n复制打开氵匋寶app''', group_uuid)
                time.sleep(2)
                del_pic(filename)
    except Exception as e:
        print("except Exception===", e)
        # tb_share_text(group_name, material_id, app_key, app_secret, adzone_id)


if __name__ == '__main__':
    print(f'''tb function''')
