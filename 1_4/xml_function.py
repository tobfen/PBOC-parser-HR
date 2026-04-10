import copy

import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
from dateutil import rrule
from dateutil.parser import parse

#%%
def dic_to_df(file):
    df = pd.DataFrame()
    for i in file:
        df1 = pd.DataFrame.from_dict(i, orient='index')
        df1 = pd.DataFrame(df1.values.T, index=df1.columns,columns=list(df1.index))
        df = pd.concat([df,df1],axis=0)
        columns = list(df.columns)
        df.reset_index(inplace=True)
        df = df[columns]
    return df

def list_to_df(file):
    df = pd.DataFrame()
    df1 = pd.DataFrame.from_dict(file, orient='index')
    df1 = pd.DataFrame(df1.values.T, index=df1.columns, columns=list(df1.index))
    df = pd.concat([df,df1],axis=0)
    return df

#%%
###获取身份证号PCRID，作为主键
# def prcid_value(temp1):
#     try:
#         prcid = temp1['Document']['PRH']['PA01']['PA01B']['PA01BI01']
#     except:
#         pass
#     return prcid

#%%
###获取报告编号、报告时间、证件类型、证件号码、姓名
def pri_key(temp1):
    try:
        prcid = '310115202501010000'
        report_id = '20250101888888888888'
        #prcid = temp1['Document']['PRH']['PA01']['PA01B']['PA01BI01']
        #report_id = temp1['Document']['PRH']['PA01']['PA01A']['PA01AI01']
        report_time = temp1['Document']['PRH']['PA01']['PA01A']['PA01AR01']
        xm = temp1['Document']['PRH']['PA01']['PA01B']['PA01BQ01']
        zj_type = temp1['Document']['PRH']['PA01']['PA01B']['PA01BD01']
    except:
        pass
    return prcid,report_id,report_time,xm,zj_type

#%%
###报告头模块
def header_df(temp1,column_type = 'CNH'):
    header_df = pd.DataFrame()
    
    try:
        tmp = temp1['Document']['PRH']['PA01']
        mid_df = pd.DataFrame()
        for j in ['PA01A','PA01B','PA01C','PA01D','PA01E']:
            if j in ['PA01A','PA01B','PA01C','PA01D','PA01E']:
                try:
                    tmp1 = tmp[j]
                    tmp1 = list_to_df(tmp1)
                    mid_df = pd.concat([mid_df,tmp1],axis=1)
                except:
                    pass
        header_df = pd.concat([header_df,mid_df],axis=0)
    except:
        pass

    if len(header_df)<1:
        header_df = pd.DataFrame({"PA01AI01":np.nan,
                                  "PA01AR01":np.nan,
                                  "PA01BQ01":np.nan,
                                  "PA01BD01":np.nan,
                                  "PA01BI01":np.nan,
                                  "PA01BI02":np.nan,
                                  "PA01BD02":np.nan,
                                  "PA01CS01":np.nan,
                                  "PA01DQ01":np.nan,
                                  "PA01DQ02":np.nan,
                                  "PA01DR01":np.nan,
                                  "PA01DR02":np.nan,
                                  "PA01ES01":np.nan,},index=[0])
            
    columns_chinese = {"PA01AI01":"人行_报告编号",
                        "PA01AR01":"人行_报告时间",
                        "PA01BQ01":"被查询者姓名",
                        "PA01BD01":"被查询者证件类型",
                        "PA01BI01":"被查询者证件号码",
                        "PA01BI02":"查询机构代码",
                        "PA01BD02":"查询原因代码",
                        "PA01CS01":"身份标识个数",
                        "PA01DQ01":"防欺诈警示标识",
                        "PA01DQ02":"防欺诈警示联系电话",
                        "PA01DR01":"防欺诈警示生效日期",
                        "PA01DR02":"防欺诈警示截止日期",
                        "PA01ES01":"异议标注数目",}
    
    # columns_english = {"PA01AI01":"report_header_report_no",
    #                     "PA01AR01":"report_header_report_time",
    #                     "PA01BQ01":"report_header_name",
    #                     "PA01BD01":"report_header_id_type",
    #                     "PA01BI01":"report_header_id_num",
    #                     "PA01BI02":"report_header_inquiry_org",
    #                     "PA01BD02":"report_header_inquiry_reason",
    #                     "PA01CS01":"report_header_id_count",
    #                     "PA01DQ01":"report_header_warning_flag",
    #                     "PA01DQ02":"report_header_warning_tel",
    #                     "PA01DR01":"report_header_warning_start_date",
    #                     "PA01DR02":"report_header_warning_end_date",
    #                     "PA01ES01":"report_header_objection_count",}
    
    columns_english = {"PA01AI01":"ReportNumber",
                    "PA01AR01":"ReportTime",
                    "PA01BQ01":"CutomerName",
                    "PA01BD01":"CustomerIDType",
                    "PA01BI01":"CutomerIDNumber",
                    "PA01BI02":"QueryOrganization",
                    "PA01BD02":"QueryReason",
                    "PA01CS01":"ReportHeaderIdCount",
                    "PA01DQ01":"WarningInformation",
                    "PA01DQ02":"ReportHeaderWarningTel",
                    "PA01DR01":"EffecgtiveDate",
                    "PA01DR02":"ExpirationDate",
                    "PA01ES01":"DissentInformation",}
    
    column_list = ["PA01AI01",
                    "PA01AR01",
                    "PA01BQ01",
                    "PA01BD01",
                    "PA01BI01",
                    "PA01BI02",
                    "PA01BD02",
                    "PA01CS01",
                    "PA01DQ01",
                    "PA01DQ02",
                    "PA01DR01",
                    "PA01DR02",
                    "PA01ES01",]
        
    for i in column_list:
        if i not in list(header_df.columns):
            header_df[i] = np.nan
    
    header_df = header_df[column_list]
    if column_type == 'CNH':
        header_df.rename(columns = columns_chinese,inplace=True)
    else:
        header_df.rename(columns = columns_english,inplace=True)
    return header_df

#%%
###基本信息段
def basicInfo_df(temp1,column_type = 'CNH'):
    basicInfo_df = pd.DataFrame()
    
    try:
        tmp = temp1['Document']['PIM']['PB01']
        mid_df = pd.DataFrame()
        for j in ['PB01A','PB01B']:
            if j in ['PB01A','PB01B']:
                try:
                    tmp1 = tmp[j]
                    tmp1 = list_to_df(tmp1)
                    mid_df = pd.concat([mid_df,tmp1],axis=1)
                except:
                    pass
        basicInfo_df = pd.concat([basicInfo_df,mid_df],axis=1)
    except:
        pass
    
    try:
        tmp = temp1['Document']['PMM']
        mid_df = pd.DataFrame()
        for j in ['PB02']:
            if j in ['PB02']:
                try:
                    tmp1 = tmp[j]
                    tmp1 = list_to_df(tmp1)
                    mid_df = pd.concat([mid_df,tmp1],axis=1)
                except:
                    pass
        basicInfo_df = pd.concat([basicInfo_df,mid_df],axis=1)
    except:
        pass
    
    
    if len(basicInfo_df) <1:
        basicInfo_df = pd.DataFrame({"PB01AD01":np.nan,
                                    "PB01AR01":np.nan,
                                    "PB01AD02":np.nan,
                                    "PB01AD03":np.nan,
                                    "PB01AD04":np.nan,
                                    "PB01AQ01":np.nan,
                                    "PB01AQ02":np.nan,
                                    "PB01AD05":np.nan,
                                    "PB01AQ03":np.nan,
                                    "PB01BS01":np.nan,
                                    "PB020D01":np.nan,
                                    "PB020Q01":np.nan,
                                    "PB020D02":np.nan,
                                    "PB020I01":np.nan,
                                    "PB020Q02":np.nan,
                                    "PB020Q03":np.nan,},index=[0])
        
    columns_chinese = {"PB01AD01":"性别",
                        "PB01AR01":"出生日期",
                        "PB01AD02":"学历",
                        "PB01AD03":"学位",
                        "PB01AD04":"就业状况",
                        "PB01AQ01":"电子邮箱",
                        "PB01AQ02":"通讯地址",
                        "PB01AD05":"国籍",
                        "PB01AQ03":"户籍地址",
                        "PB01BS01":"手机号码个数",
                        "PB020D01":"婚姻状况",
                        "PB020Q01":"配偶姓名",
                        "PB020D02":"配偶证件类型",
                        "PB020I01":"配偶证件号码",
                        "PB020Q02":"配偶工作单位",
                        "PB020Q03":"配偶联系电话"}
    
    # columns_english = {"PB01AD01":"basic_info_gender",
    #                     "PB01AR01":"basic_info_birthdate",
    #                     "PB01AD02":"basic_info_education",
    #                     "PB01AD03":"basic_info_degree",
    #                     "PB01AD04":"basic_info_work_status",
    #                     "PB01AQ01":"basic_info_email",
    #                     "PB01AQ02":"basic_info_address",
    #                     "PB01AD05":"basic_info_country",
    #                     "PB01AQ03":"basic_info_demicile_addr",
    #                     "PB01BS01":"basic_info_cellphone_num_count",
    #                     "PB020D01":"basic_info_marriage_status",
    #                     "PB020Q01":"basic_info_spouse_name",
    #                     "PB020D02":"basic_info_spouse_id_type",
    #                     "PB020I01":"basic_info_spouse_id_num",
    #                     "PB020Q02":"basic_info_spouse_company",
    #                     "PB020Q03":"basic_info_spouse_phone"}
    
    columns_english = {"PB01AD01":"Gender",
                    "PB01AR01":"DateOfBirth",
                    "PB01AD02":"EducationLevel",
                    "PB01AD03":"EducationDegree",
                    "PB01AD04":"EmploymentStatus",
                    "PB01AQ01":"EmailAddress",
                    "PB01AQ02":"MailAddress",
                    "PB01AD05":"Nationality",
                    "PB01AQ03":"HomeAddress",
                    "PB01BS01":"BasicInfoCellphoneNumCount",
                    "PB020D01":"MaritalStatus",
                    "PB020Q01":"basic_info_spouse_name",
                    "PB020D02":"basic_info_spouse_id_type",
                    "PB020I01":"basic_info_spouse_id_num",
                    "PB020Q02":"basic_info_spouse_company",
                    "PB020Q03":"basic_info_spouse_phone"}
    
    column_list = ["PB01AD01",
                    "PB01AR01",
                    "PB01AD02",
                    "PB01AD03",
                    "PB01AD04",
                    "PB01AQ01",
                    "PB01AQ02",
                    "PB01AD05",
                    "PB01AQ03",
                    "PB01BS01",
                    "PB020D01",
                    "PB020Q01",
                    "PB020D02",
                    "PB020I01",
                    "PB020Q02",
                    "PB020Q03"]
    
        
    for i in column_list:
        if i not in list(basicInfo_df.columns):
            basicInfo_df[i] = np.nan
    
    basicInfo_df = basicInfo_df[column_list]
    if column_type == 'CNH':
        basicInfo_df.rename(columns = columns_chinese,inplace=True)
    else:
        basicInfo_df.rename(columns = columns_english,inplace=True)
    return basicInfo_df

#%%
###手机模块
def biMobile_df(temp1,column_type = 'CNH'):
    biMobile_df = pd.DataFrame()
    try:
        tmp = temp1['Document']['PIM']['PB01']['PB01B']['PB01BH']
        tmp = pd.io.json.json_normalize(tmp)
        biMobile_df = pd.concat([biMobile_df,tmp],axis=1)
    except:
        pass
    
    if len(biMobile_df)<1: 
        biMobile_df = pd.DataFrame({"PB01BQ01":np.nan,
                             "PB01BR01":np.nan,},index=[0])
            

    columns_chinese = {"PB01BQ01":"手机号码",
                       "PB01BR01":"信息更新日期",}
    
    
    # columns_english = {"PB01BQ01":"bi_mobile_phone_num",
    #                    "PB01BR01":"bi_mobile_update_date",}
    columns_english = {"PB01BQ01":"PhoneNo",
                   "PB01BR01":"UpdateDate",}
    
    column_list = ["PB01BQ01",
    "PB01BR01",]
    
    
        
    for i in column_list:
        if i not in list(biMobile_df.columns):
            biMobile_df[i] = np.nan
    
    biMobile_df = biMobile_df[column_list]
    if column_type == 'CNH':
        biMobile_df.rename(columns = columns_chinese,inplace=True)
    else:
        biMobile_df.rename(columns = columns_english,inplace=True)
    return biMobile_df

#%%
###居住情况
def biHouse_df(temp1,column_type = 'CNH'):
    biHouse_df = pd.DataFrame()
    try:
        tmp = temp1['Document']['PRM']['PB03']
        tmp = pd.io.json.json_normalize(tmp)
        biHouse_df = pd.concat([biHouse_df,tmp],axis=1)
    except:
        pass

    
    if len(biHouse_df)<1:
        biHouse_df = pd.DataFrame({"PB030D01":np.nan,
                                    "PB030Q01":np.nan,
                                    "PB030Q02":np.nan,
                                    "PB030R01":np.nan,},index=[0])
        
    columns_chinese = {"PB030D01":"居住状况",
                        "PB030Q01":"居住地址",
                        "PB030Q02":"住宅电话",
                        "PB030R01":"信息更新日期",}
    
    
    # columns_english = {"PB030D01":"bi_house_house_status",
    #                     "PB030Q01":"bi_house_house_addr",
    #                     "PB030Q02":"bi_house_house_tel",
    #                     "PB030R01":"bi_house_update_date",}
    columns_english = {"PB030D01":"LivingSituation",
                    "PB030Q01":"Address",
                    "PB030Q02":"HomePhoneNo",
                    "PB030R01":"UpdateDate",}
    
    column_list = ["PB030D01",
                    "PB030Q01",
                    "PB030Q02",
                    "PB030R01",]
    
    
        
    for i in column_list:
        if i not in list(biHouse_df.columns):
            biHouse_df[i] = np.nan
    
    biHouse_df = biHouse_df[column_list]
    if column_type == 'CNH':
        biHouse_df.rename(columns = columns_chinese,inplace=True)
    else:
        biHouse_df.rename(columns = columns_english,inplace=True)
    return biHouse_df

#%%
###工作模块
def biJob_df(temp1,column_type = 'CNH'):
    biJob_df = pd.DataFrame()
    try:
        tmp = temp1['Document']['POM']['PB04']
        tmp = pd.io.json.json_normalize(tmp)
        biJob_df = pd.concat([biJob_df,tmp],axis=1)
    except:
        pass
    
    if len(biJob_df)<1:
        biJob_df = pd.DataFrame({"PB040D01":np.nan,
                                "PB040Q01":np.nan,
                                "PB040D02":np.nan,
                                "PB040D03":np.nan,
                                "PB040Q02":np.nan,
                                "PB040Q03":np.nan,
                                "PB040D04":np.nan,
                                "PB040D05":np.nan,
                                "PB040D06":np.nan,
                                "PB040R01":np.nan,
                                "PB040R02":np.nan,
                                },index=[0])
        
    columns_chinese = {"PB040D01":"就业状况",
                        "PB040Q01":"工作单位",
                        "PB040D02":"单位性质",
                        "PB040D03":"行业",
                        "PB040Q02":"单位地址",
                        "PB040Q03":"单位电话",
                        "PB040D04":"职业",
                        "PB040D05":"职务",
                        "PB040D06":"职称",
                        "PB040R01":"进入本单位年份",
                        "PB040R02":"信息更新日期",}
    # columns_english = {"PB040D01":"bi_job_work_status",
    #                     "PB040Q01":"bi_job_company",
    #                     "PB040D02":"bi_job_company_type",
    #                     "PB040D03":"bi_job_industry",
    #                     "PB040Q02":"bi_job_company_addr",
    #                     "PB040Q03":"bi_job_company_tel",
    #                     "PB040D04":"bi_job_occupation",
    #                     "PB040D05":"bi_job_position",
    #                     "PB040D06":"bi_job_position_title",
    #                     "PB040R01":"bi_job_employed_year",
    #                     "PB040R02":"bi_job_update_date",}
    columns_english = {"PB040D01":"WorkStatus",
                    "PB040Q01":"Employer",
                    "PB040D02":"CompanyType",
                    "PB040D03":"Industry",
                    "PB040Q02":"EmployerAddress",
                    "PB040Q03":"CompanyPhoneNo",
                    "PB040D04":"Profession",
                    "PB040D05":"Position",
                    "PB040D06":"Title",
                    "PB040R01":"CurrentJobYear",
                    "PB040R02":"UpdateDate",}
    
    column_list = ["PB040D01",
                    "PB040Q01",
                    "PB040D02",
                    "PB040D03",
                    "PB040Q02",
                    "PB040Q03",
                    "PB040D04",
                    "PB040D05",
                    "PB040D06",
                    "PB040R01",
                    "PB040R02",]
    
    
        
    for i in column_list:
        if i not in list(biJob_df.columns):
            biJob_df[i] = np.nan
    
    biJob_df = biJob_df[column_list]
    if column_type == 'CNH':
        biJob_df.rename(columns = columns_chinese,inplace=True)
    else:
        biJob_df.rename(columns = columns_english,inplace=True)
    return biJob_df

