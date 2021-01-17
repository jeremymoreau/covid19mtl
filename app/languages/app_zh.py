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
    'today': '今日',
    'today_short': '今日',
    'cases_montreal_label': '确诊（蒙特利尔）',
    'deaths_montreal_label': '死亡（蒙特利尔）',
    'cases_qc_label': '确诊（魁省）',
    'deaths_qc_label': '死亡（魁省）',
    'hosp_mtl_label': '新增入院 (魁省)',
    'hosp_qc_label': '新增入院 (蒙特利尔)',
    'icu': '重症患者（今日）',
    'yesterday': '昨日',
    'vs_2dago': '较2日前',
    'vaccination_perc_mtl_label': '接种百分比 (蒙特利尔)',
    'vaccination_perc_qc_label': '接种百分比 (魁省)',
    'doses_today': '接种量（今日）',
    'test_pos_mtl_label': '检测阳性率 (蒙特利尔)',
    'test_pos_qc_label': '检测阳性率 (魁省)',
    'incidence_per100k_7d_mtl_label': '7日发病率/10万 (蒙特利尔)',
    'incidence_per100k_7d_qc_label': '7日发病率/10万 (魁省)',
    'vs_last7d': '较7日前',
    'recovered_qc_label': '治愈（魁省）',
    'negative_tests_qc_box_label': '检测阴性（魁省）',
    'montreal_map_label': '病例／100 000人（蒙特利尔岛）',
    'total_cases_label': '确诊病例',
    'age_group_label': '不同年龄组确诊病例（蒙特利尔）',
    'total_deaths_label': '死亡（魁省）',
    'total_hospitalisations_label': '入院人数（魁省）',
    'intensive_care_label': '重症患者 （魁省）',
    'total_testing_label': '检测人数（魁省）',
    # footer
    'footer_left': '数据来源: [Santé Montréal](https://santemontreal.qc.ca/en/public/coronavirus-covid-19/), [INSPQ](https://www.inspq.qc.ca/covid-19/donnees), [Government of Québec](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/) / 使用软件[Dash](https://plotly.com/dash/) / [Github](https://github.com/jeremymoreau/covid19mtl)',
    'footer_centre': 'Hosting sponsored by [DigitalOcean](https://www.digitalocean.com/community/pages/covid-19)',
    'footer_right': '作者[Jeremy Moreau](https://jeremymoreau.com/), [Matthias Schoettle](https://mattsch.com), [Contributors](https://github.com/jeremymoreau/covid19mtl#contributors) / [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh)',
    'infobox': """
    ###### 相关资源

    - [新型冠状病毒症状自我评估工具](https://ca.thrive.health/covid19/en)
    - [蒙特利尔市公共卫生部门](https://santemontreal.qc.ca/en/public/coronavirus-covid-19/)
    - [公共卫生专业知识和参考资料（法语）](https://www.inspq.qc.ca/covid-19/donnees)
    - [魁北克省冠状病毒（COVID-19）相关资源](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/)
    - [加拿大冠状病毒相关资源](https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19.html)

    如果您对新型冠状病毒（COVID19）有所担心或疑问，或者出现咳嗽／发烧等症状，可拨打蒙特利尔地区的免费电话(514) 644-454-545，魁北克市地区的免费电话(418) 644-454545，或魁北克其他地区的免费电话(877) 644-4545。
    """,
    'montreal_map_colourbar_labels': {
        'date': '日期',
        'borough': '区／市',
        '7day_incidence_rate': '7日发病率',
        'new_cases': '新增确诊',
        'cases': '累计确诊',
        '7day_incidence_per100k': '7日发病率/10万',
        '7day_incidence': '7日发病率',
    },
    'montreal_map_legend_title': '<b>7日发病率/10万</b>',
    'montreal_map_hovertemplate': '<br>区／市: %{location}<br>7日发病率/10万: %{z}',
    # confirmed cases fig
    'confirmed_cases_y_label': '累计确诊',
    'confirmed_cases_y2_label': '新增确诊 (7日移动平均)',
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
    'deaths_qc_y_label': '累计死亡',
    'deaths_qc_y2_label': '新增死亡 (7日移动平均)',
    'deaths_fig_qc_label': '累计死亡（魁省）',
    'deaths_fig_mtl_label': '累计死亡（蒙特利尔）',
    'new_deaths_qc_label': '新增死亡（魁省）',
    'new_deaths_mtl_label': '新增死亡（蒙特利尔）',
    # hospitalisations fig
    'hospitalisations_label': '入院人数',
    'hospitalisations_y_label': '现入院人数',
    'hospitalisations_y2_label': '新增入院 (7日移动平均)',
    'intensive_care_qc': '新增重症患者 (魁省)',
    'intensive_care_mtl': '新增重症患者 (蒙特利尔)',
    'hospitalisations_qc': '新增入院 (魁省)',
    'hospitalisations_active_qc': '现入院人数 (魁省)',
    'intensive_care_active_qc': '现重症患者 (魁省)',
    'hospitalisations_mtl': '新增入院 (蒙特利尔)',
    # Test positivity fig
    'testing_label': '检测阳性率',
    'testing_y_label': '检测阳性率 (7日移动平均)',
    'testing_mtl': '蒙特利尔',
    'testing_qc': '魁省',
    #
    'date_slider_label': '日期: ',
    'date_label': '日期',
    'age_label': '年龄',
    'linear_label': '线性尺度',
    'log_label': '对数尺度',
    # Confirmed deaths by place of residence (MTL) fig
    'deaths_loc_fig_mtl_label': '按居住地分类死亡人数 (蒙特利尔)',
    'deaths_loc_fig_mtl_pie_labels': [
        '医院',
        '公立长期护理机构',
        '家',
        '中间',
        "私人养老院",
        '其他',
        '未知'
    ],
    # Confirmed deaths by place of residence (QC) fig
    'deaths_loc_fig_qc_label': '按居住地分类死亡人数 (魁省)',
    'chsld_label': '公立长期护理机构',
    'psr_label': "私人养老院",
    'home_label': '家',
    'other_or_unknown_label': '其他或未知',
    'deaths_loc_fig_qc_y_label': '累计死亡 （魁省)',
    # Cases vs New Cases fig
    'cases_vs_newcases_label': '新病例与累计确诊病例对比',
    'cases_vs_newcases_xlabel': '累计确诊病例 (对数比例)',
    'cases_vs_newcases_ylabel': '新增病例 (对数比例)',
    'cases_vs_newcases_legend_mtl': '蒙特利尔',
    'cases_vs_newcases_legend_qc': '魁省',
    'cases_vs_newcases_hovertemplate': '日期: %{customdata} <br> 新增病例: %{y}',
    # Vaccination_fig
    'vaccination_label': '疫苗接种量',
    'vaccination_y': '接种疫苗人口百分比',
    'vaccination_y2': '新增接种量',
    'vaccination_perc_mtl': '接种人口百分比 (蒙特利尔)',
    'vaccination_perc_qc': '接种人口百分比 (魁省)',
    'vaccination_hovertemplate': '接种人口百分比: %{y:.2f}% <br> 接种人数: %{customdata}',
    'vaccination_new_mtl': '新增接种量 (蒙特利尔)',
    'vaccination_new_qc': '新增接种量 (魁省)',
    # Range sliders
    '1m': '1m',
    '3m': '3m',
    '6m': '6m',
    'ytd': 'YTD',
    '1y': '1y',
    'all': 'all'
}

layout = generate_layout(labels)
