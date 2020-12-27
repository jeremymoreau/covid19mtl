from ..core import latest_update_date
from ..template import generate_layout

# Label text (EN) #####
# TODO: Make markdown links open in new tab
labels = {
    'language0': 'Français',
    'language_link0': '/',
    'language1': 'Español',
    'language_link1': '/es',
    'language2': '中文',
    'language_link2': '/zh',
    'title': 'COVID-19 Montreal Dashboard',
    'subtitle': 'Last update: ' + latest_update_date,
    'cases_montreal_label': 'Cases (Montreal)',
    'deaths_montreal_label': 'Deaths (Montreal)',
    'cases_qc_label': 'Cases (QC)',
    'deaths_qc_label': 'Deaths (QC)',
    'recovered_qc_label': 'Recovered (QC)',
    'negative_tests_qc_box_label': 'Negative tests (QC)',
    'montreal_map_label': 'Cases per 100,000 population (Island of Montreal)',
    'total_cases_label': 'Confirmed cases',
    'age_group_label': 'Cases by age group (MTL)',
    'total_deaths_label': 'Deaths (QC)',
    'total_hospitalisations_label': 'Hospitalisations (QC)',
    'total_testing_label': 'Diagnostic tests (QC)',
    # footer
    'footer_left': 'Data: [Santé Montréal](https://santemontreal.qc.ca/en/public/coronavirus-covid-19/), [INSPQ](https://www.inspq.qc.ca/covid-19/donnees) / Built with [Dash](https://plotly.com/dash/) / [Github](https://github.com/jeremymoreau/covid19mtl)',
    'footer_centre': 'Hosting sponsored by [DigitalOcean](https://www.digitalocean.com/community/pages/covid-19)',
    'footer_right': 'Made by [Jeremy Moreau](https://jeremymoreau.com/), [Matthias Schoettle](https://mattsch.com), and [Contributors](https://github.com/jeremymoreau/covid19mtl#contributors) / [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)',
    'infobox': """
    ###### Useful resources

    - [COVID-19 Symptom Self-Assessment Tool](https://ca.thrive.health/covid19/en)
    - [Santé Montréal](https://santemontreal.qc.ca/en/public/coronavirus-covid-19/)
    - [Public health expertise and reference centre (French only)](https://www.inspq.qc.ca/covid-19/donnees)
    - [Coronavirus disease (COVID-19) in Quebec](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/)
    - [COVID-19 Government of Canada](https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19.html)
    - [Flatten.ca](https://flatten.ca/)

    If you are worried about COVID-19 or display symptoms such as a cough or fever, you can call toll free (514) 644-4545 in the Montreal area, (418) 644-4545 in the Quebec City region, and 1 (877) 644-4545 elsewhere in Quebec.
    """,
    'montreal_map_colourbar_labels': {
        'date': 'Date',
        'borough': 'Borough/City',
        'cases_per_100_000': 'Cases per 100,000<br>population'
    },
    'montreal_map_hovertemplate': '<br>Borough/City: %{location}<br>Cases per 100,000 population: %{z}',
    'confirmed_cases_y_label': 'Confirmed cases',
    'confirmed_cases_qc_label': 'Quebec (cumulative)',
    'active_cases_qc_label': 'Quebec (active cases)',
    'confirmed_cases_mtl_label': 'Montreal (cumulative)',
    'new_confirmed_cases_qc_label': 'Quebec (new cases)',
    'new_confirmed_cases_mtl_label': 'Montreal (new cases)',
    'age_total_label': 'Distribution of total<br>cases across age groups',
    'age_per100000_label': 'Distribution of cases per<br>100,000 population in age group',
    'age_fig_hovertemplate': '%: %{y}',
    'deaths_fig_label': 'Deaths',
    'deaths_qc_y_label': 'Deaths',
    'deaths_fig_qc_label': 'Quebec (cumulative)',
    'deaths_fig_mtl_label': 'Montreal (cumulative)',
    'new_deaths_qc_label': 'Quebec (new deaths)',
    'new_deaths_mtl_label': 'Montreal (new deaths)',
    'hospitalisations_y_label': 'Hospitalisations (QC)',
    'hospitalisations_label': 'Hospitalisations (QC)',
    'intensive_care_label': 'Intensive Care (QC)',
    'testing_qc_y_label': 'Cases (QC)',
    'negative_tests_qc_label': 'Negative tests (cumulative)',
    'new_negative_tests_qc_label': 'Negative tests (new cases)',
    'positive_cases_qc_label': 'Confirmed positive cases (cumulative)',
    'date_slider_label': 'Date: ',
    'date_label': 'Date',
    'age_label': 'Age',
    'linear_label': 'Linear scale',
    'log_label': 'Log scale',
    # Confirmed deaths by place of residence (MTL) fig
    'deaths_loc_fig_mtl_label': 'Deaths by place of residence (MTL)',
    'deaths_loc_fig_mtl_pie_labels': [
        'Hospital',
        'Long-term care<br>centres (CHSLD)',
        'Home',
        'Intermediate resource',
        "Private seniors' residence",
        'Other',
        'Unknown'
    ],
    # Confirmed deaths by place of residence (QC) fig
    'deaths_loc_fig_qc_label': 'Deaths by place of residence (QC)',
    'chsld_label': 'Long-term care<br>centres (CHSLD)',
    'psr_label': "Private seniors' residence",
    'home_label': 'Home',
    'other_or_unknown_label': 'Other or unknown',
    'deaths_loc_fig_qc_y_label': 'Deaths (cumulative, QC)',
    # Cases vs New Cases fig
    'cases_vs_newcases_label': 'New cases vs. cumulative total confirmed cases',
    'cases_vs_newcases_xlabel': 'Cumulative total confirmed cases (log)',
    'cases_vs_newcases_ylabel': 'New cases (log)',
    'cases_vs_newcases_legend_mtl': 'Montreal',
    'cases_vs_newcases_legend_qc': 'Quebec',
    'cases_vs_newcases_hovertemplate': 'Date: %{customdata} <br> New Cases: %{y}'
}

layout = generate_layout(labels)
