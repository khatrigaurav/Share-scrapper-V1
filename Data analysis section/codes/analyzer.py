import talib
# import plotly_express as pe 
import pandas as pd 
# import plotly.graph_objects as go 

# filename = 'Share_Data_ADBL.csv'
# data = pd.read_csv(filename, sep='|', header=0)
# 
# fig  = pe.line(data,x='Date',y='ClosePrice')
# fig.show()

import plotly.graph_objects as go
fig = go.Figure(
    data=[go.Bar(y=[2, 1, 3])],
    layout_title_text="A Figure Displayed with fig.show()"
)
# fig.show(renderer='notebook')

# import plotly.io as pio
# # print(pio.renderers.default)
# pio.renderers.default = 'vscode'