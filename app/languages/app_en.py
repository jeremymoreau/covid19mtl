from ..core import latest_update_date, latest_vaccination_update_date
from ..template import generate_layout as build_home_layout
from ..template_vacc import generate_layout as build_vaccination_layout

# Label text (EN) #####
# TODO: Make markdown links open in new tab
labels = {
    'home_link': '/en',
    'home_link_text': 'Home',
    'vaccination_link': '/en/vaccination',
    'vaccination_link_text': 'Vaccination',
    'language0': 'Français',
    'language_link0': '/',
    'language1': 'Español',
    'language_link1': '/es',
    'language2': '中文',
    'language_link2': '/zh',
    'title': 'COVID-19 Montreal Dashboard',
    'vaccination_title': ': Vaccination',
    'subtitle': 'Last update: ' + latest_update_date,
    'vaccination_subtitle': 'Last update: ' + latest_vaccination_update_date.isoformat(),
    'today': ' today',
    'today_short': ' today',
    'cases_montreal_label': 'Cases (MTL)',
    'deaths_montreal_label': 'Deaths (MTL)',
    'cases_qc_label': 'Cases (QC)',
    'deaths_qc_label': 'Deaths (QC)',
    'hosp_mtl_label': 'New Hosp. (MTL)',
    'hosp_qc_label': 'New Hosp. (QC)',
    'icu': ' ICU today',
    'yesterday': ' yday',
    'vs_2dago': ' vs. 2 days ago',
    'vaccination_1d_mtl_label': '1st doses administered (MTL)',
    'vaccination_2d_mtl_label': '2nd doses administered (MTL)',
    'vaccination_3d_mtl_label': '3rd doses administered (MTL)',
    'vaccination_1d_perc_mtl_label': '% received 1 dose (MTL)',
    'vaccination_2d_perc_mtl_label': '% received 2 doses (MTL)',
    'vaccination_3d_perc_mtl_label': '% received 3 doses (MTL)',
    'vaccination_1d_qc_label': '1st doses administered (QC)',
    'vaccination_2d_qc_label': '2nd doses administered (QC)',
    'vaccination_3d_qc_label': '3rd doses administered (QC)',
    'vaccination_1d_perc_qc_label': '% received 1 dose (QC)',
    'vaccination_2d_perc_qc_label': '% received 2 doses (QC)',
    'vaccination_3d_perc_qc_label': '% received 3 doses (QC)',
    'doses_today': ' doses today',
    'test_pos_mtl_label': 'Test positivity rate (MTL)',
    'test_pos_qc_label': 'Test positivity rate (QC)',
    'incidence_per100k_7d_mtl_label': '7-day incid./100k (MTL)',
    'incidence_per100k_7d_qc_label': '7-day incid./100k (QC)',
    'vs_last7d': ' vs. prev. 7 days',
    'recovered_qc_label': 'Recovered (QC)',
    'recovered_mtl_label': 'Recovered (MTL)',
    'negative_tests_qc_box_label': 'Negative tests (QC)',
    'montreal_map_label': 'Cases per 100,000 population (Island of Montreal)',
    'total_cases_label': 'Confirmed cases',
    'age_group_label': 'Distribution of new cases across all age groups by week (MTL)',
    'total_deaths_label': 'Deaths (QC)',
    'total_hospitalisations_label': 'Hospitalisations (QC)',
    'intensive_care_label': 'Intensive Care (QC)',
    'total_testing_label': 'Diagnostic tests (QC)',
    # footer
    'footer_left': 'Data: [Santé Montréal](https://santemontreal.qc.ca/en/public/coronavirus-covid-19/), [INSPQ](https://www.inspq.qc.ca/covid-19/donnees), [Government of Québec](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/) / Built with [Dash](https://plotly.com/dash/) / [Github](https://github.com/jeremymoreau/covid19mtl)',
    'footer_centre': 'Hosting sponsored by [DigitalOcean](https://www.digitalocean.com/community/pages/covid-19)',
    'footer_right': 'Made by [Jeremy Moreau](https://jeremymoreau.com/), [Matthias Schoettle](https://mattsch.com), and [Contributors](https://github.com/jeremymoreau/covid19mtl#contributors) / [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)',
    'infobox': """
    ###### Useful resources

    - [COVID-19 Symptom Self-Assessment Tool](https://ca.thrive.health/covid19/en)
    - [Quebec Vaccination Campaign &ndash; Appointments](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/progress-of-the-covid-19-vaccination/)
    - [Santé Montréal](https://santemontreal.qc.ca/en/public/coronavirus-covid-19/)
    - [Public health expertise and reference centre (French only)](https://www.inspq.qc.ca/covid-19/donnees)
    - [Coronavirus disease (COVID-19) in Quebec](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/)
    - [COVID-19 Government of Canada](https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19.html)

    If you are worried about COVID-19 or display symptoms such as a cough or fever, you can call toll free (514) 644-4545 in the Montreal area, (418) 644-4545 in the Quebec City region, and 1 (877) 644-4545 elsewhere in Quebec.
    """,
    'montreal_map_colourbar_labels': {
        'date': 'Date',
        'borough': 'Borough/City',
        '7day_incidence_rate': '7-day incidence rate',
        'new_cases': 'New cases',
        'cases': 'Total cases',
        '7day_incidence_per100k': '7-day incidence per 100,000',
        '7day_incidence': '7-day incidence',
    },
    'montreal_map_legend_title': '<b>7-day incidence per 100,000</b>',
    'montreal_map_hovertemplate': '<b>%{hovertext}</b><br><br>Date=%{customdata[5]}<br>7-day incidence=%{customdata[0]}<br>7-day incidence per 100,000=%{customdata[1]}<br>Total cases=%{customdata[4]}<br>New cases=%{customdata[6]}<extra></extra>',
    '7day_avg_short': '7-day mov avg',
    '7day_avg_qc_label': '7-day moving avg (QC)',
    '7day_avg_mtl_label': '7-day moving avg (MTL)',
    # confirmed cases fig
    'confirmed_cases_y_label': 'New cases',
    'confirmed_cases_y2_label': 'Active cases',
    'active_cases_qc_label': 'Active cases (QC)',
    'new_cases_qc_label': 'New cases (QC)',
    'new_cases_mtl_label': 'New cases (MTL)',
    # age groups
    'age_total_label': 'Distribution of total<br>cases across age groups',
    'age_per100000_label': 'Distribution of cases per<br>100,000 population in age group',
    'age_fig_hovertemplate': '%: %{y}',
    # deaths fig
    'deaths_fig_label': 'Deaths',
    'deaths_qc_y_label': 'New deaths',
    'deaths_qc_y2_label': 'New deaths (7-day moving average)',
    'new_deaths_qc_label': 'New deaths (QC)',
    'new_deaths_mtl_label': 'New deaths (MTL)',
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
    'date_slider_label': 'Date: ',
    'date_label': 'Date',
    'age_label': 'Age',
    'week_label': 'Week',
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
    'cases_vs_newcases_hovertemplate': 'Date: %{customdata} <br> New Cases: %{y}',
    # Vaccination_fig
    'vaccination_label': 'Vaccination Progress',
    'vaccination_y': 'Doses (cumulative)',
    'vaccination_new': 'New doses',
    'vaccination_total': 'Doses administered',
    'vaccination_total_2d': 'Doses administered (2nd dose)',
    'vaccination_total_3d': 'Doses administered (3rd dose)',
    'vaccination_perc': '% of pop received at least 1 dose',
    'vaccination_perc_2d': '% of pop received 2 doses',
    'vaccination_total_mtl': 'Doses administered (MTL)',
    'vaccination_perc_mtl': '% of pop vaccinated (MTL)',
    'vaccination_perc_qc': '% of pop vaccinated (QC)',
    'vaccination_hovertemplate': 'Doses administered: %{y:,d}<br>Doses available: %{customdata[0]:,d}<br>% of pop received 1 dose: %{customdata[1]:.2f}%',
    'vaccination_hovertemplate_mtl': 'Doses administered: %{y:,d}<br>% of pop received 1 dose: %{customdata[0]:.2f}%',
    'vaccination_administered_hovertemplate': 'Doses administered: %{y:,d}<br>Doses available: %{customdata[0]:,d}',
    'vaccination_new_mtl': 'New doses (MTL)',
    'vaccination_new_qc': 'New doses (QC)',
    # Vaccination administered fig
    'vaccination_administered_label': 'New doses administered',
    'vaccination_new_y': 'New doses (7-day moving average)',
    'vaccination_new_1d': 'New 1st doses',
    'vaccination_new_2d': 'New 2nd doses',
    'vaccination_new_3d': 'New 3rd doses',
    # Vaccine delivery fig
    'vaccine_delivery_label': 'Vaccine doses delivered vs. administered',
    'vaccine_received': 'Doses received',
    'vaccine_administered': 'Doses administered',
    'vaccine_available': 'Doses available',
    'vaccine_received_hovertemplate': 'Doses received: %{y:,d}<br>New doses received: %{customdata:,d}',
    # Vaccination_age_fig
    'vaccination_age_label': 'Vaccination by age group',
    'vaccination_categories': ['Not vaccinated', '1 dose received', '2 doses received', '3 doses received'],
    # New cases by vaccination status figure
    'cases_vaccination_status_label': 'New cases by vaccination status (QC)',
    'cases_vaccination_status_y': 'New cases per 100,000 (7-day moving average)',
    # New hospitalisations by vaccination status figure
    'hosp_vaccination_status_label': 'New hospitalisations by vaccination status (QC)',
    'hosp_vaccination_status_y': 'New hospitalisations per 100,000 (7-day moving average)',
    # Vaccination status categories
    'vaccination_unvaccinated': 'Unvaccinated or 1 dose < 14 days',
    'vaccination_1d': '1 dose ≥ 14 days',
    'vaccination_2d': '2 doses ≥ 7 days',
    # Variants fig
    'variants_label': 'Progression of new variants of concern (VOC)',
    'variants_sequenced': 'Sequenced cases',
    'variants_presumptive': 'Presumptive cases',
    'variants_new_presumptive': 'New presumptive cases',
    'variants_new_sequenced': 'New sequenced cases',
    'variants_new_cases': 'Total new cases',
    'variants_pos_rate': 'Percent positivity',
    'variants_pos_rate_avg': 'Percent positivity (7-day mov avg)',
    'variants_screened': 'Screened samples',
    'variants_y2': 'Cases (cumulative)',
    'variants_y3': 'Percent Positivity',
    # Range sliders
    '14d': '14d',
    '1m': '1m',
    '3m': '3m',
    '6m': '6m',
    'ytd': 'YTD',
    '1y': '1y',
    'all': 'all'
}

layout = build_home_layout(labels)
layout_vaccination = build_vaccination_layout(labels)