#%%
###信息概要信息段
def infoSummary_df(temp1,column_type = 'CNH'):
    infoSummary_df = pd.DataFrame()
    
    try:
        tmp = temp1['Document']['PSM']['PC01']
        tmp = list_to_df(tmp)
        infoSummary_df = pd.concat([infoSummary_df,tmp],axis=1)
    except:
        pass
        
        
    
    for j in ['PC02A','PC02B','PC02C','PC02D','PC02E','PC02F','PC02G','PC02H','PC02I','PC02K']:
        try:
            tmp =copy.deepcopy(temp1['Document']['PCO']['PC02'][j])
            # print('tmp=',tmp,'\n')
            if 'PC02AH' in tmp:
                tmp.pop('PC02AH', None)

            if 'PC02BH' in tmp:
                tmp.pop('PC02BH', None)

            if 'PC02DH' in tmp:
                tmp.pop('PC02DH', None)

            tmp = list_to_df(tmp)
            infoSummary_df = pd.concat([infoSummary_df,tmp],axis=1)
        except:
            continue
    
    try:
        tmp =(temp1['Document']['PNO']['PC03'])
        tmp = list_to_df(tmp)
        infoSummary_df = pd.concat([infoSummary_df,tmp],axis=1)
    except:
        pass
    
    try:
        tmp =(temp1['Document']['PPO']['PC04'])
        tmp = list_to_df(tmp)
        infoSummary_df = pd.concat([infoSummary_df,tmp],axis=1)
    except:
        pass
    
    for j in ['PC05A','PC05B']:
        try:
            tmp =(temp1['Document']['PQO']['PC05'][j])
            tmp = list_to_df(tmp)
            infoSummary_df = pd.concat([infoSummary_df,tmp],axis=1)
        except:
            continue
    
    if len(infoSummary_df)<1:
        infoSummary_df = pd.DataFrame({"PC010Q01":np.nan,
                                        "PC010Q02":np.nan,
                                        "PC010S01":np.nan,
                                       "PC010D01":np.nan,
                                        "PC02AS01":np.nan,
                                        "PC02AS02":np.nan,
                                        "PC02BS01":np.nan,
                                        "PC02BJ01":np.nan,
                                        "PC02BS02":np.nan,
                                        "PC02CS01":np.nan,
                                        "PC02CJ01":np.nan,
                                        "PC02DS01":np.nan,
                                        "PC02ES01":np.nan,
                                        "PC02ES02":np.nan,
                                        "PC02EJ01":np.nan,
                                        "PC02EJ02":np.nan,
                                        "PC02EJ03":np.nan,
                                        "PC02FS01":np.nan,
                                        "PC02FS02":np.nan,
                                        "PC02FJ01":np.nan,
                                        "PC02FJ02":np.nan,
                                        "PC02FJ03":np.nan,
                                        "PC02GS01":np.nan,
                                        "PC02GS02":np.nan,
                                        "PC02GJ01":np.nan,
                                        "PC02GJ02":np.nan,
                                        "PC02GJ03":np.nan,
                                        "PC02HS01":np.nan,
                                        "PC02HS02":np.nan,
                                        "PC02HJ01":np.nan,
                                        "PC02HJ02":np.nan,
                                        "PC02HJ03":np.nan,
                                        "PC02HJ04":np.nan,
                                        "PC02HJ05":np.nan,
                                        "PC02IS01":np.nan,
                                        "PC02IS02":np.nan,
                                        "PC02IJ01":np.nan,
                                        "PC02IJ02":np.nan,
                                        "PC02IJ03":np.nan,
                                        "PC02IJ04":np.nan,
                                        "PC02IJ05":np.nan,
                                        "PC02KS01":np.nan,
                                        "PC030S01":np.nan,
                                        "PC040S01":np.nan,
                                        "PC05AR01":np.nan,
                                        "PC05AD01":np.nan,
                                        "PC05AI01":np.nan,
                                        "PC05AQ01":np.nan,
                                        "PC05BS01":np.nan,
                                        "PC05BS02":np.nan,
                                        "PC05BS03":np.nan,
                                        "PC05BS04":np.nan,
                                        "PC05BS05":np.nan,
                                        "PC05BS06":np.nan,
                                        "PC05BS07":np.nan,
                                        "PC05BS08":np.nan,
                                        },index=[0])
        
    columns_chinese = {"PC010Q01":"评分信息-评分信息-数字解读",
                        "PC010Q02":"评分信息-评分信息-相对位置",
                        "PC010S01":"评分信息-评分信息-分数说明条数",
                       "PC010D01":"评分信息-评分信息-分数说明",
                        "PC02AS01":"信贷交易信息概要-信贷交易提示-账户数合计",
                        "PC02AS02":"信贷交易信息概要-信贷交易提示-业务类型数量",
                        "PC02BS01":"信贷交易信息概要-被追偿汇总信息-账户数合计",
                        "PC02BJ01":"信贷交易信息概要-被追偿汇总信息-余额合计",
                        "PC02BS02":"信贷交易信息概要-被追偿汇总信息-业务类型数量",
                        "PC02CS01":"信贷交易信息概要-呆账汇总信息-账户数",
                        "PC02CJ01":"信贷交易信息概要-呆账汇总信息-余额",
                        "PC02DS01":"信贷交易信息概要-逾期（透支）汇总信息-账户类型数量",
                        "PC02ES01":"信贷交易信息概要-非循环贷账户汇总信息-管理机构数",
                        "PC02ES02":"信贷交易信息概要-非循环贷账户汇总信息-账户数",
                        "PC02EJ01":"信贷交易信息概要-非循环贷账户汇总信息-授信总额",
                        "PC02EJ02":"信贷交易信息概要-非循环贷账户汇总信息-余额",
                        "PC02EJ03":"信贷交易信息概要-非循环贷账户汇总信息-最近6个月平均应还款",
                        "PC02FS01":"信贷交易信息概要-循环额度下分账户汇总信息-管理机构数",
                        "PC02FS02":"信贷交易信息概要-循环额度下分账户汇总信息-账户数",
                        "PC02FJ01":"信贷交易信息概要-循环额度下分账户汇总信息-授信总额",
                        "PC02FJ02":"信贷交易信息概要-循环额度下分账户汇总信息-余额",
                        "PC02FJ03":"信贷交易信息概要-循环额度下分账户汇总信息-最近6个月平均应还款",
                        "PC02GS01":"信贷交易信息概要-循环贷账户汇总信息-管理机构数",
                        "PC02GS02":"信贷交易信息概要-循环贷账户汇总信息-账户数",
                        "PC02GJ01":"信贷交易信息概要-循环贷账户汇总信息-授信总额",
                        "PC02GJ02":"信贷交易信息概要-循环贷账户汇总信息-余额",
                        "PC02GJ03":"信贷交易信息概要-循环贷账户汇总信息-最近6个月平均应还款",
                        "PC02HS01":"信贷交易信息概要-贷记卡账户汇总信息-发卡机构数",
                        "PC02HS02":"信贷交易信息概要-贷记卡账户汇总信息-账户数",
                        "PC02HJ01":"信贷交易信息概要-贷记卡账户汇总信息-授信总额",
                        "PC02HJ02":"信贷交易信息概要-贷记卡账户汇总信息-单家行最高授信额",
                        "PC02HJ03":"信贷交易信息概要-贷记卡账户汇总信息-单家行最低授信额",
                        "PC02HJ04":"信贷交易信息概要-贷记卡账户汇总信息-已用额度",
                        "PC02HJ05":"信贷交易信息概要-贷记卡账户汇总信息-最近6个月平均使用额度",
                        "PC02IS01":"信贷交易信息概要-准贷记卡账户汇总信息-发卡机构数",
                        "PC02IS02":"信贷交易信息概要-准贷记卡账户汇总信息-账户数",
                        "PC02IJ01":"信贷交易信息概要-准贷记卡账户汇总信息-授信总额",
                        "PC02IJ02":"信贷交易信息概要-准贷记卡账户汇总信息-单家行最高授信额",
                        "PC02IJ03":"信贷交易信息概要-准贷记卡账户汇总信息-单家行最低授信额",
                        "PC02IJ04":"信贷交易信息概要-准贷记卡账户汇总信息-透支余额",
                        "PC02IJ05":"信贷交易信息概要-准贷记卡账户汇总信息-最近6个月平均透支余额",
                        "PC02KS01":"信贷交易信息概要-相关还款责任汇总信息-相关还款责任个数",
                        "PC030S01":"非信贷交易信息概要-后付费业务欠费信息-后付费业务类型数量",
                        "PC040S01":"公共信息概要-公共信息概要-公共信息类型数量",
                        "PC05AR01":"查询记录概要-上一次查询记录信息-上一次查询日期",
                        "PC05AD01":"查询记录概要-上一次查询记录信息-上一次查询机构类型",
                        "PC05AI01":"查询记录概要-上一次查询记录信息-上一次查询机构代码",
                        "PC05AQ01":"查询记录概要-上一次查询记录信息-上一次查询原因",
                        "PC05BS01":"查询记录概要-查询记录概要信息-最近1个月内的查询机构数（贷款审批）",
                        "PC05BS02":"查询记录概要-查询记录概要信息-最近1个月内的查询机构数（信用卡审批）",
                        "PC05BS03":"查询记录概要-查询记录概要信息-最近1个月内的查询次数（贷款审批）",
                        "PC05BS04":"查询记录概要-查询记录概要信息-最近1个月内的查询次数（信用卡审批）",
                        "PC05BS05":"查询记录概要-查询记录概要信息-最近1个月内的查询次数（本人查询）",
                        "PC05BS06":"查询记录概要-查询记录概要信息-最近2年内的查询次数（贷后管理）",
                        "PC05BS07":"查询记录概要-查询记录概要信息-最近2年内的查询次数（担保资格审查）",
                        "PC05BS08":"查询记录概要-查询记录概要信息-最近2年内的查询次数（特约商户实名审批）",
                        }
    
    
    # columns_english = {"PC010Q01":"info_summary_score_interpretation",
    #                     "PC010Q02":"info_summary_score_relative_position",
    #                     "PC010S01":"info_summary_score_explain_count",
    #                     "PC010D01":"info_summary_score_explain",
    #                     "PC02AS01":"info_summary_credit_account_count",
    #                     "PC02AS02":"info_summary_credit_business_type_count",
    #                     "PC02BS01":"info_summary_recovered_account_count",
    #                     "PC02BJ01":"info_summary_recovered_balance_sum",
    #                     "PC02BS02":"info_summary_recovered_business_type_count",
    #                     "PC02CS01":"info_summary_bad_debt_account_count",
    #                     "PC02CJ01":"info_summary_bad_debt_balance",
    #                     "PC02DS01":"info_summary_overdue_account_type_count",
    #                     "PC02ES01":"info_summary_noncycle_manage_org_count",
    #                     "PC02ES02":"info_summary_noncycle_account_count",
    #                     "PC02EJ01":"info_summary_noncycle_credit_amt_sum",
    #                     "PC02EJ02":"info_summary_noncycle_balance",
    #                     "PC02EJ03":"info_summary_noncycle_l6m_avg_repayable",
    #                     "PC02FS01":"info_summary_revolving_manage_org_count",
    #                     "PC02FS02":"info_summary_revolving_account_count",
    #                     "PC02FJ01":"info_summary_revolving_credit_amt_sum",
    #                     "PC02FJ02":"info_summary_revolving_balance",
    #                     "PC02FJ03":"info_summary_revolving_l6m_avg_repayable",
    #                     "PC02GS01":"info_summary_cycle_manage_org_count",
    #                     "PC02GS02":"info_summary_cycle_account_count",
    #                     "PC02GJ01":"info_summary_cycle_credit_amt_sum",
    #                     "PC02GJ02":"info_summary_cycle_balance",
    #                     "PC02GJ03":"info_summary_cycle_l6m_avg_repayable",
    #                     "PC02HS01":"info_summary_cc_issuer_count",
    #                     "PC02HS02":"info_summary_cc_account_count",
    #                     "PC02HJ01":"info_summary_cc_credit_amt_sum",
    #                     "PC02HJ02":"info_summary_cc_single_max_credit_amt",
    #                     "PC02HJ03":"info_summary_cc_single_min_credit_amt",
    #                     "PC02HJ04":"info_summary_cc_used_amt",
    #                     "PC02HJ05":"info_summary_cc_l6m_avg_used_amt",
    #                     "PC02IS01":"info_summary_qcc_issuer_count",
    #                     "PC02IS02":"info_summary_qcc_account_count",
    #                     "PC02IJ01":"info_summary_qcc_credit_amt_sum",
    #                     "PC02IJ02":"info_summary_qcc_single_max_credit_amt",
    #                     "PC02IJ03":"info_summary_qcc_single_min_credit_amt",
    #                     "PC02IJ04":"info_summary_qcc_overdraw_balance",
    #                     "PC02IJ05":"info_summary_qcc_l6m_avg_overdraw_bal",
    #                     "PC02KS01":"info_summary_related_repay_duty_count",
    #                     "PC030S01":"info_summary_postpaid_business_type_count",
    #                     "PC040S01":"info_summary_pub_info_type_count",
    #                     "PC05AR01":"info_summary_last_query_date",
    #                     "PC05AD01":"info_summary_last_query_org_type",
    #                     "PC05AI01":"info_summary_last_query_org_code",
    #                     "PC05AQ01":"info_summary_last_query_reason",
    #                     "PC05BS01":"info_summary_query_lastmonth_org_count_loan",
    #                     "PC05BS02":"info_summary_query_lastmonth_org_count_card",
    #                     "PC05BS03":"info_summary_query_lastmonth_count_loan",
    #                     "PC05BS04":"info_summary_query_lastmonth_count_card",
    #                     "PC05BS05":"info_summary_query_lastmonth_count_self",
    #                     "PC05BS06":"info_summary_query_l2y_count_loan",
    #                     "PC05BS07":"info_summary_query_l2y_count_guarantee",
    #                     "PC05BS08":"info_summary_query_l2y_count_special",
    #                     }
    
    columns_english = {"PC010Q01":"DigitalInterpretation",
                        "PC010Q02":"RelativePosition",
                        "PC010S01":"info_summary_score_explain_count",
                        "PC010D01":"info_summary_score_explain",
                        "PC02AS01":"info_summary_credit_account_count",
                        "PC02AS02":"info_summary_credit_business_type_count",
                        "PC02BS01":"info_summary_recovered_account_count",
                        "PC02BJ01":"info_summary_recovered_balance_sum",
                        "PC02BS02":"info_summary_recovered_business_type_count",
                        "PC02CS01":"CountOfAccount",
                        "PC02CJ01":"Balance",
                        "PC02DS01":"info_summary_overdue_account_type_count",
                        "PC02ES01":"info_summary_noncycle_manage_org_count",
                        "PC02ES02":"info_summary_noncycle_account_count",
                        "PC02EJ01":"info_summary_noncycle_credit_amt_sum",
                        "PC02EJ02":"info_summary_noncycle_balance",
                        "PC02EJ03":"info_summary_noncycle_l6m_avg_repayable",
                        "PC02FS01":"info_summary_revolving_manage_org_count",
                        "PC02FS02":"info_summary_revolving_account_count",
                        "PC02FJ01":"info_summary_revolving_credit_amt_sum",
                        "PC02FJ02":"info_summary_revolving_balance",
                        "PC02FJ03":"info_summary_revolving_l6m_avg_repayable",
                        "PC02GS01":"info_summary_cycle_manage_org_count",
                        "PC02GS02":"info_summary_cycle_account_count",
                        "PC02GJ01":"info_summary_cycle_credit_amt_sum",
                        "PC02GJ02":"info_summary_cycle_balance",
                        "PC02GJ03":"info_summary_cycle_l6m_avg_repayable",
                        "PC02HS01":"info_summary_cc_issuer_count",
                        "PC02HS02":"info_summary_cc_account_count",
                        "PC02HJ01":"info_summary_cc_credit_amt_sum",
                        "PC02HJ02":"info_summary_cc_single_max_credit_amt",
                        "PC02HJ03":"info_summary_cc_single_min_credit_amt",
                        "PC02HJ04":"info_summary_cc_used_amt",
                        "PC02HJ05":"info_summary_cc_l6m_avg_used_amt",
                        "PC02IS01":"info_summary_qcc_issuer_count",
                        "PC02IS02":"info_summary_qcc_account_count",
                        "PC02IJ01":"info_summary_qcc_credit_amt_sum",
                        "PC02IJ02":"info_summary_qcc_single_max_credit_amt",
                        "PC02IJ03":"info_summary_qcc_single_min_credit_amt",
                        "PC02IJ04":"info_summary_qcc_overdraw_balance",
                        "PC02IJ05":"info_summary_qcc_l6m_avg_overdraw_bal",
                        "PC02KS01":"info_summary_related_repay_duty_count",
                        "PC030S01":"info_summary_postpaid_business_type_count",
                        "PC040S01":"info_summary_pub_info_type_count",
                        "PC05AR01":"LastQueryRecordDate",
                        "PC05AD01":"info_summary_last_query_org_type",
                        "PC05AI01":"LastQueryRecordAgency",
                        "PC05AQ01":"LastQueryRecordReason",
                        "PC05BS01":"CountOfCreditApprovalQueryInstitutionInLastMonth",
                        "PC05BS02":"CountOfCreditCardApprovalQueryInstitutionInLastMonth",
                        "PC05BS03":"QueryTimesOfCreditApprovalInLastMonth",
                        "PC05BS04":"QueryTimesOfCreditCardApprovalInLastMonth",
                        "PC05BS05":"SelfQueryTimesInLastMonth",
                        "PC05BS06":"QueryTimesOfPostloanManagementInLastTwoMonth",
                        "PC05BS07":"QueryTimesOfGuaranteeQualificationAssessment",
                        "PC05BS08":"QueryTimesOfMerchantsRealnameReview",
                        }
    
    column_list = ["PC010Q01",
                    "PC010Q02",
                    "PC010S01",
                    "PC010D01",
                    "PC02AS01",
                    "PC02AS02",
                    "PC02BS01",
                    "PC02BJ01",
                    "PC02BS02",
                    "PC02CS01",
                    "PC02CJ01",
                    "PC02DS01",
                    "PC02ES01",
                    "PC02ES02",
                    "PC02EJ01",
                    "PC02EJ02",
                    "PC02EJ03",
                    "PC02FS01",
                    "PC02FS02",
                    "PC02FJ01",
                    "PC02FJ02",
                    "PC02FJ03",
                    "PC02GS01",
                    "PC02GS02",
                    "PC02GJ01",
                    "PC02GJ02",
                    "PC02GJ03",
                    "PC02HS01",
                    "PC02HS02",
                    "PC02HJ01",
                    "PC02HJ02",
                    "PC02HJ03",
                    "PC02HJ04",
                    "PC02HJ05",
                    "PC02IS01",
                    "PC02IS02",
                    "PC02IJ01",
                    "PC02IJ02",
                    "PC02IJ03",
                    "PC02IJ04",
                    "PC02IJ05",
                    "PC02KS01",
                    "PC030S01",
                    "PC040S01",
                    "PC05AR01",
                    "PC05AD01",
                    "PC05AI01",
                    "PC05AQ01",
                    "PC05BS01",
                    "PC05BS02",
                    "PC05BS03",
                    "PC05BS04",
                    "PC05BS05",
                    "PC05BS06",
                    "PC05BS07",
                    "PC05BS08",
                    ]
        
    for i in column_list:
        if i not in list(infoSummary_df.columns):
            infoSummary_df[i] = np.nan
    
    infoSummary_df = infoSummary_df[column_list]
    if column_type == 'CNH':
        infoSummary_df.rename(columns = columns_chinese,inplace=True)
    else:
        infoSummary_df.rename(columns = columns_english,inplace=True)
    return infoSummary_df

#%%
###信贷交易提示信息段
def isCreditTransInfo_df(temp1,column_type = 'CNH'):
    isCreditTransInfo_df = pd.DataFrame()
    
    try:
        tmp = temp1['Document']['PCO']['PC02']['PC02A']['PC02AH']
        tmp = pd.io.json.json_normalize(tmp)
        isCreditTransInfo_df = pd.concat([isCreditTransInfo_df,tmp],axis=1)
    except:
        pass
    
    if len(isCreditTransInfo_df)<1:
        isCreditTransInfo_df = pd.DataFrame({"PC02AD01":np.nan,
                                            "PC02AD02":np.nan,
                                            "PC02AS03":np.nan,
                                            "PC02AR01":np.nan,
                                            },index=[0])
                                                
    columns_chinese = {"PC02AD01":"业务类型",
                        "PC02AD02":"业务大类",
                        "PC02AS03":"账户数",
                        "PC02AR01":"首笔业务发放月份",}
    
    
    # columns_english = {"PC02AD01":"is_crdt_trans_info_business_type",
    #                     "PC02AD02":"is_crdt_trans_info_business_category",
    #                     "PC02AS03":"is_crdt_trans_info_account_count",
    #                     "PC02AR01":"is_crdt_trans_info_first_business_month",}
    columns_english = {"PC02AD01":"BusinessSubType",
                    "PC02AD02":"BusinessType",
                    "PC02AS03":"CountOfAccount",
                    "PC02AR01":"MonthOfFirstTransaction",}
    
    
    column_list = ["PC02AD01",
                    "PC02AD02",
                    "PC02AS03",
                    "PC02AR01",]
    
    
    
        
    for i in column_list:
        if i not in list(isCreditTransInfo_df.columns):
            isCreditTransInfo_df[i] = np.nan
    
    isCreditTransInfo_df = isCreditTransInfo_df[column_list]
    if column_type == 'CNH':
        isCreditTransInfo_df.rename(columns = columns_chinese,inplace=True)
    else:
        isCreditTransInfo_df.rename(columns = columns_english,inplace=True)
    return isCreditTransInfo_df

#%%
###被追偿汇总信息
def isRecoveredSum_df(temp1,column_type = 'CNH'):
    isRecoveredSum_df = pd.DataFrame()
    
    try:
        tmp = temp1['Document']['PCO']['PC02']['PC02B']['PC02BH']
        tmp = pd.io.json.json_normalize(tmp)
        isRecoveredSum_df = pd.concat([isRecoveredSum_df,tmp],axis=1)
    except:
        pass
    
    if len(isRecoveredSum_df)<1:
        isRecoveredSum_df = pd.DataFrame({"PC02BD01":np.nan,
                                            "PC02BS03":np.nan,
                                            "PC02BJ02":np.nan,},index=[0])
                                                
    columns_chinese = {"PC02BD01":"业务大类",
                        "PC02BS03":"账户数",
                        "PC02BJ02":"余额",}
    
    
    # columns_english = {"PC02BD01":"is_recovered_sum_business_category",
    #                     "PC02BS03":"is_recovered_sum_account_count",
    #                     "PC02BJ02":"is_recovered_sum_balance",}
    columns_english = {"PC02BD01":"BusinessType",
                    "PC02BS03":"CountOfAccount",
                    "PC02BJ02":"Balance",}
    
    
    column_list = ["PC02BD01",
                    "PC02BS03",
                    "PC02BJ02",]
    
    
    
        
    for i in column_list:
        if i not in list(isRecoveredSum_df.columns):
            isRecoveredSum_df[i] = np.nan
    
    isRecoveredSum_df = isRecoveredSum_df[column_list]
    if column_type == 'CNH':
        isRecoveredSum_df.rename(columns = columns_chinese,inplace=True)
    else:
        isRecoveredSum_df.rename(columns = columns_english,inplace=True)
    return isRecoveredSum_df

#%%
###逾期（透支）汇总信息段
def isOverdueSum_df(temp1,column_type = 'CNH'):
    isOverdueSum_df = pd.DataFrame()
    
    try:
        tmp = temp1['Document']['PCO']['PC02']['PC02D']['PC02DH']
        tmp = pd.io.json.json_normalize(tmp)
        isOverdueSum_df = pd.concat([isOverdueSum_df,tmp],axis=1)
    except:
        pass
    
    if len(isOverdueSum_df)<1:
        isOverdueSum_df = pd.DataFrame({"PC02DD01":np.nan,
                                        "PC02DS02":np.nan,
                                        "PC02DS03":np.nan,
                                        "PC02DJ01":np.nan,
                                        "PC02DS04":np.nan,},index=[0])
                                                
    columns_chinese = {"PC02DD01":"账户类型",
                        "PC02DS02":"账户数",
                        "PC02DS03":"月份数",
                        "PC02DJ01":"单月最高逾期（透支）金额",
                        "PC02DS04":"最长逾期（透支）月数",}
    
    
    # columns_english = {"PC02DD01":"is_overdue_sum_account_type",
    #                     "PC02DS02":"is_overdue_sum_account_count",
    #                     "PC02DS03":"is_overdue_sum_month_count",
    #                     "PC02DJ01":"is_overdue_sum_max_overdue_amt",
    #                     "PC02DS04":"is_overdue_sum_max_overdue_month_count",}
    
    columns_english = {"PC02DD01":"AccountType",
                    "PC02DS02":"CountOfAccount",
                    "PC02DS03":"CountOfMonth",
                    "PC02DJ01":"HighestOverdueAmountByMonth",
                    "PC02DS04":"LongestOverdueMonth",}
    
    
    column_list = ["PC02DD01",
                    "PC02DS02",
                    "PC02DS03",
                    "PC02DJ01",
                    "PC02DS04",]
    
    
    
        
    for i in column_list:
        if i not in list(isOverdueSum_df.columns):
            isOverdueSum_df[i] = np.nan
    
    isOverdueSum_df = isOverdueSum_df[column_list]
    if column_type == 'CNH':
        isOverdueSum_df.rename(columns = columns_chinese,inplace=True)
    else:
        isOverdueSum_df.rename(columns = columns_english,inplace=True)
    return isOverdueSum_df    

#%%
### 相关还款责任汇总信息
def isRepayDutySum_df(temp1,column_type = 'CNH'):
    isRepayDutySum_df = pd.DataFrame()
    
    try:
        tmp = temp1['Document']['PCO']['PC02']['PC02K']['PC02KH']
        tmp = pd.io.json.json_normalize(tmp)
        isRepayDutySum_df = pd.concat([isRepayDutySum_df,tmp],axis=1)
    except:
        pass
    
    if len(isRepayDutySum_df)<1:
        isRepayDutySum_df = pd.DataFrame({"PC02KD01":np.nan,
                                            "PC02KD02":np.nan,
                                            "PC02KS02":np.nan,
                                            "PC02KJ01":np.nan,
                                            "PC02KJ02":np.nan,
                                            },index=[0])
                                                
    columns_chinese = {"PC02KD01":"借款人身份类别",
                        "PC02KD02":"相关还款责任类型",
                        "PC02KS02":"账户数",
                        "PC02KJ01":"还款责任金额",
                        "PC02KJ02":"余额",}
    
    
    # columns_english = {"PC02KD01":"is_repay_duty_sum_borrower_type",
    #                     "PC02KD02":"is_repay_duty_sum_repay_duty_type",
    #                     "PC02KS02":"is_repay_duty_sum_account_count",
    #                     "PC02KJ01":"is_repay_duty_sum_repay_duty_amt",
    #                     "PC02KJ02":"is_repay_duty_sum_balance",}
    
    columns_english = {"PC02KD01":"BorrowerType",
                    "PC02KD02":"RepaymentType",
                    "PC02KS02":"CountOfAccount",
                    "PC02KJ01":"AmountOfGuarantee",
                    "PC02KJ02":"OutstandingBalance",}
    column_list = ["PC02KD01",
                    "PC02KD02",
                    "PC02KS02",
                    "PC02KJ01",
                    "PC02KJ02",]
    
    
    
        
    for i in column_list:
        if i not in list(isRepayDutySum_df.columns):
            isRepayDutySum_df[i] = np.nan
    
    isRepayDutySum_df = isRepayDutySum_df[column_list]
    if column_type == 'CNH':
        isRepayDutySum_df.rename(columns = columns_chinese,inplace=True)
    else:
        isRepayDutySum_df.rename(columns = columns_english,inplace=True)
    return isRepayDutySum_df    

