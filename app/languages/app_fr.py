from ..core import latest_update_date, latest_vaccination_update_date
from ..template import generate_layout as build_home_layout
from ..template_vacc import generate_layout as build_vaccination_layout

# Label text (FR) #####
# TODO: Make markdown links open in new tab
labels = {
    'home_link': '/fr',
    'home_link_text': 'Accueil',
    'vaccination_link': '/fr/vaccination',
    'vaccination_link_text': 'Vaccination',
    'language0': 'English',
    'language_link0': '/en',
    'language1': 'Español',
    'language_link1': '/es',
    'language2': '中文',
    'language_link2': '/zh',
    'title': ' Tableau de bord COVID-19 Montréal',
    'vaccination_title': ': Vaccination',
    'subtitle': 'Dernière mise à jour: ' + latest_update_date,
    'vaccination_subtitle': 'Dernière mise à jour: ' + latest_vaccination_update_date.isoformat(),
    'today': " aujourd'hui",
    'today_short': ' auj.',
    'cases_montreal_label': 'Cas (MTL)',
    'deaths_montreal_label': 'Décès (MTL)',
    'cases_qc_label': 'Cas (QC)',
    'deaths_qc_label': 'Décès (QC)',
    'hosp_mtl_label': 'Nouv. Hosp. (MTL)',
    'hosp_qc_label': 'Nouv. Hosp. (QC)',
    'icu': ' soins intensifs auj.',
    'yesterday': ' hier',
    'vs_2dago': ' vs. 2 jours préc.',
    'vaccination_1d_mtl_label': '1ère doses administrées (MTL)',
    'vaccination_2d_mtl_label': '2ème doses administrées (MTL)',
    'vaccination_3d_mtl_label': '3ème doses administrées (MTL)',
    'vaccination_1d_perc_mtl_label': '% 1 dose reçue (MTL)',
    'vaccination_2d_perc_mtl_label': '% 2 doses reçues (MTL)',
    'vaccination_3d_perc_mtl_label': '% 3 doses reçues (MTL)',
    'vaccination_1d_qc_label': '1ère doses administrées (QC)',
    'vaccination_2d_qc_label': '2ème doses administrées (QC)',
    'vaccination_3d_qc_label': '3ème doses administrées (QC)',
    'vaccination_1d_perc_qc_label': '% 1 dose reçue (QC)',
    'vaccination_2d_perc_qc_label': '% 2 doses reçues (QC)',
    'vaccination_3d_perc_qc_label': '% 3 doses reçues (QC)',
    'doses_today': ' doses auj.',
    'test_pos_mtl_label': 'Positivité des tests (MTL)',
    'test_pos_qc_label': 'Positivité des tests (QC)',
    'incidence_per100k_7d_mtl_label': 'Incid./100k 7 jours (MTL)',
    'incidence_per100k_7d_qc_label': 'Incid./100k 7 jours (QC)',
    'vs_last7d': ' vs. 7 jours préc.',
    'recovered_qc_label': 'Rétablis (QC)',
    'recovered_mtl_label': 'Rétablis (MTL)',
    'negative_tests_qc_box_label': 'Analyses négatives (QC)',
    'montreal_map_label': 'Cas pour 100 000 habitants (Île de Montréal)',
    'total_cases_label': 'Cas confirmés',
    'age_group_label': "Répartition des nouveaux cas parmi les groupes d'âge par semaine (MTL)",
    'total_deaths_label': 'Décès (QC)',
    'total_hospitalisations_label': 'Hospitalisations (QC)',
    'intensive_care_label': 'Soins Intensifs (QC)',
    'total_testing_label': 'Tests diagnostiques (QC)',
    # footer
    'footer_left': 'Données: [Santé Montréal](https://santemontreal.qc.ca/population/coronavirus-covid-19/), [INSPQ](https://www.inspq.qc.ca/covid-19/donnees), [Gouvernement du Québec](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/) / Créé avec [Dash](https://plotly.com/dash/) / [Github](https://github.com/jeremymoreau/covid19mtl)',
    'footer_centre': 'Hébergement offert par [DigitalOcean](https://www.digitalocean.com/community/pages/covid-19)',
    'footer_right': 'Créé par [Jeremy Moreau](https://jeremymoreau.com/), [Matthias Schoettle](https://mattsch.com) et [Contributeurs](https://github.com/jeremymoreau/covid19mtl#contributors) / [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.fr)',
    'datanote': '**Note :** Les jeux de données de l\'INSPQ ne sont mis à jour qu\'une fois par semaine, le mercredi. Les boîtes d\'information ci-dessous montrent donc la différence avec la semaine précédente. Santé Montréal n\'a pas mis à jour ses jeux de données depuis juillet.',
    'infobox': """
    ###### Ressources utiles

    - [Outil d'auto-évaluation des symptômes COVID-19](https://ca.thrive.health/covid19/fr)
    - [Campagne de vaccination du Québec &ndash; Rendez-vous](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/deroulement-vaccination-contre-la-covid-19/)
    - [Santé Montréal](https://santemontreal.qc.ca/population/coronavirus-covid-19/)
    - [Centre d'expertise et de référence en santé publique](https://www.inspq.qc.ca/covid-19/donnees)
    - [La maladie à coronavirus (COVID-19) au Québec](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/)
    - [COVID-19 Gouvernement du Canada](https://www.canada.ca/fr/sante-publique/services/maladies/maladie-coronavirus-covid-19.html)

    Si la COVID-19 vous inquiète ou si vous présentez des symptômes comme de la toux ou de la fièvre, vous pouvez contacter, sans frais, le (514) 644-4545 pour la région de Montréal,  le (418) 644-4545 pour la région de Québec et le 1 (877) 644-4545 ailleurs au Québec.
    """,
    'montreal_map_colourbar_labels': {
        'date': 'Date',
        'borough': 'Arrondissement/Ville',
        '7day_incidence_rate': "Taux d'incidence sur 7 jours",
        'new_cases': 'Nouveaux cas',
        'cases': 'Cas (cumul)',
        '7day_incidence_per100k': 'Incidence sur 7 jours pour 100 000',
        '7day_incidence': 'Incidence sur 7 jours',
    },
    'montreal_map_legend_title': '<b>Incidence sur 7 jours pour 100 000</b>',
    'montreal_map_hovertemplate': '<br>Arrondissement/Ville: %{location}<br>Incidence sur 7 jours pour 100 000 habitants: %{z}',
    '7day_avg_short': 'moy mob 7 jours',
    '7day_avg_qc_label': 'Moyenne mobile 7 jours (QC)',
    '7day_avg_mtl_label': 'Moyenne mobile 7 jours (MTL)',
    # confirmed cases fig
    'confirmed_cases_y_label': 'Nouveaux cas',
    'confirmed_cases_y2_label': 'Cas actif',
    'active_cases_qc_label': 'Cas actif (QC)',
    'new_cases_qc_label': 'Nouveaux cas (QC)',
    'new_cases_mtl_label': 'Nouveaux cas (MTL)',
    # age groups
    'age_total_label': "Répartition des cas<br>parmi les groupes d'âge",
    'age_per100000_label': "Répartition des cas par 100 000<br>habitants dans chaque groupe d'âge",
    'age_fig_hovertemplate': '%: %{y}',
    # deaths fig
    'deaths_fig_label': 'Décès',
    'deaths_qc_y_label': 'Nouveaux décès',
    'deaths_qc_y2_label': 'Nouveaux décès (moyenne mobile 7 jours)',
    'new_deaths_qc_label': 'Nouveaux décès (QC)',
    'new_deaths_mtl_label': 'Nouveaux décès (MTL)',
    # hospitalisations fig
    'hospitalisations_label': 'Hospitalisations',
    'hospitalisations_y_label': 'Hospitalisations en cours',
    'hospitalisations_y2_label': 'Nouvelles hospitalisations (moyenne mobile 7 jours)',
    'intensive_care_qc': 'Nouvelles admissions aux soins intensifs (QC)',
    'intensive_care_mtl': 'Nouvelles admissions aux soins intensifs (MTL)',
    'hospitalisations_qc': 'Nouvelles hospitalisations (QC)',
    'hospitalisations_active_qc': 'Hospitalisations en cours (QC)',
    'intensive_care_active_qc': 'Soins Intensifs (en cours, QC)',
    'hospitalisations_mtl': 'Nouvelles hospitalisations (MTL)',
    # Test positivity fig
    'testing_label': 'Taux de positivité des tests',
    'testing_y_label': 'Taux de positivité',
    'testing_y2_label': 'Nombre de tests effectués',
    'testing_tests_qc': 'Nombre de tests effectués (QC)',
    'testing_tests_mtl': 'Nombre de tests effectués (MTL)',
    'testing_hovertemplate_qc': '<b>Quebec</b><br>Moyenne mobile 7 jours: %{y:,.2f}%<br>Taux de positivité: %{customdata:,.2f}%',
    'testing_hovertemplate_mtl': '<b>Montreal</b><br>Moyenne mobile 7 jours: %{y:,.2f}%<br>Taux de positivité: %{customdata:,.2f}%',
    #
    'date_slider_label': 'Date: ',
    'date_label': 'Date',
    'age_label': 'Âge',
    'week_label': 'Semaine',
    'linear_label': 'Échelle linéaire',
    'log_label': 'Échelle logarithmique',
    # Confirmed deaths by place of residence (MTL) fig
    'deaths_loc_fig_mtl_label': 'Décès selon le milieu de vie (MTL)',
    'deaths_loc_fig_mtl_pie_labels': [
        'Centre hospitalier',
        "Centres d'hébergement<br>et de soins de longue<br>durée (CHSLD)",
        'Domicile',
        'Ressource intermédiaire',
        'Résidence privée<br>pour aînés',
        'Autres',
        'Inconnus'
    ],
    # Confirmed deaths by place of residence (QC) fig
    'deaths_loc_fig_qc_label': 'Décès selon le milieu de vie (QC)',
    'chsld_label': "Centres d'hébergement et de<br>soins de longue durée (CHSLD)",
    'psr_label': 'Résidence privée pour aînés',
    'home_label': 'Domicile',
    'other_or_unknown_label': 'Autres ou Inconnus',
    'deaths_loc_fig_qc_y_label': 'Décès (cumul, QC)',
    # Cases vs New Cases fig
    'cases_vs_newcases_label': 'Nouveaux cas vs. total cumulé des cas confirmés',
    'cases_vs_newcases_xlabel': 'Total cumulé des cas confirmés (log)',
    'cases_vs_newcases_ylabel': 'Nouveaux cas (log)',
    'cases_vs_newcases_legend_mtl': 'Montréal',
    'cases_vs_newcases_legend_qc': 'Québec',
    'cases_vs_newcases_hovertemplate': 'Date: %{customdata} <br> Nouveaux cas: %{y}',
    # Vaccination_fig
    'vaccination_label': 'Vaccination',
    'vaccination_y': 'Doses (cumul)',
    'vaccination_new': 'Nouvelles doses',
    'vaccination_total': 'Doses administrées',
    'vaccination_total_2d': 'Doses administrées (2e dose)',
    'vaccination_total_3d': 'Doses administered (3e dose)',
    'vaccination_perc': '% reçues au moins une dose',
    'vaccination_perc_2d': '% reçues 2 doses',
    'vaccination_total_mtl': 'Doses administrées (MTL)',
    'vaccination_perc_mtl': '% de la population vaccinée (MTL)',
    'vaccination_perc_qc': '% de la population vaccinée (QC)',
    'vaccination_hovertemplate': 'Doses administrées: %{y:d}<br>Doses disponsible: %{customdata[0]:d}<br>% 1 dose reçues: %{customdata[1]:.2f}%',
    'vaccination_hovertemplate_mtl': 'Doses administrées: %{y:d}<br>% 1 dose reçues: %{customdata[0]:.2f}%',
    'vaccination_administered_hovertemplate': 'Doses administrées: %{y:d}<br>Doses disponsible: %{customdata[0]:d}',
    'vaccination_new_mtl': 'Nouvelles doses (MTL)',
    'vaccination_new_qc': 'Nouvelles doses (QC)',
    # Vaccination administered fig
    'vaccination_administered_label': 'Nouvelles doses administrées',
    'vaccination_new_y': 'Nouvelles doses (moyenne mobile 7 jours)',
    'vaccination_new_1d': 'Nouvelles 1ère doses',
    'vaccination_new_2d': 'Nouvelles 2ème doses',
    'vaccination_new_3d': 'Nouvelles 3ème doses',
    # Vaccine delivery fig
    'vaccine_delivery_label': 'Doses de vaccin reçues vs. administrées',
    'vaccine_received': 'Doses reçues',
    'vaccine_administered': 'Doses administrées',
    'vaccine_available': 'Doses disponibles',
    'vaccine_received_hovertemplate': 'Doses reçues: %{y:d}<br>Nouvelles doses reçues: %{customdata:d}',
    # Vaccination_age_fig
    'vaccination_age_label': "Vaccination par groupe d'âge",
    'vaccination_categories': ['Non-vacciné', '1 dose reçue', '2 doses reçues', '3 doses reçues'],
    # New cases by vaccination status figure
    'cases_vaccination_status_label': 'Nouveaux cas selon le statut vaccinal (QC)',
    'cases_vaccination_status_y': 'Nouveaux cas par 100 000 (moyenne mobile 7 jours)',
    # New hospitalisations by vaccination status figure
    'hosp_vaccination_status_label': 'Nouvelles hospitalisations selon le statut vaccinal (QC)',
    'hosp_vaccination_status_y': 'Nouvelles hospitalisations par 100 000 (moyenne mobile 7 jours)',
    # Vaccination status categories
    'vaccination_unvaccinated': 'Non-vacciné ou 1 dose < 14 jours',
    'vaccination_1d': '1 dose ≥ 14 jours',
    'vaccination_2d': '2 doses ≥ 7 jours',
    'vaccination_3d': '3 doses ≥ 7 jours',
    # Variants fig
    'variants_label': 'Progression des nouveaux variants préoccupants',
    'variants_sequenced': 'Cas séquencés',
    'variants_presumptive': 'Cas présomptifs',
    'variants_new_presumptive': 'Nouveaux cas présomptifs',
    'variants_new_sequenced': 'Nouveaux cas séquencés',
    'variants_new_cases': 'Nombre total de nouveaux cas',
    'variants_pos_rate': 'Taux de positivité',
    'variants_pos_rate_avg': 'Taux de positivité (moy. mob. 7 jours)',
    'variants_screened': 'Échantillons criblés',
    'variants_y2': 'Cas (cumul)',
    'variants_y3': 'Taux de positivité',
    # Range sliders
    '14d': '14j',
    '1m': '1m',
    '3m': '3m',
    '6m': '6m',
    'ytd': 'AAJ',
    '1y': '1an',
    'all': 'tout'
}

layout = build_home_layout(labels)
layout_vaccination = build_vaccination_layout(labels)
