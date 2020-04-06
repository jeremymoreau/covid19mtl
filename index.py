import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server
from apps import app_en, app_fr


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
    else:
        return '404: Page Not Found'

if __name__ == '__main__':
    app.run_server(debug=True)
