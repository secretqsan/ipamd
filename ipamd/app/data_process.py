from ipamd.public.utils.plugin_manager_v1 import PluginBase
from ipamd.public import shared_data

class DataProcess(PluginBase):
    def __init__(self, app):
        plugin_dir = [shared_data.module_installation_dir + '/plugins/data_process']
        super().__init__(plugin_dir)
        self.app = app
        self.add_resource('persistency_dir', self.app.working_dir)
        self.load_all()
