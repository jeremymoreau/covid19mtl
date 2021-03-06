import plotly.express as px
import plotly.graph_objects as go


def add_fig_controls(fig, y_data, labels):
    """Add a dropdown menu to select between log and linear scales and range sliders/buttons

    Parameters
    ----------
    fig : plotly.graph_objs._figure.Figure
        Plotly line chart
    y_data : pandas.core.series.Series
        Pandas series containing the y axis data
    labels : dict
        Dict containing the labels to display in the dropdown and the range buttons

    Returns
    -------
    plotly.graph_objs._figure.Figure
        Plotly line chart including a linear/log dropdown and range slider/buttons
    """
    nticks_log = len(str(y_data.iloc[-1]))  # to hide minor tick labels
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=14,
                         label=labels['14d'],
                         step='day',
                         stepmode='backward'),
                    dict(count=1,
                         label=labels['1m'],
                         step='month',
                         stepmode='backward'),
                    dict(count=3,
                         label=labels['3m'],
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label=labels['6m'],
                         step='month',
                         stepmode='backward'),
                    dict(count=1,
                         label=labels['ytd'],
                         step='year',
                         stepmode='todate'),
                    dict(count=1,
                         label=labels['1y'],
                         step='year',
                         stepmode='backward'),
                    dict(label=labels['all'],
                         step='all')
                ]),
                yanchor='top',
                y=1.15,
                xanchor='left',
                x=-0.15,
            ),
            rangeslider=dict(
                visible=True
            ),
            type='date'
        ),
        legend=dict(
            yanchor='top',
            y=1.10,
            xanchor='left',
            x=0.01
        ),
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label=labels['linear_label'],
                         method='update',
                         args=[{'visible': [True, True]},
                               {'yaxis': {
                                   'type': 'linear',
                                   'gridcolor': '#f5f5f5',
                                   'title': str(fig.layout.yaxis.title.text)
                               }
                         }]),
                    dict(label=labels['log_label'],
                         method='update',
                         args=[{'visible': [True, True]},
                               {'yaxis': {
                                   'type': 'log',
                                   'nticks': nticks_log,
                                   'gridcolor': '#f5f5f5',
                                   'title': str(fig.layout.yaxis.title.text)
                               }
                         }]),
                ]),
                direction='up',
                pad={'t': 5, 'b': 5, 'r': 5},
                x=0,
                xanchor='left',
                y=-0.39,
                yanchor='bottom'
            )
        ])
    fig.update_xaxes(rangeslider_thickness=0.05)
    return fig


