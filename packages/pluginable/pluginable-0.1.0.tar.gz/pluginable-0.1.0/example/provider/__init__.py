from pluginable import PAManager
from .interface import MyAPIInterface
from .impl import MyAPIImpl


class MyManager(PAManager):
    api_mapping = {
        MyAPIInterface.name: MyAPIImpl,
    }


class MyApp(object):
    def __init__(self):
        self.plugin_manager = MyManager()
        self.my_app_context = {
            "my_private_key": "my_private_value",
        }

    def register(self, new_plugin, *args, **kwargs):
        # you can expose your app context to plugins' impl here
        return self.plugin_manager.register(new_plugin, self.my_app_context, *args, **kwargs)

    def __getattr__(self, item):
        return self.plugin_manager.get_plugin_method(item)