#%%
###后付费业务欠费信息汇总
def isPostpaidSum_df(temp1,column_type = 'CNH'):
    isPostpaidSum_df = pd.DataFrame()
    
    try:
        tmp = temp1['Document']['PNO']['PC03']['PC030H']
        tmp = pd.io.json.json_normalize(tmp)
        isPostpaidSum_df = pd.concat([isPostpaidSum_df,tmp],axis=1)
    except:
        pass
    
    if len(isPostpaidSum_df)<1:
        isPostpaidSum_df = pd.DataFrame({"PC030D01":np.nan,
                                        "PC030S02":np.nan,
                                        "PC030J01":np.nan,},index=[0])
                                                
    columns_chinese = {"PC030D01":"后付费业务类型",
                        "PC030S02":"欠费账户数",
                        "PC030J01":"欠费金额",}
    
    
    # columns_english = {"PC030D01":"is_postpaid_sum_postpaid_business_type",
    #                     "PC030S02":"is_postpaid_sum_arrear_account_count",
    #                     "PC030J01":"is_postpaid_sum_arrear_amt",}
    columns_english = {"PC030D01":"ServiceType",
                    "PC030S02":"CountOfAccounts",
                    "PC030J01":"OverdueAmount",}
    
    
    column_list = ["PC030D01",
                    "PC030S02",
                    "PC030J01",]

    
    
    
        
    for i in column_list:
        if i not in list(isPostpaidSum_df.columns):
            isPostpaidSum_df[i] = np.nan
    
    isPostpaidSum_df = isPostpaidSum_df[column_list]
    if column_type == 'CNH':
        isPostpaidSum_df.rename(columns = columns_chinese,inplace=True)
    else:
        isPostpaidSum_df.rename(columns = columns_english,inplace=True)
    return isPostpaidSum_df    

#%%
###公共信息概要
def isPubInfoSum_df(temp1,column_type = 'CNH'):
    isPubInfoSum_df = pd.DataFrame()
    
    try:
        tmp = temp1['Document']['PPO']['PC04']['PC040H']
        tmp = pd.io.json.json_normalize(tmp)
        isPubInfoSum_df = pd.concat([isPubInfoSum_df,tmp],axis=1)
    except:
        pass
    
    if len(isPubInfoSum_df)<1:
        isPubInfoSum_df = pd.DataFrame({"PC040D01":np.nan,
                                        "PC040S02":np.nan,
                                        "PC040J01":np.nan,},index=[0])
                                                
    columns_chinese = {"PC040D01":"信息类型",
                        "PC040S02":"记录数",
                        "PC040J01":"涉及金额",}
    
    
    # columns_english = {"PC040D01":"is_postpaid_sum_postpaid_business_type",
    #                     "PC040S02":"is_postpaid_sum_arrear_account_count",
    #                     "PC040J01":"is_postpaid_sum_arrear_amt",}
    
    columns_english = {"PC040D01":"InformationType",
                    "PC040S02":"CountOfRecord",
                    "PC040J01":"TotalAmount",}
    
    column_list = ["PC040D01",
                    "PC040S02",
                    "PC040J01",]

    
    
    
        
    for i in column_list:
        if i not in list(isPubInfoSum_df.columns):
            isPubInfoSum_df[i] = np.nan
    
    isPubInfoSum_df = isPubInfoSum_df[column_list]
    if column_type == 'CNH':
        isPubInfoSum_df.rename(columns = columns_chinese,inplace=True)
    else:
        isPubInfoSum_df.rename(columns = columns_english,inplace=True)
    return isPubInfoSum_df 


