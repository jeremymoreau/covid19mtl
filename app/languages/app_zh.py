from ..core import latest_update_date, latest_vaccination_update_date
from ..template import generate_layout as build_home_layout
from ..template_vacc import generate_layout as build_vaccination_layout

# Label text (EN) #####
# TODO: Make markdown links open in new tab
labels = {
    'home_link': '/zh',
    'home_link_text': 'Home',
    'vaccination_link': '/zh/vaccination',
    'vaccination_link_text': 'Vaccination',
    'language0': 'Français',
    'language_link0': '/',
    'language1': 'English',
    'language_link1': '/en',
    'language2': 'Español',
    'language_link2': '/es',
    'title': '新型冠状病毒（COVID-19）蒙特利尔数据统计',
    'vaccination_title': ': Vaccination',
    'subtitle': '上次更新: ' + latest_update_date,
    'vaccination_subtitle': '上次更新: ' + latest_vaccination_update_date.isoformat(),
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
    'vaccination_1d_mtl_label': '1st doses administered (MTL)',
    'vaccination_2d_mtl_label': '2nd doses administered (MTL)',
    'vaccination_1d_perc_mtl_label': '% received 1 dose (MTL)',
    'vaccination_2d_perc_mtl_label': '% received 2 doses (MTL)',
    'vaccination_1d_qc_label': '1st doses administered (QC)',
    'vaccination_2d_qc_label': '2nd doses administered (QC)',
    'vaccination_1d_perc_qc_label': '% received 1 dose (QC)',
    'vaccination_2d_perc_qc_label': '% received 2 doses (QC)',
    'doses_today': '接种量（今日）',
    'test_pos_mtl_label': '检测阳性率 (蒙特利尔)',
    'test_pos_qc_label': '检测阳性率 (魁省)',
    'incidence_per100k_7d_mtl_label': '7日发病率/10万 (蒙特利尔)',
    'incidence_per100k_7d_qc_label': '7日发病率/10万 (魁省)',
    'vs_last7d': '较7日前',
    'recovered_qc_label': '治愈（魁省）',
    'recovered_mtl_label': '治愈 (蒙特利尔)',
    'negative_tests_qc_box_label': '检测阴性（魁省）',
    'montreal_map_label': '病例／100 000人（蒙特利尔岛）',
    'total_cases_label': '确诊病例',
    'age_group_label': 'Distribution of new cases across all age groups by week (MTL)',
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
    - [Quebec Vaccination Campaign &ndash; Appointments](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/progress-of-the-covid-19-vaccination/)
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
    'age_total_label': '各年龄组总病例分布情况',
    'age_per100000_label': '每10万人口不同年龄组病例分布情况',
    'age_fig_hovertemplate': '%: %{y}',
    # deaths fig
    'deaths_fig_label': '死亡',
    'deaths_qc_y_label': 'New deaths',
    'deaths_qc_y2_label': '新增死亡 (7日移动平均)',
    'new_deaths_qc_label': 'New deaths (QC)',
    'new_deaths_mtl_label': 'New deaths (MTL)',
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
    'testing_label': 'Test positivity rate',
    'testing_y_label': 'Test positivity rate',
    'testing_y2_label': 'Tests performed',
    'testing_tests_qc': 'Tests performed (QC)',
    'testing_tests_mtl': 'Tests performed (MTL)',
    'testing_hovertemplate_qc': '<b>Quebec</b><br>7-day moving avg: %{y:,.2f}%<br>Test positivity: %{customdata:,.2f}%',
    'testing_hovertemplate_mtl': '<b>Montreal</b><br>7-day moving avg: %{y:,.2f}%<br>Test positivity: %{customdata:,.2f}%',
    #
    'date_slider_label': '日期: ',
    'date_label': '日期',
    'age_label': '年龄',
    'week_label': 'Week',
    'linear_label': '线性尺度',
    'log_label': '对数尺度',
    # Confirmed deaths by place of residence (MTL) fig
    'deaths_loc_fig_mtl_label': '按居住地分类死亡人数 (蒙特利尔)',
    'deaths_loc_fig_mtl_pie_labels': [
        '医院',
        '公立长期护理机构',
        '家',
        '中间',
        '私人养老院',
        '其他',
        '未知'
    ],
    # Confirmed deaths by place of residence (QC) fig
    'deaths_loc_fig_qc_label': '按居住地分类死亡人数 (魁省)',
    'chsld_label': '公立长期护理机构',
    'psr_label': '私人养老院',
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
    'vaccination_label': '疫苗接种量',  # TODO: add 'Progress'
    'vaccination_y': 'Doses (cumulative)',
    'vaccination_new': '新增接种量',
    'vaccination_total': 'Doses administered',
    'vaccination_total_2d': 'Doses administered (2nd dose)',
    'vaccination_perc': '% of pop received at least 1 dose',
    'vaccination_perc_2d': '% of pop received 2 doses',
    'vaccination_total_mtl': 'Doses administered (MTL)',
    'vaccination_perc_mtl': '接种人口百分比 (蒙特利尔)',
    'vaccination_perc_qc': '接种人口百分比 (魁省)',
    'vaccination_hovertemplate': '接种人数: %{y:,d}<br>Doses available: %{customdata[0]:,d}<br>% of pop received 1 dose: %{customdata[1]:.2f}%',
    'vaccination_hovertemplate_mtl': '接种人数: %{y:,d}<br>% of pop received 1 dose: %{customdata[0]:.2f}%',
    'vaccination_administered_hovertemplate': 'Doses administered: %{y:,d}<br>Doses available: %{customdata[0]:,d}',
    'vaccination_new_mtl': '新增接种量 (蒙特利尔)',
    'vaccination_new_qc': '新增接种量 (魁省)',
    # Vaccination administered fig
    'vaccination_administered_label': 'New doses administered',
    'vaccination_new_y': 'New doses (7-day moving average)',
    'vaccination_new_1d': 'New 1st doses',
    'vaccination_new_2d': 'New 2nd doses',
    # Vaccine delivery fig
    'vaccine_delivery_label': 'Vaccine doses delivered vs. administered',
    'vaccine_received': 'Doses received',
    'vaccine_administered': 'Doses administered',
    'vaccine_available': 'Doses available',
    'vaccine_received_hovertemplate': 'Doses received: %{y:,d}<br>New doses received: %{customdata:,d}',
    # Vaccination_age_fig
    'vaccination_age_label': 'Vaccination by age group',
    'vaccination_categories': ['Not vaccinated', '1 dose received', '2 doses received', '3 doses received'],
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
