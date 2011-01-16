class plugin(object):
   """Abstract plugin base class."""
   name = "change me"

class PluginHandler(object):
    def __init__(self):
        self.plugins = []
        self.modules = []
        
    def register_plugin(self, plugin):
        if not plugin.__module__ in self.modules:
            self.plugins += [plugin]
            self.modules += [plugin.__module__]
    
    def get_plugins(self):
        return self.plugins

plugin_handler = PluginHandler()
