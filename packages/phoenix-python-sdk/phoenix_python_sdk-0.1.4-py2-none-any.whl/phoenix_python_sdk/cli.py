import requests
import os
from .exception import ServerException
import logging

logger = logging.getLogger(__name__)
# phoenix 接口地址
PHOENIX_ENDPOINT = os.environ.get("PHOENIX_ENDPOINT", "http://127.0.0.1:8000")


class PhoenixClient(object):
    """
        调用接口
    """

    def __init__(self, endpoint=PHOENIX_ENDPOINT):
        if endpoint:
            self.endpoint = endpoint
        else:
            self.endpoint = PHOENIX_ENDPOINT

    def get_broker_info(self):
        """
            获取broker信息
        :param endpoint:
        :return:
        """
        url = str(self.endpoint) + "/api/broker/query/"
        return self.request(url, body={})

    def request(self, url, body={}, retry=0):

        try:
            logger.info("call url %s body %s retry %s" % (url, body, retry))
            response = requests.post(url, json=body)
            logger.info("call url %s result %s" % (url, response.content))
            if response.ok:
                result = response.json()
                logger.debug(result)
                return result.get("results", {})
            raise Exception(response.content)
        except Exception as e:
            # 重试，异常出力
            if retry > 3:
                raise ServerException(code=1004, traceback=str(e))
            else:
                retry += 1
                self.request(url, body, retry)

