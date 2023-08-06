# url path 统一管理 花括号中变量代表待替换值
import adapay_merchant
from adapay_core import ApiRequest

import os
from adapay_core.param_handler import read_file

pay_message_token = '/v1/token/apply'

# ----------merchant_user----------
merchant_user_create = '/v1/batchEntrys/userEntry'
merchant_user_query = '/v1/batchEntrys/userEntry'

# ----------pay_conf----------
pay_conf_create = '/v1/batchInput/merConf'
pay_conf_query = '/v1/batchInput/merConf'
pay_conf_modify = '/v1/batchInput/merResidentModify'

# ----------merchant_profile----------
profile_audit = '/v1/merProfile/merProfileForAudit'
profile_picture = '/v1/merProfile/merProfilePicture'
profile_status = '/v1/merProfile/merProfile'

# application
app = '/v1/batchEntrys/application'

pay_base_url = 'https://api.adapay.tech'

public_key = read_file(os.path.dirname(__file__) + os.sep + 'public_key.pem')


def __request_init(url, request_params, base_url):
    mer_key = request_params.pop('mer_key', None)
    config_info = adapay_merchant.mer_configs[mer_key]

    ApiRequest.base_url = base_url if base_url else pay_base_url

    ApiRequest.build(config_info["api_key"], config_info['private_key'], public_key, url,
                     request_params, adapay_merchant.__version__, adapay_merchant.connect_timeout)


def request_post(url, request_params, files=None, base_url=''):
    __request_init(url, request_params, base_url)
    return ApiRequest.post(files)


def request_get(url, request_params, base_url=''):
    __request_init(url, request_params, base_url)
    return ApiRequest.get()
