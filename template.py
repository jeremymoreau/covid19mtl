import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from app import (app, cases_per1000_long, data_mtl, data_qc, latest_cases_mtl,
                 latest_cases_qc, latest_deaths_mtl, latest_deaths_qc,
                 latest_hospitalisations_qc, latest_icu_qc,
                 latest_negative_tests_qc, latest_recovered_qc,
                 latest_update_date, mtl_age_data, mtl_geojson)


def add_ylog_menu(fig, y_data, labels):
    """Add a dropdown menu to select between log and linear scales
    
    Parameters
    ----------
    fig : plotly.graph_objs._figure.Figure
        Plotly line chart
    y_data : pandas.core.series.Series
        Pandas series containing the y axis data
    labels : dict
        Dict containing the labels to display in the dropdown
    
    Returns
    -------
    plotly.graph_objs._figure.Figure
        Plotly line chart including a dropdown menu at the bottom left
    """
    nticks_log = len(str(y_data.iloc[-1]))  # to hide minor tick labels
    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label=labels['linear_label'],
                         method='update',
                         args=[{'visible': [True, True]},
                               {'yaxis': {
                                            'type': 'linear',
                                            'gridcolor' : '#f5f5f5'
                                            }
                                }]),
                    dict(label=labels['log_label'],
                         method='update',
                         args=[{'visible': [True, True]},
                               {'yaxis': {
                                            'type': 'log', 
                                            'nticks': nticks_log,
                                            'gridcolor' : '#f5f5f5'
                                            }
                                }]),
                ]),
                direction='up',
                pad={'t': 5, 'b': 5, 'r': 5},
                x=0,
                xanchor='left',
                y=-0.125,
                yanchor='top'
            )
        ])
    return fig


