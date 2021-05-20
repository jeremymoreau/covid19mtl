import dash_core_components as dcc
import dash_html_components as html

import app.figures as figures

from .core import (data_mtl_vaccination, data_qc_vaccination, data_qc_vaccination_age, data_vaccines, new_doses_mtl_1d,
                   new_doses_mtl_2d, new_doses_qc_1d, new_doses_qc_2d, perc_vacc_mtl_1d, perc_vacc_mtl_2d,
                   perc_vacc_qc_1d, perc_vacc_qc_2d, total_doses_mtl_1d, total_doses_mtl_2d, total_doses_qc_1d,
                   total_doses_qc_2d)


def generate_layout(labels):
    # Figures #####
    vaccination_fig = figures.vaccination_fig(data_qc_vaccination, data_mtl_vaccination, labels)
    vaccination_administered_fig = figures.vaccination_administered_fig(
        data_qc_vaccination, data_mtl_vaccination, labels
    )
    vaccine_delivery_fig = figures.vaccine_delivery_fig(data_vaccines, labels)
    vaccination_age_fig = figures.vaccination_age_fig(data_qc_vaccination_age, labels)

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
                                [labels['title'] + labels['vaccination_title']],
                                id='title',
                            ),
                            # subtitle
                            html.P(
                                [labels['vaccination_subtitle']],
                                id='subtitle',
                            ),
                        ],
                        id='title-container',
                    ),
                    html.Div(
                        [
                            html.A(labels['home_link_text'], href=labels['home_link'], className='nav-link'),
                            html.A(
                                labels['vaccination_link_text'],
                                href=labels['vaccination_link'],
                                className='nav-link active'
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

            # mini info boxes
            html.Div(
                [
                    # MTL
                    html.Div(
                        [html.P([f'{new_doses_mtl_1d:+d}' + labels['today']], className='superscript'),
                         html.H3(total_doses_mtl_1d, className='main_text'),
                         html.P([labels['vaccination_1d_mtl_label']], className='subscript')],
                        className='mini_container doses',
                    ),
                    html.Div(
                        [html.H3(f'{perc_vacc_mtl_1d:.2f}%', className='main_text'),
                         html.P([labels['vaccination_1d_perc_mtl_label']], className='subscript')],
                        className='mini_container vaccines',
                    ),
                    html.Div(
                        [html.P([f'{new_doses_mtl_2d:+d}' + labels['today']], className='superscript'),
                         html.H3(total_doses_mtl_2d, className='main_text'),
                         html.P([labels['vaccination_2d_mtl_label']], className='subscript')],
                        className='mini_container doses',
                    ),
                    html.Div(
                        [html.H3(f'{perc_vacc_mtl_2d:.2f}%', className='main_text'),
                         html.P([labels['vaccination_2d_perc_mtl_label']], className='subscript')],
                        className='mini_container vaccines',
                    ),
                    # QC
                    html.Div(
                        [html.P([f'{new_doses_qc_1d:+d}' + labels['today']], className='superscript'),
                         html.H3(total_doses_qc_1d, className='main_text'),
                         html.P([labels['vaccination_1d_qc_label']], className='subscript')],
                        className='mini_container doses',
                    ),
                    html.Div(
                        [html.H3(f'{perc_vacc_qc_1d:.2f}%', className='main_text'),
                         html.P([labels['vaccination_1d_perc_qc_label']], className='subscript')],
                        className='mini_container vaccines',
                    ),
                    html.Div(
                        [html.P([f'{new_doses_qc_2d:+d}' + labels['today']], className='superscript'),
                         html.H3(total_doses_qc_2d, className='main_text'),
                         html.P([labels['vaccination_2d_qc_label']], className='subscript')],
                        className='mini_container doses',
                    ),
                    html.Div(
                        [html.H3(f'{perc_vacc_qc_2d:.2f}%', className='main_text'),
                         html.P([labels['vaccination_2d_perc_qc_label']], className='subscript')],
                        className='mini_container vaccines',
                    ),
                ],
                id='info-container',
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
                                [labels['vaccination_label']]
                            ),
                            dcc.Graph(
                                figure=vaccination_fig,
                                id='vaccination_fig',
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
                className='grid-container-onethird-twothirds-cols',
            ),

            # 2nd row: 2 boxes
            html.Div(
                [
                    # left box
                    html.Div(
                        [
                            html.H6(
                                [labels['vaccination_administered_label']]
                            ),
                            dcc.Graph(
                                figure=vaccination_administered_fig,
                                id='vaccination_administered_fig',
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
                                [labels['vaccine_delivery_label']]
                            ),
                            dcc.Graph(
                                figure=vaccine_delivery_fig,
                                id='vaccine_delivery_fig',
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
            # html.Div(
            #     [
            #         # right box
            #         html.Div(
            #             [
            #                 html.H6(
            #                     [labels['vaccination_label']]
            #                 ),
            #                 dcc.Graph(
            #                     figure=vaccination_fig,
            #                     id='vaccination_fig',
            #                     responsive=True,
            #                     config={
            #                         'modeBarButtonsToRemove': modebar_buttons_to_remove,
            #                         'doubleClick': False
            #                     },
            #                     className='figure'
            #                 ),
            #             ],
            #             className='grid-item'
            #         ),
            #     ],
            #     className='grid-container-two-cols',
            # ),

            # row: 1 box
            html.Div(
                [
                    html.Div(
                        [
                            html.H6(
                                [labels['vaccination_age_label']]
                            ),
                            dcc.Graph(
                                figure=vaccination_age_fig,
                                id='vaccination_age_fig',
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
                className='grid-container-one-col',
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
        id='main-container',
        className='vaccination',
    )

    return layout