#%%
###信贷交易明细
def debitCreditAccount_df(temp1,column_type = 'CNH'):
    debitCreditAccount_df = pd.DataFrame()

    try:
        tmp = copy.deepcopy(temp1['Document']['PDA']['PD01'])
        for n in range(len(tmp)):
            mid_df = pd.DataFrame()
            for j in ['PD01A','PD01B','PD01C','PD01E','PD01F','PD01G','PD01H','PD01Z']:
                if j in ['PD01A','PD01B','PD01C','PD01F','PD01G','PD01H','PD01Z']:
                    try:

                        tmp1 = tmp[n][j]

                        if 'PD01HH' in tmp1:
                            tmp1.pop('PD01HH',None)

                        if 'PD01GH' in tmp1:
                            tmp1.pop('PD01GH',None)

                        if 'PD01DH' in tmp1:
                            tmp1.pop('PD01DH',None)

                        if 'PD01FH' in tmp1:
                            tmp1.pop('PD01FH',None)

                        if 'PD01ZH' in tmp1:
                            tmp1.pop('PD01ZH',None)

                        tmp1 = list_to_df(tmp1)

                        mid_df = pd.concat([mid_df,tmp1],axis=1)
                    except:
                        pass
                elif j in ['PD01E']:
                    try:
                        tmp1 = tmp[n][j]
                        tmp1 = list_to_df(tmp1)
                        mid_df = pd.concat([mid_df,tmp1],axis=1)
                    except:
                        pass
                    try:
                        tmp2 = tmp[n][j]['PD01EH']
                        tmp2 = pd.io.json.json_normalize(tmp2)
                        for h in ['PD01ER03','PD01ED01','PD01EJ01']:
                            if h not in list(tmp2.columns):
                                tmp2[h] = np.nan
                        mid_dic = {}
                        for u in range(0,60):
                            if u <= len(tmp2)-1:
                                mid_dic['Rpmonth' + str(u+1)] = list(tmp2['PD01ER03'])[u]
                            else:
                                mid_dic['Rpmonth' + str(u+1)] = np.nan
                        for u in range(0,60):
                            if u <= len(tmp2)-1:
                                mid_dic['Rpstatus' + str(u+1)] = list(tmp2['PD01ED01'])[u]
                            else:
                                mid_dic['Rpstatus' + str(u+1)] = np.nan
                        for u in range(0,60):
                            if u <= len(tmp2)-1:
                                mid_dic['Rpamt' + str(u+1)] = list(tmp2['PD01EJ01'])[u]
                            else:
                                mid_dic['Rpamt' + str(u+1)] = np.nan                      
                        mid_df2 = pd.DataFrame(mid_dic,index=[0])
                        mid_df = pd.concat([mid_df,mid_df2],axis=1)
                    except:
                        pass
            debitCreditAccount_df = pd.concat([debitCreditAccount_df,mid_df],axis=0)
    except:
        pass
    
    
    
    
    
    
    if len(debitCreditAccount_df)<1:
        debitCreditAccount_df = pd.DataFrame({"PD01AI01":np.nan,
                                        "PD01AD01":np.nan,
                                        "PD01AD02":np.nan,
                                        "PD01AI02":np.nan,
                                        "PD01AI03":np.nan,
                                        "PD01AI04":np.nan,
                                        "PD01AD03":np.nan,
                                        "PD01AR01":np.nan,
                                        "PD01AD04":np.nan,
                                        "PD01AJ01":np.nan,
                                        "PD01AJ02":np.nan,
                                        "PD01AJ03":np.nan,
                                        "PD01AR02":np.nan,
                                        "PD01AD05":np.nan,
                                        "PD01AD06":np.nan,
                                        "PD01AS01":np.nan,
                                        "PD01AD07":np.nan,
                                        "PD01AD08":np.nan,
                                        "PD01AD09":np.nan,
                                        "PD01AD10":np.nan,
                                        "PD01BD01":np.nan,
                                        "PD01BR01":np.nan,
                                        "PD01BR04":np.nan,
                                        "PD01BJ01":np.nan,
                                        "PD01BR02":np.nan,
                                        "PD01BJ02":np.nan,
                                        "PD01BD03":np.nan,
                                        "PD01BD04":np.nan,
                                        "PD01BR03":np.nan,
                                        "PD01CR01":np.nan,
                                        "PD01CD01":np.nan,
                                        "PD01CJ01":np.nan,
                                        "PD01CJ02":np.nan,
                                        "PD01CJ03":np.nan,
                                        "PD01CD02":np.nan,
                                        "PD01CS01":np.nan,
                                        "PD01CR02":np.nan,
                                        "PD01CJ04":np.nan,
                                        "PD01CJ05":np.nan,
                                        "PD01CR03":np.nan,
                                        "PD01CS02":np.nan,
                                        "PD01CJ06":np.nan,
                                        "PD01CJ07":np.nan,
                                        "PD01CJ08":np.nan,
                                        "PD01CJ09":np.nan,
                                        "PD01CJ10":np.nan,
                                        "PD01CJ11":np.nan,
                                        "PD01CJ12":np.nan,
                                        "PD01CJ13":np.nan,
                                        "PD01CJ14":np.nan,
                                        "PD01CJ15":np.nan,
                                        "PD01CR04":np.nan,
                                        "PD01ER01":np.nan,
                                        "PD01ER02":np.nan,
                                        "PD01ES01":np.nan,
                                        "Rpmonth1":np.nan,
                                        "Rpmonth2":np.nan,
                                        "Rpmonth3":np.nan,
                                        "Rpmonth4":np.nan,
                                        "Rpmonth5":np.nan,
                                        "Rpmonth6":np.nan,
                                        "Rpmonth7":np.nan,
                                        "Rpmonth8":np.nan,
                                        "Rpmonth9":np.nan,
                                        "Rpmonth10":np.nan,
                                        "Rpmonth11":np.nan,
                                        "Rpmonth12":np.nan,
                                        "Rpmonth13":np.nan,
                                        "Rpmonth14":np.nan,
                                        "Rpmonth15":np.nan,
                                        "Rpmonth16":np.nan,
                                        "Rpmonth17":np.nan,
                                        "Rpmonth18":np.nan,
                                        "Rpmonth19":np.nan,
                                        "Rpmonth20":np.nan,
                                        "Rpmonth21":np.nan,
                                        "Rpmonth22":np.nan,
                                        "Rpmonth23":np.nan,
                                        "Rpmonth24":np.nan,
                                        "Rpmonth25":np.nan,
                                        "Rpmonth26":np.nan,
                                        "Rpmonth27":np.nan,
                                        "Rpmonth28":np.nan,
                                        "Rpmonth29":np.nan,
                                        "Rpmonth30":np.nan,
                                        "Rpmonth31":np.nan,
                                        "Rpmonth32":np.nan,
                                        "Rpmonth33":np.nan,
                                        "Rpmonth34":np.nan,
                                        "Rpmonth35":np.nan,
                                        "Rpmonth36":np.nan,
                                        "Rpmonth37":np.nan,
                                        "Rpmonth38":np.nan,
                                        "Rpmonth39":np.nan,
                                        "Rpmonth40":np.nan,
                                        "Rpmonth41":np.nan,
                                        "Rpmonth42":np.nan,
                                        "Rpmonth43":np.nan,
                                        "Rpmonth44":np.nan,
                                        "Rpmonth45":np.nan,
                                        "Rpmonth46":np.nan,
                                        "Rpmonth47":np.nan,
                                        "Rpmonth48":np.nan,
                                        "Rpmonth49":np.nan,
                                        "Rpmonth50":np.nan,
                                        "Rpmonth51":np.nan,
                                        "Rpmonth52":np.nan,
                                        "Rpmonth53":np.nan,
                                        "Rpmonth54":np.nan,
                                        "Rpmonth55":np.nan,
                                        "Rpmonth56":np.nan,
                                        "Rpmonth57":np.nan,
                                        "Rpmonth58":np.nan,
                                        "Rpmonth59":np.nan,
                                        "Rpmonth60":np.nan,
                                        "Rpstatus1":np.nan,
                                        "Rpstatus2":np.nan,
                                        "Rpstatus3":np.nan,
                                        "Rpstatus4":np.nan,
                                        "Rpstatus5":np.nan,
                                        "Rpstatus6":np.nan,
                                        "Rpstatus7":np.nan,
                                        "Rpstatus8":np.nan,
                                        "Rpstatus9":np.nan,
                                        "Rpstatus10":np.nan,
                                        "Rpstatus11":np.nan,
                                        "Rpstatus12":np.nan,
                                        "Rpstatus13":np.nan,
                                        "Rpstatus14":np.nan,
                                        "Rpstatus15":np.nan,
                                        "Rpstatus16":np.nan,
                                        "Rpstatus17":np.nan,
                                        "Rpstatus18":np.nan,
                                        "Rpstatus19":np.nan,
                                        "Rpstatus20":np.nan,
                                        "Rpstatus21":np.nan,
                                        "Rpstatus22":np.nan,
                                        "Rpstatus23":np.nan,
                                        "Rpstatus24":np.nan,
                                        "Rpstatus25":np.nan,
                                        "Rpstatus26":np.nan,
                                        "Rpstatus27":np.nan,
                                        "Rpstatus28":np.nan,
                                        "Rpstatus29":np.nan,
                                        "Rpstatus30":np.nan,
                                        "Rpstatus31":np.nan,
                                        "Rpstatus32":np.nan,
                                        "Rpstatus33":np.nan,
                                        "Rpstatus34":np.nan,
                                        "Rpstatus35":np.nan,
                                        "Rpstatus36":np.nan,
                                        "Rpstatus37":np.nan,
                                        "Rpstatus38":np.nan,
                                        "Rpstatus39":np.nan,
                                        "Rpstatus40":np.nan,
                                        "Rpstatus41":np.nan,
                                        "Rpstatus42":np.nan,
                                        "Rpstatus43":np.nan,
                                        "Rpstatus44":np.nan,
                                        "Rpstatus45":np.nan,
                                        "Rpstatus46":np.nan,
                                        "Rpstatus47":np.nan,
                                        "Rpstatus48":np.nan,
                                        "Rpstatus49":np.nan,
                                        "Rpstatus50":np.nan,
                                        "Rpstatus51":np.nan,
                                        "Rpstatus52":np.nan,
                                        "Rpstatus53":np.nan,
                                        "Rpstatus54":np.nan,
                                        "Rpstatus55":np.nan,
                                        "Rpstatus56":np.nan,
                                        "Rpstatus57":np.nan,
                                        "Rpstatus58":np.nan,
                                        "Rpstatus59":np.nan,
                                        "Rpstatus60":np.nan,
                                        "Rpamt1":np.nan,
                                        "Rpamt2":np.nan,
                                        "Rpamt3":np.nan,
                                        "Rpamt4":np.nan,
                                        "Rpamt5":np.nan,
                                        "Rpamt6":np.nan,
                                        "Rpamt7":np.nan,
                                        "Rpamt8":np.nan,
                                        "Rpamt9":np.nan,
                                        "Rpamt10":np.nan,
                                        "Rpamt11":np.nan,
                                        "Rpamt12":np.nan,
                                        "Rpamt13":np.nan,
                                        "Rpamt14":np.nan,
                                        "Rpamt15":np.nan,
                                        "Rpamt16":np.nan,
                                        "Rpamt17":np.nan,
                                        "Rpamt18":np.nan,
                                        "Rpamt19":np.nan,
                                        "Rpamt20":np.nan,
                                        "Rpamt21":np.nan,
                                        "Rpamt22":np.nan,
                                        "Rpamt23":np.nan,
                                        "Rpamt24":np.nan,
                                        "Rpamt25":np.nan,
                                        "Rpamt26":np.nan,
                                        "Rpamt27":np.nan,
                                        "Rpamt28":np.nan,
                                        "Rpamt29":np.nan,
                                        "Rpamt30":np.nan,
                                        "Rpamt31":np.nan,
                                        "Rpamt32":np.nan,
                                        "Rpamt33":np.nan,
                                        "Rpamt34":np.nan,
                                        "Rpamt35":np.nan,
                                        "Rpamt36":np.nan,
                                        "Rpamt37":np.nan,
                                        "Rpamt38":np.nan,
                                        "Rpamt39":np.nan,
                                        "Rpamt40":np.nan,
                                        "Rpamt41":np.nan,
                                        "Rpamt42":np.nan,
                                        "Rpamt43":np.nan,
                                        "Rpamt44":np.nan,
                                        "Rpamt45":np.nan,
                                        "Rpamt46":np.nan,
                                        "Rpamt47":np.nan,
                                        "Rpamt48":np.nan,
                                        "Rpamt49":np.nan,
                                        "Rpamt50":np.nan,
                                        "Rpamt51":np.nan,
                                        "Rpamt52":np.nan,
                                        "Rpamt53":np.nan,
                                        "Rpamt54":np.nan,
                                        "Rpamt55":np.nan,
                                        "Rpamt56":np.nan,
                                        "Rpamt57":np.nan,
                                        "Rpamt58":np.nan,
                                        "Rpamt59":np.nan,
                                        "Rpamt60":np.nan,
                                        "PD01FS01":np.nan,
                                        "PD01GS01":np.nan,
                                        "PD01HS01":np.nan,
                                        "PD01ZS01":np.nan,
                                        },index=[0])
                                                
    columns_chinese = {"PD01AI01":"基本信息-账户编号",
                        "PD01AD01":"基本信息-账户类型",
                        "PD01AD02":"基本信息-业务管理机构类型",
                        "PD01AI02":"基本信息-业务管理机构代码",
                        "PD01AI03":"基本信息-账户标识",
                        "PD01AI04":"基本信息-授权协议编号",
                        "PD01AD03":"基本信息-业务种类",
                        "PD01AR01":"基本信息-开立日期",
                        "PD01AD04":"基本信息-币种",
                        "PD01AJ01":"基本信息-借款金额",
                        "PD01AJ02":"基本信息-账户授信额度",
                        "PD01AJ03":"基本信息-共享授信额度",
                        "PD01AR02":"基本信息-到期日期",
                        "PD01AD05":"基本信息-还款方式",
                        "PD01AD06":"基本信息-还款频率",
                        "PD01AS01":"基本信息-还款期数",
                        "PD01AD07":"基本信息-担保方式",
                        "PD01AD08":"基本信息-贷款发放形式",
                        "PD01AD09":"基本信息-共同借款标志",
                        "PD01AD10":"基本信息-债权转移时的还款状态",
                        "PD01BD01":"最新表现信息-账户状态",
                        "PD01BR01":"最新表现信息-关闭日期",
                        "PD01BR04":"最新表现信息-转出月份",
                        "PD01BJ01":"最新表现信息-余额",
                        "PD01BR02":"最新表现信息-最近一次还款日期",
                        "PD01BJ02":"最新表现信息-最近一次还款金额",
                        "PD01BD03":"最新表现信息-五级分类",
                        "PD01BD04":"最新表现信息-还款状态",
                        "PD01BR03":"最新表现信息-信息报告日期",
                        "PD01CR01":"最近一次月度表现信息段-月份",
                        "PD01CD01":"最近一次月度表现信息段-账户状态",
                        "PD01CJ01":"最近一次月度表现信息段-余额",
                        "PD01CJ02":"最近一次月度表现信息段-已用额度",
                        "PD01CJ03":"最近一次月度表现信息段-未出单的大额专项分期余额",
                        "PD01CD02":"最近一次月度表现信息段-五级分类",
                        "PD01CS01":"最近一次月度表现信息段-剩余还款期数",
                        "PD01CR02":"最近一次月度表现信息段-结算/应还款日",
                        "PD01CJ04":"最近一次月度表现信息段-本月应还款",
                        "PD01CJ05":"最近一次月度表现信息段-本月实还款",
                        "PD01CR03":"最近一次月度表现信息段-最近一次还款日期",
                        "PD01CS02":"最近一次月度表现信息段-当前逾期期数",
                        "PD01CJ06":"最近一次月度表现信息段-当前逾期总额",
                        "PD01CJ07":"最近一次月度表现信息段-逾期31-60天未还本金",
                        "PD01CJ08":"最近一次月度表现信息段-逾期61-90天未还本金",
                        "PD01CJ09":"最近一次月度表现信息段-逾期91-180天未还本金",
                        "PD01CJ10":"最近一次月度表现信息段-逾期180天以上未还本金",
                        "PD01CJ11":"最近一次月度表现信息段-透支180天以上未付余额",
                        "PD01CJ12":"最近一次月度表现信息段-最近6个月平均使用额度",
                        "PD01CJ13":"最近一次月度表现信息段-最近6个月平均透支余额",
                        "PD01CJ14":"最近一次月度表现信息段-最大使用额度",
                        "PD01CJ15":"最近一次月度表现信息段-最大透支余额",
                        "PD01CR04":"最近一次月度表现信息段-信息报告日期",
                        "PD01ER01":"最近5年内历史表现信息-起始年月",
                        "PD01ER02":"最近5年内历史表现信息-截止年月",
                        "PD01ES01":"最近5年内历史表现信息-月数",
                        "Rpmonth1":"最近5年内历史表现信息-月份1",
                        "Rpmonth2":"最近5年内历史表现信息-月份2",
                        "Rpmonth3":"最近5年内历史表现信息-月份3",
                        "Rpmonth4":"最近5年内历史表现信息-月份4",
                        "Rpmonth5":"最近5年内历史表现信息-月份5",
                        "Rpmonth6":"最近5年内历史表现信息-月份6",
                        "Rpmonth7":"最近5年内历史表现信息-月份7",
                        "Rpmonth8":"最近5年内历史表现信息-月份8",
                        "Rpmonth9":"最近5年内历史表现信息-月份9",
                        "Rpmonth10":"最近5年内历史表现信息-月份10",
                        "Rpmonth11":"最近5年内历史表现信息-月份11",
                        "Rpmonth12":"最近5年内历史表现信息-月份12",
                        "Rpmonth13":"最近5年内历史表现信息-月份13",
                        "Rpmonth14":"最近5年内历史表现信息-月份14",
                        "Rpmonth15":"最近5年内历史表现信息-月份15",
                        "Rpmonth16":"最近5年内历史表现信息-月份16",
                        "Rpmonth17":"最近5年内历史表现信息-月份17",
                        "Rpmonth18":"最近5年内历史表现信息-月份18",
                        "Rpmonth19":"最近5年内历史表现信息-月份19",
                        "Rpmonth20":"最近5年内历史表现信息-月份20",
                        "Rpmonth21":"最近5年内历史表现信息-月份21",
                        "Rpmonth22":"最近5年内历史表现信息-月份22",
                        "Rpmonth23":"最近5年内历史表现信息-月份23",
                        "Rpmonth24":"最近5年内历史表现信息-月份24",
                        "Rpmonth25":"最近5年内历史表现信息-月份25",
                        "Rpmonth26":"最近5年内历史表现信息-月份26",
                        "Rpmonth27":"最近5年内历史表现信息-月份27",
                        "Rpmonth28":"最近5年内历史表现信息-月份28",
                        "Rpmonth29":"最近5年内历史表现信息-月份29",
                        "Rpmonth30":"最近5年内历史表现信息-月份30",
                        "Rpmonth31":"最近5年内历史表现信息-月份31",
                        "Rpmonth32":"最近5年内历史表现信息-月份32",
                        "Rpmonth33":"最近5年内历史表现信息-月份33",
                        "Rpmonth34":"最近5年内历史表现信息-月份34",
                        "Rpmonth35":"最近5年内历史表现信息-月份35",
                        "Rpmonth36":"最近5年内历史表现信息-月份36",
                        "Rpmonth37":"最近5年内历史表现信息-月份37",
                        "Rpmonth38":"最近5年内历史表现信息-月份38",
                        "Rpmonth39":"最近5年内历史表现信息-月份39",
                        "Rpmonth40":"最近5年内历史表现信息-月份40",
                        "Rpmonth41":"最近5年内历史表现信息-月份41",
                        "Rpmonth42":"最近5年内历史表现信息-月份42",
                        "Rpmonth43":"最近5年内历史表现信息-月份43",
                        "Rpmonth44":"最近5年内历史表现信息-月份44",
                        "Rpmonth45":"最近5年内历史表现信息-月份45",
                        "Rpmonth46":"最近5年内历史表现信息-月份46",
                        "Rpmonth47":"最近5年内历史表现信息-月份47",
                        "Rpmonth48":"最近5年内历史表现信息-月份48",
                        "Rpmonth49":"最近5年内历史表现信息-月份49",
                        "Rpmonth50":"最近5年内历史表现信息-月份50",
                        "Rpmonth51":"最近5年内历史表现信息-月份51",
                        "Rpmonth52":"最近5年内历史表现信息-月份52",
                        "Rpmonth53":"最近5年内历史表现信息-月份53",
                        "Rpmonth54":"最近5年内历史表现信息-月份54",
                        "Rpmonth55":"最近5年内历史表现信息-月份55",
                        "Rpmonth56":"最近5年内历史表现信息-月份56",
                        "Rpmonth57":"最近5年内历史表现信息-月份57",
                        "Rpmonth58":"最近5年内历史表现信息-月份58",
                        "Rpmonth59":"最近5年内历史表现信息-月份59",
                        "Rpmonth60":"最近5年内历史表现信息-月份60",
                        "Rpstatus1":"最近5年内历史表现信息-还款状态1",
                        "Rpstatus2":"最近5年内历史表现信息-还款状态2",
                        "Rpstatus3":"最近5年内历史表现信息-还款状态3",
                        "Rpstatus4":"最近5年内历史表现信息-还款状态4",
                        "Rpstatus5":"最近5年内历史表现信息-还款状态5",
                        "Rpstatus6":"最近5年内历史表现信息-还款状态6",
                        "Rpstatus7":"最近5年内历史表现信息-还款状态7",
                        "Rpstatus8":"最近5年内历史表现信息-还款状态8",
                        "Rpstatus9":"最近5年内历史表现信息-还款状态9",
                        "Rpstatus10":"最近5年内历史表现信息-还款状态10",
                        "Rpstatus11":"最近5年内历史表现信息-还款状态11",
                        "Rpstatus12":"最近5年内历史表现信息-还款状态12",
                        "Rpstatus13":"最近5年内历史表现信息-还款状态13",
                        "Rpstatus14":"最近5年内历史表现信息-还款状态14",
                        "Rpstatus15":"最近5年内历史表现信息-还款状态15",
                        "Rpstatus16":"最近5年内历史表现信息-还款状态16",
                        "Rpstatus17":"最近5年内历史表现信息-还款状态17",
                        "Rpstatus18":"最近5年内历史表现信息-还款状态18",
                        "Rpstatus19":"最近5年内历史表现信息-还款状态19",
                        "Rpstatus20":"最近5年内历史表现信息-还款状态20",
                        "Rpstatus21":"最近5年内历史表现信息-还款状态21",
                        "Rpstatus22":"最近5年内历史表现信息-还款状态22",
                        "Rpstatus23":"最近5年内历史表现信息-还款状态23",
                        "Rpstatus24":"最近5年内历史表现信息-还款状态24",
                        "Rpstatus25":"最近5年内历史表现信息-还款状态25",
                        "Rpstatus26":"最近5年内历史表现信息-还款状态26",
                        "Rpstatus27":"最近5年内历史表现信息-还款状态27",
                        "Rpstatus28":"最近5年内历史表现信息-还款状态28",
                        "Rpstatus29":"最近5年内历史表现信息-还款状态29",
                        "Rpstatus30":"最近5年内历史表现信息-还款状态30",
                        "Rpstatus31":"最近5年内历史表现信息-还款状态31",
                        "Rpstatus32":"最近5年内历史表现信息-还款状态32",
                        "Rpstatus33":"最近5年内历史表现信息-还款状态33",
                        "Rpstatus34":"最近5年内历史表现信息-还款状态34",
                        "Rpstatus35":"最近5年内历史表现信息-还款状态35",
                        "Rpstatus36":"最近5年内历史表现信息-还款状态36",
                        "Rpstatus37":"最近5年内历史表现信息-还款状态37",
                        "Rpstatus38":"最近5年内历史表现信息-还款状态38",
                        "Rpstatus39":"最近5年内历史表现信息-还款状态39",
                        "Rpstatus40":"最近5年内历史表现信息-还款状态40",
                        "Rpstatus41":"最近5年内历史表现信息-还款状态41",
                        "Rpstatus42":"最近5年内历史表现信息-还款状态42",
                        "Rpstatus43":"最近5年内历史表现信息-还款状态43",
                        "Rpstatus44":"最近5年内历史表现信息-还款状态44",
                        "Rpstatus45":"最近5年内历史表现信息-还款状态45",
                        "Rpstatus46":"最近5年内历史表现信息-还款状态46",
                        "Rpstatus47":"最近5年内历史表现信息-还款状态47",
                        "Rpstatus48":"最近5年内历史表现信息-还款状态48",
                        "Rpstatus49":"最近5年内历史表现信息-还款状态49",
                        "Rpstatus50":"最近5年内历史表现信息-还款状态50",
                        "Rpstatus51":"最近5年内历史表现信息-还款状态51",
                        "Rpstatus52":"最近5年内历史表现信息-还款状态52",
                        "Rpstatus53":"最近5年内历史表现信息-还款状态53",
                        "Rpstatus54":"最近5年内历史表现信息-还款状态54",
                        "Rpstatus55":"最近5年内历史表现信息-还款状态55",
                        "Rpstatus56":"最近5年内历史表现信息-还款状态56",
                        "Rpstatus57":"最近5年内历史表现信息-还款状态57",
                        "Rpstatus58":"最近5年内历史表现信息-还款状态58",
                        "Rpstatus59":"最近5年内历史表现信息-还款状态59",
                        "Rpstatus60":"最近5年内历史表现信息-还款状态60",
                        "Rpamt1":"最近5年内历史表现信息-逾期（透支）金额1",
                        "Rpamt2":"最近5年内历史表现信息-逾期（透支）金额2",
                        "Rpamt3":"最近5年内历史表现信息-逾期（透支）金额3",
                        "Rpamt4":"最近5年内历史表现信息-逾期（透支）金额4",
                        "Rpamt5":"最近5年内历史表现信息-逾期（透支）金额5",
                        "Rpamt6":"最近5年内历史表现信息-逾期（透支）金额6",
                        "Rpamt7":"最近5年内历史表现信息-逾期（透支）金额7",
                        "Rpamt8":"最近5年内历史表现信息-逾期（透支）金额8",
                        "Rpamt9":"最近5年内历史表现信息-逾期（透支）金额9",
                        "Rpamt10":"最近5年内历史表现信息-逾期（透支）金额10",
                        "Rpamt11":"最近5年内历史表现信息-逾期（透支）金额11",
                        "Rpamt12":"最近5年内历史表现信息-逾期（透支）金额12",
                        "Rpamt13":"最近5年内历史表现信息-逾期（透支）金额13",
                        "Rpamt14":"最近5年内历史表现信息-逾期（透支）金额14",
                        "Rpamt15":"最近5年内历史表现信息-逾期（透支）金额15",
                        "Rpamt16":"最近5年内历史表现信息-逾期（透支）金额16",
                        "Rpamt17":"最近5年内历史表现信息-逾期（透支）金额17",
                        "Rpamt18":"最近5年内历史表现信息-逾期（透支）金额18",
                        "Rpamt19":"最近5年内历史表现信息-逾期（透支）金额19",
                        "Rpamt20":"最近5年内历史表现信息-逾期（透支）金额20",
                        "Rpamt21":"最近5年内历史表现信息-逾期（透支）金额21",
                        "Rpamt22":"最近5年内历史表现信息-逾期（透支）金额22",
                        "Rpamt23":"最近5年内历史表现信息-逾期（透支）金额23",
                        "Rpamt24":"最近5年内历史表现信息-逾期（透支）金额24",
                        "Rpamt25":"最近5年内历史表现信息-逾期（透支）金额25",
                        "Rpamt26":"最近5年内历史表现信息-逾期（透支）金额26",
                        "Rpamt27":"最近5年内历史表现信息-逾期（透支）金额27",
                        "Rpamt28":"最近5年内历史表现信息-逾期（透支）金额28",
                        "Rpamt29":"最近5年内历史表现信息-逾期（透支）金额29",
                        "Rpamt30":"最近5年内历史表现信息-逾期（透支）金额30",
                        "Rpamt31":"最近5年内历史表现信息-逾期（透支）金额31",
                        "Rpamt32":"最近5年内历史表现信息-逾期（透支）金额32",
                        "Rpamt33":"最近5年内历史表现信息-逾期（透支）金额33",
                        "Rpamt34":"最近5年内历史表现信息-逾期（透支）金额34",
                        "Rpamt35":"最近5年内历史表现信息-逾期（透支）金额35",
                        "Rpamt36":"最近5年内历史表现信息-逾期（透支）金额36",
                        "Rpamt37":"最近5年内历史表现信息-逾期（透支）金额37",
                        "Rpamt38":"最近5年内历史表现信息-逾期（透支）金额38",
                        "Rpamt39":"最近5年内历史表现信息-逾期（透支）金额39",
                        "Rpamt40":"最近5年内历史表现信息-逾期（透支）金额40",
                        "Rpamt41":"最近5年内历史表现信息-逾期（透支）金额41",
                        "Rpamt42":"最近5年内历史表现信息-逾期（透支）金额42",
                        "Rpamt43":"最近5年内历史表现信息-逾期（透支）金额43",
                        "Rpamt44":"最近5年内历史表现信息-逾期（透支）金额44",
                        "Rpamt45":"最近5年内历史表现信息-逾期（透支）金额45",
                        "Rpamt46":"最近5年内历史表现信息-逾期（透支）金额46",
                        "Rpamt47":"最近5年内历史表现信息-逾期（透支）金额47",
                        "Rpamt48":"最近5年内历史表现信息-逾期（透支）金额48",
                        "Rpamt49":"最近5年内历史表现信息-逾期（透支）金额49",
                        "Rpamt50":"最近5年内历史表现信息-逾期（透支）金额50",
                        "Rpamt51":"最近5年内历史表现信息-逾期（透支）金额51",
                        "Rpamt52":"最近5年内历史表现信息-逾期（透支）金额52",
                        "Rpamt53":"最近5年内历史表现信息-逾期（透支）金额53",
                        "Rpamt54":"最近5年内历史表现信息-逾期（透支）金额54",
                        "Rpamt55":"最近5年内历史表现信息-逾期（透支）金额55",
                        "Rpamt56":"最近5年内历史表现信息-逾期（透支）金额56",
                        "Rpamt57":"最近5年内历史表现信息-逾期（透支）金额57",
                        "Rpamt58":"最近5年内历史表现信息-逾期（透支）金额58",
                        "Rpamt59":"最近5年内历史表现信息-逾期（透支）金额59",
                        "Rpamt60":"最近5年内历史表现信息-逾期（透支）金额60",
                        "PD01FS01":"特殊交易信息-特殊交易个数",
                        "PD01GS01":"特殊事件说明信息-特殊事件说明个数",
                        "PD01HS01":"大额专项分期信息-大额专项分期个数",
                        "PD01ZS01":"标注及声明信息-标注及声明个数",
                        }
    
    
    # columns_english = {"PD01AI01":"debit_credit_account_basic_account_no",
    #                     "PD01AD01":"debit_credit_account_basic_account_type",
    #                     "PD01AD02":"debit_credit_account_basic_business_manage_org_type",
    #                     "PD01AI02":"debit_credit_account_basic_business_manage_org_code",
    #                     "PD01AI03":"debit_credit_account_basic_account_flag",
    #                     "PD01AI04":"debit_credit_account_basic_credit_agreement_no",
    #                     "PD01AD03":"debit_credit_account_basic_business_type",
    #                     "PD01AR01":"debit_credit_account_basic_start_date",
    #                     "PD01AD04":"debit_credit_account_basic_currency",
    #                     "PD01AJ01":"debit_credit_account_basic_loan_amt",
    #                     "PD01AJ02":"debit_credit_account_basic_account_credit_amt",
    #                     "PD01AJ03":"debit_credit_account_basic_shared_credit_amt",
    #                     "PD01AR02":"debit_credit_account_basic_expiry_date",
    #                     "PD01AD05":"debit_credit_account_basic_repay_method",
    #                     "PD01AD06":"debit_credit_account_basic_repay_frequency",
    #                     "PD01AS01":"debit_credit_account_basic_repay_period_count",
    #                     "PD01AD07":"debit_credit_account_basic_guarantee_method",
    #                     "PD01AD08":"debit_credit_account_basic_loan_issue_form",
    #                     "PD01AD09":"debit_credit_account_basic_co_borrowing_flag",
    #                     "PD01AD10":"debit_credit_account_basic_repay_status_tr_rights",
    #                     "PD01BD01":"debit_credit_account_latest_account_status",
    #                     "PD01BR01":"debit_credit_account_latest_close_date",
    #                     "PD01BR04":"debit_credit_account_latest_transfer_out_month",
    #                     "PD01BJ01":"debit_credit_account_latest_balance",
    #                     "PD01BR02":"debit_credit_account_latest_repay_date",
    #                     "PD01BJ02":"debit_credit_account_latest_repay_amt",
    #                     "PD01BD03":"debit_credit_account_latest_five_level",
    #                     "PD01BD04":"debit_credit_account_latest_repay_status",
    #                     "PD01BR03":"debit_credit_account_latest_report_date",
    #                     "PD01CR01":"debit_credit_account_monpf_month",
    #                     "PD01CD01":"debit_credit_account_monpf_account_status",
    #                     "PD01CJ01":"debit_credit_account_monpf_balance",
    #                     "PD01CJ02":"debit_credit_account_monpf_used_amt",
    #                     "PD01CJ03":"debit_credit_account_monpf_unissued_large_stage_bal",
    #                     "PD01CD02":"debit_credit_account_monpf_five_level",
    #                     "PD01CS01":"debit_credit_account_monpf_remaining_repay_period",
    #                     "PD01CR02":"debit_credit_account_monpf_repay_date",
    #                     "PD01CJ04":"debit_credit_account_monpf_repayable_amt",
    #                     "PD01CJ05":"debit_credit_account_monpf_actually_repaid_amt",
    #                     "PD01CR03":"debit_credit_account_monpf_last_repay_date",
    #                     "PD01CS02":"debit_credit_account_monpf_current_overdue_periods",
    #                     "PD01CJ06":"debit_credit_account_monpf_current_overdue_sum",
    #                     "PD01CJ07":"debit_credit_account_monpf_overdue_31_60_debit",
    #                     "PD01CJ08":"debit_credit_account_monpf_overdue_61_90_debit",
    #                     "PD01CJ09":"debit_credit_account_monpf_overdue_91_180_debit",
    #                     "PD01CJ10":"debit_credit_account_monpf_overdue_over_180_debit",
    #                     "PD01CJ11":"debit_credit_account_monpf_overdraw_over_180_debit",
    #                     "PD01CJ12":"debit_credit_account_monpf_l6m_avg_used_amt",
    #                     "PD01CJ13":"debit_credit_account_monpf_l6m_avg_overdraw_bal",
    #                     "PD01CJ14":"debit_credit_account_monpf_max_use_amt",
    #                     "PD01CJ15":"debit_credit_account_monpf_max_overdraw_bal",
    #                     "PD01CR04":"debit_credit_account_monpf_report_date",
    #                     "PD01ER01":"debit_credit_account_latest5year_start_month",
    #                     "PD01ER02":"debit_credit_account_latest5year_end_month",
    #                     "PD01ES01":"debit_credit_account_latest5year_month_count",
    #                     "Rpmonth01":"debit_credit_account_l5y_month1",
    #                     "Rpmonth02":"debit_credit_account_l5y_month2",
    #                     "Rpmonth03":"debit_credit_account_l5y_month3",
    #                     "Rpmonth04":"debit_credit_account_l5y_month4",
    #                     "Rpmonth05":"debit_credit_account_l5y_month5",
    #                     "Rpmonth06":"debit_credit_account_l5y_month6",
    #                     "Rpmonth07":"debit_credit_account_l5y_month7",
    #                     "Rpmonth08":"debit_credit_account_l5y_month8",
    #                     "Rpmonth09":"debit_credit_account_l5y_month9",
    #                     "Rpmonth10":"debit_credit_account_l5y_month10",
    #                     "Rpmonth11":"debit_credit_account_l5y_month11",
    #                     "Rpmonth12":"debit_credit_account_l5y_month12",
    #                     "Rpmonth13":"debit_credit_account_l5y_month13",
    #                     "Rpmonth14":"debit_credit_account_l5y_month14",
    #                     "Rpmonth15":"debit_credit_account_l5y_month15",
    #                     "Rpmonth16":"debit_credit_account_l5y_month16",
    #                     "Rpmonth17":"debit_credit_account_l5y_month17",
    #                     "Rpmonth18":"debit_credit_account_l5y_month18",
    #                     "Rpmonth19":"debit_credit_account_l5y_month19",
    #                     "Rpmonth20":"debit_credit_account_l5y_month20",
    #                     "Rpmonth21":"debit_credit_account_l5y_month21",
    #                     "Rpmonth22":"debit_credit_account_l5y_month22",
    #                     "Rpmonth23":"debit_credit_account_l5y_month23",
    #                     "Rpmonth24":"debit_credit_account_l5y_month24",
    #                     "Rpmonth25":"debit_credit_account_l5y_month25",
    #                     "Rpmonth26":"debit_credit_account_l5y_month26",
    #                     "Rpmonth27":"debit_credit_account_l5y_month27",
    #                     "Rpmonth28":"debit_credit_account_l5y_month28",
    #                     "Rpmonth29":"debit_credit_account_l5y_month29",
    #                     "Rpmonth30":"debit_credit_account_l5y_month30",
    #                     "Rpmonth31":"debit_credit_account_l5y_month31",
    #                     "Rpmonth32":"debit_credit_account_l5y_month32",
    #                     "Rpmonth33":"debit_credit_account_l5y_month33",
    #                     "Rpmonth34":"debit_credit_account_l5y_month34",
    #                     "Rpmonth35":"debit_credit_account_l5y_month35",
    #                     "Rpmonth36":"debit_credit_account_l5y_month36",
    #                     "Rpmonth37":"debit_credit_account_l5y_month37",
    #                     "Rpmonth38":"debit_credit_account_l5y_month38",
    #                     "Rpmonth39":"debit_credit_account_l5y_month39",
    #                     "Rpmonth40":"debit_credit_account_l5y_month40",
    #                     "Rpmonth41":"debit_credit_account_l5y_month41",
    #                     "Rpmonth42":"debit_credit_account_l5y_month42",
    #                     "Rpmonth43":"debit_credit_account_l5y_month43",
    #                     "Rpmonth44":"debit_credit_account_l5y_month44",
    #                     "Rpmonth45":"debit_credit_account_l5y_month45",
    #                     "Rpmonth46":"debit_credit_account_l5y_month46",
    #                     "Rpmonth47":"debit_credit_account_l5y_month47",
    #                     "Rpmonth48":"debit_credit_account_l5y_month48",
    #                     "Rpmonth49":"debit_credit_account_l5y_month49",
    #                     "Rpmonth50":"debit_credit_account_l5y_month50",
    #                     "Rpmonth51":"debit_credit_account_l5y_month51",
    #                     "Rpmonth52":"debit_credit_account_l5y_month52",
    #                     "Rpmonth53":"debit_credit_account_l5y_month53",
    #                     "Rpmonth54":"debit_credit_account_l5y_month54",
    #                     "Rpmonth55":"debit_credit_account_l5y_month55",
    #                     "Rpmonth56":"debit_credit_account_l5y_month56",
    #                     "Rpmonth57":"debit_credit_account_l5y_month57",
    #                     "Rpmonth58":"debit_credit_account_l5y_month58",
    #                     "Rpmonth59":"debit_credit_account_l5y_month59",
    #                     "Rpmonth60":"debit_credit_account_l5y_month60",
    #                     "Rpstatus01":"debit_credit_account_l5y_repay_status1",
    #                     "Rpstatus02":"debit_credit_account_l5y_repay_status2",
    #                     "Rpstatus03":"debit_credit_account_l5y_repay_status3",
    #                     "Rpstatus04":"debit_credit_account_l5y_repay_status4",
    #                     "Rpstatus05":"debit_credit_account_l5y_repay_status5",
    #                     "Rpstatus06":"debit_credit_account_l5y_repay_status6",
    #                     "Rpstatus07":"debit_credit_account_l5y_repay_status7",
    #                     "Rpstatus08":"debit_credit_account_l5y_repay_status8",
    #                     "Rpstatus09":"debit_credit_account_l5y_repay_status9",
    #                     "Rpstatus10":"debit_credit_account_l5y_repay_status10",
    #                     "Rpstatus11":"debit_credit_account_l5y_repay_status11",
    #                     "Rpstatus12":"debit_credit_account_l5y_repay_status12",
    #                     "Rpstatus13":"debit_credit_account_l5y_repay_status13",
    #                     "Rpstatus14":"debit_credit_account_l5y_repay_status14",
    #                     "Rpstatus15":"debit_credit_account_l5y_repay_status15",
    #                     "Rpstatus16":"debit_credit_account_l5y_repay_status16",
    #                     "Rpstatus17":"debit_credit_account_l5y_repay_status17",
    #                     "Rpstatus18":"debit_credit_account_l5y_repay_status18",
    #                     "Rpstatus19":"debit_credit_account_l5y_repay_status19",
    #                     "Rpstatus20":"debit_credit_account_l5y_repay_status20",
    #                     "Rpstatus21":"debit_credit_account_l5y_repay_status21",
    #                     "Rpstatus22":"debit_credit_account_l5y_repay_status22",
    #                     "Rpstatus23":"debit_credit_account_l5y_repay_status23",
    #                     "Rpstatus24":"debit_credit_account_l5y_repay_status24",
    #                     "Rpstatus25":"debit_credit_account_l5y_repay_status25",
    #                     "Rpstatus26":"debit_credit_account_l5y_repay_status26",
    #                     "Rpstatus27":"debit_credit_account_l5y_repay_status27",
    #                     "Rpstatus28":"debit_credit_account_l5y_repay_status28",
    #                     "Rpstatus29":"debit_credit_account_l5y_repay_status29",
    #                     "Rpstatus30":"debit_credit_account_l5y_repay_status30",
    #                     "Rpstatus31":"debit_credit_account_l5y_repay_status31",
    #                     "Rpstatus32":"debit_credit_account_l5y_repay_status32",
    #                     "Rpstatus33":"debit_credit_account_l5y_repay_status33",
    #                     "Rpstatus34":"debit_credit_account_l5y_repay_status34",
    #                     "Rpstatus35":"debit_credit_account_l5y_repay_status35",
    #                     "Rpstatus36":"debit_credit_account_l5y_repay_status36",
    #                     "Rpstatus37":"debit_credit_account_l5y_repay_status37",
    #                     "Rpstatus38":"debit_credit_account_l5y_repay_status38",
    #                     "Rpstatus39":"debit_credit_account_l5y_repay_status39",
    #                     "Rpstatus40":"debit_credit_account_l5y_repay_status40",
    #                     "Rpstatus41":"debit_credit_account_l5y_repay_status41",
    #                     "Rpstatus42":"debit_credit_account_l5y_repay_status42",
    #                     "Rpstatus43":"debit_credit_account_l5y_repay_status43",
    #                     "Rpstatus44":"debit_credit_account_l5y_repay_status44",
    #                     "Rpstatus45":"debit_credit_account_l5y_repay_status45",
    #                     "Rpstatus46":"debit_credit_account_l5y_repay_status46",
    #                     "Rpstatus47":"debit_credit_account_l5y_repay_status47",
    #                     "Rpstatus48":"debit_credit_account_l5y_repay_status48",
    #                     "Rpstatus49":"debit_credit_account_l5y_repay_status49",
    #                     "Rpstatus50":"debit_credit_account_l5y_repay_status50",
    #                     "Rpstatus51":"debit_credit_account_l5y_repay_status51",
    #                     "Rpstatus52":"debit_credit_account_l5y_repay_status52",
    #                     "Rpstatus53":"debit_credit_account_l5y_repay_status53",
    #                     "Rpstatus54":"debit_credit_account_l5y_repay_status54",
    #                     "Rpstatus55":"debit_credit_account_l5y_repay_status55",
    #                     "Rpstatus56":"debit_credit_account_l5y_repay_status56",
    #                     "Rpstatus57":"debit_credit_account_l5y_repay_status57",
    #                     "Rpstatus58":"debit_credit_account_l5y_repay_status58",
    #                     "Rpstatus59":"debit_credit_account_l5y_repay_status59",
    #                     "Rpstatus60":"debit_credit_account_l5y_repay_status60",
    #                     "Rpamt1":"debit_credit_account_l5y_overdue_amt1",
    #                     "Rpamt2":"debit_credit_account_l5y_overdue_amt2",
    #                     "Rpamt3":"debit_credit_account_l5y_overdue_amt3",
    #                     "Rpamt4":"debit_credit_account_l5y_overdue_amt4",
    #                     "Rpamt5":"debit_credit_account_l5y_overdue_amt5",
    #                     "Rpamt6":"debit_credit_account_l5y_overdue_amt6",
    #                     "Rpamt7":"debit_credit_account_l5y_overdue_amt7",
    #                     "Rpamt8":"debit_credit_account_l5y_overdue_amt8",
    #                     "Rpamt9":"debit_credit_account_l5y_overdue_amt9",
    #                     "Rpamt10":"debit_credit_account_l5y_overdue_amt10",
    #                     "Rpamt11":"debit_credit_account_l5y_overdue_amt11",
    #                     "Rpamt12":"debit_credit_account_l5y_overdue_amt12",
    #                     "Rpamt13":"debit_credit_account_l5y_overdue_amt13",
    #                     "Rpamt14":"debit_credit_account_l5y_overdue_amt14",
    #                     "Rpamt15":"debit_credit_account_l5y_overdue_amt15",
    #                     "Rpamt16":"debit_credit_account_l5y_overdue_amt16",
    #                     "Rpamt17":"debit_credit_account_l5y_overdue_amt17",
    #                     "Rpamt18":"debit_credit_account_l5y_overdue_amt18",
    #                     "Rpamt19":"debit_credit_account_l5y_overdue_amt19",
    #                     "Rpamt20":"debit_credit_account_l5y_overdue_amt20",
    #                     "Rpamt21":"debit_credit_account_l5y_overdue_amt21",
    #                     "Rpamt22":"debit_credit_account_l5y_overdue_amt22",
    #                     "Rpamt23":"debit_credit_account_l5y_overdue_amt23",
    #                     "Rpamt24":"debit_credit_account_l5y_overdue_amt24",
    #                     "Rpamt25":"debit_credit_account_l5y_overdue_amt25",
    #                     "Rpamt26":"debit_credit_account_l5y_overdue_amt26",
    #                     "Rpamt27":"debit_credit_account_l5y_overdue_amt27",
    #                     "Rpamt28":"debit_credit_account_l5y_overdue_amt28",
    #                     "Rpamt29":"debit_credit_account_l5y_overdue_amt29",
    #                     "Rpamt30":"debit_credit_account_l5y_overdue_amt30",
    #                     "Rpamt31":"debit_credit_account_l5y_overdue_amt31",
    #                     "Rpamt32":"debit_credit_account_l5y_overdue_amt32",
    #                     "Rpamt33":"debit_credit_account_l5y_overdue_amt33",
    #                     "Rpamt34":"debit_credit_account_l5y_overdue_amt34",
    #                     "Rpamt35":"debit_credit_account_l5y_overdue_amt35",
    #                     "Rpamt36":"debit_credit_account_l5y_overdue_amt36",
    #                     "Rpamt37":"debit_credit_account_l5y_overdue_amt37",
    #                     "Rpamt38":"debit_credit_account_l5y_overdue_amt38",
    #                     "Rpamt39":"debit_credit_account_l5y_overdue_amt39",
    #                     "Rpamt40":"debit_credit_account_l5y_overdue_amt40",
    #                     "Rpamt41":"debit_credit_account_l5y_overdue_amt41",
    #                     "Rpamt42":"debit_credit_account_l5y_overdue_amt42",
    #                     "Rpamt43":"debit_credit_account_l5y_overdue_amt43",
    #                     "Rpamt44":"debit_credit_account_l5y_overdue_amt44",
    #                     "Rpamt45":"debit_credit_account_l5y_overdue_amt45",
    #                     "Rpamt46":"debit_credit_account_l5y_overdue_amt46",
    #                     "Rpamt47":"debit_credit_account_l5y_overdue_amt47",
    #                     "Rpamt48":"debit_credit_account_l5y_overdue_amt48",
    #                     "Rpamt49":"debit_credit_account_l5y_overdue_amt49",
    #                     "Rpamt50":"debit_credit_account_l5y_overdue_amt50",
    #                     "Rpamt51":"debit_credit_account_l5y_overdue_amt51",
    #                     "Rpamt52":"debit_credit_account_l5y_overdue_amt52",
    #                     "Rpamt53":"debit_credit_account_l5y_overdue_amt53",
    #                     "Rpamt54":"debit_credit_account_l5y_overdue_amt54",
    #                     "Rpamt55":"debit_credit_account_l5y_overdue_amt55",
    #                     "Rpamt56":"debit_credit_account_l5y_overdue_amt56",
    #                     "Rpamt57":"debit_credit_account_l5y_overdue_amt57",
    #                     "Rpamt58":"debit_credit_account_l5y_overdue_amt58",
    #                     "Rpamt59":"debit_credit_account_l5y_overdue_amt59",
    #                     "Rpamt60":"debit_credit_account_l5y_overdue_amt60",
    #                     "PD01FS01":"debit_credit_account_special_transaction_count",
    #                     "PD01GS01":"debit_credit_account_special_event_count",
    #                     "PD01HS01":"debit_credit_account_large_spec_stage_count",
    #                     "PD01ZS01":"debit_credit_account_mark_count",
    #                     }
                            
    columns_english = {"PD01AI01":"AccountNumber",
        "PD01AD01":"CreditType",
        "PD01AD02":"ManagementInstituion",
        "PD01AI02":"ManageOrgCode",
        "PD01AI03":"AccountIdentity",
        "PD01AI04":"debit_credit_account_basic_credit_agreement_no",
        "PD01AD03":"BusinessType",
        "PD01AR01":"LoanIssuingDate",
        "PD01AD04":"Currency",
        "PD01AJ01":"LoanAmount",
        "PD01AJ02":"CreditLine",
        "PD01AJ03":"ShareCreditLine",
        "PD01AR02":"MaturityDate",
        "PD01AD05":"RepaymentMethod",
        "PD01AD06":"RepaymentPeriod",
        "PD01AS01":"Tenor",
        "PD01AD07":"GuarantorType",
        "PD01AD08":"debit_credit_account_basic_loan_issue_form",
        "PD01AD09":"CoBorrowingFlag",
        "PD01AD10":"RepaymentStateWhenTransferingClaim",
        "PD01BD01":"debit_credit_account_latest_account_status",
        "PD01BR01":"debit_credit_account_latest_close_date",
        "PD01BR04":"debit_credit_account_latest_transfer_out_month",
        "PD01BJ01":"debit_credit_account_latest_balance",
        "PD01BR02":"debit_credit_account_latest_repay_date",
        "PD01BJ02":"debit_credit_account_latest_repay_amt",
        "PD01BD03":"debit_credit_account_latest_five_level",
        "PD01BD04":"debit_credit_account_latest_repay_status",
        "PD01BR03":"debit_credit_account_latest_report_date",
        "PD01CR01":"debit_credit_account_monpf_month",
        "PD01CD01":"debit_credit_account_monpf_account_status",
        "PD01CJ01":"debit_credit_account_monpf_balance",
        "PD01CJ02":"debit_credit_account_monpf_used_amt",
        "PD01CJ03":"debit_credit_account_monpf_unissued_large_stage_bal",
        "PD01CD02":"debit_credit_account_monpf_five_level",
        "PD01CS01":"debit_credit_account_monpf_remaining_repay_period",
        "PD01CR02":"debit_credit_account_monpf_repay_date",
        "PD01CJ04":"debit_credit_account_monpf_repayable_amt",
        "PD01CJ05":"debit_credit_account_monpf_actually_repaid_amt",
        "PD01CR03":"debit_credit_account_monpf_last_repay_date",
        "PD01CS02":"debit_credit_account_monpf_current_overdue_periods",
        "PD01CJ06":"debit_credit_account_monpf_current_overdue_sum",
        "PD01CJ07":"debit_credit_account_monpf_overdue_31_60_debit",
        "PD01CJ08":"debit_credit_account_monpf_overdue_61_90_debit",
        "PD01CJ09":"debit_credit_account_monpf_overdue_91_180_debit",
        "PD01CJ10":"debit_credit_account_monpf_overdue_over_180_debit",
        "PD01CJ11":"debit_credit_account_monpf_overdraw_over_180_debit",
        "PD01CJ12":"debit_credit_account_monpf_l6m_avg_used_amt",
        "PD01CJ13":"debit_credit_account_monpf_l6m_avg_overdraw_bal",
        "PD01CJ14":"debit_credit_account_monpf_max_use_amt",
        "PD01CJ15":"debit_credit_account_monpf_max_overdraw_bal",
        "PD01CR04":"debit_credit_account_monpf_report_date",
        "PD01ER01":"debit_credit_account_latest5year_start_month",
        "PD01ER02":"debit_credit_account_latest5year_end_month",
        "PD01ES01":"debit_credit_account_latest5year_month_count",
        "Rpmonth1":"debit_credit_account_l5y_month1",
        "Rpmonth2":"debit_credit_account_l5y_month2",
        "Rpmonth3":"debit_credit_account_l5y_month3",
        "Rpmonth4":"debit_credit_account_l5y_month4",
        "Rpmonth5":"debit_credit_account_l5y_month5",
        "Rpmonth6":"debit_credit_account_l5y_month6",
        "Rpmonth7":"debit_credit_account_l5y_month7",
        "Rpmonth8":"debit_credit_account_l5y_month8",
        "Rpmonth9":"debit_credit_account_l5y_month9",
        "Rpmonth10":"debit_credit_account_l5y_month10",
        "Rpmonth11":"debit_credit_account_l5y_month11",
        "Rpmonth12":"debit_credit_account_l5y_month12",
        "Rpmonth13":"debit_credit_account_l5y_month13",
        "Rpmonth14":"debit_credit_account_l5y_month14",
        "Rpmonth15":"debit_credit_account_l5y_month15",
        "Rpmonth16":"debit_credit_account_l5y_month16",
        "Rpmonth17":"debit_credit_account_l5y_month17",
        "Rpmonth18":"debit_credit_account_l5y_month18",
        "Rpmonth19":"debit_credit_account_l5y_month19",
        "Rpmonth20":"debit_credit_account_l5y_month20",
        "Rpmonth21":"debit_credit_account_l5y_month21",
        "Rpmonth22":"debit_credit_account_l5y_month22",
        "Rpmonth23":"debit_credit_account_l5y_month23",
        "Rpmonth24":"debit_credit_account_l5y_month24",
        "Rpmonth25":"debit_credit_account_l5y_month25",
        "Rpmonth26":"debit_credit_account_l5y_month26",
        "Rpmonth27":"debit_credit_account_l5y_month27",
        "Rpmonth28":"debit_credit_account_l5y_month28",
        "Rpmonth29":"debit_credit_account_l5y_month29",
        "Rpmonth30":"debit_credit_account_l5y_month30",
        "Rpmonth31":"debit_credit_account_l5y_month31",
        "Rpmonth32":"debit_credit_account_l5y_month32",
        "Rpmonth33":"debit_credit_account_l5y_month33",
        "Rpmonth34":"debit_credit_account_l5y_month34",
        "Rpmonth35":"debit_credit_account_l5y_month35",
        "Rpmonth36":"debit_credit_account_l5y_month36",
        "Rpmonth37":"debit_credit_account_l5y_month37",
        "Rpmonth38":"debit_credit_account_l5y_month38",
        "Rpmonth39":"debit_credit_account_l5y_month39",
        "Rpmonth40":"debit_credit_account_l5y_month40",
        "Rpmonth41":"debit_credit_account_l5y_month41",
        "Rpmonth42":"debit_credit_account_l5y_month42",
        "Rpmonth43":"debit_credit_account_l5y_month43",
        "Rpmonth44":"debit_credit_account_l5y_month44",
        "Rpmonth45":"debit_credit_account_l5y_month45",
        "Rpmonth46":"debit_credit_account_l5y_month46",
        "Rpmonth47":"debit_credit_account_l5y_month47",
        "Rpmonth48":"debit_credit_account_l5y_month48",
        "Rpmonth49":"debit_credit_account_l5y_month49",
        "Rpmonth50":"debit_credit_account_l5y_month50",
        "Rpmonth51":"debit_credit_account_l5y_month51",
        "Rpmonth52":"debit_credit_account_l5y_month52",
        "Rpmonth53":"debit_credit_account_l5y_month53",
        "Rpmonth54":"debit_credit_account_l5y_month54",
        "Rpmonth55":"debit_credit_account_l5y_month55",
        "Rpmonth56":"debit_credit_account_l5y_month56",
        "Rpmonth57":"debit_credit_account_l5y_month57",
        "Rpmonth58":"debit_credit_account_l5y_month58",
        "Rpmonth59":"debit_credit_account_l5y_month59",
        "Rpmonth60":"debit_credit_account_l5y_month60",
        "Rpstatus1":"debit_credit_account_l5y_repay_status1",
        "Rpstatus2":"debit_credit_account_l5y_repay_status2",
        "Rpstatus3":"debit_credit_account_l5y_repay_status3",
        "Rpstatus4":"debit_credit_account_l5y_repay_status4",
        "Rpstatus5":"debit_credit_account_l5y_repay_status5",
        "Rpstatus6":"debit_credit_account_l5y_repay_status6",
        "Rpstatus7":"debit_credit_account_l5y_repay_status7",
        "Rpstatus8":"debit_credit_account_l5y_repay_status8",
        "Rpstatus9":"debit_credit_account_l5y_repay_status9",
        "Rpstatus10":"debit_credit_account_l5y_repay_status10",
        "Rpstatus11":"debit_credit_account_l5y_repay_status11",
        "Rpstatus12":"debit_credit_account_l5y_repay_status12",
        "Rpstatus13":"debit_credit_account_l5y_repay_status13",
        "Rpstatus14":"debit_credit_account_l5y_repay_status14",
        "Rpstatus15":"debit_credit_account_l5y_repay_status15",
        "Rpstatus16":"debit_credit_account_l5y_repay_status16",
        "Rpstatus17":"debit_credit_account_l5y_repay_status17",
        "Rpstatus18":"debit_credit_account_l5y_repay_status18",
        "Rpstatus19":"debit_credit_account_l5y_repay_status19",
        "Rpstatus20":"debit_credit_account_l5y_repay_status20",
        "Rpstatus21":"debit_credit_account_l5y_repay_status21",
        "Rpstatus22":"debit_credit_account_l5y_repay_status22",
        "Rpstatus23":"debit_credit_account_l5y_repay_status23",
        "Rpstatus24":"debit_credit_account_l5y_repay_status24",
        "Rpstatus25":"debit_credit_account_l5y_repay_status25",
        "Rpstatus26":"debit_credit_account_l5y_repay_status26",
        "Rpstatus27":"debit_credit_account_l5y_repay_status27",
        "Rpstatus28":"debit_credit_account_l5y_repay_status28",
        "Rpstatus29":"debit_credit_account_l5y_repay_status29",
        "Rpstatus30":"debit_credit_account_l5y_repay_status30",
        "Rpstatus31":"debit_credit_account_l5y_repay_status31",
        "Rpstatus32":"debit_credit_account_l5y_repay_status32",
        "Rpstatus33":"debit_credit_account_l5y_repay_status33",
        "Rpstatus34":"debit_credit_account_l5y_repay_status34",
        "Rpstatus35":"debit_credit_account_l5y_repay_status35",
        "Rpstatus36":"debit_credit_account_l5y_repay_status36",
        "Rpstatus37":"debit_credit_account_l5y_repay_status37",
        "Rpstatus38":"debit_credit_account_l5y_repay_status38",
        "Rpstatus39":"debit_credit_account_l5y_repay_status39",
        "Rpstatus40":"debit_credit_account_l5y_repay_status40",
        "Rpstatus41":"debit_credit_account_l5y_repay_status41",
        "Rpstatus42":"debit_credit_account_l5y_repay_status42",
        "Rpstatus43":"debit_credit_account_l5y_repay_status43",
        "Rpstatus44":"debit_credit_account_l5y_repay_status44",
        "Rpstatus45":"debit_credit_account_l5y_repay_status45",
        "Rpstatus46":"debit_credit_account_l5y_repay_status46",
        "Rpstatus47":"debit_credit_account_l5y_repay_status47",
        "Rpstatus48":"debit_credit_account_l5y_repay_status48",
        "Rpstatus49":"debit_credit_account_l5y_repay_status49",
        "Rpstatus50":"debit_credit_account_l5y_repay_status50",
        "Rpstatus51":"debit_credit_account_l5y_repay_status51",
        "Rpstatus52":"debit_credit_account_l5y_repay_status52",
        "Rpstatus53":"debit_credit_account_l5y_repay_status53",
        "Rpstatus54":"debit_credit_account_l5y_repay_status54",
        "Rpstatus55":"debit_credit_account_l5y_repay_status55",
        "Rpstatus56":"debit_credit_account_l5y_repay_status56",
        "Rpstatus57":"debit_credit_account_l5y_repay_status57",
        "Rpstatus58":"debit_credit_account_l5y_repay_status58",
        "Rpstatus59":"debit_credit_account_l5y_repay_status59",
        "Rpstatus60":"debit_credit_account_l5y_repay_status60",
        "Rpamt1":"debit_credit_account_l5y_overdue_amt1",
        "Rpamt2":"debit_credit_account_l5y_overdue_amt2",
        "Rpamt3":"debit_credit_account_l5y_overdue_amt3",
        "Rpamt4":"debit_credit_account_l5y_overdue_amt4",
        "Rpamt5":"debit_credit_account_l5y_overdue_amt5",
        "Rpamt6":"debit_credit_account_l5y_overdue_amt6",
        "Rpamt7":"debit_credit_account_l5y_overdue_amt7",
        "Rpamt8":"debit_credit_account_l5y_overdue_amt8",
        "Rpamt9":"debit_credit_account_l5y_overdue_amt9",
        "Rpamt10":"debit_credit_account_l5y_overdue_amt10",
        "Rpamt11":"debit_credit_account_l5y_overdue_amt11",
        "Rpamt12":"debit_credit_account_l5y_overdue_amt12",
        "Rpamt13":"debit_credit_account_l5y_overdue_amt13",
        "Rpamt14":"debit_credit_account_l5y_overdue_amt14",
        "Rpamt15":"debit_credit_account_l5y_overdue_amt15",
        "Rpamt16":"debit_credit_account_l5y_overdue_amt16",
        "Rpamt17":"debit_credit_account_l5y_overdue_amt17",
        "Rpamt18":"debit_credit_account_l5y_overdue_amt18",
        "Rpamt19":"debit_credit_account_l5y_overdue_amt19",
        "Rpamt20":"debit_credit_account_l5y_overdue_amt20",
        "Rpamt21":"debit_credit_account_l5y_overdue_amt21",
        "Rpamt22":"debit_credit_account_l5y_overdue_amt22",
        "Rpamt23":"debit_credit_account_l5y_overdue_amt23",
        "Rpamt24":"debit_credit_account_l5y_overdue_amt24",
        "Rpamt25":"debit_credit_account_l5y_overdue_amt25",
        "Rpamt26":"debit_credit_account_l5y_overdue_amt26",
        "Rpamt27":"debit_credit_account_l5y_overdue_amt27",
        "Rpamt28":"debit_credit_account_l5y_overdue_amt28",
        "Rpamt29":"debit_credit_account_l5y_overdue_amt29",
        "Rpamt30":"debit_credit_account_l5y_overdue_amt30",
        "Rpamt31":"debit_credit_account_l5y_overdue_amt31",
        "Rpamt32":"debit_credit_account_l5y_overdue_amt32",
        "Rpamt33":"debit_credit_account_l5y_overdue_amt33",
        "Rpamt34":"debit_credit_account_l5y_overdue_amt34",
        "Rpamt35":"debit_credit_account_l5y_overdue_amt35",
        "Rpamt36":"debit_credit_account_l5y_overdue_amt36",
        "Rpamt37":"debit_credit_account_l5y_overdue_amt37",
        "Rpamt38":"debit_credit_account_l5y_overdue_amt38",
        "Rpamt39":"debit_credit_account_l5y_overdue_amt39",
        "Rpamt40":"debit_credit_account_l5y_overdue_amt40",
        "Rpamt41":"debit_credit_account_l5y_overdue_amt41",
        "Rpamt42":"debit_credit_account_l5y_overdue_amt42",
        "Rpamt43":"debit_credit_account_l5y_overdue_amt43",
        "Rpamt44":"debit_credit_account_l5y_overdue_amt44",
        "Rpamt45":"debit_credit_account_l5y_overdue_amt45",
        "Rpamt46":"debit_credit_account_l5y_overdue_amt46",
        "Rpamt47":"debit_credit_account_l5y_overdue_amt47",
        "Rpamt48":"debit_credit_account_l5y_overdue_amt48",
        "Rpamt49":"debit_credit_account_l5y_overdue_amt49",
        "Rpamt50":"debit_credit_account_l5y_overdue_amt50",
        "Rpamt51":"debit_credit_account_l5y_overdue_amt51",
        "Rpamt52":"debit_credit_account_l5y_overdue_amt52",
        "Rpamt53":"debit_credit_account_l5y_overdue_amt53",
        "Rpamt54":"debit_credit_account_l5y_overdue_amt54",
        "Rpamt55":"debit_credit_account_l5y_overdue_amt55",
        "Rpamt56":"debit_credit_account_l5y_overdue_amt56",
        "Rpamt57":"debit_credit_account_l5y_overdue_amt57",
        "Rpamt58":"debit_credit_account_l5y_overdue_amt58",
        "Rpamt59":"debit_credit_account_l5y_overdue_amt59",
        "Rpamt60":"debit_credit_account_l5y_overdue_amt60",
        "PD01FS01":"debit_credit_account_special_transaction_count",
        "PD01GS01":"debit_credit_account_special_event_count",
        "PD01HS01":"debit_credit_account_large_spec_stage_count",
        "PD01ZS01":"debit_credit_account_mark_count",
        }
    column_list = ["PD01AI01",
                    "PD01AD01",
                    "PD01AD02",
                    "PD01AI02",
                    "PD01AI03",
                    "PD01AI04",
                    "PD01AD03",
                    "PD01AR01",
                    "PD01AD04",
                    "PD01AJ01",
                    "PD01AJ02",
                    "PD01AJ03",
                    "PD01AR02",
                    "PD01AD05",
                    "PD01AD06",
                    "PD01AS01",
                    "PD01AD07",
                    "PD01AD08",
                    "PD01AD09",
                    "PD01AD10",
                    "PD01BD01",
                    "PD01BR01",
                    "PD01BR04",
                    "PD01BJ01",
                    "PD01BR02",
                    "PD01BJ02",
                    "PD01BD03",
                    "PD01BD04",
                    "PD01BR03",
                    "PD01CR01",
                    "PD01CD01",
                    "PD01CJ01",
                    "PD01CJ02",
                    "PD01CJ03",
                    "PD01CD02",
                    "PD01CS01",
                    "PD01CR02",
                    "PD01CJ04",
                    "PD01CJ05",
                    "PD01CR03",
                    "PD01CS02",
                    "PD01CJ06",
                    "PD01CJ07",
                    "PD01CJ08",
                    "PD01CJ09",
                    "PD01CJ10",
                    "PD01CJ11",
                    "PD01CJ12",
                    "PD01CJ13",
                    "PD01CJ14",
                    "PD01CJ15",
                    "PD01CR04",
                    "PD01ER01",
                    "PD01ER02",
                    "PD01ES01",
                    "Rpmonth1",
                    "Rpmonth2",
                    "Rpmonth3",
                    "Rpmonth4",
                    "Rpmonth5",
                    "Rpmonth6",
                    "Rpmonth7",
                    "Rpmonth8",
                    "Rpmonth9",
                    "Rpmonth10",
                    "Rpmonth11",
                    "Rpmonth12",
                    "Rpmonth13",
                    "Rpmonth14",
                    "Rpmonth15",
                    "Rpmonth16",
                    "Rpmonth17",
                    "Rpmonth18",
                    "Rpmonth19",
                    "Rpmonth20",
                    "Rpmonth21",
                    "Rpmonth22",
                    "Rpmonth23",
                    "Rpmonth24",
                    "Rpmonth25",
                    "Rpmonth26",
                    "Rpmonth27",
                    "Rpmonth28",
                    "Rpmonth29",
                    "Rpmonth30",
                    "Rpmonth31",
                    "Rpmonth32",
                    "Rpmonth33",
                    "Rpmonth34",
                    "Rpmonth35",
                    "Rpmonth36",
                    "Rpmonth37",
                    "Rpmonth38",
                    "Rpmonth39",
                    "Rpmonth40",
                    "Rpmonth41",
                    "Rpmonth42",
                    "Rpmonth43",
                    "Rpmonth44",
                    "Rpmonth45",
                    "Rpmonth46",
                    "Rpmonth47",
                    "Rpmonth48",
                    "Rpmonth49",
                    "Rpmonth50",
                    "Rpmonth51",
                    "Rpmonth52",
                    "Rpmonth53",
                    "Rpmonth54",
                    "Rpmonth55",
                    "Rpmonth56",
                    "Rpmonth57",
                    "Rpmonth58",
                    "Rpmonth59",
                    "Rpmonth60",
                    "Rpstatus1",
                    "Rpstatus2",
                    "Rpstatus3",
                    "Rpstatus4",
                    "Rpstatus5",
                    "Rpstatus6",
                    "Rpstatus7",
                    "Rpstatus8",
                    "Rpstatus9",
                    "Rpstatus10",
                    "Rpstatus11",
                    "Rpstatus12",
                    "Rpstatus13",
                    "Rpstatus14",
                    "Rpstatus15",
                    "Rpstatus16",
                    "Rpstatus17",
                    "Rpstatus18",
                    "Rpstatus19",
                    "Rpstatus20",
                    "Rpstatus21",
                    "Rpstatus22",
                    "Rpstatus23",
                    "Rpstatus24",
                    "Rpstatus25",
                    "Rpstatus26",
                    "Rpstatus27",
                    "Rpstatus28",
                    "Rpstatus29",
                    "Rpstatus30",
                    "Rpstatus31",
                    "Rpstatus32",
                    "Rpstatus33",
                    "Rpstatus34",
                    "Rpstatus35",
                    "Rpstatus36",
                    "Rpstatus37",
                    "Rpstatus38",
                    "Rpstatus39",
                    "Rpstatus40",
                    "Rpstatus41",
                    "Rpstatus42",
                    "Rpstatus43",
                    "Rpstatus44",
                    "Rpstatus45",
                    "Rpstatus46",
                    "Rpstatus47",
                    "Rpstatus48",
                    "Rpstatus49",
                    "Rpstatus50",
                    "Rpstatus51",
                    "Rpstatus52",
                    "Rpstatus53",
                    "Rpstatus54",
                    "Rpstatus55",
                    "Rpstatus56",
                    "Rpstatus57",
                    "Rpstatus58",
                    "Rpstatus59",
                    "Rpstatus60",
                    "Rpamt1",
                    "Rpamt2",
                    "Rpamt3",
                    "Rpamt4",
                    "Rpamt5",
                    "Rpamt6",
                    "Rpamt7",
                    "Rpamt8",
                    "Rpamt9",
                    "Rpamt10",
                    "Rpamt11",
                    "Rpamt12",
                    "Rpamt13",
                    "Rpamt14",
                    "Rpamt15",
                    "Rpamt16",
                    "Rpamt17",
                    "Rpamt18",
                    "Rpamt19",
                    "Rpamt20",
                    "Rpamt21",
                    "Rpamt22",
                    "Rpamt23",
                    "Rpamt24",
                    "Rpamt25",
                    "Rpamt26",
                    "Rpamt27",
                    "Rpamt28",
                    "Rpamt29",
                    "Rpamt30",
                    "Rpamt31",
                    "Rpamt32",
                    "Rpamt33",
                    "Rpamt34",
                    "Rpamt35",
                    "Rpamt36",
                    "Rpamt37",
                    "Rpamt38",
                    "Rpamt39",
                    "Rpamt40",
                    "Rpamt41",
                    "Rpamt42",
                    "Rpamt43",
                    "Rpamt44",
                    "Rpamt45",
                    "Rpamt46",
                    "Rpamt47",
                    "Rpamt48",
                    "Rpamt49",
                    "Rpamt50",
                    "Rpamt51",
                    "Rpamt52",
                    "Rpamt53",
                    "Rpamt54",
                    "Rpamt55",
                    "Rpamt56",
                    "Rpamt57",
                    "Rpamt58",
                    "Rpamt59",
                    "Rpamt60",
                    "PD01FS01",
                    "PD01GS01",
                    "PD01HS01",
                    "PD01ZS01",
                    ]

    for i in column_list:
        if i not in list(debitCreditAccount_df.columns):
            debitCreditAccount_df[i] = np.nan
    
    debitCreditAccount_df = debitCreditAccount_df[column_list]
    
    debitCreditAccount_df.reset_index(inplace=True,drop=True)
    status_columns=[]
    month_columns=[]
    overdueAmt_columns=[]
    
    for i in range(1,61):
        status_columns.append('RpStatus'+str(i))
        month_columns.append('RpMonth'+str(i))
        overdueAmt_columns.append('RpAmt'+str(i))
    l5y_columns = status_columns+month_columns+overdueAmt_columns
    
    l5y_df = pd.DataFrame()
    
    for i in range(len(debitCreditAccount_df)):
        if pd.isnull(debitCreditAccount_df.loc[i]['Rpstatus1'])==False:
            report_month = pd.to_datetime(temp1['Document']['PRH']['PA01']['PA01A']['PA01AR01']).strftime(format='%Y-%m')
            pianyiliang = rrule.rrule(rrule.MONTHLY,dtstart = parse(debitCreditAccount_df.loc[i]['Rpmonth1']),until=parse(report_month)).count()-1
            j = 1
            mid_list_status = []
            mid_list_month = []
            mid_list_amt = []
            while j <= pianyiliang:
                mid_list_status.append('*')
                mid_list_month.append(np.nan)
                mid_list_amt.append(0)
                j=j+1
            while j <= 60:
                mid_list_status.append(debitCreditAccount_df.loc[i]['Rpstatus'+str(j-pianyiliang)])
                mid_list_month.append(debitCreditAccount_df.loc[i]['Rpmonth'+str(j-pianyiliang)])
                mid_list_amt.append(debitCreditAccount_df.loc[i]['Rpamt'+str(j-pianyiliang)])
                j=j+1
            mid_list = mid_list_status+mid_list_month+mid_list_amt
            mid_df = pd.DataFrame({i:mid_list},index=l5y_columns)
            mid_df = mid_df.T
            l5y_df = pd.concat([l5y_df,mid_df],axis=0)
        else:
            j = 1
            mid_list_status = []
            mid_list_month = []
            mid_list_amt = []
            while j <= 60:
                mid_list_status.append('*')
                mid_list_month.append(np.nan)
                mid_list_amt.append(0)
                j=j+1
            mid_list = mid_list_status+mid_list_month+mid_list_amt
            mid_df = pd.DataFrame({i:mid_list},index=l5y_columns)
            mid_df = mid_df.T
            l5y_df = pd.concat([l5y_df,mid_df],axis=0)
    
    for i in range(1,61):
        debitCreditAccount_df['Rpstatus'+str(i)] = l5y_df['RpStatus'+str(i)]
        debitCreditAccount_df['Rpmonth'+str(i)] = l5y_df['RpMonth'+str(i)]
        debitCreditAccount_df['Rpamt'+str(i)] = l5y_df['RpAmt'+str(i)]
    
    if column_type == 'CNH':
        debitCreditAccount_df.rename(columns = columns_chinese,inplace=True)
    else:
        debitCreditAccount_df.rename(columns = columns_english,inplace=True)
    return debitCreditAccount_df 