def generate_layout(labels):
    ##### Figures #####
    # get max cases value
    cases_max_val = cases_per1000_long['cases_per_1000'].max()
    # Montreal cases per 1000 map
    mtlmap_fig = px.choropleth(cases_per1000_long, geojson=mtl_geojson, locations='borough', color='cases_per_1000',
                        featureidkey="properties.borough", animation_frame='date', range_color=[0, cases_max_val],
                        projection="winkel tripel", labels=labels['montreal_map_colourbar_labels'])
    mtlmap_fig.update_geos(fitbounds="locations", visible=False)
    mtlmap_fig.layout.sliders[0]['pad'] = {'b': 10, 't': 0}
    mtlmap_fig.layout.sliders[0]['currentvalue']['prefix'] = labels['date_slider_label']
    mtlmap_fig.layout.updatemenus[0]['pad'] = {'r': 10, 't': 10}
    mtlmap_fig.update_layout({
        'margin': {"r":0,"t":0,"l":0,"b":0},
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'coloraxis' : {'colorbar': {
                            'thicknessmode': 'fraction',
                            'thickness': 0.03,
                            'lenmode': 'fraction',
                            'len': 0.7,
                            'title': {'text': ''}
                            }
                        }
        })
    mtlmap_fig.update_traces({
        'hovertemplate': labels['montreal_map_hovertemplate']
        })


    # Confirmed cases
    cases_fig = go.Figure({
        'data' : [
            {
                'type': 'scatter',
                'x' : data_qc['date'],
                'y' : data_qc['cases_qc'],
                'mode': 'lines+markers',
                'marker': {'color': '#001F97'},
                'name': labels['confirmed_cases_qc_label'],
            },
            {
                'type': 'scatter',
                'x' : data_mtl['date'],
                'y' : data_mtl['cases_mtl'],
                'mode': 'lines+markers',
                'marker': {'color': '#D6142C'},
                'name': labels['confirmed_cases_mtl_label'],
            }
        ],
        'layout': {
            'autosize': True,
            'legend': {'bgcolor': 'rgba(0,0,0,0)', 'x': 0, 'y': 1},
            'xaxis': {'tickformat': '%m-%d', 'title': {'text': labels['date_label']}},
            'yaxis': {'title': {'text': labels['confirmed_cases_y_label']}, 'gridcolor' : '#f5f5f5'},
            'margin': {"r":0,"t":10,"l":60,"b":50},
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'hovermode': 'x'
        }
    })
    cases_fig = add_ylog_menu(cases_fig, data_qc['cases_qc'], labels)

    # Age histogram
    mtl_age_data_copy = mtl_age_data.copy()
    mtl_age_data_copy['per100000'] = [labels['age_per100000_label'] if '100000' in x else labels['age_total_label'] for x in mtl_age_data['age_group']]
    mtl_age_data_copy['age_group'] = [x.split('_')[2] for x in mtl_age_data_copy['age_group']]
    # Get max value
    max_count = max(mtl_age_data_copy['percent'])
    # Plot % in each age group
    age_fig = px.bar(mtl_age_data_copy, x='age_group', y='percent', color='per100000', animation_frame='date',
                range_y=[0, max_count + 0.25*max_count], barmode='group')
    age_fig.update_layout({
        'legend' : {'bgcolor': 'rgba(0,0,0,0)', 'x': 0, 'y': 1, 'title' : ''},
        'xaxis' : {'title': {'text': labels['age_label']}},
        'yaxis' : {'title': {'text': '%'}, 'gridcolor' : '#f5f5f5'},
        'margin': {"r":0,"t":10,"l":0,"b":0},
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'hovermode': 'x',
        'hoverlabel' : {'font' : {'color' : '#ffffff'}}
    })
    age_fig.layout.sliders[0]['pad'] = {'r': 30, 'b': 10, 't': 65}
    age_fig.layout.sliders[0]['currentvalue']['prefix'] = labels['date_slider_label']
    age_fig.layout.updatemenus[0]['pad'] = {'r': 10, 't': 75}
    age_fig.update_traces({
        'hovertemplate': labels['age_fig_hovertemplate']
        })

    # Deaths (QC)
    deaths_qc_fig = go.Figure({
        'data' : [
            {
                'type': 'scatter',
                'x' : data_qc['date'],
                'y' : data_qc['deaths_qc'],
                'mode': 'lines+markers',
                'marker': {'color': '#001F97'},
                'name': labels['deaths_qc_label'],
            },
            {
                'type': 'scatter',
                'x' : data_mtl['date'],
                'y' : data_mtl['deaths_mtl'],
                'mode': 'lines+markers',
                'marker': {'color': '#D6142C'},
                'name': labels['deaths_montreal_label'],
            }
        ],
        'layout': {
            'autosize': True,
            'legend': {'bgcolor': 'rgba(0,0,0,0)', 'x': 0, 'y': 1},
            'xaxis': {'tickformat': '%m-%d', 'title': {'text': labels['date_label']}},
            'yaxis': {'title': {'text': labels['deaths_qc_y_label']}, 'gridcolor' : '#f5f5f5'},
            'margin': {"r":0,"t":10,"l":30,"b":50},
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'hovermode': 'x'
        }
    })
    deaths_qc_fig = add_ylog_menu(deaths_qc_fig, data_qc['deaths_qc'], labels)

    # Hospitalisations (QC)
    hospitalisations_qc_fig = go.Figure({
        'data' : [
            {
                'type': 'scatter',
                'x' : data_qc['date'],
                'y' : data_qc['hospitalisations_qc'],
                'mode': 'lines+markers',
                'marker': {'color': '#F87E3F'},
                'name': labels['hospitalisations_label'],
            },
            {
                'type': 'scatter',
                'mode': 'lines+markers',
                'marker': {'color': '#0083CB'},
                'x' : data_qc['date'],
                'y' : data_qc['icu_qc'],
                'name': labels['intensive_care_label'],
            }
        ],
        'layout': {
            'autosize': True,
            'legend': {'bgcolor': 'rgba(0,0,0,0)', 'x': 0, 'y': 1},
            'xaxis': {'tickformat': '%m-%d', 'title': {'text': labels['date_label']}},
            'yaxis': {'title': {'text': labels['hospitalisations_y_label']}, 'gridcolor' : '#f5f5f5'},
            'margin': {"r":0,"t":10,"l":30,"b":50},
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'hovermode': 'x',
            'hoverlabel' : {'font' : {'color' : '#ffffff'}}
        }
    })
    hospitalisations_qc_fig = add_ylog_menu(hospitalisations_qc_fig, data_qc['hospitalisations_qc'], labels)

    # Testing (QC)
    testing_qc_fig = go.Figure({
        'data' : [
            {
                'type': 'scatter',
                'x' : data_qc['date'],
                'y' : data_qc['negative_tests_qc'],
                'mode': 'lines+markers',
                'marker': {'color': '#39b686'},
                'name': labels['negative_tests_qc_label'],
            },
            {
                'type': 'scatter',
                'mode': 'lines+markers',
                'x' : data_qc['date'],
                'y' : data_qc['cases_qc'],
                'marker': {'color': '#c51515'},
                'name': labels['positive_cases_qc_label'],
            }
        ],
        'layout': {
        'autosize': True,
        'legend': {'bgcolor': 'rgba(0,0,0,0)', 'x': 0, 'y': 1},
        'xaxis': {'tickformat': '%m-%d', 'title': {'text': labels['date_label']}},
        'yaxis': {'title': {'text': labels['testing_qc_y_label']}, 'gridcolor' : '#f5f5f5'},
        'margin': {"r":0,"t":10,"l":60,"b":50},
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'hovermode': 'x',
        }
    })
    testing_qc_fig = add_ylog_menu(testing_qc_fig, data_qc['negative_tests_qc'], labels)

    # modebar buttons to remove
    modebar_buttons_to_remove = ['select2d',
                                'lasso2d',
                                'autoScale2d',
                                'hoverCompareCartesian',
                                'hoverClosestCartesian',
                                'toggleSpikelines'
                                ]

    ##### App layout #####
    layout = html.Div(
        [
            dcc.Store(id="aggregate_data"),
            # empty Div to trigger javascript file for graph resizing
            html.Div(id="output-clientside"),
            # language select
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    # Load in a new tab because some figures do not resize properly otherwise
                                    # TODO: Fix this bug
                                    html.A([labels['language0']], href=labels['language_link0'], target='_blank', className='lang_link'),
                                    html.A([labels['language1']], href=labels['language_link1'], target='_blank', className='lang_link'),
                                ],
                                id="language_select_link"
                            )
                        ],
                        className="twelve column",
                        id="language_select",
                    ),
                        ],
                id="language_select_header",
                className="row flex-display",
            ),
            html.Div(
                [
                    # title
                    html.Div(
                        [
                            html.Div(
                                [   
                                    # title
                                    html.H3(
                                        [labels['title']],
                                        id="title_text",
                                        style={"margin-bottom": "0px"},
                                        ),
                                    #subtitle
                                    html.H6(
                                        [labels['subtitle']],
                                        id="last_update_text",
                                    ),
                                ]
                            )
                        ],
                        className="twelve column",
                        id="title",
                    ),
                ],
                id="header",
                className="row flex-display",
            ),
            html.Div(
                [

                    html.Div(
                        [
                            html.Div(
                                [html.H3(latest_cases_mtl, id="cases_mtl_text"), html.P([labels['cases_montreal_label']], id='cases_montreal_label')],
                                id="cases_mtl",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H3(latest_deaths_mtl, id="deaths_mtl_text"), html.P([labels['deaths_montreal_label']], id='deaths_montreal_label')],
                                id="deaths_mtl",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H3(latest_cases_qc, id="cases_qc_text"), html.P([labels['cases_qc_label']], id='cases_qc_label')],
                                id="cases_qc",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H3(latest_deaths_qc, id="deaths_qc_text"), html.P([labels['deaths_qc_label']], id='deaths_qc_label')],
                                id="deaths_qc",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H3(latest_hospitalisations_qc, id="hospitalisations_qc_text"), html.P([labels['hospitalisations_label']], id='hospitalisations_qc_label')],
                                id="hospitalisations_qc",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H3(latest_icu_qc, id="icu_qc_text"), html.P([labels['intensive_care_label']], id='icu_qc_label')],
                                id="icu_qc",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H3(latest_recovered_qc, id="recovered_qc_text"), html.P([labels['recovered_qc_label']], id='recovered_qc_label')],
                                id="recovered_qc",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H3(latest_negative_tests_qc, id="negative_tests_qc_text"), html.P([labels['negative_tests_qc_label']], id='negative_tests_qc_label')],
                                id="negative_tests_qc",
                                className="mini_container",
                            ),
                        ],
                        id="info-container",
                        className="row",
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    # infobox
                    html.Div(
                        [
                            dcc.Markdown([labels['infobox']], id='infobox_text')
                        ],
                        className="pretty_container four columns",
                        id="infobox_container",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div([

                                        html.Div([
                                            html.H6([labels['montreal_map_label']], id='montreal_map_label')
                                        ]),
                                        dcc.Graph(
                                            figure=mtlmap_fig,
                                            id='montreal_map',
                                            config={
                                                'modeBarButtonsToRemove': [
                                                    'select2d',
                                                    'lasso2d',
                                                    'hoverClosestGeo',
                                                    ],
                                                }
                                            ),

                                    ]),
                                ],
                                id="countGraphContainer",
                                className="pretty_container",
                            ),
                        ],
                        id="right-column",
                        className="eight columns",
                    ),
                ],
                className="row flex-display",
            ),
            # middle 2 boxes
            html.Div(
                [
                    # left box
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div([
                                        html.H6([labels['total_cases_label']], id='total_cases_label'),
                                    ]),
                                    dcc.Graph(
                                        figure=cases_fig,
                                        id='confirmed_cases_fig',
                                        responsive=True,
                                        config={
                                            'modeBarButtonsToRemove': modebar_buttons_to_remove,
                                            }
                                        ),
                                ],
                                id="total_cases_box",
                                className="pretty_container",
                            ),
                        ],
                        id="total_cases_col",
                        className="six columns",
                    ),
                    # right box
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6([labels['age_group_label']], id='age_group'),
                                    dcc.Graph(
                                        figure=age_fig,
                                        id='age_fig_mtl',
                                        responsive=True,
                                        config={
                                            'modeBarButtonsToRemove': modebar_buttons_to_remove,
                                            }
                                        ),
                                ],
                                id="age_group_box",
                                className="pretty_container",
                            ),
                        ],
                        className="six columns",
                    ),
                ],
                className="row flex-display",
            ),
            # bottom 3 boxes
            html.Div(
                [
                    # left box
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6([labels['deaths_fig_label']], id='total_deaths'),
                                    dcc.Graph(
                                            figure=deaths_qc_fig,
                                            id='deaths_fig_qc',
                                            responsive=True,
                                        config={
                                            'modeBarButtonsToRemove': modebar_buttons_to_remove,
                                            }
                                        ),
                                ],
                                id="total_deaths_box",
                                className="pretty_container",
                            ),
                        ],
                        className="four columns",
                        id="total_deaths_col",
                    ),
                    # middle box
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6([labels['total_hospitalisations_label']], id='total_hospitalisations'),
                                    dcc.Graph(
                                        figure=hospitalisations_qc_fig,
                                        id='hospitalisations_fig_qc',
                                        responsive=True,
                                    config={
                                        'modeBarButtonsToRemove': modebar_buttons_to_remove,
                                        }
                                        ),
                                ],
                                id="total_hospitalisations_box",
                                className="pretty_container",
                            ),
                        ],
                        className="four columns",
                        id="total_hospitalisations_col",
                    ),
                    # left
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6([labels['total_testing_label']], id='total_testing'),
                                    dcc.Graph(
                                        figure=testing_qc_fig,
                                        id='testing_fig_qc',
                                        responsive=True,
                                        config={
                                            'modeBarButtonsToRemove': modebar_buttons_to_remove,
                                            }
                                        ),
                                ],
                                id="total_testing_box",
                                className="pretty_container",
                            ),
                        ],
                        className="four columns",
                        id="total_testing_col",
                    ),
                ],
                className="row flex-display third-row",
            ),

            # footer
            html.Div([
                html.Div([
                    dcc.Markdown([labels['footer_left']], id="footer_left_text"),
                ],
                id="footer_left",
                className="six column"
                ),
                html.Div([
                    dcc.Markdown([labels['footer_right']], id="footer_right_text"),
                ],
                id="footer_right",
                className="six column"
                )
            ],
            id="footer",
            className="row flex-display",
            )

        ],
        id="mainContainer",
        style={"display": "flex", "flex-direction": "column"},
    )
    return layout
