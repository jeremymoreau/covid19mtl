import plotly.express as px
import plotly.graph_objects as go


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
                                   'gridcolor': '#f5f5f5'
                               }
                         }]),
                    dict(label=labels['log_label'],
                         method='update',
                         args=[{'visible': [True, True]},
                               {'yaxis': {
                                   'type': 'log',
                                   'nticks': nticks_log,
                                   'gridcolor': '#f5f5f5'
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


def mtl_cases_map_fig(cases_per1000_long, mtl_geojson, labels):
    # get max cases value
    cases_max_val = cases_per1000_long['cases_per_1000'].max()
    # Montreal cases per 1000 map
    mtlmap_fig = px.choropleth_mapbox(
        cases_per1000_long, geojson=mtl_geojson,
        locations='borough', color='cases_per_1000',
        featureidkey='properties.borough',
        animation_frame='date', animation_group='borough',
        mapbox_style='carto-positron', range_color=[0, cases_max_val],
        zoom=9, center={'lat': 45.55, 'lon': -73.75},
        labels=labels['montreal_map_colourbar_labels']
    )

    # set the default frame to the latest date
    mtlmap_fig.layout.sliders[0]['active'] = len(mtlmap_fig.frames) - 1  # slider
    mtlmap_fig.update_traces(z=mtlmap_fig.frames[-1].data[0].z)  # frame

    mtlmap_fig.layout.sliders[0]['currentvalue']['prefix'] = labels['date_slider_label']
    mtlmap_fig.layout.sliders[0]['xanchor'] = 'left'
    mtlmap_fig.layout.sliders[0]['pad'] = {'b': 10, 't': 0, 'l': 50}
    mtlmap_fig.layout.updatemenus[0]['xanchor'] = 'left'
    mtlmap_fig.layout.updatemenus[0]['x'] = 0
    mtlmap_fig.layout.updatemenus[0]['pad'] = {'r': 50, 't': 15}

    mtlmap_fig.update_layout({
        'margin': {'r': 0, 't': 0, 'l': 0, 'b': 0},
        'plot_bgcolor': 'rgba(255,255,255,1)',
        'paper_bgcolor': 'rgba(255,255,255,1)',
        'coloraxis': {
            'colorbar': {
                'thicknessmode': 'fraction',
                'thickness': 0.03,
                'lenmode': 'fraction',
                'len': 0.7,
                'title': {'text': ''}
            }
        }
    })
    # Update hoverlabel for all frames
    mtlmap_fig.update_traces({
        'hovertemplate': labels['montreal_map_hovertemplate']
    })
    for frame in mtlmap_fig.frames:
        frame['data'][0]['hovertemplate'] = labels['montreal_map_hovertemplate']

    return mtlmap_fig


def cases_fig(data_mtl, data_qc, labels):
    # Confirmed cases
    cases_fig = go.Figure({
        'data': [
            {
                'type': 'scatter',
                'x': data_qc['date'],
                'y': data_qc['cases'],
                'mode': 'lines+markers',
                'marker': {'color': '#001F97'},
                'name': labels['confirmed_cases_qc_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'x': data_qc['date'],
                'y': data_qc['active_cases'],
                'mode': 'lines',
                'marker': {'color': '#001F97'},
                'line': {'dash': 'dash'},
                'name': labels['active_cases_qc_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'x': data_mtl['date'],
                'y': data_mtl['cases'],
                'mode': 'lines+markers',
                'marker': {'color': '#D6142C'},
                'name': labels['confirmed_cases_mtl_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'x': data_qc['date'],
                'y': data_qc['new_cases'],
                'mode': 'lines',
                'marker': {'color': '#00104f'},
                'name': labels['new_confirmed_cases_qc_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'x': data_mtl['date'],
                'y': data_mtl['new_cases'],
                'mode': 'lines',
                'marker': {'color': '#780b18'},
                'name': labels['new_confirmed_cases_mtl_label'],
                'hoverlabel': {'namelength': 25},
            }

        ],
        'layout': {
            'autosize': True,
            'legend': {'bgcolor': 'rgba(255,255,255,0)', 'x': 0, 'y': 1},
            'xaxis': {'tickformat': '%m-%d', 'title': {'text': labels['date_label']}},
            'yaxis': {'title': {'text': labels['confirmed_cases_y_label']},
                      'gridcolor': '#f5f5f5'},
            'margin': {'r': 0, 't': 10, 'l': 60, 'b': 50},
            'plot_bgcolor': 'rgba(255,255,255,1)',
            'paper_bgcolor': 'rgba(255,255,255,1)',
            'hovermode': 'x',
            'dragmode': False
        }
    })
    cases_fig = add_ylog_menu(cases_fig, data_qc['cases'], labels)

    return cases_fig


def mtl_age_hist_fig(mtl_age_data, labels):
    # Age histogram
    mtl_age_data_copy = mtl_age_data.copy()
    mtl_age_data_copy['per100000'] = [
        labels['age_per100000_label']
        if '100000' in x else labels['age_total_label']
        for x in mtl_age_data['age_group']
    ]
    mtl_age_data_copy['age_group'] = [x.split('_')[2] for x in mtl_age_data_copy['age_group']]
    # Get max value
    max_count = max(mtl_age_data_copy['percent'])
    # Plot % in each age group
    age_fig = px.bar(
        mtl_age_data_copy, x='age_group', y='percent',
        color='per100000', animation_frame='date',
        range_y=[0, max_count + 0.25 * max_count], barmode='group'
    )
    age_fig.update_layout({
        'legend': {'bgcolor': 'rgba(255,255,255,1)', 'x': 0, 'y': 1, 'title': ''},
        'xaxis': {'title': {'text': labels['age_label']}},
        'yaxis': {'title': {'text': '%'}, 'gridcolor': '#f5f5f5'},
        'margin': {'r': 0, 't': 10, 'l': 0, 'b': 0},
        'plot_bgcolor': 'rgba(255,255,255,1)',
        'paper_bgcolor': 'rgba(255,255,255,1)',
        'hovermode': 'x',
        'hoverlabel': {'font': {'color': '#ffffff'}},
        'dragmode': False
    })

    # set the default frame to the latest date
    age_fig.layout.sliders[0]['active'] = len(age_fig.frames) - 1  # slider
    age_fig.update_traces(
        y=age_fig.frames[-1].data[0].y,
        selector=dict(marker_color='#636efa')
    )  # frame
    age_fig.update_traces(
        y=age_fig.frames[-1].data[1].y,
        selector=dict(marker_color='#EF553B')
    )  # frame

    age_fig.layout.sliders[0]['pad'] = {'r': 30, 'b': 10, 't': 65}
    age_fig.layout.sliders[0]['currentvalue']['prefix'] = labels['date_slider_label']
    age_fig.layout.updatemenus[0]['pad'] = {'r': 10, 't': 75}
    # Update hoverlabel for all frames
    age_fig.update_traces({
        'hovertemplate': labels['age_fig_hovertemplate']
    })
    for frame in age_fig.frames:
        frame['data'][0]['hovertemplate'] = labels['age_fig_hovertemplate']
        frame['data'][1]['hovertemplate'] = labels['age_fig_hovertemplate']

    return age_fig


def deaths_fig(data_mtl, data_qc, labels):
    # Deaths (QC)
    deaths_fig = go.Figure({
        'data': [
            {
                'type': 'scatter',
                'x': data_qc['date'],
                'y': data_qc['deaths'],
                'mode': 'lines+markers',
                'marker': {'color': '#001F97'},
                'name': labels['deaths_fig_qc_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'x': data_mtl['date'],
                'y': data_mtl['deaths'],
                'mode': 'lines+markers',
                'marker': {'color': '#D6142C'},
                'name': labels['deaths_fig_mtl_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'x': data_qc['date'],
                'y': data_qc['new_deaths'],
                'mode': 'lines',
                'marker': {'color': '#00104f'},
                'name': labels['new_deaths_qc_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'x': data_mtl['date'],
                'y': data_mtl['new_deaths'],
                'mode': 'lines',
                'marker': {'color': '#780b18'},
                'name': labels['new_deaths_mtl_label'],
                'hoverlabel': {'namelength': 25},
            }
        ],
        'layout': {
            'autosize': True,
            'legend': {'bgcolor': 'rgba(255,255,255,0)', 'x': 0, 'y': 1},
            'xaxis': {'tickformat': '%m-%d', 'title': {'text': labels['date_label']}},
            'yaxis': {
                'title': {'text': labels['deaths_qc_y_label']},
                'gridcolor': '#f5f5f5'
            },
            'margin': {'r': 0, 't': 10, 'l': 30, 'b': 50},
            'plot_bgcolor': 'rgba(255,255,255,1)',
            'paper_bgcolor': 'rgba(255,255,255,1)',
            'hovermode': 'x',
            'dragmode': False
        }
    })
    deaths_fig = add_ylog_menu(deaths_fig, data_qc['deaths'], labels)

    return deaths_fig


def qc_hospitalisations_fig(data_qc_hosp, labels):
    # Hospitalisations (QC)
    hospitalisations_qc_fig = go.Figure({
        'data': [
            {
                'type': 'scatter',
                'x': data_qc_hosp['date'],
                'y': data_qc_hosp['hospitalisations_all'],
                'mode': 'lines+markers',
                'marker': {'color': '#F87E3F'},
                'name': labels['hospitalisations_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'mode': 'lines+markers',
                'marker': {'color': '#0083CB'},
                'x': data_qc_hosp['date'],
                'y': data_qc_hosp['icu'],
                'name': labels['intensive_care_label'],
                'hoverlabel': {'namelength': 25},
            }
        ],
        'layout': {
            'autosize': True,
            'legend': {'bgcolor': 'rgba(255,255,255,0)', 'x': 0, 'y': 1},
            'xaxis': {'tickformat': '%m-%d', 'title': {'text': labels['date_label']}},
            'yaxis': {
                'title': {'text': labels['hospitalisations_y_label']},
                'gridcolor': '#f5f5f5'
            },
            'margin': {'r': 0, 't': 10, 'l': 30, 'b': 50},
            'plot_bgcolor': 'rgba(255,255,255,1)',
            'paper_bgcolor': 'rgba(255,255,255,1)',
            'hovermode': 'x',
            'hoverlabel': {'font': {'color': '#ffffff'}},
            'dragmode': False
        }
    })
    hospitalisations_qc_fig = add_ylog_menu(hospitalisations_qc_fig,
                                            data_qc_hosp['hospitalisations_all'], labels)

    return hospitalisations_qc_fig


def qc_testing_fig(data_qc, labels):
    # Testing (QC)
    testing_qc_fig = go.Figure({
        'data': [
            {
                'type': 'scatter',
                'x': data_qc['date'],
                'y': data_qc['negative_tests'],
                'mode': 'lines+markers',
                'marker': {'color': '#39b686'},
                'name': labels['negative_tests_qc_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'mode': 'lines+markers',
                'x': data_qc['date'],
                'y': data_qc['cases'],
                'marker': {'color': '#c51515'},
                'name': labels['positive_cases_qc_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'x': data_qc['date'],
                'y': data_qc['new_negative_tests'],
                'mode': 'lines',
                'marker': {'color': '#206e50'},
                'name': labels['new_negative_tests_qc_label'],
                'hoverlabel': {'namelength': 25},
            }
        ],
        'layout': {
            'autosize': True,
            'legend': {'bgcolor': 'rgba(255,255,255,0)', 'x': 0, 'y': 1},
            'xaxis': {'tickformat': '%m-%d', 'title': {'text': labels['date_label']}},
            'yaxis': {'title': {'text': labels['testing_qc_y_label']}, 'gridcolor': '#f5f5f5'},
            'margin': {'r': 0, 't': 10, 'l': 60, 'b': 50},
            'plot_bgcolor': 'rgba(255,255,255,1)',
            'paper_bgcolor': 'rgba(255,255,255,1)',
            'hovermode': 'x',
            'dragmode': False
        }
    })
    testing_qc_fig = add_ylog_menu(testing_qc_fig, data_qc['negative_tests'], labels)

    return testing_qc_fig


def mtl_deaths_loc_fig(data_mtl_death_loc, labels):
    # Confirmed deaths by place of residence (MTL)
    deaths_loc_mtl_fig = go.Figure({
        'data': [
            {
                'type': 'pie',
                'labels': labels['deaths_loc_fig_mtl_pie_labels'],
                'values': data_mtl_death_loc.iloc[-1, 1:-1].tolist(),  # only display latest day for now
                'marker': {
                    'colors': [
                        'rgb(213, 94, 0)', 'rgb(0, 114, 178)',
                        'rgb(0, 158, 115)', 'rgb(204, 121, 167)',
                        'rgb(240, 228, 66)', 'rgb(230, 159, 0)',
                        'rgb(0, 0, 0)'
                    ]
                },
            }
        ],
        'layout': {
            'autosize': True,
            'legend': {
                'orientation': 'h',
                'bgcolor': 'rgba(255,255,255,0)',
                'xanchor': 'left', 'x': -0.1, 'y': -0.05,
            },
            'plot_bgcolor': 'rgba(255,255,255,1)',
            'paper_bgcolor': 'rgba(255,255,255,1)',
            'margin': {'t': 10, 'r': 10, 'b': 10, 'l': 10},
            'dragmode': False,
        }
    })

    return deaths_loc_mtl_fig


def qc_deaths_loc_fig(data_qc, labels):
    # Confirmed deaths by place of residence (QC)
    deaths_loc_qc_fig = go.Figure({
        'data': [
            {
                'type': 'scatter',
                'x': data_qc['date'],
                'y': data_qc['deaths_chsld'],
                'mode': 'lines+markers',
                'marker': {'color': 'rgb(0, 114, 178)'},
                'name': labels['chsld_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'mode': 'lines+markers',
                'marker': {'color': 'rgb(240, 228, 66)'},
                'x': data_qc['date'],
                'y': data_qc['deaths_psr'],
                'name': labels['psr_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'mode': 'lines+markers',
                'marker': {'color': 'rgb(0, 158, 115)'},
                'x': data_qc['date'],
                'y': data_qc['deaths_home'],
                'name': labels['home_label'],
                'hoverlabel': {'namelength': 25},
            },
            {

                'type': 'scatter',
                'mode': 'lines+markers',
                'marker': {'color': 'rgb(230, 159, 0)'},
                'x': data_qc['date'],
                'y': data_qc['deaths_other'],
                'name': labels['other_or_unknown_label'],
                'hoverlabel': {'namelength': 25},
            }
        ],
        'layout': {
            'autosize': True,
            'legend': {'bgcolor': 'rgba(255,255,255,0)', 'x': 0, 'y': 1},
            'xaxis': {'tickformat': '%m-%d', 'title': {'text': labels['date_label']}},
            'yaxis': {
                'title': {'text': labels['deaths_loc_fig_qc_y_label']},
                'gridcolor': '#f5f5f5'
            },
            'margin': {'r': 0, 't': 10, 'l': 30, 'b': 50},
            'plot_bgcolor': 'rgba(255,255,255,1)',
            'paper_bgcolor': 'rgba(255,255,255,1)',
            'hovermode': 'x',
            'hoverlabel': {'font': {'color': '#ffffff'}},
            'dragmode': False
        }
    })
    deaths_loc_qc_fig = add_ylog_menu(deaths_loc_qc_fig, data_qc[
        'deaths_chsld'], labels)

    return deaths_loc_qc_fig