#%%
###特殊交易信息
def crSpecialTrans(temp1,column_type = 'CNH'):
    crSpecialTrans_df = pd.DataFrame()

    try:
        tmp = temp1['Document']['PDA']['PD01']
        for n in range(len(tmp)):
            mid_df = pd.DataFrame()
            try:
                tmp1 = tmp[n]['PD01F']['PD01FH']
                PSID = tmp[n]['PD01A']['PD01AI01']
                # print(PSID)
                # tmp2 = dic_to_df(tmp1)
                tmp2 = pd.io.json.json_normalize(tmp1)
                tmp2.loc[:,'PD01AI01'] = PSID
                mid_df = pd.concat([mid_df,tmp2],axis=1)
            except:
                pass         
            crSpecialTrans_df = pd.concat([crSpecialTrans_df,mid_df],axis=0)
    except:
        pass

    if len(crSpecialTrans_df)<1:
        crSpecialTrans_df = pd.DataFrame({
                                            "PD01FD01":np.nan,
                                            "PD01FR01":np.nan,
                                            "PD01FS02":np.nan,
                                            "PD01FJ01":np.nan,
                                            "PD01FQ01":np.nan,
                                            "PD01AI01":np.nan,
                                            },index=[0])
                                                
    columns_chinese = {
                        "PD01FD01":"特殊交易类型",
                        "PD01FR01":"特殊交易发生日期",
                        "PD01FS02":"到期日期变更月数",
                        "PD01FJ01":"特殊交易发生金额",
                        "PD01FQ01":"特殊交易明细记录",
                        "PD01AI01":"基本信息-账户编号",
                        }
    
    
    # columns_english = {"PD01FD01":"cr_special_trans_special_trans_type",
    #                     "PD01FR01":"cr_special_trans_special_trans_date",
    #                     "PD01FS02":"cr_special_trans_due_date_month_of_change",
    #                     "PD01FJ01":"cr_special_trans_special_trans_amt",
    #                     "PD01FQ01":"cr_special_trans_special_trans_record",
    #                     }
    columns_english = {
                    "PD01FD01":"SpecialTransactionType",
                    "PD01FR01":"TransactionDate",
                    "PD01FS02":"ChangedMonths",
                    "PD01FJ01":"TransactionAmount",
                    "PD01FQ01":"DetailedRecord",
                    "PD01AI01":"PSID",
                    }
    
    column_list = [ 
                    "PD01FD01",
                    "PD01FR01",
                    "PD01FS02",
                    "PD01FJ01",
                    "PD01FQ01",
                    "PD01AI01",
                    ]
    
    for i in column_list:
        if i not in list(crSpecialTrans_df.columns):
            crSpecialTrans_df[i] = np.nan
    
    crSpecialTrans_df = crSpecialTrans_df[column_list]
    if column_type == 'CNH':
        crSpecialTrans_df.rename(columns = columns_chinese,inplace=True)
    else:
        crSpecialTrans_df.rename(columns = columns_english,inplace=True)
    return crSpecialTrans_df 

