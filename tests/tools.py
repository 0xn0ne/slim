from unittest import mock
from aiohttp.test_utils import make_mocked_request

from slim.base._view.base_view import BaseView


async def make_mocked_view_instance(app, view_cls, method, url, params=None, post=None, *, headers=None) -> BaseView:
    request = make_mocked_request(method, url, headers=headers or {}, protocol=mock.Mock(), app=app)
    request._post = post
    view = view_cls(app, request)
    view._params_cache = params
    await view._prepare()
    return view
