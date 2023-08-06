import typing
from abc import ABC


class PAInterface(ABC):
    # declaration only
    name: str

    def __init__(self, *args, **kwargs):
        pass


class PAPlugin(ABC):
    name: str
    api_kls: typing.Type[PAInterface]

    def __init__(self, *args, **kwargs):
        self.api = self.api_kls(*args, **kwargs)


class _PARegistryLayer(object):
    api_mapping: typing.Dict[str, PAInterface] = {
        # api interface name: api impl
    }

    def __init__(self):
        self._plugins: typing.Dict[str, PAPlugin] = dict()

    def register(self, new_plugin: typing.Type[PAPlugin], *args, **kwargs):
        assert new_plugin.api_kls.name in self.api_mapping
        # replace its api kls with real impl
        new_plugin.api_kls = self.api_mapping[new_plugin.api_kls.name]
        self._plugins[new_plugin.name] = new_plugin(*args, **kwargs)

    def unregister(self, plugin_name: str):
        assert plugin_name in self._plugins
        del self._plugins[plugin_name]

    def has_plugin(self, name: str) -> bool:
        return name in self._plugins

    def _get_plugin(self, name: str) -> PAPlugin:
        # it's dangerous because user can easily access your app via real api impl
        # should be a protected method
        return self._plugins[name]

    def get_plugin_list(self) -> typing.List[str]:
        return list(self._plugins.keys())


class PAManager(_PARegistryLayer):
    def get_plugin_method(self, method_name: str):
        # after py36, dict already in order
        for each in self._plugins.values():
            if hasattr(each, method_name):
                return getattr(each, method_name)

    def get_spec_plugin_method(self, plugin_name: str, method_name: str):
        assert plugin_name in self._plugins
        return getattr(self._plugins[plugin_name], method_name)
