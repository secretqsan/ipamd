from test_data import *
from ipamd import App
app = App(name='test', gpu_id=3)
app.data_process.print(app.data_process.flatten(vector, title='res', unit='m/s'))
app.data_process.print(app.data_process.flatten(matrix, axis=0))
app.data_process.print(app.data_process.normalize(vector))
app.data_process.print(app.data_process.normalize(series, target='x'))
app.data_process.print(app.data_process.normalize(matrix))
app.data_process.print(app.data_process.normalize(ratio))