from .interface import MyAPIInterface


class MyAPIImpl(MyAPIInterface):
    # access your context here safely
    def __init__(self, app_context: dict, *args, **kwargs):
        super(MyAPIImpl, self).__init__(*args, **kwargs)
        self.app_context = app_context

    def do_something(self):
        print("doing something!")

    def do_something_private(self):
        print(self.app_context.items())
