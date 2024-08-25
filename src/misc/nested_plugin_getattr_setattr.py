class P1:
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3

class P2:
    def __init__(self):
        self.x = 10
        self.y = 20
        self.z = 30

class App:
    def __init__(self):
        super().__setattr__(
            "plugins", {
                "p1": P1(),
                "p2": P2()
            }
        )
    def __getattr__(self, name):
        # Check if the attribute exists in the AppBase instance
        if name in self.__dict__:
            return self.__dict__[name]

        # Check if the attribute exists in any of the plugins
        for plugin in self.plugins.values():
            if hasattr(plugin, name):
                return getattr(plugin, name)

        # If the attribute is not found, raise an AttributeError
        raise AttributeError(f"'{self.__class__.__name__}' object and its plugins have no attribute '{name}'")

    def __setattr__(self, name, value):
        # Check if the attribute exists in the AppBase instance
        if name in self.__dict__:
            self.__dict__[name] = value
            return

        # Check if the attribute exists in any of the plugins
        for plugin in self.plugins.values():
            if hasattr(plugin, name):
                setattr(plugin, name, value)
                return

        self.__dict__[name] = value


if __name__ == '__main__':
    app = App()
    p1 = app.plugins["p1"]
    p2 = app.plugins["p2"]
    #%%
    print(p1.a)
    #%%
    app.a = 100
    #%%
    print(p1.a)
    #%%
    app.x = 'a'
    #%%
    print(p2.x)
    #%%
    print(app.b)
    #%%
    print(app.plugins["p1"].b)
    #%%
    app.plugins = {}
    #%%
    print(app.plugins)