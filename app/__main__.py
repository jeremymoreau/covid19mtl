import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from .languages import app_en, app_es, app_fr, app_zh

app = dash.Dash(__name__, meta_tags=[
    {'name': 'viewport', 'content': 'width=device-width'},
    {'name': 'description', 'content': 'COVID-19 Montreal Dashboard / Tableau de bord COVID-19 Montréal'},
])
app.title = 'COVID-19 MTL'
app.config.suppress_callback_exceptions = True
# WSGI entry point
server = app.server


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
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
    else:
        return '404: Page Not Found'


if __name__ == '__main__':
    # Development server
    app.run_server(debug=True)
