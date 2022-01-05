import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import gunicorn

app = dash.Dash(__name__)
server = app.server

df = pd.read_csv('data/3D_viri.csv')
df.GrossDx.replace({1:'Control',2:'MCI',3:'Dementia'}, inplace=True)


app.layout = html.Div([
    html.H4("Input the values of VI, RI, and NSCT"),
    html.Div([
        "VI Score: ",
        dcc.Input(id='vi-input', value=None, type='number', min=2, max=20)
    ]),
    html.Div([
        "RI Score: ",
        dcc.Input(id='ri-input', value=None,  type='number')
    ]),
    html.Div([
        "NSCT Score: ",
        dcc.Input(id='nsct-input', value=None, type='number')
    ]),
    html.Br(),
    html.Button('Plot Point on Graph', id='button_plot'),
    dcc.Graph(id='3d_scatter', config={'autosizable':True}),
    html.H6("Click and drag the graph to change viewpoints. Scroll to zoom in or out."),

])


@app.callback(
    Output('3d_scatter', 'figure'),
    Input('button_plot', 'n_clicks'),
    state=[
        State(component_id='vi-input', component_property='value'),
        State(component_id='ri-input', component_property='value'),
        State(component_id='nsct-input', component_property='value')
    ])
def plot_point(button_plot, input_vi, input_ri, input_nsct):

    df_new = df.copy()
    df_new = df_new.append({'VI':input_vi,'RI':input_ri,'coding_score':input_nsct,'GrossDx':'Your Input'}, ignore_index=True)

    fig = px.scatter_3d(df_new, x='RI', y='VI', z='coding_score', color='GrossDx', height=600, width=750,
                        color_discrete_map={'Your Input':'#000000','Control':'#07ed6f','MCI':'#1b5ffe','Dementia':'#e00e0b'},
                        category_orders={'GrossDx':['Control','MCI','Dementia','Your Input']},
                        labels={'GrossDx':'Diagnosis','coding_score':'Number-Symbol Coding','VI':'Vulnerability Index','RI':'Resilience Index'})

    return fig

# For local runtime
# if __name__ == '__main__':
#     app.run_server()