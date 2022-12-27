import dash_core_components as dcc
import dash_html_components as html

import app.figures as figures

from .core import (data_mtl, data_qc, data_qc_cases_vacc_status, data_qc_hosp, data_qc_hosp_vacc_status,
                   incid_per100k_7d_mtl, incid_per100k_7d_mtl_colour, incid_per100k_7d_qc, incid_per100k_7d_qc_colour,
                   incid_per100K_perc_change_mtl, incid_per100K_perc_change_qc, latest_cases_mtl, latest_cases_qc,
                   latest_deaths_mtl, latest_deaths_qc, latest_recovered_mtl, latest_recovered_qc, mtl_age_data,
                   mtl_boroughs, mtl_geojson, new_cases_mtl, new_cases_qc, new_deaths_mtl, new_deaths_qc, new_hosp_mtl,
                   new_hosp_qc, new_icu_mtl, new_icu_qc, new_recovered_mtl, new_recovered_qc, pos_rate_change_mtl,
                   pos_rate_change_qc, pos_rate_mtl, pos_rate_mtl_colour, pos_rate_qc, pos_rate_qc_colour)


def generate_layout(labels):
    # Figures #####
    mtlmap_fig = figures.mtl_cases_map_fig(mtl_boroughs, mtl_geojson, labels)
    cases_fig = figures.cases_fig(data_mtl, data_qc, labels)
    age_fig = figures.mtl_age_fig(mtl_age_data, labels)
    deaths_fig = figures.deaths_fig(data_mtl, data_qc, labels)
    hospitalisations_fig = figures.hospitalisations_fig(data_qc_hosp, data_qc, data_mtl, labels)
    testing_fig = figures.testing_fig(data_qc, data_mtl, labels)
    cases_by_vaccination_status_fig = figures.qc_data_by_vacc_status_fig(
        data_qc_cases_vacc_status,
        'cases_vaccination_status_y',
        labels,
    )
    hosp_by_vaccination_status_fig = figures.qc_data_by_vacc_status_fig(
        data_qc_hosp_vacc_status,
        'hosp_vaccination_status_y',
        labels,
    )
    # deaths_loc_mtl_fig = figures.mtl_deaths_loc_fig(data_mtl_death_loc, labels)
    # deaths_loc_qc_fig = figures.qc_deaths_loc_fig(data_qc, labels)
    # cases_vs_newcases_fig = figures.cases_vs_newcases_fig(data_mtl, data_qc, labels)
    # variants_fig = figures.variants_fig(data_variants, labels)

    # Plotly modebar buttons to remove
    modebar_buttons_to_remove = ['select2d',
                                 'lasso2d',
                                 'zoomIn2d',
                                 'zoomOut2d',
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
                            html.A(labels['home_link_text'], href=labels['home_link'], className='nav-link active'),
                            html.A(
                                labels['vaccination_link_text'],
                                href=labels['vaccination_link'],
                                className='nav-link'
                            ),
                            html.Span('|', className='divider'),
                            # Load in a new tab because some figures do not resize properly otherwise
                            # TODO: Fix this bug. Removed: Seems to work?!
                            html.A([labels['language0']], href=labels['language_link0'], className='lang-link'),
                            html.A([labels['language1']], href=labels['language_link1'], className='lang-link'),
                            html.A([labels['language2']], href=labels['language_link2'], className='lang-link'),
                        ],
                        id='language-container',
                    ),
                ],
                id='header',
            ),
            # data update note
            html.Div(
                [
                    html.P([dcc.Markdown(labels['datanote'])]),
                ],
                className='note-container',
            ),
            # mini info boxes
            html.Div(
                [
                    # MTL
                    html.Div(
                        [html.P([f'{new_cases_mtl:+d}' + labels['today']], className='superscript'),
                         html.H3(latest_cases_mtl, className='main_text'),
                         html.P([labels['cases_montreal_label']], className='subscript')],
                        className='mini_container cases',
                    ),
                    html.Div(
                        [
                            html.P(
                                [f'{incid_per100K_perc_change_mtl:+.0f}%' + labels['vs_last7d']],
                                className='superscript'
                            ),
                            html.H3(f'{incid_per100k_7d_mtl:.0f}', className='main_text'),
                            html.P([labels['incidence_per100k_7d_mtl_label']], className='subscript')
                        ],
                        className='mini_container', style={'color': incid_per100k_7d_mtl_colour}
                    ),
                    html.Div(
                        [html.P([f'{new_deaths_mtl:+d}' + labels['today']], className='superscript'),
                         html.H3(latest_deaths_mtl, className='main_text'),
                         html.P([labels['deaths_montreal_label']], className='subscript')],
                        className='mini_container deaths',
                    ),
                    html.Div(
                        [html.P([f'{new_icu_mtl:+d}' + labels['icu']], className='superscript icu'),
                         html.H3(f'{new_hosp_mtl:+d}' + labels['today_short'], className='main_text hosp'),
                         html.P([labels['hosp_mtl_label']], className='subscript hosp')],
                        className='mini_container',
                    ),
                    html.Div(
                        [html.P([f'{pos_rate_change_mtl:+.1f}%' + labels['vs_2dago']], className='superscript'),
                         html.H3(f'{pos_rate_mtl:.1f}%' + labels['yesterday'], className='main_text'),
                         html.P([labels['test_pos_mtl_label']], className='subscript')],
                        className='mini_container', style={'color': pos_rate_mtl_colour}
                    ),
                    html.Div(
                        [html.P([f'{new_recovered_mtl:+d}' + labels['today']], className='superscript'),
                         html.H3(latest_recovered_mtl, className='main_text'),
                         html.P([labels['recovered_mtl_label']], className='subscript')],
                        className='mini_container recovered',
                    ),
                    # QC
                    html.Div(
                        [html.P([f'{new_cases_qc:+d}' + labels['today']], className='superscript'),
                         html.H3(latest_cases_qc, className='main_text'),
                         html.P([labels['cases_qc_label']], className='subscript')],
                        className='mini_container cases',
                    ),
                    html.Div(
                        [
                            html.P(
                                [f'{incid_per100K_perc_change_qc:+.0f}%' + labels['vs_last7d']],
                                className='superscript'
                            ),
                            html.H3(f'{incid_per100k_7d_qc:.0f}', className='main_text'),
                            html.P([labels['incidence_per100k_7d_qc_label']], className='subscript')
                        ],
                        className='mini_container', style={'color': incid_per100k_7d_qc_colour}
                    ),
                    html.Div(
                        [html.P([f'{new_deaths_qc:+d}' + labels['today']], className='superscript'),
                         html.H3(latest_deaths_qc, className='main_text'),
                         html.P([labels['deaths_qc_label']], className='subscript')],
                        className='mini_container deaths',
                    ),
                    html.Div(
                        [html.P([f'{new_icu_qc:+d}' + labels['icu']], className='superscript icu'),
                         html.H3(f'{new_hosp_qc:+d}' + labels['today_short'], className='main_text hosp'),
                         html.P([labels['hosp_qc_label']], className='subscript hosp')],
                        className='mini_container',
                    ),
                    html.Div(
                        [html.P([f'{pos_rate_change_qc:+.1f}%' + labels['vs_2dago']], className='superscript'),
                         html.H3(f'{pos_rate_qc:.1f}%' + labels['yesterday'], className='main_text'),
                         html.P([labels['test_pos_qc_label']], className='subscript')],
                        className='mini_container', style={'color': pos_rate_qc_colour}
                    ),
                    html.Div(
                        [html.P([f'{new_recovered_qc:+d}' + labels['today']], className='superscript'),
                         html.H3(latest_recovered_qc, className='main_text'),
                         html.P([labels['recovered_qc_label']], className='subscript')],
                        className='mini_container recovered',
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
                                    'scrollZoom': True,
                                    'doubleClick': False
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
                                    'doubleClick': False
                                },
                                className='figure'
                            ),
                        ],
                        className='grid-item'
                    ),
                    # right box
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
                                    'doubleClick': False
                                },
                                className='figure'
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
                                    'doubleClick': False
                                },
                                className='figure'
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
                                    'doubleClick': False
                                },
                                className='figure'
                            ),
                        ],
                        className='grid-item'
                    ),
                    # right box
                    # html.Div(
                    #     [
                    #         html.H6(
                    #             [labels['vaccination_label']]
                    #         ),
                    #         dcc.Graph(
                    #             figure=vaccination_fig,
                    #             id='vaccination_fig',
                    #             responsive=True,
                    #             config={
                    #                 'modeBarButtonsToRemove': modebar_buttons_to_remove,
                    #                 'doubleClick': False
                    #             },
                    #             className='figure'
                    #         ),
                    #     ],
                    #     className='grid-item'
                    # ),
                ],
                className='grid-container-two-cols',
            ),

            # 4th row: 2 boxes
            html.Div(
                [
                    # left box
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
                                    'doubleClick': False
                                },
                                className='figure'
                            ),
                        ],
                        className='grid-item'
                    ),
                    # right box
                    html.Div(
                        [
                            # html.H6(
                            #     labels['variants_label'],
                            # ),
                            # dcc.Graph(
                            #     figure=variants_fig,
                            #     id='variants_fig',
                            #     responsive=True,
                            #     config={
                            #         'modeBarButtonsToRemove': modebar_buttons_to_remove,
                            #         'doubleClick': False
                            #     },
                            #     className='figure'
                            # ),
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
                                [labels['cases_vaccination_status_label']],
                            ),
                            dcc.Graph(
                                figure=cases_by_vaccination_status_fig,
                                id='cases_vaccination_status_fig',
                                responsive=True,
                                config={
                                    'modeBarButtonsToRemove': modebar_buttons_to_remove,
                                    'doubleClick': False
                                },
                                className='figure'
                            ),
                        ],
                        className='grid-item'
                    ),
                    # right box
                    html.Div(
                        [
                            html.H6(
                                [labels['hosp_vaccination_status_label']],
                            ),
                            dcc.Graph(
                                figure=hosp_by_vaccination_status_fig,
                                id='hosp_vaccination_status_fig',
                                responsive=True,
                                config={
                                    'modeBarButtonsToRemove': modebar_buttons_to_remove,
                                    'doubleClick': False
                                },
                                className='figure'
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
