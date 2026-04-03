from ipamd import App
from test_data import *
app = App(name='test', gpu_id=3)

app.data_process.print(scalar)
app.data_process.print(vector)
app.data_process.print(series)
app.data_process.print(matrix)
app.data_process.print(ratio)
app.data_process.print(distribution)