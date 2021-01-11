from ..core import latest_update_date
from ..template import generate_layout

# Label text (FR) #####
# TODO: Make markdown links open in new tab
labels = {
    'language0': 'English',
    'language_link0': '/en',
    'language1': 'Español',
    'language_link1': '/es',
    'language2': '中文',
    'language_link2': '/zh',
    'title': ' Tableau de bord COVID-19 Montréal',
    'subtitle': 'Dernière mise à jour: ' + latest_update_date,
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
    'vaccination_perc_mtl_label': '% vacciné est. (MTL)',
    'vaccination_perc_qc_label': '% vacciné est. (QC)',
    'doses_today': ' doses auj.',
    'test_pos_mtl_label': 'Positivité des tests (MTL)',
    'test_pos_qc_label': 'Positivité des tests (QC)',
    'incidence_per100k_7d_mtl_label': 'Incid./100k 7 jours (MTL)',
    'incidence_per100k_7d_qc_label': 'Incid./100k 7 jours (QC)',
    'vs_last7d': ' vs. 7 jours préc.',
    'recovered_qc_label': 'Rétablis (QC)',
    'negative_tests_qc_box_label': 'Analyses négatives (QC)',
    'montreal_map_label': 'Cas pour 100 000 habitants (Île de Montréal)',
    'total_cases_label': 'Cas confirmés',
    'age_group_label': "Cas confirmés selon le groupe d'âge (MTL)",
    'total_deaths_label': 'Décès (QC)',
    'total_hospitalisations_label': 'Hospitalisations (QC)',
    'intensive_care_label': 'Soins Intensifs (QC)',
    'total_testing_label': 'Tests diagnostiques (QC)',
    # footer
    'footer_left': 'Données: [Santé Montréal](https://santemontreal.qc.ca/population/coronavirus-covid-19/), [INSPQ](https://www.inspq.qc.ca/covid-19/donnees) / Créé avec [Dash](https://plotly.com/dash/) / [Github](https://github.com/jeremymoreau/covid19mtl)',
    'footer_centre': 'Hébergement offert par [DigitalOcean](https://www.digitalocean.com/community/pages/covid-19)',
    'footer_right': 'Créé par [Jeremy Moreau](https://jeremymoreau.com/), [Matthias Schoettle](https://mattsch.com) et [Contributeurs](https://github.com/jeremymoreau/covid19mtl#contributors) / [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.fr)',
    'infobox': """
    ###### Ressources utiles

    - [Outil d'auto-évaluation des symptômes COVID-19](https://ca.thrive.health/covid19/fr)
    - [Santé Montréal](https://santemontreal.qc.ca/population/coronavirus-covid-19/)
    - [Centre d'expertise et de référence en santé publique](https://www.inspq.qc.ca/covid-19/donnees)
    - [La maladie à coronavirus (COVID-19) au Québec](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/)
    - [COVID-19 Gouvernement du Canada](https://www.canada.ca/fr/sante-publique/services/maladies/maladie-coronavirus-covid-19.html)
    - [Aplatir.ca](https://fr.flatten.ca/)

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
    # confirmed cases fig
    'confirmed_cases_y_label': 'Cas (cumul)',
    'confirmed_cases_y2_label': 'Nouveaux  cas (moyenne mobile 7 jours)',
    'confirmed_cases_qc_label': 'Québec (cumul)',
    'active_cases_qc_label': 'Québec (cas actif)',
    'confirmed_cases_mtl_label': 'Montréal (cumul)',
    'new_confirmed_cases_qc_label': 'Québec  (nouveaux cas)',
    'new_confirmed_cases_mtl_label': 'Montréal (nouveaux cas)',
    'age_total_label': "Répartition des cas<br>parmi les groupes d'âge",
    'age_per100000_label': "Répartition des cas par 100 000<br>habitants dans chaque groupe d'âge",
    'age_fig_hovertemplate': '%: %{y}',
    # deaths fig
    'deaths_fig_label': 'Décès',
    'deaths_qc_y_label': 'Décès (cumul)',
    'deaths_qc_y2_label': 'Nouveaux décès (moyenne mobile 7 jours)',
    'deaths_fig_qc_label': 'Québec (cumul)',
    'deaths_fig_mtl_label': 'Montréal (cumul)',
    'new_deaths_qc_label': 'Québec (nouveaux décès)',
    'new_deaths_mtl_label': 'Montréal (nouveaux décès)',
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
    'testing_y_label': 'Taux de positivité (moyenne mobile 7 jours)',
    'testing_mtl': 'Montréal',
    'testing_qc': 'Québec',
    #
    'date_slider_label': 'Date: ',
    'date_label': 'Date',
    'age_label': 'Age',
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
    'vaccination_y': '% de la population vaccinée (approximatif)',
    'vaccination_y2': 'Nouvelles doses',
    'vaccination_perc_mtl': '% de la population vaccinée (MTL)',
    'vaccination_perc_qc': '% de la population vaccinée (QC)',
    'vaccination_hovertemplate': '% vacciné: %{y:.2f}% <br> # de doses: %{customdata}',
    'vaccination_new_mtl': 'Nouvelles doses (MTL)',
    'vaccination_new_qc': 'Nouvelles doses (QC)'
}

layout = generate_layout(labels)
