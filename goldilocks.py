#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 17:09:29 2019

@author: arungovindm
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
from dash.dependencies import Input, Output


plotly.tools.set_credentials_file(username='arungovindm', api_key='Z09F8aeHPWYFxcR4cdbo')

# Get Data: this ex will only use part of it (i.e. rows 750-1500)
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
data=pd.read_csv('/home/chennam/Downloads/compositepars_2019.04.03_01.12.07.csv')
sol=pd.read_csv('/home/chennam/Downloads/sol.csv')
sol=sol.dropna(axis=1)
#data = data.drop(104,axis=0)
data=data.dropna()
#data['fpl_bmasse']=np.log(data.fpl_bmasse)
data['fpl_lograde']=np.log(data.fpl_rade)
sol['fpl_lograde']=np.log(sol.fpl_rade)
#data['fpl_dens']=np.log(data.fpl_dens)
#data['fpl_smax']=np.log(data.fpl_smax)
data['fpl_logtemp']=np.log(data.fpl_eqt)
def get_val(name,value):
    sol=pd.read_csv('/home/chennam/Downloads/sol.csv')
    sol=sol.dropna(axis=1)
    data=pd.read_csv('/home/chennam/Downloads/compositepars_2019.04.03_01.12.07.csv')
    data=data.dropna()
    d=pd.concat([sol,data],ignore_index=True)
    return float(d.loc[d['fpl_name']==name][value])

def get_axes(value):
    if value=='fpl_bmasse':
        earth_data=1
        label='Mass (relative to Earth)'
        yrange=[np.log10(0.01),np.log10(5000)]
    elif value=='fpl_eqt':
        earth_data=255
        label='Temperature (K)'
        yrange=[np.log10(1),np.log10(5000)]
    elif value=='fpl_orbper':
        earth_data = 365.256
        label = 'Orbital period (days)'
        yrange=[np.log10(1),np.log10(7300000)]
    elif value =='fpl_dens':
        earth_data = 5.51
        label = 'Density (g/cc)'
        yrange=[np.log10(0.01),np.log10(1300)]
    elif value =='fpl_eccen':
        earth_data = 0.0167
        label = 'Orbital eccentricity'
        yrange=[np.log10(0.0000000001),np.log10(1)]
    else:
        earth_data=1
        label='Orbital Radius (AU)'
        yrange=[np.log10(0.01),np.log10(100)]
    return earth_data,label,yrange

trace1 = go.Scatter3d(name='exoplanets',
    text=data['fpl_name'],
    x=data['fpl_bmasse'],#df['year'][750:1500],
    y=data['fpl_eqt'],#df['continent'][750:1500],
    z=data['fpl_smax'],#df['pop'][750:1500],
    hoverinfo = 'text',
    #df['country'][750:1500],
    mode='markers',
    marker=dict(
        sizemode='diameter',
        sizeref=750,
        size=5000*(1+data['fpl_lograde']),#df['gdpPercap'][750:1500],
        color = data['fpl_eqt'],#df['lifeExp'][750:1500],
        colorscale=[[0.0, 'rgb(9, 158, 244)'],[100/4000, 'rgb(8, 244, 212)'], [200/4000, 'rgb(8, 244, 137)'], [300/4000, 'rgb(31, 244, 8)'],
        [500/4000, 'rgb(173, 244, 8)'], [1000/4000, 'rgb(232, 206, 9)'], [2000/4000, 'rgb(232, 157, 9)'],
        [3000/4000, 'rgb(232, 113, 9)'],[1,'rgb(249, 79, 17)']],
        opacity=1,
        colorbar = dict(title = 'Exoplanets<br>temperature'),
        #line=dict(color='rgb(140, 140, 170)')
    )
)
trace2 = go.Scatter3d(name='solar system',
    text=sol['fpl_name'],
    x=sol['fpl_bmasse'],#df['year'][750:1500],
    y=sol['fpl_eqt'],#df['continent'][750:1500],
    z=sol['fpl_smax'],#df['pop'][750:1500],
    hoverinfo = 'text',
    #df['country'][750:1500],
    mode='markers',
    marker=dict(
        sizemode='diameter',
        sizeref=750,
        size=5000*(1+sol['fpl_lograde']),#df['gdpPercap'][750:1500],
        color = data['fpl_eqt'],#df['lifeExp'][750:1500],
        colorscale=[[0.0, 'rgb(9, 158, 244)'],[100/4000, 'rgb(8, 244, 212)'], [200/4000, 'rgb(8, 244, 137)'], [300/4000, 'rgb(31, 244, 8)'],
        [500/4000, 'rgb(173, 244, 8)'], [1000/4000, 'rgb(232, 206, 9)'], [2000/4000, 'rgb(232, 157, 9)'],
        [3000/4000, 'rgb(232, 113, 9)'],[1,'rgb(249, 79, 17)']],
        opacity=1,
        colorbar = dict(title = 'Exoplanets<br>temperature'),
        #line=dict(color='rgb(140, 140, 170)')
    )
)

