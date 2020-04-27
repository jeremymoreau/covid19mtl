from app import latest_update_date
from template import generate_layout

##### Label text (EN) #####
# TODO: Make markdown links open in new tab
labels = {
    'language0' : 'Français',
    'language_link0' : '/',
    'language1' : 'English',
    'language_link1' : '/en',
    'language2' : '中文',
    'language_link2' : '/zh',
    'title' : 'Información de COVID-19 en Montreal',
    'subtitle' : 'Última actualización: ' + latest_update_date,
    'cases_montreal_label' : 'Casos (Montreal)',
    'deaths_montreal_label' : 'Muertes (Montreal)',
    'cases_qc_label' : 'Casos (QC)',
    'deaths_qc_label' : 'Muertes (QC)',
    'recovered_qc_label' : 'Recuperados (QC)',
    'montreal_map_label' : 'Casos por cada 1000 habitantes (Isla de Montreal)',
    'total_cases_label' : 'Casos confirmados',
    'age_group_label' : 'Casos por grupo de edad',
    'total_deaths_label' : 'Muertes (QC)',
    'total_hospitalisations_label': 'Hospitalizaciones (QC)',
    'total_testing_label' : 'Pruebas diagnósticas (QC)',
    'footer_left' : 'Datos: [Santé Montréal](https://santemontreal.qc.ca/en/public/coronavirus-covid-19/), [INSPQ](https://www.inspq.qc.ca/covid-19/donnees) / Construido con [Dash](https://plotly.com/dash/) / [Github](https://github.com/jeremymoreau/covid19mtl)',
    'footer_right' : 'Hecho por [Jeremy Moreau](https://jeremymoreau.com/) ([RI-MUHC](https://rimuhc.ca/), McGill) / [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)',
    'infobox' : """
    ###### Enlaces importantes
    
    - [Herramienta de autoevaluación de síntomas COVID-19 (inglés y francés)](https://ca.thrive.health/covid19/en)
    - [Información de COVID-19 para Montreal (inglés y francés)](https://santemontreal.qc.ca/en/public/coronavirus-covid-19/)
    - [Centro de experiencia y de consulta en salud pública (sólo francés)](https://www.inspq.qc.ca/covid-19/donnees)
    - [La enfermedad del coronavirus (COVID-19) en Quebec (inglés y francés)](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/)
    - [Gobierno de Canadá: COVID-19 (inglés y francés)](https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19.html)
    - [Flatten.ca: auto-reporte de estado de salud (inglés y francés)](https://flatten.ca/)

    Si se encuentra preocupado por el COVID-19 o presenta síntomas como tos o fiebre, llame sin costo al (514) 644-4545 en el área de Montreal, al (418) 644-4545 en la región de la Ciudad de Quebec y al 1 (877) 644-4545 en cualquier otra parte de la Provincia de Quebec.
    """,
    'montreal_map_colourbar_labels' : {
                                        'date': 'Fecha', 
                                        'borough': 'Vecindario/Ciudad',
                                        'cases_per_1000': 'Casos por cada 1000<br>habitantes'
                                        },
    'montreal_map_hovertemplate' : '<br>Vecindario/Ciudad: %{location}<br>Casos por cada 1000 habitantes: %{z}',
    'confirmed_cases_y_label' : 'Casos confirmados',
    'confirmed_cases_qc_label' : 'Quebec (acumulativo)',
    'confirmed_cases_mtl_label' : 'Montreal (acumulativo)',
    'active_cases_qc_label' : 'Quebec (casos activos)',
    'new_confirmed_cases_qc_label' : 'Quebec (casos nuevos)',
    'new_confirmed_cases_mtl_label' : 'Montreal (casos nuevos)',
    'age_total_label' : 'Distribución del total<br>de casos en el grupo de edad',
    'age_per100000_label' : 'Distribución de casos por cada<br>100,000 habitantes en el grupo de edad',
    'age_fig_hovertemplate' : '%: %{y}',
    'deaths_fig_label' : 'Muertes',
    'deaths_qc_y_label' : 'Muertes',
    'deaths_fig_qc_label' : 'Quebec (acumulativo)',
    'deaths_fig_mtl_label' : 'Montreal (acumulativo)',
    'new_deaths_qc_label' : 'Quebec (nuevas muertes)',
    'new_deaths_mtl_label' : 'Montreal (nuevas muertes)',
    'hospitalisations_y_label' : 'Hospitalizaciones (QC)',
    'hospitalisations_label' : 'Hospitalizaciones (QC)',
    'intensive_care_label' : 'Cuidados intensivos (QC)',
    'testing_qc_y_label' : 'Casos (QC)',
    'negative_tests_qc_label' : 'Pruebas negativas (acumulativo)',
    'new_negative_tests_qc_label' : 'Pruebas negativas (casos nuevos)',
    'positive_cases_qc_label' : 'Casos positivos confirmados (acumulativo)',
    'date_slider_label' : 'Fecha: ',
    'date_label' : 'Fecha',
    'age_label' : 'Edad',
    'linear_label' : 'Escala lineal',
    'log_label' : 'Escala logarítmica'
}

layout = generate_layout(labels)
