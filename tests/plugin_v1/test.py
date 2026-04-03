from ipamd.public.utils.plugin_manager_v1 import PluginBase
from ipamd.public import shared_data

class TestPlugin(PluginBase):
    def __init__(self):
        plugin_dir = ([shared_data.module_installation_dir + '/plugins/data_process'])
        super().__init__(plugin_dir)
        self.load_all()

plugin = TestPlugin()
plugin.average([1, 2])
