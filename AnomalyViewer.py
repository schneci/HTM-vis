from IPython.core.display import display
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import pandas as pd
from pprint import pprint 

rows,cols = 100,2
data = np.random.rand(rows,cols) 
tidx = pd.date_range('2019-01-01', periods=rows, freq='T') 
df = pd.DataFrame(data, columns=['value','score'], index=tidx)
range = abs(df.max().value) - abs(df.min().value)
band = range
zero = df.min().value - band
heighmax = abs(zero + band * 0.6)
heighmid = abs(zero + band * 0.7)
heighmin = abs(zero + band * 0.8)

mid, high = 0.4, 0.8
#df["color"] = np.where((df.score < mid), "green", np.where((df.score < high) & (df.score >= mid), "yellow", "red"))
#df["anomaly"] = np.where((df.score < mid), "LOW", np.where((df.score < high) & (df.score >= mid), "MID", "HIGH"))

tdiff = np.diff(df.score.index.values).min()
#freq = 1e9 / np.diff(outdf.score.index.values).min().astype(int)
fr = str(int(tdiff/(1e9))) + "S"
freq = str(int(tdiff/(1e9) * 2)) + "S"
dfbucket = pd.DataFrame()
dfbucket["score"] = df.score.resample(freq).max()
dfbucket = dfbucket.resample(fr).asfreq()
dfbucket["anomalycolor"] = np.where(dfbucket.score.isnull(), "white",
                           np.where(dfbucket.score < mid, "green", 
                           np.where((dfbucket.score < high) & (dfbucket.score >= mid), "orange", "red")))
dfbucket["anomaly"] =      np.where(dfbucket.score.isnull(), "",
                           np.where(dfbucket.score < mid, "LOW", 
                           np.where((dfbucket.score < high)  & (dfbucket.score >= mid), "MID", "HIGH")))
#dfbucket.loc[dfbucket['score'].isnull(), 'anomalycolor'] = "white"
#dfbucket.loc[dfbucket['score'].isnull(), 'anomaly'] = np.NaN

mid, high = 0.4, 0.51

trace1 = go.Scatter(
    x = df.index,
    y = df.value,
    name = "value",
    yaxis = "y"
)
trace2 = go.Bar(
    x = df.index,
    y = dfbucket.anomaly,  
    
    opacity = 0.3,
    name = "score",
    yaxis = 'y2',
    showlegend = False,
    marker = dict(color = dfbucket["anomalycolor"],
             line = dict(
                    color = 'black',
                    width = 1.5,)
        )
)
data = [trace1, trace2]
layout = go.Layout(
    title = "Anomaly",
    xaxis = dict(
        rangeselector=dict(
        buttons=list([
            dict(count=1,
                    label='1h',
                    step='hour',
                    stepmode= "backward"),
            dict(count=1,
                    label='1d',
                    step='day',
                    stepmode='todate'),
            dict(count=1,
                label='1m',
                step='month',
                stepmode='todate'),
            dict(step='all')
        ])
        ),
        rangeslider=dict(
            visible = True
        ),
        type='date',
    ),
    yaxis = dict(
        #overlaying = "y",
        rangemode = "normal",
        autorange = True,
        title = "yaxis title",
        zeroline = True,
        domain = [0.4, 1]
    ),    
    yaxis2 = dict(
        autorange = True,
        title = "yaxis2 title",
        titlefont = dict(
            color = "blue"
        ),
        #tickfont = dict(
        #    color = "gray"
        #),
        categoryorder = "array",
        categoryarray = ["", "LOW", "MID", "HIGH"],
        overlaying = "y2",
        side = "right",
        zeroline = True,
        domain=[0.0, 0.2],
        visible = False,
        rangemode = "tozero",
        ),
    autosize = True,
    width = 700,
    height = 450,     
    #paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'  
)

initial_range = [
    df.head(1).index, df.tail(1).index
]

fig = go.FigureWidget(data, layout)
#fig["layout"]["xaxis"].update(range=initial_range)
def handle_zoom(layout, xrange, yrange):
    print('new x-range:', xrange)
    print('new y-range:', yrange)
fig.layout.on_change(handle_zoom, 'xaxis.range', 'yaxis.range')
iplot(fig)
display(fig)
