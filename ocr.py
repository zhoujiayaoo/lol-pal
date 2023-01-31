import requests
import base64
from urllib.parse import urlencode
from configUtils import conf

API_KEY = conf.get("baidu_ai", "API_KEY")
SECRET_KEY = conf.get("baidu_ai", "SECRET_KEY")


def get_image_text_info(image_path):
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=" + get_access_token()
    f = open(image_path, 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=params)
    print(response.text)
    return response.text


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    result = get_image_text_info("temp/finish_image.jpg")