#%%
###特殊事件信息
def crSpecialEvent(temp1,column_type = 'CNH'):
    crSpecialEvent_df = pd.DataFrame()

    try:
        tmp = temp1['Document']['PDA']['PD01']
        for n in range(len(tmp)):
            mid_df = pd.DataFrame()
            try:
                tmp2 = tmp[n]['PD01G']['PD01GH']
                tmp2 = pd.io.json.json_normalize(tmp2)
                mid_df = pd.concat([mid_df,tmp2],axis=1)
            except:
                pass         
            crSpecialEvent_df = pd.concat([crSpecialEvent_df,mid_df],axis=0)
    except:
        pass

    if len(crSpecialEvent_df)<1:
        crSpecialEvent_df = pd.DataFrame({"PD01GR01":np.nan,
                                        "PD01GD01":np.nan,
                                        },index=[0])
                                                
    columns_chinese = {"PD01GR01":"特殊事件发生月份",
                        "PD01GD01":"特殊事件类型",
                        }
    
    
    columns_english = {"PD01GR01":"cr_special_event_special_event_month",
                        "PD01GD01":"cr_special_event_special_event_type",
                        }
    
    
    column_list = ["PD01GR01",
                    "PD01GD01",
                    ]
    
    for i in column_list:
        if i not in list(crSpecialEvent_df.columns):
            crSpecialEvent_df[i] = np.nan
    
    crSpecialEvent_df = crSpecialEvent_df[column_list]
    if column_type == 'CNH':
        crSpecialEvent_df.rename(columns = columns_chinese,inplace=True)
    else:
        crSpecialEvent_df.rename(columns = columns_english,inplace=True)
    return crSpecialEvent_df 

#%%
###大额专项分期信息
def largeSpecStage(temp1,column_type = 'CNH'):
    largeSpecStage_df = pd.DataFrame()
    try:
        tmp = temp1['Document']['PDA']['PD01']
        for n in range(len(tmp)):
            mid_df = pd.DataFrame()
            PSID = tmp[n]['PD01A']['PD01AI01']
            try:
                tmp2 = tmp[n]['PD01H']['PD01HH']  
                tmp3 = pd.io.json.json_normalize(tmp2)
                tmp3.loc[:,'PD01AI01'] = PSID
                # for h in ['PD01ER03','PD01ED01','PD01EJ01']:
                #     if h not in list(tmp3.columns):
                #         tmp3[h] = np.nan
                mid_df = pd.concat([mid_df,tmp3],axis=1)
            except:
                # tmp3 = pd.DataFrame()
                # tmp3.loc[n,'PD01AI01'] = PSID
                # for h in ['PD01ER03','PD01ED01','PD01EJ01']:
                #     if h not in list(tmp3.columns):
                #         tmp3[h] = np.nan
                # mid_df = pd.concat([mid_df,tmp3],axis=1)
                pass
            largeSpecStage_df = pd.concat([largeSpecStage_df,mid_df],axis=0)
    except:
        pass

    if len(largeSpecStage_df)<1:
        largeSpecStage_df = pd.DataFrame({"PD01HJ01":np.nan,
                                        "PD01HR01":np.nan,
                                        "PD01HR02":np.nan,
                                        "PD01HJ02":np.nan,
                                          "PD01AI01":np.nan,
                                        },index=[0])
                                                
    columns_chinese = {"PD01HJ01":"大额专项分期额度",
                        "PD01HR01":"分期额度生效日期",
                        "PD01HR02":"分期额度到期日期",
                        "PD01HJ02":"已用分期金额",
                       "PD01AI01":"基本信息-账户编号",
                        }
    
    
    # columns_english = {"PD01HJ01":"cr_large_spec_stage_big_stage_amt",
    #                     "PD01HR01":"cr_large_spec_stage_start_date",
    #                     "PD01HR02":"cr_large_spec_stage_end_date",
    #                     "PD01HJ02":"cr_large_spec_stage_used_amt",
    #                     }
    columns_english = {"PD01HJ01":"SpecialInstalmentCreditLine",
                    "PD01HR01":"SpecialInstalmentBeginDate",
                    "PD01HR02":"SpecialInstalmentEndDate",
                    "PD01HJ02":"SpecialInstalmentUsedAmount",
                    "PD01AI01":"SID",
                    }
    
    column_list = ["PD01HJ01",
                    "PD01HR01",
                    "PD01HR02",
                    "PD01HJ02",
                   "PD01AI01"
                    ]
    
    for i in column_list:
        if i not in list(largeSpecStage_df.columns):
            largeSpecStage_df[i] = np.nan
    
    largeSpecStage_df = largeSpecStage_df[column_list]
    if column_type == 'CNH':
        largeSpecStage_df.rename(columns = columns_chinese,inplace=True)
    else:
        largeSpecStage_df.rename(columns = columns_english,inplace=True)
    return largeSpecStage_df

#%%
###授信协议基本信息段
def crAgreement(temp1,column_type = 'CNH'):
    crAgreement_df = pd.DataFrame()

    try:
        tmp = temp1['Document']['PCA']['PD02']
        for n in range(len(tmp)):
            mid_df = pd.DataFrame()
            for j in ['PD02A','PD02Z']:
                if j in ['PD02A','PD02Z']:
                    try:
                        tmp1 = tmp[n][j]
                        tmp1 = list_to_df(tmp1)
                        mid_df = pd.concat([mid_df,tmp1],axis=1)
                    except:
                        pass
            crAgreement_df = pd.concat([crAgreement_df,mid_df],axis=0)
    except:
        pass

    if len(crAgreement_df)<1:
        crAgreement_df = pd.DataFrame({"PD02AI01":np.nan,
                                        "PD02AD01":np.nan,
                                        "PD02AI02":np.nan,
                                        "PD02AI03":np.nan,
                                        "PD02AD02":np.nan,
                                        "PD02AJ01":np.nan,
                                        "PD02AD03":np.nan,
                                        "PD02AR01":np.nan,
                                        "PD02AR02":np.nan,
                                        "PD02AD04":np.nan,
                                        "PD02AJ04":np.nan,
                                        "PD02AI04":np.nan,
                                        "PD02AJ03":np.nan,
                                        "PD02ZS01":np.nan,
                                        },index=[0])
                                                
    columns_chinese = {"PD02AI01":"基本信息-授信协议编号",
                        "PD02AD01":"基本信息-业务管理机构类型",
                        "PD02AI02":"基本信息-业务管理机构",
                        "PD02AI03":"基本信息-授信协议标识",
                        "PD02AD02":"基本信息-授信额度用途",
                        "PD02AJ01":"基本信息-授信额度",
                        "PD02AD03":"基本信息-币种",
                        "PD02AR01":"基本信息-生效日期",
                        "PD02AR02":"基本信息-到期日期",
                        "PD02AD04":"基本信息-授信协议状态",
                        "PD02AJ04":"基本信息-已用额度",
                        "PD02AI04":"基本信息-授信限额编号",
                        "PD02AJ03":"基本信息-授信限额",
                        "PD02ZS01":"标注及声明信息-标注及声明个数",
                        }
    
    
    # columns_english = {"PD02AI01":"cr_agreement_credit_agreement_no",
    #                     "PD02AD01":"cr_agreement_business_manage_org_type",
    #                     "PD02AI02":"cr_agreement_business_manage_org_name",
    #                     "PD02AI03":"cr_agreement_credit_agreement_flag",
    #                     "PD02AD02":"cr_agreement_credit_amt_use",
    #                     "PD02AJ01":"cr_agreement_credit_amt",
    #                     "PD02AD03":"cr_agreement_currency",
    #                     "PD02AR01":"cr_agreement_start_date",
    #                     "PD02AR02":"cr_agreement_end_date",
    #                     "PD02AD04":"cr_agreement_credit_agreement_status",
    #                     "PD02AJ04":"cr_agreement_used_amt",
    #                     "PD02AI04":"cr_agreement_credit_limit_no",
    #                     "PD02AJ03":"cr_agreement_credit_limit",
    #                     "PD02ZS01":"cr_agreement_mark_count",
    #                     }
    columns_english = {"PD02AI01":"SerialNumber",
                    "PD02AD01":"ManageOrgType",
                    "PD02AI02":"ManagementCompany",
                    "PD02AI03":"CreditIdentity",
                    "PD02AD02":"CreditLineReason",
                    "PD02AJ01":"CreditLine",
                    "PD02AD03":"Currency",
                    "PD02AR01":"CreditBeginDate",
                    "PD02AR02":"CreditEndDate",
                    "PD02AD04":"AgreementStatus",
                    "PD02AJ04":"UsedAmount",
                    "PD02AI04":"CreditLimitNumber",
                    "PD02AJ03":"CreditLimit",
                    "PD02ZS01":"AgreementMarkCount",
                    }
    
    
    column_list = ["PD02AI01",
                    "PD02AD01",
                    "PD02AI02",
                    "PD02AI03",
                    "PD02AD02",
                    "PD02AJ01",
                    "PD02AD03",
                    "PD02AR01",
                    "PD02AR02",
                    "PD02AD04",
                    "PD02AJ04",
                    "PD02AI04",
                    "PD02AJ03",
                    "PD02ZS01",
                    ]
    
    for i in column_list:
        if i not in list(crAgreement_df.columns):
            crAgreement_df[i] = np.nan
    
    crAgreement_df = crAgreement_df[column_list]
    if column_type == 'CNH':
        crAgreement_df.rename(columns = columns_chinese,inplace=True)
    else:
        crAgreement_df.rename(columns = columns_english,inplace=True)
    return crAgreement_df