colors={'background': '#111111',
    'text': '#7FDBFF'}

data1=[trace1,trace2]

layout1=go.Layout(legend=dict(orientation="h"),
                  height=600, width=600, title='Visualizing exoplanets',
                 plot_bgcolor=colors['background'],
                 paper_bgcolor=colors['background'],
                 
                 font = dict(color = colors['text']),
                 scene=dict(
                 xaxis = dict(title = 'Mass',
                              type='log',
                              gridcolor='#bdbdbd'),
                 yaxis = dict(title = 'Temperature',
                              type='log'),
                 zaxis = dict(title = 'Orbital radius',
                              type='log')))

fig=go.Figure(data=data1, layout=layout1)
#py.iplot(fig, filename='3DBubble')


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(style={}, children=[
    html.H1(children='Goldilocks Exoplanets : A 3D visualization',
            style={'textAlign':'center'}),
            html.Div(children='''
                     Powered by Dash.
                     '''),

            html.Div(style={'display':'inline-block','width':'49%'},children = [
                    
                    dcc.Graph(
                            id='planets',
                            figure=fig
                            ),
                    
                    ]),
            html.Div(style={'display':'inline-block','width':'49%',
                            'vertical-align': 'top'},
                     children = [
                             dcc.Dropdown(
                                     id='x-dropdown',
                                     options=[
                                             {'label': 'Mass', 'value': 'fpl_bmasse'},
                                             {'label': 'Temperature', 'value': 'fpl_eqt'},
                                             {'label': 'Density', 'value': 'fpl_dens'},
                                             {'label': 'Orbital radius', 'value': 'fpl_smax'},
                                             {'label': 'Orbital period', 'value': 'fpl_orbper'},
                                             {'label': 'Orbital eccentricity', 'value': 'fpl_eccen'}
                                             ],
                                     value='fpl_bmasse',
                                     placeholder='choose x-axis'
                                     ),
                             dcc.Dropdown(
                                     id='y-dropdown',
                                     options=[
                                             {'label': 'Mass', 'value': 'fpl_bmasse'},
                                             {'label': 'Temperature', 'value': 'fpl_eqt'},
                                             {'label': 'Density', 'value': 'fpl_dens'},
                                             {'label': 'Orbital radius', 'value': 'fpl_smax'},
                                             {'label': 'Orbital period', 'value': 'fpl_orbper'},
                                             {'label': 'Orbital eccentricity', 'value': 'fpl_eccen'}
                                             ],
                                     value='fpl_eqt',
                                     placeholder='choose x-axis'
                                     ),
                             dcc.Graph(id='side plot'
                                       ),])
])
            
    
@app.callback(
    Output('side plot', 'figure'),
    [Input('planets', 'clickData'),
     Input('y-dropdown','value'),
     Input('x-dropdown','value')])    
def display_click_data(clickData,yvalue,xvalue):
    if not clickData:
        name='bet Pic b'
        mass=0
        temp=0
        yearth_data=255
        xearth_data=1
        yrange=[np.log10(1),np.log10(5000)],
        xrange=[np.log10(1),np.log10(5000)]
        ylabel='Temperature (K)'
        xlabel = 'Mass relative to Earth'
    else:
        name=clickData['points'][0]['text']
        mass=get_val(name,xvalue)
        temp=get_val(name,yvalue)
        yearth_data,ylabel, yrange=get_axes(yvalue)
        xearth_data,xlabel, xrange=get_axes(xvalue)
    data=[go.Scatter(
            x=[mass,xearth_data],
            y=[temp,yearth_data],
            text=[name,'Earth'],
            mode='markers',
            marker=dict(sizemode='diameter',
                        sizeref=0.1,
                        size=[get_val(name,'fpl_rade'),1],#df['gdpPercap'][750:1500],
                        color = [get_val(name,'fpl_eqt'),255,4000],#df['lifeExp'][750:1500],
                        colorscale=[[0.0, 'rgb(9, 158, 244)'],[100/4000, 'rgb(8, 244, 212)'], [200/4000, 'rgb(8, 244, 137)'], [300/4000, 'rgb(31, 244, 8)'],
                        [500/4000, 'rgb(173, 244, 8)'], [1000/4000, 'rgb(232, 206, 9)'], [2000/4000, 'rgb(232, 157, 9)'],
                        [3000/4000, 'rgb(232, 113, 9)'],[1,'rgb(249, 79, 17)']],
                        opacity=1,
                        colorbar = dict(title = 'Exoplanets<br>temperature'),
        #line=dict(color='rgb(140, 140, 170)')
    ))
            ]
    layout=go.Layout(title='Earth-Similarity',
            xaxis={'type': 'log', 
                   'title': xlabel,
                   'range':xrange},
            yaxis={'type': 'log',
                   'title': ylabel,
                   'range':yrange}
            #margin={'l': 60, 'b': 40, 'r': 10, 't': 10},
            #hovermode="False"
            )
    return {'data':data,'layout':layout}

if __name__ == '__main__':
    app.run_server(debug=True)