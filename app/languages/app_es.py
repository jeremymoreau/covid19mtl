from ..core import latest_update_date
from ..template import generate_layout

# Label text (EN) #####
# TODO: Make markdown links open in new tab
labels = {
    'language0': 'Français',
    'language_link0': '/',
    'language1': 'English',
    'language_link1': '/en',
    'language2': '中文',
    'language_link2': '/zh',
    'title': 'Información de COVID-19 en Montreal',
    'subtitle': 'Última actualización: ' + latest_update_date,
    'today': ' today',
    'today_short': ' today',
    'cases_montreal_label': 'Casos (MTL)',
    'deaths_montreal_label': 'Muertes (MTL)',
    'cases_qc_label': 'Casos (QC)',
    'deaths_qc_label': 'Muertes (QC)',
    'hosp_mtl_label': 'New Hosp. (MTL)',
    'hosp_qc_label': 'New Hosp. (QC)',
    'icu': ' ICU today',
    'yesterday': ' yday',
    'vs_2dago': ' vs. 2 days ago',
    'vaccination_perc_mtl_label': '% received 1 dose (MTL)',
    'vaccination_perc_qc_label': '% received 1 dose (QC)',
    'doses_today': ' doses today',
    'test_pos_mtl_label': 'Test positivity rate (MTL)',
    'test_pos_qc_label': 'Test positivity rate (QC)',
    'incidence_per100k_7d_mtl_label': '7-day incidence per 100k (MTL)',
    'incidence_per100k_7d_qc_label': '7-day incidence per 100k (QC)',
    'vs_last7d': ' vs. prev. 7 days',
    'recovered_qc_label': 'Recuperados (QC)',
    'negative_tests_qc_box_label': 'Pruebas negativas (QC)',
    'montreal_map_label': 'Casos por cada 100 000 habitantes (Isla de Montreal)',
    'total_cases_label': 'Casos confirmados',
    'age_group_label': 'Casos por grupo de edad (MTL)',
    'total_deaths_label': 'Muertes (QC)',
    'total_hospitalisations_label': 'Hospitalizaciones (QC)',
    'intensive_care_label': 'Cuidados intensivos (QC)',
    'total_testing_label': 'Pruebas diagnósticas (QC)',
    # footer
    'footer_left': 'Datos: [Santé Montréal](https://santemontreal.qc.ca/en/public/coronavirus-covid-19/), [INSPQ](https://www.inspq.qc.ca/covid-19/donnees), [Gobierno de Québec](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/) / Construido con [Dash](https://plotly.com/dash/) / [Github](https://github.com/jeremymoreau/covid19mtl)',
    'footer_centre': 'Patrocinado por [DigitalOcean](https://www.digitalocean.com/community/pages/covid-19)',
    'footer_right': 'Hecho por [Jeremy Moreau](https://jeremymoreau.com/), [Matthias Schoettle](https://mattsch.com), [Colaboradores](https://github.com/jeremymoreau/covid19mtl#contributors) / [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.est)',
    'infobox': """
    ###### Enlaces importantes

    - [Herramienta de autoevaluación de síntomas COVID-19 (inglés y francés)](https://ca.thrive.health/covid19/en)
    - [Información de COVID-19 para Montreal (inglés y francés)](https://santemontreal.qc.ca/en/public/coronavirus-covid-19/)
    - [Centro de experiencia y de consulta en salud pública (sólo francés)](https://www.inspq.qc.ca/covid-19/donnees)
    - [La enfermedad del coronavirus (COVID-19) en Quebec (inglés y francés)](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/)
    - [Gobierno de Canadá: COVID-19 (inglés y francés)](https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19.html)

    Si está preocupado por el COVID-19 o presenta síntomas como tos o fiebre, llame sin costo al (514) 644-4545 en el área de Montreal, al (418) 644-4545 en la región de la Ciudad de Quebec y al 1 (877) 644-4545 en cualquier otra parte de la Provincia de Quebec.
    """,
    'montreal_map_colourbar_labels': {
        'date': 'Fecha',
        'borough': 'Vecindario/Ciudad',
        '7day_incidence_rate': 'Tasa de incidencia de 7 días',
        'new_cases': 'Nuevos casos',
        'cases': 'Casos',
        '7day_incidence_per100k': 'Incidencia de 7 días por 100 000',
        '7day_incidence': 'Incidencia de 7 días',
    },
    'montreal_map_legend_title': '<b>Incidencia de 7 días por 100 000</b>',
    'montreal_map_hovertemplate': '<br>Vecindario/Ciudad: %{location}<br>Incidencia de 7 días por 100 000: %{z}',
    '7day_avg_qc_label': '7-day moving avg (QC)',
    '7day_avg_mtl_label': '7-day moving avg (MTL)',
    # confirmed cases fig
    'confirmed_cases_y_label': 'Casos nuevos',
    'confirmed_cases_y2_label': 'Casos activos',
    'active_cases_qc_label': 'Casos activos (QC)',
    'new_cases_qc_label': 'Casos nuevos (QC)',
    'new_cases_mtl_label': 'Casos nuevos (MTL)',
    'age_total_label': 'Distribución del total<br>de casos en el grupo de edad',
    'age_per100000_label': 'Distribución de casos por cada<br>100,000 habitantes en el grupo de edad',
    'age_fig_hovertemplate': '%: %{y}',
    # deaths fig
    'deaths_fig_label': 'Muertes',
    'deaths_qc_y_label': 'Nuevas muertes',
    'deaths_qc_y2_label': 'New deaths (7-day moving average)',
    'new_deaths_qc_label': 'Nuevas muertes (QC)',
    'new_deaths_mtl_label': 'Nuevas muertes (MTL)',
    # hospitalisations fig
    'hospitalisations_label': 'Hospitalisations',
    'hospitalisations_y_label': 'Active hospitalisations',
    'hospitalisations_y2_label': 'New hospitalisations (7-day moving average)',
    'intensive_care_qc': 'New intensive care admissions (QC)',
    'intensive_care_mtl': 'New intensive care admissions (MTL)',
    'hospitalisations_qc': 'New hospitalisations (QC)',
    'hospitalisations_active_qc': 'Active hospitalisations (QC)',
    'intensive_care_active_qc': 'Active ICU hospitalisations (QC)',
    'hospitalisations_mtl': 'New hospitalisations(MTL)',
    # Test positivity fig
    'testing_label': 'Test positivity rate',
    'testing_y_label': 'Test positivity rate',
    'testing_y2_label': 'Tests performed',
    'testing_tests_qc': 'Tests performed (QC)',
    'testing_tests_mtl': 'Tests performed (MTL)',
    'testing_hovertemplate_qc': '<b>Quebec</b><br>7-day moving avg: %{y:,.2f}%<br>Test positivity: %{customdata:,.2f}%',
    'testing_hovertemplate_mtl': '<b>Montreal</b><br>7-day moving avg: %{y:,.2f}%<br>Test positivity: %{customdata:,.2f}%',
    #
    'date_slider_label': 'Fecha: ',
    'date_label': 'Fecha',
    'age_label': 'Edad',
    'linear_label': 'Escala lineal',
    'log_label': 'Escala logarítmica',
    # Confirmed deaths by place of residence (MTL) fig
    'deaths_loc_fig_mtl_label': 'Muertes por lugar de residencia (MTL)',
    'deaths_loc_fig_mtl_pie_labels': [
        'Hospital',
        'Centros de cuidado<br>a largo plazo (CHSLD)',
        'Hogar',
        'Centro de atención<br>intermedio',
        'Casa hogar para<br>adultos mayores',
        'Otro',
        'Desconocido'
    ],
    # Confirmed deaths by place of residence (QC) fig
    'deaths_loc_fig_qc_label': 'Muertes por lugar de residencia (QC)',
    'chsld_label': 'Centros de cuidado<br>a largo plazo (CHSLD)',
    'psr_label': 'Casa hogar para adultos mayores',
    'home_label': 'Hogar',
    'other_or_unknown_label': 'Otro o desconocido',
    'deaths_loc_fig_qc_y_label': 'Muertes (acumulativo, QC)',
    # Cases vs New Cases fig
    'cases_vs_newcases_label': 'New cases vs. cumulative total confirmed cases',
    'cases_vs_newcases_xlabel': 'Cumulative total confirmed cases (log)',
    'cases_vs_newcases_ylabel': 'New cases (log)',
    'cases_vs_newcases_legend_mtl': 'Montreal',
    'cases_vs_newcases_legend_qc': 'Quebec',
    'cases_vs_newcases_hovertemplate': 'Date: %{customdata} <br> New Cases: %{y}',
    # Vaccination_fig
    'vaccination_label': 'Vaccination',
    'vaccination_y': 'Doses (cumulative)',
    'vaccination_y2': 'New doses',
    'vaccination_total_received_qc': 'Doses received (QC)',
    'vaccination_total_qc': 'Doses administered (QC)',
    'vaccination_total_mtl': 'Doses administered (MTL)',
    'vaccination_perc_mtl': '% of pop received 1 dose (MTL)',
    'vaccination_perc_qc': '% of pop received 1 dose (QC)',
    'vaccination_hovertemplate': 'Doses administered: %{y:,d}<br>% vaccinated: %{customdata[0]:.2f}%',
    'vaccination_received_hovertemplate': 'Doses received: %{y:,d}<br>New doses received: %{customdata:,d}',
    'vaccination_new_mtl': 'New doses (MTL)',
    'vaccination_new_qc': 'New doses (QC)',
    # Variants fig
    'variants_sequenced': 'Sequenced cases',
    'variants_presumptive': 'Presumptive cases',
    'variants_new_presumptive': 'New presumptive cases',
    'variants_new_sequenced': 'New sequenced cases',
    'variants_new_cases': 'Total new cases',
    'variants_y2': 'Cases',
    # Range sliders
    '14d': '14d',
    '1m': '1m',
    '3m': '3m',
    '6m': '6m',
    'ytd': 'YTD',
    '1y': '1y',
    'all': 'all'
}

layout = generate_layout(labels)
