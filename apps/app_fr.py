from app import latest_update_date
from template import generate_layout

##### Label text (FR) #####
# TODO: Make markdown links open in new tab
labels = {
    'language' : 'English',
    'language_link' : '/en',
    'title' : u' Tableau de bord COVID-19 Montréal',
    'subtitle' : u'Dernière mise à jour: ' + latest_update_date,
    'cases_montreal_label' : u'Cas (Montréal)',
    'cases_qc_label' : u'Cas (QC)',
    'deaths_qc_label' : u'Décès (QC)',
    'recovered_qc_label' : u'Guéris (QC)',
    'montreal_map_label' : 'Nombre total de cas',
    'total_cases_label' : u'Cas confirmés',
    'age_group_label' : "Cas confirmés selon le groupe d'âge",
    'total_deaths_label' : 'Décès (QC)',
    'total_hospitalisations_label': 'Hospitalisations (QC)',
    'total_testing_label' : 'Tests diagnostiques (QC)',
    'footer_left' : u'Données: [Santé Montréal](https://santemontreal.qc.ca/population/coronavirus-covid-19/), [INSPQ](https://www.inspq.qc.ca/covid-19/donnees) / Créé avec [Dash](https://plotly.com/dash/)',
    'footer_right' : 'Créé par [Jeremy Moreau](https://jeremymoreau.com/) ([IR-CUSM](https://rimuhc.ca/fr/home), McGill) / [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.fr)',
    'infobox' : u"""
    #### Ressources utiles

    - [Outil d'auto-évaluation des symptômes COVID-19](https://ca.thrive.health/covid19/fr)
    - [Santé Montréal](https://santemontreal.qc.ca/population/coronavirus-covid-19/)
    - [Centre d'expertise et de référence en santé publique](https://www.inspq.qc.ca/covid-19/donnees)
    - [La maladie à coronavirus (COVID-19) au Québec](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/)
    - [COVID-19 Gouvernement du Canada](https://www.canada.ca/fr/sante-publique/services/maladies/maladie-coronavirus-covid-19.html)
    - [Aplatir.ca](https://fr.flatten.ca/)

    Si la COVID-19 vous inquiète ou si vous présentez des symptômes comme de la toux ou de la fièvre, vous pouvez contacter, sans frais, le (514) 644-4545 pour la région de Montréal,  le (418) 644-4545 pour la région de Québec et le 1 (877) 644-4545 ailleurs au Québec.
    """,
    'montreal_map_colourbar_labels' : {
                                        'date': 'Date', 
                                        'borough': 'Arrondissement/Ville',
                                        'cases_per_1000': 'Cas par 1000<br>habitants'
                                        },
    'montreal_map_hovertemplate' : '<br>Arrondissement/Ville: %{location}<br>Cas par 1000 habitants: %{z}',
    'confirmed_cases_y_label' : 'Cas confirmés',
    'confirmed_cases_qc_label' : u'Québec',
    'confirmed_cases_mtl_label' : u'Montréal',
    'age_total_label' : u"Répartition des cas<br>parmi les groupes d'âge",
    'age_per100000_label' : u"Répartition des cas par 100 000<br>habitants dans chaque groupe d'âge",
    'age_fig_hovertemplate' : '%: %{y}',
    'deaths_qc_y_label' : 'Décès (QC)',
    'intensive_care_label' : 'Soins Intensifs',
    'testing_qc_y_label' : 'Cas (QC)',
    'negative_tests_qc_label' : 'Analyses négatives (QC)',
    'positive_cases_qc_label' : 'Cas confirmés (QC)',
}

layout = generate_layout(labels)