def mtl_cases_map_fig(mtl_boroughs, mtl_geojson, labels):
    # Add all available categories to each date
    # see: https://medium.com/@mahshadn/animated-choropleth-map-with-discrete-colors-using-python-and-plotly-styling-5e208e5b6bf8  # noqa: E501
    category = mtl_boroughs['7day_incidence_rate'].unique()
    dates = mtl_boroughs['date'].unique()
    for date in dates:
        for i in category:
            mtl_boroughs = mtl_boroughs.append({
                'date': date,
                '7day_incidence_rate': i
            }, ignore_index=True)

    # sort backwards as a workaround to show latest date first
    mtl_boroughs = mtl_boroughs.sort_values('date', ascending=False)

    # Montreal cases per 100k map
    mtlmap_fig = px.choropleth_mapbox(
        mtl_boroughs,
        geojson=mtl_geojson,
        locations='borough',
        color='7day_incidence_rate',
        featureidkey='properties.borough',
        animation_frame='date',
        animation_group='borough',
        mapbox_style='carto-positron',
        color_discrete_map={
            '< 10': '#7ea47c',
            '> 10-25': '#ecd93b',
            '> 25-50': '#dfae5a',
            '> 50-100': '#df825a',
            '> 100-200': '#CC0101',
            '> 200-300': '#A80101',
            '> 300-500': '#800000',
            '> 500': '#600000',
        },
        category_orders={
            '7day_incidence_rate': [
                '> 500',
                '> 300-500',
                '> 200-300',
                '> 100-200',
                '> 50-100',
                '> 25-50',
                '> 10-25',
                '< 10',
            ]
        },
        zoom=9,
        center={'lat': 45.55, 'lon': -73.75},
        labels=labels['montreal_map_colourbar_labels'],
        hover_name='borough',
        hover_data={
            '7day_incidence': True,
            '7day_incidence_per100k': True,
            '7day_incidence_rate': False,
            'borough': False,
            'cases': True,
            'date': True,
            'new_cases': True,
        }
    )

    mtlmap_fig.update_layout(
        showlegend=True,
        legend_title_text=labels['montreal_map_legend_title'],
        legend={'yanchor': 'top', 'y': 0.99, 'xanchor': 'left', 'x': 0.01, 'bgcolor': 'rgba(0,0,0,0)'},
        margin={'r': 0, 't': 0, 'l': 0, 'b': 0},
        plot_bgcolor='rgba(255,255,255,1)',
        paper_bgcolor='rgba(255,255,255,1)',
    )

    # # set the default frame to the latest date
    # mtlmap_fig.layout.sliders[0]['active'] = len(mtlmap_fig.frames) - 1  # slider
    # mtlmap_fig.update_traces(z=mtlmap_fig.frames[-1].data[0].z)  # frame

    mtlmap_fig.layout.sliders[0]['currentvalue']['prefix'] = labels['date_slider_label']
    mtlmap_fig.layout.sliders[0]['xanchor'] = 'left'
    mtlmap_fig.layout.sliders[0]['pad'] = {'b': 10, 't': 0, 'l': 50}
    mtlmap_fig.layout.updatemenus[0]['xanchor'] = 'left'
    mtlmap_fig.layout.updatemenus[0]['x'] = 0
    mtlmap_fig.layout.updatemenus[0]['pad'] = {'r': 50, 't': 15}

    # Update hoverlabel for all frames
    # mtlmap_fig.update_traces({
    #     'hovertemplate': labels['montreal_map_hovertemplate']
    # })
    # for frame in mtlmap_fig.frames:
    #     frame['data'][0]['hovertemplate'] = labels['montreal_map_hovertemplate']

    return mtlmap_fig


