from ipamd import App
from test_data import *

app = App(name='test', gpu_id=3)
app.data_process.plot(scalar)
app.data_process.plot(vector)
app.data_process.plot(series)
app.data_process.plot(matrix)
app.data_process.plot(ratio)
app.data_process.plot(distribution)