import requests
import hashlib
import time

PDD_API_ROOT = 'https://gw-api.pinduoduo.com/api/router'


class PddApiClient(object):
    def __init__(self, app_key, secret_key, access_token, refresh_token):
        self.app_key = app_key
        self.secret_key = secret_key
        self.access_token = access_token
        self.refresh_token = refresh_token

    def get_sign(self, params):
        params_list = sorted(list(params.items()), key=lambda x: x[0])
        params_bytes = (self.secret_key + ''.join("%s%s" % (k, v) for k, v in params_list) + self.secret_key).encode(
            'utf-8')
        sign = hashlib.md5(params_bytes).hexdigest().upper()
        return sign

    def call(self, method, param_json, **kwargs):
        params = {
            "type": method,
            "data_type": "JSON",
            "client_id": self.app_key,
            "access_token": self.access_token,
            "timestamp": int(time.time()),
        }
        if isinstance(param_json, (dict, list)):
            for key in param_json:
                params[key] = param_json[key]
        params['sign'] = self.get_sign(params)
        resp = requests.get(PDD_API_ROOT, params=params, **kwargs)
        print('resp.url===', resp.url)
        return resp


if __name__ == '__main__':
    pass
    # pdd = PddApiClient(app_key='', secret_key='')
    # resp = pdd.call("pdd.ddk.top.goods.list.query",{"p_id": ""})
    # print(resp)