def cases_fig(data_mtl, data_qc, labels):
    # Confirmed cases
    cases_fig = go.Figure({
        'data': [
            {
                'type': 'scatter',
                'x': data_qc['date'],
                'y': data_qc['cases'],
                'mode': 'lines',
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
                'mode': 'lines',
                'marker': {'color': '#D6142C'},
                'name': labels['confirmed_cases_mtl_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'x': data_qc['date'],
                'y': data_qc['new_cases'].rolling(7).mean().round(),
                'yaxis': 'y2',
                'mode': 'lines',
                'marker': {'color': '#1bd1c2'},
                'line': {'dash': 'dot'},
                'name': labels['new_confirmed_cases_qc_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'x': data_mtl['date'],
                'y': data_mtl['new_cases'].rolling(7).mean().round(),
                'yaxis': 'y2',
                'mode': 'lines',
                'marker': {'color': '#f7289d'},
                'line': {'dash': 'dot'},
                'name': labels['new_confirmed_cases_mtl_label'],
                'hoverlabel': {'namelength': 25},
            }

        ],
        'layout': {
            'autosize': True,
            'legend': {'bgcolor': 'rgba(255,255,255,0)', 'x': 0, 'y': 1},
            'xaxis': {'tickformat': '%m-%d', 'title': {'text': labels['date_label']}},
            'yaxis': {
                'title': {'text': labels['confirmed_cases_y_label']},
                'gridcolor': '#f5f5f5',
                'rangemode': 'tozero',
            },
            'yaxis2': {
                'title': {'text': labels['confirmed_cases_y2_label']},
                'overlaying': 'y',
                'rangemode': 'tozero',
                'side': 'right'
            },
            'margin': {'r': 0, 't': 10, 'l': 60, 'b': 50},
            'plot_bgcolor': 'rgba(255,255,255,1)',
            'paper_bgcolor': 'rgba(255,255,255,1)',
            'hovermode': 'x',
            'dragmode': False
        }
    })
    cases_fig = add_fig_controls(cases_fig, data_qc['cases'], labels)

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
                'mode': 'lines',
                'marker': {'color': '#001F97'},
                'name': labels['deaths_fig_qc_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'x': data_mtl['date'],
                'y': data_mtl['deaths'],
                'mode': 'lines',
                'marker': {'color': '#D6142C'},
                'name': labels['deaths_fig_mtl_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'x': data_qc['date'],
                'y': data_qc['new_deaths'].rolling(7).mean().round(),
                'yaxis': 'y2',
                'mode': 'lines',
                'marker': {'color': '#1bd1c2'},
                'line': {'dash': 'dot'},
                'name': labels['new_deaths_qc_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'x': data_mtl['date'],
                'y': data_mtl['new_deaths'].rolling(7).mean().round(),
                'yaxis': 'y2',
                'mode': 'lines',
                'marker': {'color': '#f7289d'},
                'line': {'dash': 'dot'},
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
                'gridcolor': '#f5f5f5',
                'rangemode': 'tozero'
            },
            'yaxis2': {
                'title': {'text': labels['deaths_qc_y2_label']},
                'overlaying': 'y',
                'rangemode': 'tozero',
                'side': 'right'
            },
            'margin': {'r': 0, 't': 10, 'l': 30, 'b': 50},
            'plot_bgcolor': 'rgba(255,255,255,1)',
            'paper_bgcolor': 'rgba(255,255,255,1)',
            'hovermode': 'x',
            'dragmode': False
        }
    })
    deaths_fig = add_fig_controls(deaths_fig, data_qc['deaths'], labels)

    return deaths_fig


def hospitalisations_fig(data_qc_hosp, data_qc, data_mtl, labels):
    # Hospitalisations (QC)
    hospitalisations_fig = go.Figure({
        'data': [
            {
                'type': 'bar',
                'x': data_qc_hosp['date'],
                'y': data_qc_hosp['hospitalisations_all'],
                'yaxis': 'y1',
                'marker': {'color': '#5c6dad', 'opacity': 0.3},
                'name': labels['hospitalisations_active_qc'],
                'hoverlabel': {'namelength': 35},
            },
            {
                'type': 'bar',
                'x': data_qc_hosp['date'],
                'y': data_qc_hosp['icu'],
                'yaxis': 'y1',
                'marker': {'color': '#158c17', 'opacity': 0.5},
                'name': labels['intensive_care_active_qc'],
                'hoverlabel': {'namelength': 35},
            },
            {
                'type': 'scatter',
                'x': data_qc['date'],
                # drop the last date since numbers are delayed by a day
                'y': data_qc['hos_quo_tot_n'].iloc[:-1].rolling(7).mean().round(),
                'yaxis': 'y2',
                'mode': 'lines',
                'marker': {'color': '#001F97'},
                'line': {'dash': 'dot'},
                'name': labels['hospitalisations_qc'],
                'hoverlabel': {'namelength': 35},
            },
            {
                'type': 'scatter',
                'mode': 'lines',
                'marker': {'color': '#1bd1c2'},
                'line': {'dash': 'dot'},
                'x': data_qc['date'],
                # drop the last date since numbers are delayed by a day
                'y': data_qc['hos_quo_si_n'].iloc[:-1].rolling(7).mean().round(),
                'yaxis': 'y2',
                'name': labels['intensive_care_qc'],
                'hoverlabel': {'namelength': 35},
            },
            {
                'type': 'scatter',
                'x': data_mtl['date'],
                # drop the last date since numbers are delayed by a day
                'y': data_mtl['hos_quo_tot_n'].iloc[:-1].rolling(7).mean().round(),
                'yaxis': 'y2',
                'mode': 'lines',
                'marker': {'color': '#D6142C'},
                'line': {'dash': 'dot'},
                'name': labels['hospitalisations_mtl'],
                'hoverlabel': {'namelength': 35},
            },
            {
                'type': 'scatter',
                'mode': 'lines',
                'marker': {'color': '#f7289d'},
                'line': {'dash': 'dot'},
                'x': data_mtl['date'],
                # drop the last date since numbers are delayed by a day
                'y': data_mtl['hos_quo_si_n'].iloc[:-1].rolling(7).mean().round(),
                'yaxis': 'y2',
                'name': labels['intensive_care_mtl'],
                'hoverlabel': {'namelength': 35},
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
            'yaxis2': {
                'title': {'text': labels['hospitalisations_y2_label']},
                'overlaying': 'y',
                'rangemode': 'tozero',
                'side': 'right'

            },
            'margin': {'r': 0, 't': 10, 'l': 30, 'b': 50},
            'plot_bgcolor': 'rgba(255,255,255,1)',
            'paper_bgcolor': 'rgba(255,255,255,1)',
            'hovermode': 'x',
            'barmode': 'overlay',
            'hoverlabel': {'font': {'color': '#ffffff'}},
            'dragmode': False
        }
    })
    hospitalisations_fig = add_fig_controls(hospitalisations_fig,
                                         data_qc['hos_quo_reg_n'], labels)

    return hospitalisations_fig


def testing_fig(data_qc, data_mtl, labels):
    # reduce dfs by NaNs in 'psi_quo_pos_t' column assuring equal lengths of x/y lists
    data_mtl = data_mtl.dropna(subset=['psi_quo_pos_t'])
    data_qc = data_qc.dropna(subset=['psi_quo_pos_t'])

    # Testing (QC)
    testing_fig = go.Figure({
        'data': [
            {
                'type': 'scatter',
                'x': data_qc['date'],
                # divide by 100 because '%' tickformat is x100
                'y': data_qc['psi_quo_pos_t'].rolling(7).mean() / 100,
                'mode': 'lines',
                'marker': {'color': '#001F97'},
                'name': labels['testing_qc'],
                'hoverlabel': {'namelength': 25},
                'hovertemplate': '%{y:,.1%}'
            },
            {
                'type': 'scatter',
                'x': data_mtl['date'],
                # divide by 100 because '%' tickformat is x100
                'y': data_mtl['psi_quo_pos_t'].rolling(7).mean() / 100,
                'mode': 'lines',
                'marker': {'color': '#D6142C'},
                'name': labels['testing_mtl'],
                'hoverlabel': {'namelength': 25},
                'hovertemplate': '%{y:,.1%}'
            },
        ],
        'layout': {
            'autosize': True,
            'legend': {'bgcolor': 'rgba(255,255,255,0)', 'x': 0, 'y': 1},
            'xaxis': {'tickformat': '%m-%d', 'title': {'text': labels['date_label']}},
            'yaxis': {'title': {'text': labels['testing_y_label']}, 'gridcolor': '#f5f5f5', 'tickformat': ',.0%'},
            'margin': {'r': 0, 't': 10, 'l': 60, 'b': 50},
            'plot_bgcolor': 'rgba(255,255,255,1)',
            'paper_bgcolor': 'rgba(255,255,255,1)',
            'hovermode': 'x',
            'dragmode': False
        }
    })
    testing_fig = add_fig_controls(testing_fig, data_qc['negative_tests'], labels)

    return testing_fig


def vaccination_fig(data_vaccination, labels):
    vaccination_fig = go.Figure({
        'data': [
            {
                'type': 'scatter',
                'x': data_vaccination['date'],
                'y': data_vaccination['qc_percent_vaccinated'],
                'customdata': data_vaccination['qc_doses'],
                'yaxis': 'y1',
                'mode': 'lines',
                'marker': {'color': '#001F97'},
                'name': labels['vaccination_perc_qc'],
                'hoverlabel': {'namelength': 0},
                'hovertemplate': labels['vaccination_hovertemplate']
            },
            {
                'type': 'scatter',
                'x': data_vaccination['date'],
                'y': data_vaccination['mtl_percent_vaccinated'],
                'customdata': data_vaccination['mtl_doses'],
                'yaxis': 'y1',
                'mode': 'lines',
                'marker': {'color': '#D6142C'},
                'name': labels['vaccination_perc_mtl'],
                'hoverlabel': {'namelength': 0},
                'hovertemplate': labels['vaccination_hovertemplate']
            },
            {
                'type': 'scatter',
                'x': data_vaccination['date'],
                'y': data_vaccination['qc_new_doses'],
                'yaxis': 'y2',
                'mode': 'lines',
                'line': {'dash': 'dot'},
                'marker': {'color': '#1bd1c2'},
                'name': labels['vaccination_new_qc'],
                'hoverlabel': {'namelength': 35},
            },
            {
                'type': 'scatter',
                'x': data_vaccination['date'],
                'y': data_vaccination['mtl_new_doses'],
                'yaxis': 'y2',
                'mode': 'lines',
                'line': {'dash': 'dot'},
                'marker': {'color': '#f7289d'},
                'name': labels['vaccination_new_mtl'],
                'hoverlabel': {'namelength': 35},
            },
        ],
        'layout': {
            'autosize': True,
            'legend': {'bgcolor': 'rgba(255,255,255,0)', 'x': 0, 'y': 1},
            'xaxis': {'tickformat': '%m-%d', 'title': {'text': labels['date_label']}},
            'yaxis': {
                'title': {'text': labels['vaccination_y']},
                'gridcolor': '#f5f5f5'
            },
            'yaxis2': {
                'title': {'text': labels['vaccination_y2']},
                'overlaying': 'y',
                'rangemode': 'tozero',
                'side': 'right'

            },
            'margin': {'r': 0, 't': 10, 'l': 30, 'b': 50},
            'plot_bgcolor': 'rgba(255,255,255,1)',
            'paper_bgcolor': 'rgba(255,255,255,1)',
            'hovermode': 'x',
            'barmode': 'overlay',
            'hoverlabel': {'font': {'color': '#ffffff'}},
            'dragmode': False
        }
    })
    vaccination_fig = add_fig_controls(vaccination_fig, data_vaccination['qc_percent_vaccinated'], labels)

    return vaccination_fig


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
                'mode': 'lines',
                'marker': {'color': 'rgb(0, 114, 178)'},
                'name': labels['chsld_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'mode': 'lines',
                'marker': {'color': 'rgb(240, 228, 66)'},
                'x': data_qc['date'],
                'y': data_qc['deaths_psr'],
                'name': labels['psr_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'mode': 'lines',
                'marker': {'color': 'rgb(0, 158, 115)'},
                'x': data_qc['date'],
                'y': data_qc['deaths_home'],
                'name': labels['home_label'],
                'hoverlabel': {'namelength': 25},
            },
            {

                'type': 'scatter',
                'mode': 'lines',
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
    deaths_loc_qc_fig = add_fig_controls(deaths_loc_qc_fig, data_qc[
        'deaths_chsld'], labels)

    return deaths_loc_qc_fig


def cases_vs_newcases_fig(data_mtl, data_qc, labels):
    cases_vs_newcases_fig = go.Figure({
        'data': [

            {
                'type': 'scatter',
                'x': data_mtl['cases'],
                'y': data_mtl['new_cases'].rolling(7).mean().round(),
                'customdata': data_mtl['date'],
                'mode': 'lines',
                'name': labels['cases_vs_newcases_legend_mtl'],
                'marker': {'color': '#D6142C'},
                'hovertemplate': labels['cases_vs_newcases_hovertemplate'],
            },
            {
                'type': 'scatter',
                'x': data_qc['cases'],
                'y': data_qc['new_cases'].rolling(7).mean().round(),
                'customdata': data_qc['date'],
                'mode': 'lines',
                'name': labels['cases_vs_newcases_legend_qc'],
                'marker': {'color': '#001F97'},
                'hovertemplate': labels['cases_vs_newcases_hovertemplate'],
            },
        ],
        'layout': {
            'xaxis': {'type': 'log', 'title': {'text': labels['cases_vs_newcases_xlabel']}},
            'yaxis': {'type': 'log', 'title': {'text': labels['cases_vs_newcases_ylabel']}, 'gridcolor': '#f5f5f5'},
            'autosize': True,
            'legend': {'bgcolor': 'rgba(255,255,255,0)', 'x': 0, 'y': 1},
            'margin': {'r': 0, 't': 10, 'l': 30, 'b': 50},
            'plot_bgcolor': 'rgba(255,255,255,1)',
            'paper_bgcolor': 'rgba(255,255,255,1)',
            'hovermode': 'closest',
            'dragmode': False
        }
    })

    return cases_vs_newcases_fig
