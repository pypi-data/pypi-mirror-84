from provider import MyApp
from consumer import MyPlugin


app = MyApp()
app.register(MyPlugin)
app.custom_method()
