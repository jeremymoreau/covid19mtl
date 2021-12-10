from itertools import cycle

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

COLOUR_QC = '#001F97'
# slightly more blue: #4677e7
COLOUR_QC_LIGHT = '#5c6dad'
COLOUR_MTL = '#D6142C'
COLOUR_MTL_LIGHT = '#d64b5b'
COLOUR_EXTRA = '#1b97d1'
COLOUR_GRID = '#f5f5f5'


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
                                   'gridcolor': COLOUR_GRID,
                                   'title': str(fig.layout.yaxis.title.text)
                               }
                         }]),
                    dict(label=labels['log_label'],
                         method='update',
                         args=[{'visible': [True, True]},
                               {'yaxis': {
                                   'type': 'log',
                                   'nticks': nticks_log,
                                   'gridcolor': COLOUR_GRID,
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
                'y': data_qc['active_cases'],
                'yaxis': 'y2',
                'mode': 'lines',
                'marker': {'color': COLOUR_EXTRA},
                'line': {'dash': 'dash'},
                'name': labels['active_cases_qc_label'],
                'hoverlabel': {'namelength': 25},
                'hovertemplate': '%{y:d}',
            },
            {
                'type': 'bar',
                'x': data_qc['date'],
                'y': data_qc['new_cases'],
                'marker': {'color': COLOUR_QC_LIGHT, 'opacity': 0.5},
                'name': labels['new_cases_qc_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'bar',
                'x': data_mtl['date'],
                'y': data_mtl['new_cases'],
                'marker': {'color': COLOUR_MTL_LIGHT, 'opacity': 0.5},
                'name': labels['new_cases_mtl_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'x': data_qc['date'],
                'y': data_qc['new_cases'].rolling(7).mean().round().fillna(0),
                'mode': 'lines',
                'marker': {'color': COLOUR_QC},
                'name': labels['7day_avg_qc_label'],
                'hoverlabel': {'namelength': 30},
            },
            {
                'type': 'scatter',
                'x': data_mtl['date'],
                'y': data_mtl['new_cases'].rolling(7).mean().round().fillna(0),
                'mode': 'lines',
                'marker': {'color': COLOUR_MTL},
                'name': labels['7day_avg_mtl_label'],
                'hoverlabel': {'namelength': 30},
            },
        ],
        'layout': {
            'autosize': True,
            'legend': {'bgcolor': 'rgba(255,255,255,0)', 'x': 0, 'y': 1},
            'xaxis': {'tickformat': '%m-%d\n%Y', 'title': {'text': labels['date_label']}},
            'yaxis': {
                'title': {'text': labels['confirmed_cases_y_label']},
                'gridcolor': COLOUR_GRID,
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


def mtl_age_fig(mtl_age_data, labels):
    figure = px.line(
        mtl_age_data,
        x='date',
        y='new_cases',
        color='age',
        # split into subplots
        # facet_col='age',
        # facet_col_wrap=5,
        hover_name='age',
        hover_data={
            'date': False,
            'age': True,
        },
    )

    figure.update_layout({
        'autosize': True,
        'showlegend': True,
        'legend_title_text': '',
        'legend': {
            'bgcolor': 'rgba(255,255,255,0)',
            'x': 0,
            'y': 1.03,
            'xanchor': 'left',
            'orientation': 'h',
            'font': {'size': 11}
        },
        'xaxis': {
            # 'tickformat': '%m-%d\n%Y',
            'tickformat': '%V\n%b %Y',
            'title': {'text': labels['week_label']},
            'hoverformat': labels['week_of_label'],
            'ticks': 'inside',
            'dtick': 7 * 86400000.0,
            'tick0': mtl_age_data['date'][0],
            'tickcolor': '#ccc',
        },
        'yaxis': {
            'title': {'text': '%'},
            'gridcolor': COLOUR_GRID,
            'rangemode': 'tozero',
            'constrain': 'domain',
            'ticksuffix': '%',
        },
        'margin': {'r': 0, 't': 30, 'l': 60, 'b': 30},
        'plot_bgcolor': 'rgba(255,255,255,1)',
        'paper_bgcolor': 'rgba(255,255,255,1)',
        'hovermode': 'x unified',
        'dragmode': False,
    })

    figure.update_traces({
        'mode': 'lines+markers',
        # 'line_shape': 'spline',
        'hovertemplate': '%{y}',
    })

    return figure


def qc_age_fig(qc_age_data, labels):
    figure = px.line(
        qc_age_data,
        x='date',
        y='new_hosp_per100k',
        color='age_group',
        # split into subplots
        # facet_col='age',
        # facet_col_wrap=5,
        hover_name='age_group',
        hover_data={
            'new_hosp': True,
        },
    )

    figure.update_layout({
        'autosize': True,
        'showlegend': True,
        'legend_title_text': '',
        'legend': {
            'bgcolor': 'rgba(255,255,255,0)',
            'x': 0,
            'y': 1.03,
            'xanchor': 'left',
            'orientation': 'h',
            'font': {'size': 11}
        },
        'xaxis': {
            # 'tickformat': '%m-%d\n%Y',
            'tickformat': '%V\n%b %Y',
            'title': {'text': labels['week_label']},
            'hoverformat': labels['week_of_label'] + '<br>' + labels['hospitalisations_hover_subtitle'],
            'ticks': 'inside',
            'dtick': 7 * 86400000.0,
            'tick0': qc_age_data['date'][0],
            'tickcolor': '#ccc',
        },
        'yaxis': {
            'title': {'text': labels['hospitalisations_age_y_label']},
            'gridcolor': COLOUR_GRID,
            'rangemode': 'tozero',
            'constrain': 'domain',
            # 'ticksuffix': '%',
        },
        'margin': {'r': 0, 't': 30, 'l': 60, 'b': 30},
        'plot_bgcolor': 'rgba(255,255,255,1)',
        'paper_bgcolor': 'rgba(255,255,255,1)',
        'hovermode': 'x unified',
        'dragmode': False,
    })

    figure.update_traces({
        'mode': 'lines+markers',
        # 'line_shape': 'spline',
        'hovertemplate': '%{y:.1f} (%{customdata})',
    })

    return figure


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
        'yaxis': {'title': {'text': '%'}, 'gridcolor': COLOUR_GRID},
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
                'type': 'bar',
                'x': data_qc['date'],
                'y': data_qc['new_deaths'],
                'marker': {'color': COLOUR_QC_LIGHT, 'opacity': 0.5},
                'name': labels['new_deaths_qc_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'bar',
                'x': data_mtl['date'],
                'y': data_mtl['new_deaths'],
                'marker': {'color': COLOUR_MTL_LIGHT, 'opacity': 0.5},
                'name': labels['new_deaths_mtl_label'],
                'hoverlabel': {'namelength': 25},
            },
            {
                'type': 'scatter',
                'x': data_qc['date'],
                'y': data_qc['new_deaths'].rolling(7).mean().round().fillna(0),
                'mode': 'lines',
                'marker': {'color': COLOUR_QC},
                'name': labels['7day_avg_qc_label'],
                'hoverlabel': {'namelength': 30},
            },
            {
                'type': 'scatter',
                'x': data_mtl['date'],
                'y': data_mtl['new_deaths'].rolling(7).mean().round().fillna(0),
                'mode': 'lines',
                'marker': {'color': COLOUR_MTL},
                'name': labels['7day_avg_mtl_label'],
                'hoverlabel': {'namelength': 30},
            }
        ],
        'layout': {
            'autosize': True,
            'legend': {'bgcolor': 'rgba(255,255,255,0)', 'x': 0, 'y': 1},
            'xaxis': {'tickformat': '%m-%d\n%Y', 'title': {'text': labels['date_label']}},
            'yaxis': {
                'title': {'text': labels['deaths_qc_y_label']},
                'gridcolor': COLOUR_GRID,
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
                'x': data_qc['date'],
                'y': data_qc['hos_act_reg_n'],
                'yaxis': 'y1',
                'marker': {'color': COLOUR_QC_LIGHT, 'opacity': 0.3},
                'name': labels['hospitalisations_active_qc'],
                'hoverlabel': {'namelength': 35},
            },
            {
                'type': 'bar',
                'x': data_qc['date'],
                'y': data_qc['hos_act_si_n'],
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
                'marker': {'color': COLOUR_QC},
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
                'marker': {'color': COLOUR_MTL},
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
            'xaxis': {'tickformat': '%m-%d\n%Y', 'title': {'text': labels['date_label']}},
            'yaxis': {
                'title': {'text': labels['hospitalisations_y_label']},
                'gridcolor': COLOUR_GRID
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
                'type': 'bar',
                'x': data_qc['date'],
                'y': data_qc['psi_quo_tes_n'],
                'yaxis': 'y2',
                'marker': {'color': COLOUR_QC_LIGHT, 'opacity': 0.5},
                'name': labels['testing_tests_qc'],
                'hoverlabel': {'namelength': 25},
                'hovertemplate': '%{y:d}',
            },
            {
                'type': 'bar',
                'x': data_mtl['date'],
                'y': data_mtl['psi_quo_tes_n'],
                'yaxis': 'y2',
                'marker': {'color': COLOUR_MTL_LIGHT, 'opacity': 0.5},
                'name': labels['testing_tests_mtl'],
                'hoverlabel': {'namelength': 25},
                'hovertemplate': '%{y:d}',
            },
            {
                'type': 'scatter',
                'x': data_qc['date'],
                'y': data_qc['psi_quo_pos_t'].rolling(7).mean(),
                'customdata': data_qc['psi_quo_pos_t'],
                'mode': 'lines',
                'marker': {'color': COLOUR_QC},
                'name': labels['7day_avg_qc_label'],
                'hoverlabel': {'namelength': 0},
                'hovertemplate': labels['testing_hovertemplate_qc'],
            },
            {
                'type': 'scatter',
                'x': data_mtl['date'],
                'y': data_mtl['psi_quo_pos_t'].rolling(7).mean(),
                'customdata': data_mtl['psi_quo_pos_t'],
                'mode': 'lines',
                'marker': {'color': COLOUR_MTL},
                'name': labels['7day_avg_mtl_label'],
                'hoverlabel': {'namelength': 0},
                'hovertemplate': labels['testing_hovertemplate_mtl'],
            },
        ],
        'layout': {
            'autosize': True,
            'legend': {'bgcolor': 'rgba(255,255,255,0)', 'x': 0, 'y': 1},
            'xaxis': {'tickformat': '%m-%d\n%Y', 'title': {'text': labels['date_label']}},
            'yaxis': {
                'title': {'text': labels['testing_y_label']},
                'gridcolor': COLOUR_GRID,
                'ticksuffix': '%'
            },
            'yaxis2': {
                'title': {'text': labels['testing_y2_label']},
                'overlaying': 'y',
                'rangemode': 'tozero',
                'side': 'right',
                'constrain': 'domain',
            },
            'margin': {'r': 0, 't': 10, 'l': 60, 'b': 50},
            'plot_bgcolor': 'rgba(255,255,255,1)',
            'paper_bgcolor': 'rgba(255,255,255,1)',
            'hovermode': 'x',
            'dragmode': False
        }
    })
    testing_fig = add_fig_controls(testing_fig, data_qc['negative_tests'], labels)

    return testing_fig


def vaccination_fig(data_qc_vaccination, data_mtl_vaccination, labels):
    vaccination_fig = go.Figure({
        'data': [
            {
                'type': 'bar',
                'x': data_qc_vaccination['date'],
                'y': data_qc_vaccination['total_doses'],
                'customdata': data_qc_vaccination[['calc_perc', 'total_doses_1d']],
                'yaxis': 'y1',
                'marker': {'color': COLOUR_QC_LIGHT, 'opacity': 0.7},
                'name': labels['vaccination_total'],
                'hoverlabel': {'namelength': 0},
                'hovertemplate': labels['vaccination_total'] + ': %{y:,d} (%{customdata[0]:.2f}%)',
            },
            {
                'type': 'bar',
                'x': data_qc_vaccination['date'],
                'y': data_qc_vaccination['total_doses_2d'],
                'customdata': data_qc_vaccination['calc_perc_2d'],
                'yaxis': 'y1',
                'marker': {'color': COLOUR_QC},
                'name': labels['vaccination_total_2d'],
                'hoverlabel': {'namelength': 0},
                'hovertemplate': labels['vaccination_total_2d'] + ': %{y:,d} (%{customdata:.2f}%)',
            },
            {
                'type': 'bar',
                'x': data_mtl_vaccination['date'],
                'y': data_mtl_vaccination['total_doses'],
                'customdata': data_mtl_vaccination[['calc_perc_1d', 'total_doses_1d']],
                'yaxis': 'y1',
                'marker': {'color': COLOUR_MTL_LIGHT, 'opacity': 0.7},
                'name': labels['vaccination_total'],
                'hoverlabel': {'namelength': 0},
                'hovertemplate': labels['vaccination_total'] + ': %{y:,d} (%{customdata[0]:.2f}%)',
                # hide by default
                'visible': False,
            },
            {
                'type': 'bar',
                'x': data_mtl_vaccination['date'],
                'y': data_mtl_vaccination['total_doses_2d'],
                'customdata': data_qc_vaccination['calc_perc_2d'],
                'yaxis': 'y1',
                'marker': {'color': COLOUR_MTL},
                'name': 'Doses administered (2nd dose)',
                'hoverlabel': {'namelength': 0},
                'hovertemplate': labels['vaccination_total_2d'] + ': %{y:,d} (%{customdata:.2f}%)',
                # hide by default
                'visible': False,
            },
        ],
        'layout': {
            'autosize': True,
            'legend': {'bgcolor': 'rgba(255,255,255,0)', 'x': 0, 'y': 1},
            'xaxis': {'tickformat': '%m-%d\n%Y', 'title': {'text': labels['date_label']}},
            'yaxis': {
                'title': {'text': labels['vaccination_y']},
                'gridcolor': COLOUR_GRID
            },
            'yaxis2': {
                'title': {'text': labels['vaccination_new']},
                'overlaying': 'y',
                'rangemode': 'tozero',
                'side': 'right',
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
    vaccination_fig = add_fig_controls(vaccination_fig, data_qc_vaccination['total_doses'], labels)

    # add buttons to switch between QC/MTL
    vaccination_fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        label='Quebec',
                        method='update',
                        args=[{'visible': [True, True, False, False]}],
                    ),
                    dict(
                        label='Montreal',
                        method='update',
                        args=[{'visible': [False, False, True, True]}],
                    ),
                ]),
                type='buttons',
                direction='right',
                pad={'r': 10, 't': 10},
                showactive=True,
                active=0,
                x=0.4,
                xanchor='left',
                y=1.1,
                yanchor='top',
            ),
        ],
    )

    return vaccination_fig


def vaccination_administered_fig(data_qc_vaccination, data_mtl_vaccination, labels):
    vaccination_fig = go.Figure({
        'data': [
            {
                'type': 'bar',
                'x': data_qc_vaccination['date'],
                'y': data_qc_vaccination['new_doses'],
                'customdata': data_qc_vaccination['new_doses'].rolling(7).mean().round(),
                'yaxis': 'y1',
                'marker': {'color': COLOUR_QC_LIGHT, 'opacity': 0.7},
                'name': labels['vaccination_new'],
                'hoverlabel': {'namelength': 0},
                'hovertemplate':
                    labels['vaccination_new_qc'] + ': %{y:,d}<br>'
                    + labels['7day_avg_short'] + ': %{customdata:,d}',
            },
            {
                'type': 'bar',
                'x': data_qc_vaccination['date'],
                'y': data_qc_vaccination['new_doses_2d'],
                'customdata': data_qc_vaccination['new_doses_2d'].rolling(7).mean().round(),
                'yaxis': 'y1',
                'marker': {'color': COLOUR_QC},
                'name': labels['vaccination_new_2d'],
                'hoverlabel': {'namelength': 0},
                'hovertemplate':
                    labels['vaccination_new_2d'] + ' (QC): %{y:,d}<br>'
                    + labels['7day_avg_short'] + ': %{customdata:,d}',
            },
            {
                'type': 'bar',
                'x': data_mtl_vaccination['date'],
                'y': data_mtl_vaccination['new_doses'],
                'customdata': data_mtl_vaccination['new_doses'].rolling(7).mean().round(),
                'yaxis': 'y1',
                'marker': {'color': COLOUR_MTL_LIGHT, 'opacity': 0.7},
                'name': labels['vaccination_new'],
                'hoverlabel': {'namelength': 0},
                'hovertemplate':
                    labels['vaccination_new_mtl'] + ': %{y:,d}<br>'
                    + labels['7day_avg_short'] + ': %{customdata:,d}',
                # hide by default
                'visible': False,
            },
            {
                'type': 'bar',
                'x': data_mtl_vaccination['date'],
                'y': data_mtl_vaccination['new_doses_2d'],
                'customdata': data_mtl_vaccination['new_doses_2d'].rolling(7).mean().round(),
                'yaxis': 'y1',
                'marker': {'color': COLOUR_MTL},
                'name': labels['vaccination_new_2d'],
                'hoverlabel': {'namelength': 0},
                'hovertemplate':
                    labels['vaccination_new_2d'] + ' (MTL): %{y:,d}<br>'
                    + labels['7day_avg_short'] + ': %{customdata:,d}',
                # hide by default
                'visible': False,
            },
        ],
        'layout': {
            'autosize': True,
            'legend': {'bgcolor': 'rgba(255,255,255,0)', 'x': 0, 'y': 1},
            'xaxis': {'tickformat': '%m-%d\n%Y', 'title': {'text': labels['date_label']}},
            'yaxis': {
                'title': {'text': labels['vaccination_new']},
                'gridcolor': COLOUR_GRID
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
    vaccination_fig = add_fig_controls(vaccination_fig, data_qc_vaccination['new_doses_1d'], labels)

    # add buttons to switch between QC/MTL
    vaccination_fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        label='Quebec',
                        method='update',
                        args=[{'visible': [True, True, False, False]}],
                    ),
                    dict(
                        label='Montreal',
                        method='update',
                        args=[{'visible': [False, False, True, True]}],
                    ),
                ]),
                type='buttons',
                direction='right',
                pad={'r': 10, 't': 10},
                showactive=True,
                active=0,
                x=0.4,
                xanchor='left',
                y=1.1,
                yanchor='top',
            ),
        ]
    )

    return vaccination_fig


