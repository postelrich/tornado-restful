# tornado_restful - RESTful extension for tornado

This library aims to make it quicker and easier to define a RESTful API in tornado. Originally inspired by github.com/rancavil/tornado-rest.

## Installation
```
pip install tornado_restful
```

## Usage

```python
from tornado_restful import RestfulHandler, RestfulMetaType, get, post


class WidgetHandler(RestfulHandler, metaclass=RestfulMetaType):

    @get('/widgets')
    def all_widgets(self):
        return [widget1, widget2, ...]

    @get('/widgets/<int:id>')
    def get_widget(self, id):
        return widgets[id]

    @post('/widgets'):
    def add_widget(self):
        return 'Widget added'

app = Application(WidgetHandler.get_handlers(dict(db=db))
```

## License
New BSD. See [license](https://github.com/postelrich/tornado_restful/blob/master/LICENSE).
