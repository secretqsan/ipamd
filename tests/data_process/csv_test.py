from test_data import *
from ipamd import App
app = App(name='test', gpu_id=3)

app.data_process.to_csv(vector, 'test.csv')
app.data_process.to_csv(matrix, 'test_matrix.csv')
app.data_process.to_csv(series, 'test_series.csv')
app.data_process.to_csv(distribution, 'test_distribution.csv')
app.data_process.to_csv(ratio, 'ratio.csv')