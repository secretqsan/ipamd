from test_data import *
from ipamd import App
app = App(name='test', gpu_id=3)

print(app.data_process.to_df(scalar))
print(app.data_process.to_df(vector))
print(app.data_process.to_df(series))
print(app.data_process.to_df(matrix))
print(app.data_process.to_df(ratio))
print(app.data_process.to_df(distribution))
