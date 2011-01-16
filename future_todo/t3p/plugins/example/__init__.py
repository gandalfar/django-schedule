from future_todo.t3p.views import plugin, plugin_handler

class fooplugin(plugin):
    """Concrete class for foo plugin."""
    def __init__(self):
        print "meow!"
    
    name = "fooplugin"
    description = "insert description here"

plugin_handler.register_plugin(fooplugin)