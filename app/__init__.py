import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask, request
from flask_babel import Babel

from .template import create_layout

# Regular Flask config
flapp = Flask(__name__)
babel = Babel(flapp, default_locale='fr', configure_jinja=False)
# XXX investigate if translations are reloaded every request

languages = {'en', 'es', 'zh'}
default_language = 'fr'


@babel.localeselector
def get_locale():
    referrer_url = request.headers.get('Referer', '/')
    code = referrer_url.rpartition('/')[-1]

    if code in languages:
        return code
    else:
        return default_language


# Dash-specific config
app = dash.Dash(__name__, server=flapp, meta_tags=[
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
page_layout = create_layout()


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    return page_layout
