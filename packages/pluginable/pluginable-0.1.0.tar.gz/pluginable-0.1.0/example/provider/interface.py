from pluginable import PAInterface


class MyAPIInterface(PAInterface):
    name = "myapi"

    def do_something(self):
        pass
