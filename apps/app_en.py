from app import latest_update_date
from template import generate_layout

##### Label text (EN) #####
# TODO: Make markdown links open in new tab
labels = {
    'language' : u'Français',
    'language_link' : '/',
    'title' : 'COVID-19 Montreal Dashboard',
    'subtitle' : 'Last update: ' + latest_update_date,
    'cases_montreal_label' : 'Cases (Montreal)',
    'cases_qc_label' : 'Cases (QC)',
    'deaths_qc_label' : 'Deaths (QC)',
    'recovered_qc_label' : 'Recovered (QC)',
    'montreal_map_label' : 'Cases per 1000 population (Island of Montreal)',
    'total_cases_label' : 'Confirmed cases',
    'age_group_label' : 'Cases by age group',
    'total_deaths_label' : 'Deaths (QC)',
    'total_hospitalisations_label': 'Hospitalisations (QC)',
    'total_testing_label' : 'Diagnostic tests (QC)',
    'footer_left' : u'Data: [Santé Montréal](https://santemontreal.qc.ca/en/public/coronavirus-covid-19/), [INSPQ](https://www.inspq.qc.ca/covid-19/donnees) / Built with [Dash](https://plotly.com/dash/)',
    'footer_right' : 'Made by [Jeremy Moreau](https://jeremymoreau.com/) ([RI-MUHC](https://rimuhc.ca/), McGill) / [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)',
    'infobox' : u"""
    #### Useful resources
    
    - [COVID-19 Symptom Self-Assessment Tool](https://ca.thrive.health/covid19/en)
    - [Santé Montréal](https://santemontreal.qc.ca/en/public/coronavirus-covid-19/)
    - [Public health expertise and reference centre (French only)](https://www.inspq.qc.ca/covid-19/donnees)
    - [Coronavirus disease (COVID-19) in Quebec](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/)
    - [COVID-19 Government of Canada](https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19.html)
    - [Flatten.ca](https://flatten.ca/)

    If you are worried about COVID-19 or display symptoms such as a cough or fever, you can call toll free (514) 644-4545 in the Montreal area, (418) 644-4545 in the Quebec City region, and 1 (877) 644-4545 elsewhere in Quebec.
    """,
    'montreal_map_colourbar_labels' : {
                                        'date': 'Date', 
                                        'borough': 'Borough/City',
                                        'cases_per_1000': 'Cases per 1000<br>population'
                                        },
    'montreal_map_hovertemplate' : '<br>Borough/City: %{location}<br>Cases per 1000 population: %{z}',
    'confirmed_cases_y_label' : 'Confirmed cases (cumulative)',
    'confirmed_cases_qc_label' : 'Quebec',
    'confirmed_cases_mtl_label' : 'Montreal',
    'age_total_label' : 'Distribution of total<br>cases across age groups',
    'age_per100000_label' : 'Distribution of cases per<br>100,000 population in age group',
    'age_fig_hovertemplate' : '%: %{y}',
    'deaths_qc_y_label' : 'Deaths (cumulative, QC)',
    'hospitalisations_y_label' : 'Hospitalisations (cumulative, QC)',
    'hospitalisations_label' : 'Hospitalisations (QC)',
    'intensive_care_label' : 'Intensive Care (QC)',
    'testing_qc_y_label' : 'Cases (cumulative, QC)',
    'negative_tests_qc_label' : 'Negative tests (QC)',
    'positive_cases_qc_label' : 'Confirmed positive cases (QC)',
    'date_slider_label' : 'Date: ',
    'date_label' : 'Date',
    'age_label' : 'Age'
}

layout = generate_layout(labels)