#%%
###相关还款责任信息
def crRelatedRepayDuty(temp1,column_type = 'CNH'):
    crRelatedRepayDuty_df = pd.DataFrame()

    try:
        tmp = temp1['Document']['PCR']['PD03']
        for n in range(len(tmp)):
            mid_df = pd.DataFrame()
            for j in ['PD03A','PD03Z']:
                if j in ['PD03A','PD03Z']:
                    try:
                        tmp1 = tmp[n][j]
                        tmp1 = list_to_df(tmp1)
                        mid_df = pd.concat([mid_df,tmp1],axis=1)
                    except:
                        pass
            crRelatedRepayDuty_df = pd.concat([crRelatedRepayDuty_df,mid_df],axis=0)
    except:
        pass

    if len(crRelatedRepayDuty_df)<1:
        crRelatedRepayDuty_df = pd.DataFrame({"PD03AD08":np.nan,
                                                "PD03AD01":np.nan,
                                                "PD03AQ01":np.nan,
                                                "PD03AD02":np.nan,
                                                "PD03AR01":np.nan,
                                                "PD03AR02":np.nan,
                                                "PD03AD03":np.nan,
                                                "PD03AQ02":np.nan,
                                                "PD03AJ01":np.nan,
                                                "PD03AD04":np.nan,
                                                "PD03AJ02":np.nan,
                                                "PD03AD05":np.nan,
                                                "PD03AD06":np.nan,
                                                "PD03AD07":np.nan,
                                                "PD03AS01":np.nan,
                                                "PD03AR03":np.nan,
                                                "PD03ZS01":np.nan,
                                                },index=[0])
                                                
    columns_chinese = {"PD03AD08":"相关还款责任信息-主借款人身份类别",
                        "PD03AD01":"相关还款责任信息-业务管理机构类型",
                        "PD03AQ01":"相关还款责任信息-业务管理机构",
                        "PD03AD02":"相关还款责任信息-业务种类",
                        "PD03AR01":"相关还款责任信息-开立日期",
                        "PD03AR02":"相关还款责任信息-到期日期",
                        "PD03AD03":"相关还款责任信息-相关还款责任人类型",
                        "PD03AQ02":"相关还款责任信息-保证合同编号",
                        "PD03AJ01":"相关还款责任信息-相关还款责任金额",
                        "PD03AD04":"相关还款责任信息-币种",
                        "PD03AJ02":"相关还款责任信息-余额",
                        "PD03AD05":"相关还款责任信息-五级分类",
                        "PD03AD06":"相关还款责任信息-账户类型",
                        "PD03AD07":"相关还款责任信息-还款状态",
                        "PD03AS01":"相关还款责任信息-逾期月数",
                        "PD03AR03":"相关还款责任信息-信息报告日期",
                        "PD03ZS01":"标注及声明信息-标注及声明个数",
                        }
    
    
    # columns_english = {"PD03AD08":"cr_related_repay_duty_borrower_type",
    #                     "PD03AD01":"cr_related_repay_duty_business_manage_org_type",
    #                     "PD03AQ01":"cr_related_repay_duty_business_manage_org_name",
    #                     "PD03AD02":"cr_related_repay_duty_business_type",
    #                     "PD03AR01":"cr_related_repay_duty_start_date",
    #                     "PD03AR02":"cr_related_repay_duty_end_date",
    #                     "PD03AD03":"cr_related_repay_duty_repay_person_type",
    #                     "PD03AQ02":"cr_related_repay_duty_contract_no",
    #                     "PD03AJ01":"cr_related_repay_duty_repay_amt",
    #                     "PD03AD04":"cr_related_repay_duty_currency",
    #                     "PD03AJ02":"cr_related_repay_duty_balance",
    #                     "PD03AD05":"cr_related_repay_duty_five_level_classification",
    #                     "PD03AD06":"cr_related_repay_duty_account_type",
    #                     "PD03AD07":"cr_related_repay_duty_repay_status",
    #                     "PD03AS01":"cr_related_repay_duty_overdue_month_count",
    #                     "PD03AR03":"cr_related_repay_duty_report_date",
    #                     "PD03ZS01":"cr_related_repay_duty_mark_count",
    #                     }
    
    columns_english = {"PD03AD08":"PrimaryBorrowerFlag",
                        "PD03AD01":"RelatedRepayDutyBusinessManageOrgType",
                        "PD03AQ01":"SecuredLoanIssuer",
                        "PD03AD02":"BusinessType",
                        "PD03AR01":"SecuredLoanIssuingDate",
                        "PD03AR02":"SecuredLoanMaturityDate",
                        "PD03AD03":"CoBorrowingFlag",
                        "PD03AQ02":"GuaranteeContractNumber",
                        "PD03AJ01":"SecuredAmount",
                        "PD03AD04":"Currency",
                        "PD03AJ02":"BadDebtAmount",
                        "PD03AD05":"SecuredLoanGrade",
                        "PD03AD06":"RelatedRepayDutyAccountType",
                        "PD03AD07":"RepaymentState",
                        "PD03AS01":"ArrearMonth",
                        "PD03AR03":"RecordDescription",
                        "PD03ZS01":"RelatedRepayDutyMarkCount",
                        }
    
    column_list = ["PD03AD08",
                    "PD03AD01",
                    "PD03AQ01",
                    "PD03AD02",
                    "PD03AR01",
                    "PD03AR02",
                    "PD03AD03",
                    "PD03AQ02",
                    "PD03AJ01",
                    "PD03AD04",
                    "PD03AJ02",
                    "PD03AD05",
                    "PD03AD06",
                    "PD03AD07",
                    "PD03AS01",
                    "PD03AR03",
                    "PD03ZS01",
                    ]
    
    for i in column_list:
        if i not in list(crRelatedRepayDuty_df.columns):
            crRelatedRepayDuty_df[i] = np.nan
    
    crRelatedRepayDuty_df = crRelatedRepayDuty_df[column_list]
    if column_type == 'CNH':
        crRelatedRepayDuty_df.rename(columns = columns_chinese,inplace=True)
    else:
        crRelatedRepayDuty_df.rename(columns = columns_english,inplace=True)
    return crRelatedRepayDuty_df

#%%
###后付费信息
def ncrTransDetail(temp1,column_type = 'CNH'):
    ncrTransDetail_df = pd.DataFrame()

    try:
        tmp = temp1['Document']['PND']['PE01']
        for n in range(len(tmp)):
            mid_df = pd.DataFrame()
            for j in ['PE01A','PE01Z']:
                if j in ['PE01A','PE01Z']:
                    try:
                        tmp1 = tmp[n][j]
                        tmp1 = list_to_df(tmp1)
                        mid_df = pd.concat([mid_df,tmp1],axis=1)
                    except:
                        pass
            ncrTransDetail_df = pd.concat([ncrTransDetail_df,mid_df],axis=0)
    except:
        pass

    if len(ncrTransDetail_df)<1:
        ncrTransDetail_df = pd.DataFrame({"PE01AD01":np.nan,
                                            "PE01AQ01":np.nan,
                                            "PE01AD02":np.nan,
                                            "PE01AR01":np.nan,
                                            "PE01AD03":np.nan,
                                            "PE01AJ01":np.nan,
                                            "PE01AR02":np.nan,
                                            "PE01AQ02":np.nan,
                                            "PE01ZS01":np.nan,
                                            },index=[0])
                                                
    columns_chinese = {"PE01AD01":"后付费账户类型",
                        "PE01AQ01":"机构名称",
                        "PE01AD02":"业务类型",
                        "PE01AR01":"业务开通日期",
                        "PE01AD03":"当前缴费状态",
                        "PE01AJ01":"当前欠费金额",
                        "PE01AR02":"记账年月",
                        "PE01AQ02":"最近24个月缴费记录",
                        "PE01ZS01":"标注及声明个数",
                        }
    
    
    # columns_english = {"PE01AD01":"ncr_trans_detail_postpaid_account_type",
    #                     "PE01AQ01":"ncr_trans_detail_org_name",
    #                     "PE01AD02":"ncr_trans_detail_business_type",
    #                     "PE01AR01":"ncr_trans_detail_start_date",
    #                     "PE01AD03":"ncr_trans_detail_pay_status",
    #                     "PE01AJ01":"ncr_trans_detail_arrear_amt",
    #                     "PE01AR02":"ncr_trans_detail_accounting_month",
    #                     "PE01AQ02":"ncr_trans_detail_l24m_payment_record",
    #                     "PE01ZS01":"ncr_trans_detail_mark_count",
    #                     }
    
    columns_english = {"PE01AD01":"NcrTransDetailPostpaidAccountType",
                    "PE01AQ01":"Instituion",
                    "PE01AD02":"BusinessType",
                    "PE01AR01":"BusinessDate",
                    "PE01AD03":"PaymentStatus",
                    "PE01AJ01":"ArrearAmount",
                    "PE01AR02":"BillingDate",
                    "PE01AQ02":"PaymentRecordDescription",
                    "PE01ZS01":"NcrTransDetailMarkCount",
                    }
    
    
    column_list = ["PE01AD01",
                    "PE01AQ01",
                    "PE01AD02",
                    "PE01AR01",
                    "PE01AD03",
                    "PE01AJ01",
                    "PE01AR02",
                    "PE01AQ02",
                    "PE01ZS01",
                    ]
    
    for i in column_list:
        if i not in list(ncrTransDetail_df.columns):
            ncrTransDetail_df[i] = np.nan
    
    ncrTransDetail_df = ncrTransDetail_df[column_list]
    if column_type == 'CNH':
        ncrTransDetail_df.rename(columns = columns_chinese,inplace=True)
    else:
        ncrTransDetail_df.rename(columns = columns_english,inplace=True)
    return ncrTransDetail_df

#%%
###税务信息
def pubTaxOwed(temp1,column_type = 'CNH'):
    pubTaxOwed_df = pd.DataFrame()

    try:
        tmp = temp1['Document']['POT']['PF01']
        for n in range(len(tmp)):
            mid_df = pd.DataFrame()
            for j in ['PF01A','PF01Z']:
                if j in ['PF01A','PF01Z']:
                    try:
                        tmp1 = tmp[n][j]
                        tmp1 = list_to_df(tmp1)
                        mid_df = pd.concat([mid_df,tmp1],axis=1)
                    except:
                        pass
            pubTaxOwed_df = pd.concat([pubTaxOwed_df,mid_df],axis=0)
    except:
        pass

    if len(pubTaxOwed_df)<1:
        pubTaxOwed_df = pd.DataFrame({"PF01AQ01":np.nan,
                                        "PF01AJ01":np.nan,
                                        "PF01AR01":np.nan,
                                        "PF01ZS01":np.nan,
                                        },index=[0])
                                                
    columns_chinese = {"PF01AQ01":"主管税务机关",
                        "PF01AJ01":"欠税总额",
                        "PF01AR01":"欠税统计日期",
                        "PF01ZS01":"标注及声明个数",
                        }
                            
    
    # columns_english = {"PF01AQ01":"pub_tax_owed_tax_org",
    #                     "PF01AJ01":"pub_tax_owed_tax_owed_amt",
    #                     "PF01AR01":"pub_tax_owed_tax_owed_date",
    #                     "PF01ZS01":"pub_tax_owed_mark_count",
    #                     }
    columns_english = {"PF01AQ01":"TaxAuthority",
                    "PF01AJ01":"TotalTaxArrears",
                    "PF01AR01":"StatisticsDate",
                    "PF01ZS01":"PubTaxOwedMarkCount",
                    }
    
    column_list = ["PF01AQ01",
                    "PF01AJ01",
                    "PF01AR01",
                    "PF01ZS01",
                    ]
    
    for i in column_list:
        if i not in list(pubTaxOwed_df.columns):
            pubTaxOwed_df[i] = np.nan
    
    pubTaxOwed_df = pubTaxOwed_df[column_list]
    if column_type == 'CNH':
        pubTaxOwed_df.rename(columns = columns_chinese,inplace=True)
    else:
        pubTaxOwed_df.rename(columns = columns_english,inplace=True)
    return pubTaxOwed_df

#%%
###民事判决记录信息
def pubCivilJudgement(temp1,column_type = 'CNH'):
    pubCivilJudgement_df = pd.DataFrame()

    try:
        tmp = temp1['Document']['PCJ']['PF02']
        for n in range(len(tmp)):
            mid_df = pd.DataFrame()
            for j in ['PF02A','PF02Z']:
                if j in ['PF02A','PF02Z']:
                    try:
                        tmp1 = tmp[n][j]
                        tmp1 = list_to_df(tmp1)
                        mid_df = pd.concat([mid_df,tmp1],axis=1)
                    except:
                        pass
            pubCivilJudgement_df = pd.concat([pubCivilJudgement_df,mid_df],axis=0)
    except:
        pass

    if len(pubCivilJudgement_df)<1:
        pubCivilJudgement_df = pd.DataFrame({"PF02AQ01":np.nan,
                                            "PF02AQ02":np.nan,
                                            "PF02AR01":np.nan,
                                            "PF02AD01":np.nan,
                                            "PF02AQ03":np.nan,
                                            "PF02AR02":np.nan,
                                            "PF02AQ04":np.nan,
                                            "PF02AJ01":np.nan,
                                            "PF02ZS01":np.nan,
                                            },index=[0])
                                                
    columns_chinese = {"PF02AQ01":"立案法院",
                        "PF02AQ02":"案由",
                        "PF02AR01":"立案日期",
                        "PF02AD01":"结案方式",
                        "PF02AQ03":"判决/调解结果",
                        "PF02AR02":"判决/调解生效日期",
                        "PF02AQ04":"诉讼标的",
                        "PF02AJ01":"诉讼标的金额",
                        "PF02ZS01":"标注及声明个数",
                        }
                            
    
    # columns_english = {"PF02AQ01":"pub_civil_judgement_court",
    #                     "PF02AQ02":"pub_civil_judgement_case_reason",
    #                     "PF02AR01":"pub_civil_judgement_case_start_date",
    #                     "PF02AD01":"pub_civil_judgement_case_closed_way",
    #                     "PF02AQ03":"pub_civil_judgement_judgement_result",
    #                     "PF02AR02":"pub_civil_judgement_judgement_effective_date",
    #                     "PF02AQ04":"pub_civil_judgement_litigation_target",
    #                     "PF02AJ01":"pub_civil_judgement_litigation_amt",
    #                     "PF02ZS01":"pub_civil_judgement_mark_count",
    #                     }
    columns_english = {"PF02AQ01":"Court",
                    "PF02AQ02":"Cause",
                    "PF02AR01":"RegisterDate",
                    "PF02AD01":"ClosedMode",
                    "PF02AQ03":"Conclusion",
                    "PF02AR02":"EffectiveDate",
                    "PF02AQ04":"LitigationObject",
                    "PF02AJ01":"LitigationAmount",
                    "PF02ZS01":"JudgementMarkCount",
                    }
    
    
    column_list = ["PF02AQ01",
                    "PF02AQ02",
                    "PF02AR01",
                    "PF02AD01",
                    "PF02AQ03",
                    "PF02AR02",
                    "PF02AQ04",
                    "PF02AJ01",
                    "PF02ZS01",
                    ]
    
    for i in column_list:
        if i not in list(pubCivilJudgement_df.columns):
            pubCivilJudgement_df[i] = np.nan
    
    pubCivilJudgement_df = pubCivilJudgement_df[column_list]
    if column_type == 'CNH':
        pubCivilJudgement_df.rename(columns = columns_chinese,inplace=True)
    else:
        pubCivilJudgement_df.rename(columns = columns_english,inplace=True)
    return pubCivilJudgement_df

#%%
###强制执行记录信息
def pubForceExecute(temp1,column_type = 'CNH'):
    pubForceExecute_df = pd.DataFrame()

    try:
        tmp = temp1['Document']['PCE']['PF03']
        for n in range(len(tmp)):
            mid_df = pd.DataFrame()
            for j in ['PF03A','PF03Z']:
                if j in ['PF03A','PF03Z']:
                    try:
                        tmp1 = tmp[n][j]
                        tmp1 = list_to_df(tmp1)
                        mid_df = pd.concat([mid_df,tmp1],axis=1)
                    except:
                        pass
            pubForceExecute_df = pd.concat([pubForceExecute_df,mid_df],axis=0)
    except:
        pass

    if len(pubForceExecute_df)<1:
        pubForceExecute_df = pd.DataFrame({"PF03AQ01":np.nan,
                                            "PF03AQ02":np.nan,
                                            "PF03AR01":np.nan,
                                            "PF03AD01":np.nan,
                                            "PF03AQ03":np.nan,
                                            "PF03AR02":np.nan,
                                            "PF03AQ04":np.nan,
                                            "PF03AJ01":np.nan,
                                            "PF03AQ05":np.nan,
                                            "PF03AJ02":np.nan,
                                            "PF03ZS01":np.nan,
                                            },index=[0])
                                                
    columns_chinese = {"PF03AQ01":"执行法院",
                        "PF03AQ02":"执行案由",
                        "PF03AR01":"立案日期",
                        "PF03AD01":"结案方式",
                        "PF03AQ03":"案件状态",
                        "PF03AR02":"结案日期",
                        "PF03AQ04":"申请执行标的",
                        "PF03AJ01":"申请执行标的金额",
                        "PF03AQ05":"已执行标的",
                        "PF03AJ02":"已执行标的金额",
                        "PF03ZS01":"标注及声明个数",
                        }
                            
    
    # columns_english = {"PF03AQ01":"pub_force_execute_court",
    #                     "PF03AQ02":"pub_force_execute_case_reason",
    #                     "PF03AR01":"pub_force_execute_case_start_date",
    #                     "PF03AD01":"pub_force_execute_case_closed_way",
    #                     "PF03AQ03":"pub_force_execute_case_status",
    #                     "PF03AR02":"pub_force_execute_case_closed_date",
    #                     "PF03AQ04":"pub_force_execute_application_target",
    #                     "PF03AJ01":"pub_force_execute_application_amt",
    #                     "PF03AQ05":"pub_force_execute_executed_target",
    #                     "PF03AJ02":"pub_force_execute_executed_amt",
    #                     "PF03ZS01":"pub_force_execute_mark_count",
    #                     }
    
    columns_english = {"PF03AQ01":"ExecutiveCourt",
                    "PF03AQ02":"ExecutiveCase",
                    "PF03AR01":"RegisterDate",
                    "PF03AD01":"ClosedMode",
                    "PF03AQ03":"CaseStatus",
                    "PF03AR02":"ClosedDate",
                    "PF03AQ04":"ApplicationExecution",
                    "PF03AJ01":"ApplicationExecutionAmount",
                    "PF03AQ05":"ImplementedObject",
                    "PF03AJ02":"ImplementedAmount",
                    "PF03ZS01":"PubForceExecuteMarkCount",
                    }
    
    
    column_list = ["PF03AQ01",
                    "PF03AQ02",
                    "PF03AR01",
                    "PF03AD01",
                    "PF03AQ03",
                    "PF03AR02",
                    "PF03AQ04",
                    "PF03AJ01",
                    "PF03AQ05",
                    "PF03AJ02",
                    "PF03ZS01",
                    ]
    
    for i in column_list:
        if i not in list(pubForceExecute_df.columns):
            pubForceExecute_df[i] = np.nan
    
    pubForceExecute_df = pubForceExecute_df[column_list]
    if column_type == 'CNH':
        pubForceExecute_df.rename(columns = columns_chinese,inplace=True)
    else:
        pubForceExecute_df.rename(columns = columns_english,inplace=True)
    return pubForceExecute_df