def vaccine_delivery_fig(data_vaccine, labels):
    data_vaccine['qc_doses_available'] = data_vaccine['qc_doses_received'] - data_vaccine['qc_doses']

    vaccine_fig = go.Figure({
        'data': [
            {
                'type': 'bar',
                'x': data_vaccine['date'],
                'y': data_vaccine['qc_doses_received'],
                'yaxis': 'y1',
                'marker': {'color': COLOUR_QC_LIGHT, 'opacity': 0.3},
                'name': labels['vaccine_received'],
                'customdata': data_vaccine['qc_new_doses_received'],
                'hoverlabel': {'namelength': 0},
                'hovertemplate': labels['vaccine_received_hovertemplate'],
            },
            {
                'type': 'scatter',
                'x': data_vaccine['date'],
                'y': data_vaccine['qc_doses'],
                'yaxis': 'y1',
                'mode': 'lines',
                'marker': {'color': COLOUR_QC},
                'name': labels['vaccine_administered'],
                'hoverlabel': {'namelength': 30},
                'hovertemplate': '%{y:,d}',
            },
            {
                'type': 'scatter',
                'x': data_vaccine['date'],
                'y': data_vaccine['qc_doses_available'],
                'yaxis': 'y1',
                'mode': 'lines',
                'marker': {'color': COLOUR_MTL_LIGHT},
                'name': labels['vaccine_available'],
                'hoverlabel': {'namelength': 30},
                'hovertemplate': '%{y:,d}',
            },
        ],
        'layout': {
            'autosize': True,
            'legend': {'bgcolor': 'rgba(255,255,255,0)', 'x': 0, 'y': 1},
            'xaxis': {'tickformat': '%m-%d\n%Y', 'title': {'text': labels['date_label']}},
            'yaxis': {
                'title': {'text': labels['vaccination_y']},
                'gridcolor': COLOUR_GRID
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
    vaccine_fig = add_fig_controls(vaccine_fig, data_vaccine['qc_doses_received'], labels)

    return vaccine_fig


def vaccination_qc_age_fig(data_vaccination, labels):
    figure = make_subplots(rows=2, cols=4, specs=[
        # [{'type':'domain'}, {'type': 'domain'}],
        # [{'type':'domain'}, {'type': 'domain'}],
        # [{'type':'domain'}, {'type': 'domain'}]
        [{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}],
        [{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]
    ])

    colours = [
        'rgb(179, 179, 179)',
        'rgb(179, 222, 105)',
        'rgb(102, 166, 30)',
    ]

    for index, row in data_vaccination.iterrows():
        values = [row['0d'], row['1d'], row['2d']]
        chart = go.Pie(
            labels=labels['vaccination_categories'],
            values=values,
            title=f"<b>{row['group']}</b><br>({row['pop 2021']:,d})",
            # hole=0.5
        )
        row = int(index / 4) + 1
        col = index % 4 + 1
        figure.add_trace(chart, row, col)

    figure.update_traces(
        # textposition='outside',
        # textinfo='percent+label+value',
        # hovertemplate='%{value}',
        hovertemplate='',
        # texttemplate='<b>%{label}</b><br>%{percent} (%{value})',
        texttemplate='%{value}<br>(%{percent})',
        hoverinfo='skip',
        title={'position': 'bottom center', 'font': {'size': 12}},
        # showlegend=False,
        insidetextorientation='horizontal',
    )

    figure.update_layout(
        piecolorway=colours,
        legend_title_text='',
        legend={
            'bgcolor': 'rgba(255,255,255,0)',
            'x': 0,
            'y': 1.2,
            'xanchor': 'left',
            'orientation': 'h',
            'font': {'size': 11}
        },
        margin={'r': 10, 't': 0, 'l': 10, 'b': 0},
    )

    return figure


def vaccination_age_fig(data_vaccination, labels):
    colours = [
        # fully vaccinated
        'rgb(102, 166, 30)',
        # 1 dose
        'rgb(179, 222, 105)',
        # no dose
        'rgb(179, 179, 179, 50)',
    ]

    figure = px.bar(
        data_vaccination,
        x='perc',
        y=data_vaccination.index,
        color='variable',
        orientation='h',
        color_discrete_sequence=colours,
        text='perc',
        custom_data=['value'],
    )

    figure.update_traces(
        texttemplate='%{text:.2f}%',
        hovertemplate='%{customdata} (%{text:.2f}%)',
        # textfont={'size': 10},
    )

    figure.update_layout(
        legend_title_text='',
        legend={
            'bgcolor': 'rgba(255,255,255,0)',
            'x': 0,
            'y': 1.05,
            'xanchor': 'left',
            'orientation': 'h',
            'font': {'size': 11}
        },
        xaxis={
            'ticksuffix': '%',
            'dtick': 10,
            'ticks': 'inside',
            'tickcolor': '#ccc',
            'title': '%',
        },
        yaxis={
            'title': labels['age_label'],
        },
        barmode='stack',
        hovermode='y unified',
        margin={'r': 0, 't': 0, 'l': 10, 'b': 0},
        plot_bgcolor='rgba(255,255,255,1)',
        paper_bgcolor='rgba(255,255,255,1)',
        dragmode=False,
    )

    # update labels of traces
    # see: https://stackoverflow.com/a/64378982
    the_labels = cycle(reversed(labels['vaccination_categories']))

    figure.for_each_trace(lambda t: t.update(name=next(the_labels)))

    return figure


def variants_fig(data_variants, labels):
    variants_fig = go.Figure({
        'data': [
            {
                'type': 'bar',
                'x': data_variants.index,
                'y': data_variants['new_presumptive'],
                'yaxis': 'y1',
                'marker': {'color': COLOUR_QC_LIGHT, 'opacity': 0.3},
                'name': labels['variants_new_presumptive'] + ' (QC)',
                'hoverlabel': {'namelength': 0},
                'hoverinfo': 'skip',
            },
            {
                'type': 'bar',
                'x': data_variants.index,
                'y': data_variants['new_presumptive_mtl'],
                'yaxis': 'y1',
                'marker': {'color': COLOUR_MTL_LIGHT, 'opacity': 0.3},
                'name': labels['variants_new_presumptive'] + ' (MTL)',
                'hoverlabel': {'namelength': 0},
                'hoverinfo': 'skip',
            },
            {
                'type': 'scatter',
                'x': data_variants.index,
                'y': data_variants['new_presumptive_7dma'],
                'yaxis': 'y1',
                'mode': 'lines',
                'marker': {'color': COLOUR_QC_LIGHT},
                'name': f"{labels['variants_new_presumptive']} ({labels['7day_avg_short']}, QC)",
                'hoverlabel': {'namelength': 0},
                'customdata': data_variants[['new_presumptive', 'new_sequenced']],
                'hovertemplate':
                    '<b>Québec</b><br>'
                    + labels['variants_new_presumptive'] + ' (' + labels['7day_avg_short'] + '): %{y}<br>'
                    + labels['variants_new_presumptive'] + ': %{customdata[0]}<br>'
                    + labels['variants_new_sequenced'] + ': %{customdata[1]}',
            },
            {
                'type': 'scatter',
                'x': data_variants.index,
                'y': data_variants['new_presumptive_mtl_7dma'],
                'yaxis': 'y1',
                'mode': 'lines',
                'marker': {'color': COLOUR_MTL_LIGHT},
                'name': f"{labels['variants_new_presumptive']} ({labels['7day_avg_short']}, MTL)",
                'hoverlabel': {'namelength': 0},
                'customdata': data_variants[['new_presumptive_mtl', 'new_sequenced_mtl']],
                'hovertemplate':
                    '<b>Montréal</b><br>'
                    + labels['variants_new_presumptive'] + ' (' + labels['7day_avg_short'] + '): %{y}<br>'
                    + labels['variants_new_presumptive'] + ': %{customdata[0]}<br>'
                    + labels['variants_new_sequenced'] + ': %{customdata[1]}',
            },
            {
                'type': 'scatter',
                'x': data_variants.index,
                'y': data_variants['new_cases'].rolling(7, min_periods=2).mean().round(),
                'yaxis': 'y1',
                'mode': 'lines',
                'line': {'dash': 'dot'},
                'marker': {'color': COLOUR_QC},
                'name': f"{labels['variants_new_cases']} ({labels['7day_avg_short']}, QC)",
                'hoverlabel': {'namelength': 40},
            },
            {
                'type': 'scatter',
                'x': data_variants.index,
                'y': data_variants['new_cases_mtl'].rolling(7, min_periods=2).mean().round(),
                'yaxis': 'y1',
                'mode': 'lines',
                'line': {'dash': 'dot'},
                'marker': {'color': COLOUR_MTL},
                'name': f"{labels['variants_new_cases']} ({labels['7day_avg_short']}, MTL)",
                'hoverlabel': {'namelength': 40},
            },
            {
                'type': 'scatter',
                'x': data_variants.index,
                'y': data_variants['pos_rate_7d_avg'],
                'yaxis': 'y3',
                'mode': 'lines+markers',
                # 'line': {'dash': 'dash'},
                'marker': {'color': COLOUR_EXTRA},
                'name': labels['variants_pos_rate_avg'],
                'hoverlabel': {'namelength': 0},
                'customdata': data_variants[['pos_rate', 'new_screened']],
                'hovertemplate':
                    '<b>' + labels['variants_pos_rate_avg'] + ': %{y:.1f}%</b><br>'
                    + labels['variants_pos_rate'] + ': %{customdata[0]:.1f}%<br>'
                    + labels['variants_screened'] + ': %{customdata[1]}',
            },
        ],
        'layout': {
            'autosize': True,
            'legend': {'bgcolor': 'rgba(255,255,255,0)', 'x': 0, 'y': 1},
            'xaxis': {
                'tickformat': '%m-%d',
                'title': {'text': labels['date_label']},
                # make more space for 2 yaxes on right
                # 'domain': [0, 0.9],
            },
            'yaxis': {
                'title': {'text': labels['confirmed_cases_y_label']},
                # 'gridcolor': COLOUR_GRID,
                # force higher range to keep new presumptive cases at a lower level
                # 'range': [0, 1000],
                'rangemode': 'tozero',
            },
            # currently unused
            'yaxis2': {
                'title': {'text': labels['variants_y2']},
                'title_standoff': 10,
                'overlaying': 'y',
                'rangemode': 'tozero',
                'side': 'right',
                'constrain': 'domain',
                'gridcolor': COLOUR_GRID,
            },
            'yaxis3': {
                'title': {'text': labels['variants_y3']},
                'title_standoff': 10,
                'ticksuffix': '%',
                'overlaying': 'y',
                'range': [0, 100],
                'side': 'right',
                # 'tickfont': {
                #     'size': 10,
                # },
                'dtick': 10,
                # move slightly to the left right next to the graph
                # 'anchor': 'free',
                # 'position': 0.955,
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

    return variants_fig


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
            'xaxis': {'tickformat': '%m-%d\n%Y', 'title': {'text': labels['date_label']}},
            'yaxis': {
                'title': {'text': labels['deaths_loc_fig_qc_y_label']},
                'gridcolor': COLOUR_GRID
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
                'marker': {'color': COLOUR_MTL},
                'hovertemplate': labels['cases_vs_newcases_hovertemplate'],
            },
            {
                'type': 'scatter',
                'x': data_qc['cases'],
                'y': data_qc['new_cases'].rolling(7).mean().round(),
                'customdata': data_qc['date'],
                'mode': 'lines',
                'name': labels['cases_vs_newcases_legend_qc'],
                'marker': {'color': COLOUR_QC},
                'hovertemplate': labels['cases_vs_newcases_hovertemplate'],
            },
        ],
        'layout': {
            'xaxis': {'type': 'log', 'title': {'text': labels['cases_vs_newcases_xlabel']}},
            'yaxis': {'type': 'log', 'title': {'text': labels['cases_vs_newcases_ylabel']}, 'gridcolor': COLOUR_GRID},
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
