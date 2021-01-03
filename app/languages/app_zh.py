from ..core import latest_update_date
from ..template import generate_layout

# Label text (EN) #####
# TODO: Make markdown links open in new tab
labels = {
    'language0': 'Français',
    'language_link0': '/',
    'language1': 'English',
    'language_link1': '/en',
    'language2': 'Español',
    'language_link2': '/es',
    'title': '新型冠状病毒（COVID-19）蒙特利尔数据统计',
    'subtitle': '上次更新: ' + latest_update_date,
    'today': ' today',
    'cases_montreal_label': '确诊（蒙特利尔）',
    'deaths_montreal_label': '死亡（蒙特利尔）',
    'cases_qc_label': '确诊（魁省）',
    'deaths_qc_label': '死亡（魁省）',
    'hosp_mtl_label': 'Hospitalisations (MTL)',
    'hosp_qc_label': 'Hospitalisations (QC)',
    'icu': ' ICU yesterday',
    'yesterday': ' yester.',
    'vaccination_perc_mtl_label': 'Est. % vaccinated (MTL)',
    'vaccination_perc_qc_label': 'Est. % vaccinated (QC)',
    'doses_today': ' doses today',
    'test_pos_mtl_label': 'Test positivity rate (MTL)',
    'test_pos_qc_label': 'Test positivity rate (QC)',
    'incidence_per100k_7d_mtl_label': '7-day incid. / 100k (MTL)',
    'incidence_per100k_7d_qc_label': '7-day incid. / 100k (QC)',
    'vs_last7d': ' vs. prev. 7 days',
    'recovered_qc_label': '治愈（魁省）',
    'negative_tests_qc_box_label': '检测阴性（魁省）',
    'montreal_map_label': '病例／1000人（蒙特利尔岛）',
    'total_cases_label': '确诊病例',
    'age_group_label': '不同年龄组确诊病例（蒙特利尔）',
    'total_deaths_label': '死亡（魁省）',
    'total_hospitalisations_label': '入院人数（魁省）',
    'intensive_care_label': '重症患者 （魁省）',
    'total_testing_label': '检测人数（魁省）',
    # footer
    'footer_left': '数据来源: [Santé Montréal](https://santemontreal.qc.ca/en/public/coronavirus-covid-19/), [INSPQ](https://www.inspq.qc.ca/covid-19/donnees) / 使用软件[Dash](https://plotly.com/dash/) / [Github](https://github.com/jeremymoreau/covid19mtl)',
    'footer_centre': 'Hosting sponsored by [DigitalOcean](https://www.digitalocean.com/community/pages/covid-19)',
    'footer_right': '作者[Jeremy Moreau](https://jeremymoreau.com/), [Matthias Schoettle](https://mattsch.com), [Contributors](https://github.com/jeremymoreau/covid19mtl#contributors) / [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh)',
    'infobox': """
    ###### 相关资源

    - [新型冠状病毒症状自我评估工具](https://ca.thrive.health/covid19/en)
    - [蒙特利尔市公共卫生部门](https://santemontreal.qc.ca/en/public/coronavirus-covid-19/)
    - [公共卫生专业知识和参考资料（法语）](https://www.inspq.qc.ca/covid-19/donnees)
    - [魁北克省冠状病毒（COVID-19）相关资源](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/)
    - [加拿大冠状病毒相关资源](https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19.html)
    - [Flatten.ca](https://flatten.ca/)

    如果您对新型冠状病毒（COVID19）有所担心或疑问，或者出现咳嗽／发烧等症状，可拨打蒙特利尔地区的免费电话(514) 644-454-545，魁北克市地区的免费电话(418) 644-454545，或魁北克其他地区的免费电话(877) 644-4545。
    """,
    'montreal_map_colourbar_labels': {
        'date': '日期',
        'borough': '区／市',
        'cases_per_1000': '病例／1000人'
    },
    'montreal_map_hovertemplate': '<br>区／市: %{location}<br>病例／1000人: %{z}',
    # confirmed cases fig
    'confirmed_cases_y_label': 'Cumulative cases',
    'confirmed_cases_y2_label': 'New cases (7-day moving average)',
    'confirmed_cases_qc_label': '累计确诊（魁省）',
    'confirmed_cases_mtl_label': '累计确诊（蒙特利尔）',
    'active_cases_qc_label': '现存确诊 （魁省）',
    'new_confirmed_cases_qc_label': '新增确诊（魁省）',
    'new_confirmed_cases_mtl_label': '新增确诊（蒙特利尔）',
    'age_total_label': '各年龄组总病例分布情况',
    'age_per100000_label': '每10万人口不同年龄组病例分布情况',
    'age_fig_hovertemplate': '%: %{y}',
    # deaths fig
    'deaths_fig_label': '死亡',
    'deaths_qc_y_label': 'Cumulative deaths',
    'deaths_qc_y2_label': 'New deaths (7-day moving average)',
    'deaths_fig_qc_label': '累计死亡（魁省）',
    'deaths_fig_mtl_label': '累计死亡（蒙特利尔）',
    'new_deaths_qc_label': '新增死亡（魁省）',
    'new_deaths_mtl_label': '新增死亡（蒙特利尔）',
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
    'testing_y_label': 'Test positivity rate (7-day moving average)',
    'testing_mtl': 'Montreal',
    'testing_qc': 'Quebec',
    #
    'date_slider_label': '日期: ',
    'date_label': '日期',
    'age_label': '年龄',
    'linear_label': '线性尺度',
    'log_label': '对数尺度',
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
    'vaccination_label': 'Vaccination',
    'vaccination_y': 'Approx. % of population vaccinated',
    'vaccination_y2': 'New doses',
    'vaccination_perc_mtl': '% of pop vaccinated (MTL)',
    'vaccination_perc_qc': '% of pop vaccinated (QC)',
    'vaccination_hovertemplate': '% vaccinated: %{y:.2f}% <br> # of doses: %{customdata}',
    'vaccination_new_mtl': 'New doses (MTL)',
    'vaccination_new_qc': 'New doses (QC)'
}

layout = generate_layout(labels)
