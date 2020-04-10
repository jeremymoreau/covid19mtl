from app import latest_update_date
from template import generate_layout

##### Label text (EN) #####
# TODO: Make markdown links open in new tab
labels = {
    'language0' : 'Français',
    'language_link0' : '/',
    'language1' : 'English',
    'language_link1' : '/en',
    'title' : '新型冠状病毒（COVID-19）蒙特利尔数据统计',
    'subtitle' : '上次更新: ' + latest_update_date,
    'cases_montreal_label' : '确诊（蒙特利尔）',
    'deaths_montreal_label' : '死亡（蒙特利尔）',
    'cases_qc_label' : '确诊（魁省）',
    'deaths_qc_label' : '死亡（魁省）',
    'recovered_qc_label' : '治愈（魁省）',
    'montreal_map_label' : '病例／1000人（蒙特利尔岛）',
    'total_cases_label' : '确诊病例',
    'age_group_label' : '不同年龄组确诊病例',
    'total_deaths_label' : '死亡（魁省）',
    'total_hospitalisations_label': '入院人数（魁省）',
    'total_testing_label' : '检测人数（魁省）',
    'footer_left' : '数据来源: [Santé Montréal](https://santemontreal.qc.ca/en/public/coronavirus-covid-19/), [INSPQ](https://www.inspq.qc.ca/covid-19/donnees) / 使用软件[Dash](https://plotly.com/dash/) / [Github](https://github.com/jeremymoreau/covid19mtl)',
    'footer_right' : '作者[Jeremy Moreau](https://jeremymoreau.com/) ([RI-MUHC](https://rimuhc.ca/), McGill) / [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh)',
    'infobox' : """
    ###### 相关资源
    
    - [新型冠状病毒症状自我评估工具](https://ca.thrive.health/covid19/en)
    - [蒙特利尔市公共卫生部门](https://santemontreal.qc.ca/en/public/coronavirus-covid-19/)
    - [公共卫生专业知识和参考资料（法语）](https://www.inspq.qc.ca/covid-19/donnees)
    - [魁北克省冠状病毒（COVID-19）相关资源](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/)
    - [加拿大冠状病毒相关资源](https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19.html)
    - [Flatten.ca](https://flatten.ca/)

    如果您对新型冠状病毒（COVID19）有所担心或疑问，或者出现咳嗽／发烧等症状，可拨打蒙特利尔地区的免费电话(514) 644-454-545，魁北克市地区的免费电话(418) 644-454545，或魁北克其他地区的免费电话(877) 644-4545。
    """,
    'montreal_map_colourbar_labels' : {
                                        'date': '日期', 
                                        'borough': '区／市',
                                        'cases_per_1000': '病例／1000人'
                                        },
    'montreal_map_hovertemplate' : '<br>区／市: %{location}<br>病例／1000人: %{z}',
    'confirmed_cases_y_label' : '累计确诊',
    'confirmed_cases_qc_label' : '魁北克省',
    'confirmed_cases_mtl_label' : '蒙特利尔市',
    'age_total_label' : '各年龄组总病例分布情况',
    'age_per100000_label' : '每10万人口不同年龄组病例分布情况',
    'age_fig_hovertemplate' : '%: %{y}',
    'deaths_fig_label' : '死亡',
    'deaths_qc_y_label' : '累计死亡',
    'hospitalisations_y_label' : '累计入院人数（魁省）',
    'hospitalisations_label' : '入院人数（魁省）',
    'intensive_care_label' : '重症患者 （魁省）',
    'testing_qc_y_label' : '累计人数（魁省）',
    'negative_tests_qc_label' : '检测阴性（魁省）',
    'positive_cases_qc_label' : '确诊阳性病例（魁省）',
    'date_slider_label' : '日期: ',
    'date_label' : '日期',
    'age_label' : '年龄',
    'linear_label' : '线性尺度',
    'log_label' : '对数尺度'
}

layout = generate_layout(labels)
