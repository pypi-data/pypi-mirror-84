

error_message_dict = {
    1000: "连接异常",
    1001: "发送消息异常",
    1002: "当前broker类型不支持",
    1003: "未找到有效的broker"

}


class ServerException(Exception):
    """
        服务器异常
    """

    def __init__(self, code, traceback="", error_dict={}):
        """
            错误初始化
        :param code: 错误码
        :param traceback: 堆栈
        :param traceback: 堆栈
        """
        if not error_dict:
            error_dict = error_message_dict
        self.error_message = error_dict.get(code, 1)
        self.traceback = traceback
        self.code = code


class ConnectionException(ServerException):
    """
        连接异常
    """
    pass