import json

import tornado.web
from tornado.testing import AsyncHTTPTestCase

from tornado_restful.handler import RestfulMetaType, RestfulHandler, get, post


class WidgetHandler(RestfulHandler, metaclass=RestfulMetaType):
    widgets = {1: 'w1', 2: 'w2', 3: 'w3'}

    @get('/widgets')
    def get_all_widgets(self):
        return list(self.widgets)

    @get('/widgets/<int:widget_id>')
    def get_widget(self, widget_id):
        return self.widgets[widget_id]

    @post('/widgets')
    def add_widget(self):
        n = len(self.widgets) + 1
        widgets = self.widgets.copy()
        widgets[n] = f'w{n}'
        return widgets[n]


class TestWidgetHandler(AsyncHTTPTestCase):

    def get_app(self):
        return tornado.web.Application(WidgetHandler.get_handlers())

    def test_get_all_widgets(self):
        resp = self.fetch('/widgets')
        res = json.loads(resp.body)
        assert res['data'] == [1, 2, 3]
        assert res['error'] is None

    def test_get_widget(self):
        resp = self.fetch('/widgets/2')
        res = json.loads(resp.body)
        assert res['data'] == 'w2'
        assert res['error'] is None

    def test_add_widget(self):
        resp = self.fetch('/widgets', method='POST', body='')
        res = json.loads(resp.body)
        assert res['data'] == 'w4'