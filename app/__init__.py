import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from .languages import app_en, app_es, app_fr, app_zh

app = dash.Dash(__name__, meta_tags=[
    {'name': 'viewport', 'content': 'width=device-width'},
    {'name': 'description', 'content': 'COVID-19 Montreal Dashboard / Tableau de bord COVID-19 Montréal'},
])
app.title = 'COVID-19 Montréal Dashboard'
app.config.suppress_callback_exceptions = True
# WSGI entry point
server = app.server


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Loading(
        id='main-loading',
        children=[html.Div(id='page-content')],
        type='graph',
        fullscreen=True
    )
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return app_fr.layout
    elif pathname == '/fr':
        return app_fr.layout
    elif pathname == '/en':
        return app_en.layout
    elif pathname == '/zh':
        return app_zh.layout
    elif pathname == '/es':
        return app_es.layout
    elif pathname == '/vaccination' or pathname == '/fr/vaccination':
        return app_fr.layout_vaccination
    elif pathname == '/en/vaccination':
        return app_en.layout_vaccination
    elif pathname == '/zh/vaccination':
        return app_zh.layout_vaccination
    elif pathname == '/es/vaccination':
        return app_es.layout_vaccination
    else:
        return '404: Page Not Found'
