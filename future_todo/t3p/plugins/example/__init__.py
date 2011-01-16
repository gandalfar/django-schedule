from future_todo.t3p.views import plugin, plugin_handler

class fooplugin(plugin):
    """Concrete class for foo plugin."""
    def __init__(self, list):
        print "meow!"
        self.list = list
        
    def run(self):
        #do something here
        list = self.list
        output_log = "You called me with: %s, %s, %s, %s" % (list.api_url, list.api_username, list.api_password, list.api_token)
        return output_log
        
    name = "example"
    description = "insert description here"

plugin_handler.register_plugin(fooplugin)