#%%
###行政处罚记录信息
def pubAdminPenalty(temp1,column_type = 'CNH'):
    pubAdminPenalty_df = pd.DataFrame()

    try:
        tmp = temp1['Document']['PAP']['PF04']
        for n in range(len(tmp)):
            mid_df = pd.DataFrame()
            for j in ['PF04A','PF04Z']:
                if j in ['PF04A','PF04Z']:
                    try:
                        tmp1 = tmp[n][j]
                        tmp1 = list_to_df(tmp1)
                        mid_df = pd.concat([mid_df,tmp1],axis=1)
                    except:
                        pass
            pubAdminPenalty_df = pd.concat([pubAdminPenalty_df,mid_df],axis=0)
    except:
        pass

    if len(pubAdminPenalty_df)<1:
        pubAdminPenalty_df = pd.DataFrame({"PF04AQ01":np.nan,
                                            "PF04AQ02":np.nan,
                                            "PF04AJ01":np.nan,
                                            "PF04AR01":np.nan,
                                            "PF04AR02":np.nan,
                                            "PF04AQ03":np.nan,
                                            "PF04ZS01":np.nan,
                                            },index=[0])
                                                
    columns_chinese = {"PF04AQ01":"处罚机构",
                        "PF04AQ02":"处罚内容",
                        "PF04AJ01":"处罚金额",
                        "PF04AR01":"处罚生效日期",
                        "PF04AR02":"处罚截止日期",
                        "PF04AQ03":"行政复议结果",
                        "PF04ZS01":"标注及声明个数",
                        }
                            
    
    # columns_english = {"PF04AQ01":"pub_admin_penalty_punish_org",
    #                     "PF04AQ02":"pub_admin_penalty_punish_content",
    #                     "PF04AJ01":"pub_admin_penalty_punish_amt",
    #                     "PF04AR01":"pub_admin_penalty_start_date",
    #                     "PF04AR02":"pub_admin_penalty_end_date",
    #                     "PF04AQ03":"pub_admin_penalty_reconsider_result",
    #                     "PF04ZS01":"pub_admin_penalty_mark_count",
    #                     }
    columns_english = {"PF04AQ01":"PunishmentInstitution",
                    "PF04AQ02":"PunishingMatter",
                    "PF04AJ01":"PunishmentAmount",
                    "PF04AR01":"EffectiveDate",
                    "PF04AR02":"Deadline",
                    "PF04AQ03":"ReviewResults",
                    "PF04ZS01":"PubAdminPenaltyMarkCount",
                    }
    
    
    column_list = ["PF04AQ01",
                    "PF04AQ02",
                    "PF04AJ01",
                    "PF04AR01",
                    "PF04AR02",
                    "PF04AQ03",
                    "PF04ZS01",
                    ]
    
    for i in column_list:
        if i not in list(pubAdminPenalty_df.columns):
            pubAdminPenalty_df[i] = np.nan
    
    pubAdminPenalty_df = pubAdminPenalty_df[column_list]
    if column_type == 'CNH':
        pubAdminPenalty_df.rename(columns = columns_chinese,inplace=True)
    else:
        pubAdminPenalty_df.rename(columns = columns_english,inplace=True)
    return pubAdminPenalty_df

#%%
###住房公积金参缴记录信息
def pubHousingFund(temp1,column_type = 'CNH'):
    pubAdminPenalty_df = pd.DataFrame()

    try:
        tmp = temp1['Document']['PHF']['PF05']
        for n in range(len(tmp)):
            mid_df = pd.DataFrame()
            for j in ['PF05A','PF05Z']:
                if j in ['PF05A','PF05Z']:
                    try:
                        tmp1 = tmp[n][j]
                        tmp1 = list_to_df(tmp1)
                        mid_df = pd.concat([mid_df,tmp1],axis=1)
                    except:
                        pass
            pubAdminPenalty_df = pd.concat([pubAdminPenalty_df,mid_df],axis=0)
    except:
        pass

    if len(pubAdminPenalty_df)<1:
        pubAdminPenalty_df = pd.DataFrame({"PF05AQ01":np.nan,
                                            "PF05AR01":np.nan,
                                            "PF05AD01":np.nan,
                                            "PF05AR02":np.nan,
                                            "PF05AR03":np.nan,
                                            "PF05AQ02":np.nan,
                                            "PF05AQ03":np.nan,
                                            "PF05AJ01":np.nan,
                                            "PF05AQ04":np.nan,
                                            "PF05AR04":np.nan,
                                            "PF05ZS01":np.nan,
                                            },index=[0])
                                                
    columns_chinese = {"PF05AQ01":"参缴地",
                        "PF05AR01":"参缴日期",
                        "PF05AD01":"缴费状态",
                        "PF05AR02":"初缴月份",
                        "PF05AR03":"缴至月份",
                        "PF05AQ02":"单位缴存比例",
                        "PF05AQ03":"个人缴存比例",
                        "PF05AJ01":"月缴存额",
                        "PF05AQ04":"缴费单位",
                        "PF05AR04":"信息更新日期",
                        "PF05ZS01":"标注及声明个数",
                        }
                                                    
    # columns_english = {"PF05AQ01":"pub_housing_fund_pay_addr",
    #                     "PF05AR01":"pub_housing_fund_pay_date",
    #                     "PF05AD01":"pub_housing_fund_pay_status",
    #                     "PF05AR02":"pub_housing_fund_start_month",
    #                     "PF05AR03":"pub_housing_fund_end_month",
    #                     "PF05AQ02":"pub_housing_fund_company_ratio",
    #                     "PF05AQ03":"pub_housing_fund_person_ratio",
    #                     "PF05AJ01":"pub_housing_fund_monthly_amt",
    #                     "PF05AQ04":"pub_housing_fund_pay_company",
    #                     "PF05AR04":"pub_housing_fund_update_date",
    #                     "PF05ZS01":"pub_housing_fund_mark_count",
    #                     }
    columns_english = {"PF05AQ01":"PaymentPlace",
                    "PF05AR01":"PaymentDate",
                    "PF05AD01":"PaymentStatus",
                    "PF05AR02":"FisrtPaymentMonth",
                    "PF05AR03":"EndPaymentMonth",
                    "PF05AQ02":"CompanyRatio",
                    "PF05AQ03":"IndividualRatio",
                    "PF05AJ01":"MonthPayAmount",
                    "PF05AQ04":"Company",
                    "PF05AR04":"UpdateDate",
                    "PF05ZS01":"PubHousingFundMarkCount",
                    }
    
    
    column_list = ["PF05AQ01",
                    "PF05AR01",
                    "PF05AD01",
                    "PF05AR02",
                    "PF05AR03",
                    "PF05AQ02",
                    "PF05AQ03",
                    "PF05AJ01",
                    "PF05AQ04",
                    "PF05AR04",
                    "PF05ZS01",
                    ]
    
    for i in column_list:
        if i not in list(pubAdminPenalty_df.columns):
            pubAdminPenalty_df[i] = np.nan
    
    pubAdminPenalty_df = pubAdminPenalty_df[column_list]
    if column_type == 'CNH':
        pubAdminPenalty_df.rename(columns = columns_chinese,inplace=True)
    else:
        pubAdminPenalty_df.rename(columns = columns_english,inplace=True)
    return pubAdminPenalty_df

#%%
###低保救助信息记录信息
def pubSubsistanceAllowance(temp1,column_type = 'CNH'):
    pubSubsistanceAllowance_df = pd.DataFrame()

    try:
        tmp = temp1['Document']['PBS']['PF06']
        for n in range(len(tmp)):
            mid_df = pd.DataFrame()
            for j in ['PF06A','PF06Z']:
                if j in ['PF06A','PF06Z']:
                    try:
                        tmp1 = tmp[n][j]
                        tmp1 = list_to_df(tmp1)
                        mid_df = pd.concat([mid_df,tmp1],axis=1)
                    except:
                        pass
            pubSubsistanceAllowance_df = pd.concat([pubSubsistanceAllowance_df,mid_df],axis=0)
    except:
        pass

    if len(pubSubsistanceAllowance_df)<1:
        pubSubsistanceAllowance_df = pd.DataFrame({"PF06AD01":np.nan,
                                                    "PF06AQ01":np.nan,
                                                    "PF06AQ02":np.nan,
                                                    "PF06AQ03":np.nan,
                                                    "PF06AR01":np.nan,
                                                    "PF06AR02":np.nan,
                                                    "PF06AR03":np.nan,
                                                    "PF06ZS01":np.nan,
                                                    },index=[0])
                                                                                                    
    columns_chinese = {"PF06AD01":"人员类别",
                        "PF06AQ01":"所在地",
                        "PF06AQ02":"工作单位",
                        "PF06AQ03":"家庭月收入",
                        "PF06AR01":"申请日期",
                        "PF06AR02":"批准日期",
                        "PF06AR03":"信息更新日期",
                        "PF06ZS01":"标注及声明个数",
                        }
                                                    
    # columns_english = {"PF06AD01":"pub_subsistance_allowance_person_type",
    #                     "PF06AQ01":"pub_subsistance_allowance_address",
    #                     "PF06AQ02":"pub_subsistance_allowance_company",
    #                     "PF06AQ03":"pub_subsistance_allowance_family_monthly_income",
    #                     "PF06AR01":"pub_subsistance_allowance_apply_date",
    #                     "PF06AR02":"pub_subsistance_allowance_approve_date",
    #                     "PF06AR03":"pub_subsistance_allowance_update_date",
    #                     "PF06ZS01":"pub_subsistance_allowance_mark_count",
    #                     }
    
    columns_english = {"PF06AD01":"Category",
                    "PF06AQ01":"Place",
                    "PF06AQ02":"Company",
                    "PF06AQ03":"FamilyMonthIncome",
                    "PF06AR01":"ApplyDate",
                    "PF06AR02":"ApproveDate",
                    "PF06AR03":"UpdateDate",
                    "PF06ZS01":"PubSubsistanceAllowanceMarkCount",
                    }
    
    column_list = ["PF06AD01",
                    "PF06AQ01",
                    "PF06AQ02",
                    "PF06AQ03",
                    "PF06AR01",
                    "PF06AR02",
                    "PF06AR03",
                    "PF06ZS01",
                    ]
                        
    for i in column_list:
        if i not in list(pubSubsistanceAllowance_df.columns):
            pubSubsistanceAllowance_df[i] = np.nan
    
    pubSubsistanceAllowance_df = pubSubsistanceAllowance_df[column_list]
    if column_type == 'CNH':
        pubSubsistanceAllowance_df.rename(columns = columns_chinese,inplace=True)
    else:
        pubSubsistanceAllowance_df.rename(columns = columns_english,inplace=True)
    return pubSubsistanceAllowance_df

#%%
###执业资格记录信息
def pubQualification(temp1,column_type = 'CNH'):
    pubQualification_df = pd.DataFrame()

    try:
        tmp = temp1['Document']['PPQ']['PF07']
        for n in range(len(tmp)):
            mid_df = pd.DataFrame()
            for j in ['PF07A','PF07Z']:
                if j in ['PF07A','PF07Z']:
                    try:
                        tmp1 = tmp[n][j]
                        tmp1 = list_to_df(tmp1)
                        mid_df = pd.concat([mid_df,tmp1],axis=1)
                    except:
                        pass
            pubQualification_df = pd.concat([pubQualification_df,mid_df],axis=0)
    except:
        pass

    if len(pubQualification_df)<1:
        pubQualification_df = pd.DataFrame({"PF07AQ01":np.nan,
                                            "PF07AQ02":np.nan,
                                            "PF07AD01":np.nan,
                                            "PF07AD02":np.nan,
                                            "PF07AR01":np.nan,
                                            "PF07AR02":np.nan,
                                            "PF07AR03":np.nan,
                                            "PF07ZS01":np.nan,
                                            },index=[0])
                                                                                                    
    columns_chinese = {"PF07AQ01":"执业资格名称",
                        "PF07AQ02":"颁发机构",
                        "PF07AD01":"等级",
                        "PF07AD02":"机构所在地",
                        "PF07AR01":"获得年月",
                        "PF07AR02":"到期年月",
                        "PF07AR03":"吊销年月",
                        "PF07ZS01":"标注及声明个数",
                        }
                                                    
    # columns_english = {"PF07AQ01":"pub_qualification_qualification_name",
    #                     "PF07AQ02":"pub_qualification_issue_org",
    #                     "PF07AD01":"pub_qualification_grade",
    #                     "PF07AD02":"pub_qualification_org_location",
    #                     "PF07AR01":"pub_qualification_obtain_month",
    #                     "PF07AR02":"pub_qualification_expire_month",
    #                     "PF07AR03":"pub_qualification_revoke_month",
    #                     "PF07ZS01":"pub_qualification_mark_count",
    #                     }
    columns_english = {"PF07AQ01":"QualificationName",
                    "PF07AQ02":"Authority",
                    "PF07AD01":"Grade",
                    "PF07AD02":"AuthorityLocation",
                    "PF07AR01":"GrantDate",
                    "PF07AR02":"ExpiryDate",
                    "PF07AR03":"RevocationDate",
                    "PF07ZS01":"PubQualificationMarkCount",
                    }
    
    
    column_list = ["PF07AQ01",
                    "PF07AQ02",
                    "PF07AD01",
                    "PF07AD02",
                    "PF07AR01",
                    "PF07AR02",
                    "PF07AR03",
                    "PF07ZS01",
                    ]
                        
    for i in column_list:
        if i not in list(pubQualification_df.columns):
            pubQualification_df[i] = np.nan
    
    pubQualification_df = pubQualification_df[column_list]
    if column_type == 'CNH':
        pubQualification_df.rename(columns = columns_chinese,inplace=True)
    else:
        pubQualification_df.rename(columns = columns_english,inplace=True)
    return pubQualification_df

#%%
###行政奖励记录信息
def pubAdminReward(temp1,column_type = 'CNH'):
    pubAdminReward_df = pd.DataFrame()

    try:
        tmp = temp1['Document']['PAH']['PF08']
        for n in range(len(tmp)):
            mid_df = pd.DataFrame()
            for j in ['PF08A','PF08Z']:
                if j in ['PF08A','PF08Z']:
                    try:
                        tmp1 = tmp[n][j]
                        tmp1 = list_to_df(tmp1)
                        mid_df = pd.concat([mid_df,tmp1],axis=1)
                    except:
                        pass
            pubAdminReward_df = pd.concat([pubAdminReward_df,mid_df],axis=0)
    except:
        pass

    if len(pubAdminReward_df)<1:
        pubAdminReward_df = pd.DataFrame({"PF08AQ01":np.nan,
                                        "PF08AQ02":np.nan,
                                        "PF08AR01":np.nan,
                                        "PF08AR02":np.nan,
                                        "PF08ZS01":np.nan,
                                        },index=[0])
                                                                                                    
    columns_chinese = {"PF08AQ01":"奖励机构",
                        "PF08AQ02":"奖励内容",
                        "PF08AR01":"生效年月",
                        "PF08AR02":"截止年月",
                        "PF08ZS01":"标注及声明个数",
                        }
                                                    
    columns_english = {"PF08AQ01":"AwardAuthority",
                        "PF08AQ02":"AwardContent",
                        "PF08AR01":"EffectiveDate",
                        "PF08AR02":"ExpiryDate",
                        "PF08ZS01":"RewardMarkCount",
                        }
    
    
    column_list = ["PF08AQ01",
                    "PF08AQ02",
                    "PF08AR01",
                    "PF08AR02",
                    "PF08ZS01",
                    ]
                        
    for i in column_list:
        if i not in list(pubAdminReward_df.columns):
            pubAdminReward_df[i] = np.nan
    
    pubAdminReward_df = pubAdminReward_df[column_list]
    if column_type == 'CNH':
        pubAdminReward_df.rename(columns = columns_chinese,inplace=True)
    else:
        pubAdminReward_df.rename(columns = columns_english,inplace=True)
    return pubAdminReward_df

#%%
###行政奖励记录信息-标注及声明信息段
def pubAdminRewardMark(temp1,column_type = 'CNH'):
    pubAdminRewardMark_df = pd.DataFrame()

    try:
        tmp = temp1['Document']['PAH']['PF08']['PF08Z']['PF08ZH']
        for n in range(len(tmp)):
            mid_df = pd.DataFrame()
            try:
                tmp1 = tmp[n]
                tmp1 = list_to_df(tmp1)
                mid_df = pd.concat([mid_df,tmp1],axis=1)
            except:
                pass
            pubAdminRewardMark_df = pd.concat([rhId_df,mid_df],axis=0)
    except:
        pass

    if len(pubAdminRewardMark_df)<1:
        pubAdminRewardMark_df = pd.DataFrame({"PF08ZD01":np.nan,
                                "PF08ZQ01":np.nan,
                                "PF08ZR01":np.nan,
                                },index=[0])
                                                                                                    
    columns_chinese = {"PF08ZD01":"标注及声明类型",
                        "PF08ZQ01":"标注或声明内容",
                       "PF08ZR01":"添加日期",
                        }
                                                    
    columns_english = {"PF08ZD01":"CalloutType",
                        "PF08ZQ01":"CalloutContent",
                       "PF08ZR01":"AddDate",
                        }
    
    column_list = ["PF08ZD01",
                    "PF08ZQ01",
                   "PF08ZR01",
                    ]


                        
    for i in column_list:
        if i not in list(pubAdminRewardMark_df.columns):
            pubAdminRewardMark_df[i] = np.nan
    
    pubAdminRewardMark_df = pubAdminRewardMark_df[column_list]
    if column_type == 'CNH':
        pubAdminRewardMark_df.rename(columns = columns_chinese,inplace=True)
    else:
        pubAdminRewardMark_df.rename(columns = columns_english,inplace=True)
    return pubAdminRewardMark_df

#%%
###查询记录
def inquiryRecord(temp1,column_type = 'CNH'):
    inquiryRecord_df = pd.DataFrame()

    try:
        tmp = temp1['Document']['POQ']['PH01']
        for n in range(len(tmp)):
            mid_df = pd.DataFrame()
            try:
                tmp1 = tmp[n]
                tmp1 = list_to_df(tmp1)
                mid_df = pd.concat([mid_df,tmp1],axis=1)
            except:
                pass
            inquiryRecord_df = pd.concat([inquiryRecord_df,mid_df],axis=0)
    except:
        pass

    if len(inquiryRecord_df)<1:
        inquiryRecord_df = pd.DataFrame({"PH010R01":np.nan,
                                        "PH010D01":np.nan,
                                        "PH010Q02":np.nan,
                                        "PH010Q03":np.nan,
                                        },index=[0])
                                                                                                    
    columns_chinese = {"PH010R01":"查询日期",
                        "PH010D01":"查询机构类型",
                        "PH010Q02":"查询机构",
                        "PH010Q03":"查询原因",
                        }
                                                    
    # columns_english = {"PH010R01":"inquiry_record_inquiry_date",
    #                     "PH010D01":"inquiry_record_inquiry_org_type",
    #                     "PH010Q02":"inquiry_record_inquiry_org",
    #                     "PH010Q03":"inquiry_record_inquiry_reason",
    #                     }
    
    columns_english = {"PH010R01":"QueryDate",
                    "PH010D01":"InquiryRecordInquiryOrgType",
                    "PH010Q02":"QueryInstitution",
                    "PH010Q03":"QueryReason",
                    }
    
    column_list = ["PH010R01",
                    "PH010D01",
                    "PH010Q02",
                    "PH010Q03",
                    ]
                        
    for i in column_list:
        if i not in list(inquiryRecord_df.columns):
            inquiryRecord_df[i] = np.nan
    
    inquiryRecord_df = inquiryRecord_df[column_list]
    if column_type == 'CNH':
        inquiryRecord_df.rename(columns = columns_chinese,inplace=True)
    else:
        inquiryRecord_df.rename(columns = columns_english,inplace=True)
    return inquiryRecord_df

#%%
###标注及声明信息
def otherMarkDeclaration(temp1,column_type = 'CNH'):
    otherMarkDeclaration_df = pd.DataFrame()

    try:
        tmp = temp1['Document']['POS']['PG01']
        for n in range(len(tmp)):
            mid_df = pd.DataFrame()
            try:
                tmp1 = tmp[n]
                tmp1 = list_to_df(tmp1)
                mid_df = pd.concat([mid_df,tmp1],axis=1)
            except:
                pass
            otherMarkDeclaration_df = pd.concat([otherMarkDeclaration_df,mid_df],axis=0)
    except:
        pass

    if len(otherMarkDeclaration_df)<1:
        otherMarkDeclaration_df = pd.DataFrame({"PG010D01":np.nan,
                                                "PG010D02":np.nan,
                                                "PG010S01":np.nan,
                                                },index=[0])
                                                                                                    
    columns_chinese = {"PG010D01":"对象类型",
                        "PG010D02":"对象标识",
                        "PG010S01":"标注及声明类型个数",
                        }
                                                    
    columns_english = {"PG010D01":"other_mark_declaration_object_type",
                        "PG010D02":"other_mark_declaration_object_flag",
                        "PG010S01":"other_mark_declaration_mark_type_count",
                        }
    
    column_list = ["PG010D01",
                    "PG010D02",
                    "PG010S01",
                    ]


                        
    for i in column_list:
        if i not in list(otherMarkDeclaration_df.columns):
            otherMarkDeclaration_df[i] = np.nan
    
    otherMarkDeclaration_df = otherMarkDeclaration_df[column_list]
    if column_type == 'CNH':
        otherMarkDeclaration_df.rename(columns = columns_chinese,inplace=True)
    else:
        otherMarkDeclaration_df.rename(columns = columns_english,inplace=True)
    return otherMarkDeclaration_df

#%%
###证件信息
def rhId(temp1,column_type = 'CNH'):
    rhId_df = pd.DataFrame()
    try:
        tmp = temp1['Document']['PRH']['PA01']['PA01C']
        # 检查 PA01CH 是否存在
        if 'PA01CH' in tmp:
            pa01ch_data = tmp['PA01CH']

            # 根据 PA01CH 的类型进行不同处理
            if isinstance(pa01ch_data, list):
                # 如果是列表，则遍历每个字典并转换为 DataFrame
                for item in pa01ch_data:
                    df_item = pd.DataFrame([item])
                    rhId_df = pd.concat([rhId_df, df_item], ignore_index=True)
            elif isinstance(pa01ch_data, dict):
                # 如果是单个字典，直接转换为 DataFrame
                df_pa01ch = pd.DataFrame([pa01ch_data])
                rhId_df = pd.concat([rhId_df, df_pa01ch], ignore_index=True)
            else:
                pass
    except:
        pass

    if len(rhId_df)<1:
        rhId_df = pd.DataFrame({"PA01CD01":np.nan,
                                "PA01CI01":np.nan,
                                },index=[0])
                                                                                                    
    columns_chinese = {"PA01CD01":"证件类型",
                        "PA01CI01":"证件号码",
                        }
                                                    
    # columns_english = {"PA01CD01":"rh_id_id_type",
    #                     "PA01CI01":"rh_id_id_num",
    #                     }
    columns_english = {"PA01CD01":"OtherIDType",
                    "PA01CI01":"OtherIDNumber",
                    }
    
    column_list = ["PA01CD01",
                    "PA01CI01",
                    ]


                        
    for i in column_list:
        if i not in list(rhId_df.columns):
            rhId_df[i] = np.nan
    
    rhId_df = rhId_df[column_list]
    if column_type == 'CNH':
        rhId_df.rename(columns = columns_chinese,inplace=True)
    else:
        rhId_df.rename(columns = columns_english,inplace=True)
    return rhId_df
