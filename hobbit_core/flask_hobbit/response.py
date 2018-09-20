from flask.json import dumps
from werkzeug import Response

RESP_MSGS = {
    401: '未登录',
    403: '未授权',
    404: '不正确的链接地址',
    422: '请求数据校验失败',

    500: '服务器内部错误',
}


def gen_response(code, message='', detail=None):
    return {
        'code': str(code),
        'message': message or RESP_MSGS.get(code, '未知错误'),
        'detail': detail,
    }


class Result(Response):
    status = 200

    def __init__(self, response=None, status=None, headers=None,
                 mimetype='application/json', content_type=None,
                 direct_passthrough=False):
        assert sorted(response.keys()) == ['code', 'detail', 'message'], \
            '错误的返回格式'
        return super().__init__(
            response=dumps(response, indent=0, separators=(',', ':')) + '\n',
            status=status or self.status, headers=headers, mimetype=mimetype,
            content_type=content_type, direct_passthrough=direct_passthrough)


class SuccessResult(Result):
    status = 200

    def __init__(self, code=None, message='', detail=None, status=None):
        return super().__init__(
            gen_response(code or self.status, message, detail),
            self.status or status)


class FailedResult(Result):
    status = 400

    def __init__(self, code=None, message='', detail=None):
        return super().__init__(
            gen_response(code or self.status, message, detail), self.status)


class UnauthorizedResult(FailedResult):
    status = 401


class ForbiddenResult(FailedResult):
    status = 403


class ValidationErrorResult(FailedResult):
    status = 422


class ServerErrorResult(FailedResult):
    status = 500