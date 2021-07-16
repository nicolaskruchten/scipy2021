
# v1 - text input drives text output


from jupyter_dash import JupyterDash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

app = JupyterDash(__name__)

app.layout = html.Div(children = [
  html.H1(id="the_output"),
  dcc.Input(id="the_input")
])

@app.callback(Output('the_output', 'children'),
              Input('the_input', 'value'))
def cb(input_value):
    return "Hello %s!" % (input_value or "World")

app.run_server(mode="jupyterlab")







# v2 - dropdown drives graph


from jupyter_dash import JupyterDash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
df = px.data.gapminder()

app = JupyterDash(__name__)

app.layout = html.Div(children = [
  dcc.Dropdown(id="year", value=2007, clearable=False,
    options=[{"label": y, "value": y} for y in df['year'].unique()]),
  dcc.Graph(id="graph", figure={})
])

@app.callback(Output('graph', 'figure'), Input('year', 'value'))
def cb(year):
    df_year = df.query("year == @year")
    return px.scatter(df_year, x="gdpPercap", y="lifeExp", size="pop",
          log_x=True, size_max=60, hover_name="country", height=400)

app.run_server(mode="jupyterlab")






# v3 - dropdown driving graph and map, graph drives map


from jupyter_dash import JupyterDash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
df = px.data.gapminder()

app = JupyterDash(__name__)

app.layout = html.Div(children = [
  dcc.Dropdown(id="year", value=2007, clearable=False,
    options=[{"label": y, "value": y} for y in df['year'].unique()]),
  dcc.Graph(id="graph", figure={}),
  dcc.Graph(id="map", figure={})
])

@app.callback(Output('graph', 'figure'), Input('year', 'value'))
def cb(year):
    df_year = df.query("year == @year")
    return px.scatter(df_year, x="gdpPercap", y="lifeExp", size="pop",
          log_x=True, size_max=60, hover_name="country", height=400,
          custom_data=[df_year.index]).update_layout(dragmode='lasso')

@app.callback(Output('map', 'figure'),
    Input('year', 'value'), Input('graph', 'selectedData'))
def display_selected_data(year, selectedData):
    df_year = df.query("year == @year")
    if selectedData:
        indices = [p["customdata"][0] for p in selectedData["points"]]
        try:
            df_year = df_year.loc[indices]
        except:
            pass

    return px.scatter_geo(df_year, locations="iso_alpha",size="pop", 
                          hover_name="country", height=400)

app.run_server(mode="jupyterlab")
