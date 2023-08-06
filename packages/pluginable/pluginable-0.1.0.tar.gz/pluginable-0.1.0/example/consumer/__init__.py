from pluginable import PAPlugin
from provider import MyAPIInterface


class MyPlugin(PAPlugin):
    name = "my custom plugin"
    api_kls = MyAPIInterface

    def custom_method(self):
        self.api.do_something_private()
