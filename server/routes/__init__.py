from flask import (
    make_response,
    request,
)

from functools import wraps
from utils import log

def interceptor(route_fn, response_maked):
    '''
    拦截器，用于检查响应路由的请求和响应

    route_fn: 路由函数
    response_maked: 表示路由函数是不是返回一个 response 实例
    '''

    @wraps(route_fn)
    def fn(*args, **kwargs):
        log(request.headers)

        # 设置 headers 允许跨域
        headers = {
            'Access-Control-Allow-Origin': request.headers.get('Origin'),
            'Access-Control-Allow-Headers': 'Content-Type,Content-Length,Authorization,\'Origin\',Accept,X-Requested-With',
            'Access-Control-Allow-Credentials': 'true',
        }

        response = route_fn(*args, **kwargs)
        if not response_maked:
            response = make_response(response)

        for k, v in headers.items():
            response.headers[k] = v
        return response

    return fn


def set_route(blueprint, *args, response_maked=False, **kwargs):
    """
    封装拦截器
    """

    def fn(route_fn):
        route_fn = interceptor(route_fn, response_maked)
        blueprint.route(*args, **kwargs)(route_fn)

    return fn
