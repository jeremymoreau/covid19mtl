import dash_core_components as dcc
import dash_html_components as html

import app.figures as figures

from .core import (latest_cases_mtl, new_cases_mtl, latest_cases_qc, new_cases_qc,
                   incid_per100k_7d_mtl, incid_per100K_perc_change_mtl,
                   incid_per100k_7d_qc, incid_per100K_perc_change_qc,
                   latest_deaths_mtl, new_deaths_mtl, latest_deaths_qc, new_deaths_qc,
                   new_hosp_mtl, new_icu_mtl, new_hosp_qc, new_icu_qc,
                   perc_vac_mtl, new_doses_mtl, perc_vac_qc, new_doses_qc,
                   pos_rate_mtl, pos_rate_change_mtl, pos_rate_qc, pos_rate_change_qc,
                   cases_per1000_long, data_mtl, data_mtl_death_loc, data_qc, data_qc_hosp,
                   mtl_age_data, mtl_geojson, data_vaccination)


def generate_layout(labels):
    # Figures #####
    mtlmap_fig = figures.mtl_cases_map_fig(cases_per1000_long, mtl_geojson, labels)
    cases_fig = figures.cases_fig(data_mtl, data_qc, labels)
    age_fig = figures.mtl_age_hist_fig(mtl_age_data, labels)
    deaths_fig = figures.deaths_fig(data_mtl, data_qc, labels)
    hospitalisations_fig = figures.hospitalisations_fig(data_qc_hosp, data_qc, data_mtl, labels)
    testing_fig = figures.testing_fig(data_qc, data_mtl, labels)
    deaths_loc_mtl_fig = figures.mtl_deaths_loc_fig(data_mtl_death_loc, labels)
    deaths_loc_qc_fig = figures.qc_deaths_loc_fig(data_qc, labels)
    cases_vs_newcases_fig = figures.cases_vs_newcases_fig(data_mtl, data_qc, labels)
    vaccination_fig = figures.vaccination_fig(data_vaccination, labels)

    # Plotly modebar buttons to remove
    modebar_buttons_to_remove = ['select2d',
                                 'lasso2d',
                                 'autoScale2d',
                                 'hoverCompareCartesian',
                                 'hoverClosestCartesian',
                                 'toggleSpikelines'
                                 ]

    # App layout #####
    layout = html.Div(
        [
            # language select
            html.Div(
                [
                    html.Div(
                        [
                            # title
                            html.P(
                                [labels['title']],
                                id='title',
                            ),
                            # subtitle
                            html.P(
                                [labels['subtitle']],
                                id='subtitle',
                            ),
                        ],
                        id='title-container',
                    ),
                    html.Div(
                        [
                            # Load in a new tab because some figures do not resize properly otherwise
                            # TODO: Fix this bug
                            html.A([labels['language0']], href=labels['language_link0'], target='_blank', className='lang-link'),
                            html.A([labels['language1']], href=labels['language_link1'], target='_blank', className='lang-link'),
                            html.A([labels['language2']], href=labels['language_link2'], target='_blank', className='lang-link'),
                        ],
                        id='language-container',
                    ),
                ],
                id='header',
            ),

            # mini info boxes
            html.Div(
                [
                    ####### MTL #######
                    html.Div(
                        [html.P(['+' + new_cases_mtl + labels['today']], className='superscript'),
                         html.H3(latest_cases_mtl, className='main_text'),
                         html.P([labels['cases_montreal_label']], className='subscript')],
                        className='mini_container cases',
                    ),
                    html.Div(
                        [html.P([incid_per100K_perc_change_mtl + '%' + labels['vs_last7d']], className='superscript'),
                         html.H3(incid_per100k_7d_mtl, className='main_text'),
                         html.P([labels['incidence_per100k_7d_mtl_label']], className='subscript')],
                        className='mini_container cases',
                    ),
                    html.Div(
                        [html.P(['+' + new_deaths_mtl + labels['today']], className='superscript'),
                         html.H3(latest_deaths_mtl, className='main_text'),
                         html.P([labels['deaths_montreal_label']], className='subscript')],
                        className='mini_container deaths',
                    ),
                    html.Div(
                        [html.P(['+' + new_icu_qc + labels['icu']], className='superscript icu'),
                         html.H3('+' + new_hosp_mtl + labels['yesterday'], className='main_text hosp'),
                         html.P([labels['hosp_mtl_label']], className='subscript hosp')],
                        className='mini_container',
                    ),
                    html.Div(
                        [html.P([pos_rate_change_mtl + '%' + labels['yesterday']], className='superscript'),
                         html.H3(pos_rate_mtl + '%', className='main_text'),
                         html.P([labels['test_pos_mtl_label']], className='subscript')],
                        className='mini_container tests',
                    ),
                    html.Div(
                        [html.P(['+' + new_doses_mtl + labels['doses_today']], className='superscript'),
                         html.H3(perc_vac_mtl + '%', className='main_text'),
                         html.P([labels['vaccination_perc_mtl_label']], className='subscript')],
                        className='mini_container vaccines',
                    ),
                    ####### QC #######
                    html.Div(
                        [html.P(['+' + new_cases_qc + labels['today']], className='superscript'),
                         html.H3(latest_cases_qc, className='main_text'),
                         html.P([labels['cases_qc_label']], className='subscript')],
                        className='mini_container cases',
                    ),
                    html.Div(
                        [html.P([incid_per100K_perc_change_qc + '%' + labels['vs_last7d']], className='superscript'),
                         html.H3(incid_per100k_7d_qc, className='main_text'),
                         html.P([labels['incidence_per100k_7d_qc_label']], className='subscript')],
                        className='mini_container cases',
                    ),
                    html.Div(
                        [html.P(['+' + new_deaths_qc + labels['today']], className='superscript'),
                         html.H3(latest_deaths_qc, className='main_text'),
                         html.P([labels['deaths_qc_label']], className='subscript')],
                        className='mini_container deaths',
                    ),
                    html.Div(
                        [html.P(['+' + new_icu_qc + labels['icu']], className='superscript icu'),
                         html.H3('+' + new_hosp_qc + labels['yesterday'], className='main_text hosp'),
                         html.P([labels['hosp_qc_label']], className='subscript hosp')],
                        className='mini_container',
                    ),
                    html.Div(
                        [html.P([pos_rate_change_qc + '%' + labels['yesterday']], className='superscript'),
                         html.H3(pos_rate_qc + '%', className='main_text'),
                         html.P([labels['test_pos_qc_label']], className='subscript')],
                        className='mini_container tests',
                    ),
                    html.Div(
                        [html.P(['+' + new_doses_qc + labels['doses_today']], className='superscript'),
                         html.H3(perc_vac_qc + '%', className='main_text'),
                         html.P([labels['vaccination_perc_qc_label']], className='subscript')],
                        className='mini_container vaccines',
                    ),
                ],
                id='info-container'
            ),

            # 1st row: two boxes
            html.Div(
                [
                    # left box
                    html.Div(
                        [
                            dcc.Markdown([labels['infobox']], id='infobox_text')
                        ],
                        className='grid-item',
                        id='infobox_container',
                    ),
                    # right box
                    html.Div(
                        [
                            html.H6(
                                [labels['montreal_map_label']],
                            ),
                            dcc.Graph(
                                figure=mtlmap_fig,
                                id='montreal_map',
                                responsive=True,
                                config={
                                    'modeBarButtonsToRemove': [
                                        'select2d',
                                        'lasso2d',
                                        'hoverClosestGeo',
                                    ],
                                    'scrollZoom': True
                                }
                            ),
                        ],
                        className='grid-item'
                    ),
                ],
                className='grid-container-onethird-twothirds-cols',
            ),

            # 2nd row: 2 boxes
            html.Div(
                [
                    # left box
                    html.Div(
                        [

                            html.H6(
                                [labels['total_cases_label']],
                            ),
                            dcc.Graph(
                                figure=cases_fig,
                                id='cases_fig',
                                responsive=True,
                                config={
                                    'modeBarButtonsToRemove': modebar_buttons_to_remove,
                                }
                            ),
                        ],
                        className='grid-item'
                    ),
                    # right box
                    html.Div(
                        [
                            html.H6(
                                [labels['age_group_label']],
                            ),
                            dcc.Graph(
                                figure=age_fig,
                                id='age_fig',
                                responsive=True,
                                config={
                                    'modeBarButtonsToRemove': modebar_buttons_to_remove,
                                }
                            ),
                        ],
                        className='grid-item'
                    ),
                ],
                className='grid-container-two-cols',
            ),

            # 3rd row: 3 boxes
            html.Div(
                [
                    # left box
                    html.Div(
                        [

                            html.H6(
                                [labels['deaths_fig_label']],
                            ),
                            dcc.Graph(
                                figure=deaths_fig,
                                id='deaths_fig',
                                responsive=True,
                                config={
                                    'modeBarButtonsToRemove': modebar_buttons_to_remove,
                                }
                            ),
                        ],
                        className='grid-item'
                    ),
                    # middle box
                    html.Div(
                        [
                            html.H6(
                                [labels['testing_label']],
                            ),
                            dcc.Graph(
                                figure=testing_fig,
                                id='testing_fig',
                                responsive=True,
                                config={
                                    'modeBarButtonsToRemove': modebar_buttons_to_remove,
                                }
                            ),
                        ],
                        className='grid-item'
                    ),
                    # right box
                    html.Div(
                        [
                            html.H6(
                                [labels['vaccination_label']]
                            ),
                            dcc.Graph(
                                figure=vaccination_fig,
                                id='vaccination_fig',
                                responsive=True,
                                config={
                                    'modeBarButtonsToRemove': modebar_buttons_to_remove,
                                }
                            ),
                        ],
                        className='grid-item'
                    ),
                ],
                className='grid-container-three-cols',
            ),

            # 4th row: 2 boxes
            html.Div(
                [
                    # left box
                    html.Div(
                        [
                            html.H6(
                                [labels['hospitalisations_label']],
                            ),
                            dcc.Graph(
                                figure=hospitalisations_fig,
                                id='hospitalisations_fig',
                                responsive=True,
                                config={
                                    'modeBarButtonsToRemove': modebar_buttons_to_remove,
                                }
                            ),
                        ],
                        className='grid-item'
                    ),
                    # right box
                    html.Div(
                        [
                            html.H6(
                                [labels['cases_vs_newcases_label']],
                            ),
                            dcc.Graph(
                                figure=cases_vs_newcases_fig,
                                id='cases_vs_newcases_fig',
                                responsive=True,
                                config={
                                    'modeBarButtonsToRemove': modebar_buttons_to_remove,
                                }
                            ),
                        ],
                        className='grid-item'
                    ),
                ],
                className='grid-container-two-cols',
            ),

            # 5th row: 2 boxes
            html.Div(
                [
                    # left box
                    html.Div(
                        [

                            html.H6(
                                [labels['deaths_loc_fig_mtl_label']],
                            ),
                            dcc.Graph(
                                figure=deaths_loc_mtl_fig,
                                id='deaths_loc_fig_mtl',
                                responsive=True,
                                config={
                                    'modeBarButtonsToRemove': modebar_buttons_to_remove,
                                }
                            ),
                        ],
                        className='grid-item'
                    ),
                    # right box
                    html.Div(
                        [
                            html.H6(
                                [labels['deaths_loc_fig_qc_label']],
                            ),
                            dcc.Graph(
                                figure=deaths_loc_qc_fig,
                                id='deaths_loc_fig_qc',
                                responsive=True,
                                config={
                                    'modeBarButtonsToRemove': modebar_buttons_to_remove,
                                }
                            ),
                        ],
                        className='grid-item'
                    ),
                ],
                className='grid-container-two-cols',
            ),

            # footer
            html.Div([
                html.Div([
                    dcc.Markdown([labels['footer_left']]),
                ],
                    id='footer-left',
                    className='footer-item'
                ),
                html.Div([
                    dcc.Markdown([labels['footer_centre']]),
                ],
                    id='footer-centre',
                    className='footer-item'
                ),
                html.Div([
                    dcc.Markdown([labels['footer_right']]),
                ],
                    id='footer-right',
                    className='footer-item'
                )
            ],
                id='footer'
            )

        ],
        id='main-container'
    )

    return layout
