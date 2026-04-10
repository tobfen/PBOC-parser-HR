# -*- coding: utf-8 -*-
"""
"""
import sys
import pandas as pd
import numpy as np
import datetime as dt
import os

path = sys.argv[1]
# path = r'C:\Users\tobfe\Documents\codespace\parseZx\xml'
os.chdir(path)

#===报告头===
df_ReportHeaderInformation = pd.read_csv('PCR2_ReportHeaderInformation.csv', low_memory=False)
df_ReportHeaderInformation['ReportTime'] = pd.to_datetime(df_ReportHeaderInformation['ReportTime'])
df_ReportHeaderInformation['ReportDate'] = pd.to_datetime(df_ReportHeaderInformation.ReportTime.dt.date)
report_dates = df_ReportHeaderInformation[['PCRID','ReportDate']]

#===防欺诈警示===
df_ReportheaderAntiFraudWarning = pd.read_csv('PCR2_ReportheaderAntiFraudWarning.csv', low_memory=False)
df_ReportheaderAntiFraudWarning['SID'] = df_ReportheaderAntiFraudWarning.groupby('PCRID')[['EffecgtiveDate']].rank(ascending=False,method='first')


#===个人基本信息===
df_IdentifiableInformation = pd.read_csv('PCR2_IdentifiableInformation.csv', low_memory=False)
df_IdentifiableInformation['PCRID2'] = df_IdentifiableInformation['PCRID']
df_IdentifiableInformation.DateOfBirth = pd.to_datetime(df_IdentifiableInformation.DateOfBirth)
df_IdentifiableInformation.loc[df_IdentifiableInformation.DateOfBirth<dt.datetime(1920,1,1,0,0,0),'DateOfBirth'] = pd.NaT

df_IdentifiableInformation = pd.merge(df_IdentifiableInformation,report_dates,how='left',on='PCRID')
df_IdentifiableInformation['DaySinceBirth'] = \
    (df_IdentifiableInformation.ReportDate - df_IdentifiableInformation.DateOfBirth)/np.timedelta64(1,'D')
df_IdentifiableInformation['Age'] = np.floor(df_IdentifiableInformation['DaySinceBirth']/365)

df_IdentifiableInformation.Gender = df_IdentifiableInformation.Gender.replace('--',np.nan)
df_IdentifiableInformation.MaritalStatus = df_IdentifiableInformation.MaritalStatus.replace('--',np.nan)
df_IdentifiableInformation.EducationLevel = df_IdentifiableInformation.EducationLevel.replace('--',np.nan)
df_IdentifiableInformation.EducationDegree = df_IdentifiableInformation.EducationDegree.replace('--',np.nan)
df_IdentifiableInformation.EmploymentStatus = df_IdentifiableInformation.EmploymentStatus.replace('--',np.nan)

#===手机号码===
df_PhoneInformation = pd.read_csv('PCR2_PhoneInformation.csv', low_memory=False, dtype={'PhoneNo':str})
df_PhoneInformation.UpdateDate = pd.to_datetime(df_PhoneInformation.UpdateDate)
df_PhoneInformation.loc[df_PhoneInformation.UpdateDate<dt.datetime(1920,1,1,0,0,0),'UpdateDate'] = pd.NaT

df_PhoneInformation.PhoneNo = df_PhoneInformation.PhoneNo.astype(str)
df_PhoneInformation.loc[df_PhoneInformation.PhoneNo.str.len()<11,'PhoneNo'] = np.nan
df_PhoneInformation.loc[df_PhoneInformation.PhoneNo.notnull(),'PhoneNo'] = \
    df_PhoneInformation.loc[df_PhoneInformation.PhoneNo.notnull(),'PhoneNo'].apply(lambda x:x[-11:])

df_PhoneInformation = pd.merge(df_PhoneInformation,report_dates,how='left',on='PCRID')
df_PhoneInformation['DaySinceUpdate'] = \
    (df_PhoneInformation.ReportDate - df_PhoneInformation.UpdateDate)/np.timedelta64(1,'D')

#===居住信息===
df_LivingInformation = pd.read_csv('PCR2_LivingInformation.csv', low_memory=False)
df_LivingInformation.LivingSituation = df_LivingInformation.LivingSituation.replace('--',np.nan)
df_LivingInformation.UpdateDate = pd.to_datetime(df_LivingInformation.UpdateDate)
df_LivingInformation.loc[df_LivingInformation.UpdateDate<dt.datetime(1920,1,1,0,0,0),'UpdateDate'] = pd.NaT
df_LivingInformation['SerialNumber'] = df_LivingInformation.groupby('PCRID')[['UpdateDate']].rank(ascending=False,method='first')

df_LivingInformation = pd.merge(df_LivingInformation,report_dates,how='left',on='PCRID')
df_LivingInformation['DaySinceUpdate'] = \
    (df_LivingInformation.ReportDate - df_LivingInformation.UpdateDate)/np.timedelta64(1,'D')
df_LivingInformation['UpdateRank'] = \
    df_LivingInformation.groupby('PCRID').DaySinceUpdate.rank(method='min')
df_LivingInformation['SerialRank'] = \
    df_LivingInformation.groupby(['PCRID','UpdateRank']).SerialNumber.rank(method='min') 

#===工作信息===
df_CareeInformation = pd.read_csv('PCR2_CareeInformation.csv', low_memory=False,
                                  keep_default_na=False, na_values=['','NA','N/A','na','n/a'])
df_CareeInformation.Profession = df_CareeInformation.Profession.replace('--',np.nan)
df_CareeInformation.Industry = df_CareeInformation.Industry.replace('--',np.nan)
df_CareeInformation.Position = df_CareeInformation.Position.replace('--',np.nan)
df_CareeInformation.Title = df_CareeInformation.Title.replace('--',np.nan)
df_CareeInformation.UpdateDate = pd.to_datetime(df_CareeInformation.UpdateDate)
df_CareeInformation.loc[df_CareeInformation.UpdateDate<dt.datetime(1920,1,1,0,0,0),'UpdateDate'] = pd.NaT
df_CareeInformation['SerialNumber'] = df_CareeInformation.groupby('PCRID')[['UpdateDate']].rank(ascending=False,method='first')

df_CareeInformation = pd.merge(df_CareeInformation,report_dates,how='left',on='PCRID')
df_CareeInformation['DaySinceUpdate'] = \
   (df_CareeInformation.ReportDate - df_CareeInformation.UpdateDate)/np.timedelta64(1,'D')
df_CareeInformation['UpdateRank'] = \
  df_CareeInformation.groupby('PCRID').DaySinceUpdate.rank(method='min')
df_CareeInformation['SerialRank'] = \
   df_CareeInformation.groupby(['PCRID','UpdateRank']).SerialNumber.rank(method='min') 

#===信息概要===
df_SummaryDigitalInterpretation = pd.read_csv('PCR2_SummaryDigitalInterpretation.csv', low_memory=False)
df_SummaryDigitalInterpretation.DigitalInterpretation = df_SummaryDigitalInterpretation.DigitalInterpretation.replace('--',np.nan)
df_SummaryDigitalInterpretation.loc[df_SummaryDigitalInterpretation.DigitalInterpretation.notnull(),'DigitalInterpretation'] = \
    df_SummaryDigitalInterpretation.loc[df_SummaryDigitalInterpretation.DigitalInterpretation.notnull(),'DigitalInterpretation'].astype(int)

# df_SummaryDigitalInterpretation.RelativePosition = df_SummaryDigitalInterpretation['RelativePosition'].astype(str).str.extract('> (\d+)%')
# df_SummaryDigitalInterpretation.RelativePosition = df_SummaryDigitalInterpretation.RelativePosition.astype(float)/100
#df_SummaryDigitalInterpretation.RelativePosition = df_SummaryDigitalInterpretation.RelativePosition.astype(int)

#===信贷交易信息提示===
df_SummaryCreditTips = pd.read_csv('PCR2_SummaryCreditTips.csv', low_memory=False)
df_SummaryCreditTips.MonthOfFirstTransaction.replace('--',np.nan,inplace=True)
df_SummaryCreditTips.loc[df_SummaryCreditTips.MonthOfFirstTransaction.notnull(),'MonthOfFirstTransaction'] = \
    df_SummaryCreditTips.loc[df_SummaryCreditTips.MonthOfFirstTransaction.notnull(),'MonthOfFirstTransaction'].astype(str).str.pad(7,side='right',fillchar='0')
df_SummaryCreditTips.MonthOfFirstTransaction = pd.to_datetime(df_SummaryCreditTips.MonthOfFirstTransaction)
df_SummaryCreditTips.loc[df_SummaryCreditTips.MonthOfFirstTransaction<dt.datetime(1920,1,1,0,0,0),'MonthOfFirstTransaction'] =pd.NaT

df_SummaryCreditTips = pd.merge(df_SummaryCreditTips,report_dates,how='left',on='PCRID')
df_SummaryCreditTips['MonSinceFirstTrans'] = \
    (df_SummaryCreditTips.ReportDate.dt.year-df_SummaryCreditTips.MonthOfFirstTransaction.dt.year)*12+ \
    (df_SummaryCreditTips.ReportDate.dt.month-df_SummaryCreditTips.MonthOfFirstTransaction.dt.month)  

#===被追偿信息汇总===
df_SummaryDunningInformation = pd.read_csv('PCR2_SummaryDunningInformation.csv', low_memory=False)

#===呆账信息汇总===
df_SummaryBadDebts = pd.read_csv('PCR2_SummaryBadDebts.csv', low_memory=False)

#===逾期（透支）信息汇总===
df_SummaryOverdue = pd.read_csv('PCR2_SummaryOverdue.csv', low_memory=False)

#===信贷交易授信及负债信息概要===
df_SummaryCreditAcountInformation =  pd.read_csv('PCR2_SummaryCreditAcountInformation.csv', low_memory=False)

#===相关还款责任信息汇总===
df_SummaryReleatedRepayment = pd.read_csv('PCR2_SummaryReleatedRepayment.csv', low_memory=False)

#===公共信息概要===
df_SummaryPublicInformation = pd.read_csv('PCR2_SummaryPublicInformation.csv', low_memory=False)

#===后付费业务欠费信息汇总===
df_SummaryOverduePostpayFee = pd.read_csv('PCR2_SummaryOverduePostpayFee.csv', low_memory=False)

#===查询记录概要===
df_SummaryQueryInformation = pd.read_csv('PCR2_SummaryQueryInformation.csv', low_memory=False)

#===信贷交易明细===
df_CreditTransaction = pd.read_csv('PCR2_CreditTransaction.csv', low_memory=False,dtype={'RepaymentMethod':str,'RepaymentPeriod':str,'GuarantorType':str,'CoBorrowingFlag':str})
df_CreditTransaction.LoanIssuingDate = pd.to_datetime(df_CreditTransaction.LoanIssuingDate)
df_CreditTransaction.loc[df_CreditTransaction.LoanIssuingDate<dt.datetime(1920,1,1,0,0,0),'LoanIssuingDate'] = pd.NaT

#授信额度
df_CreditTransaction['CreditAmt'] = df_CreditTransaction.LoanAmount \
    .combine_first(df_CreditTransaction.CreditLine)

#yl===start===
creditType_Mapping = {'D1':1,'R4':2,'R1':3,'R2':4,'R3':5,'C1':6,}
managementInstituion_Mapping = {'11':'商业银行','12':'村镇银行','14':'住房储蓄银行','15':'外资银行','16':'财务公司','21':'信托公司','22':'融资租赁公司','23':'汽车金融公司','24':'消费金融公司','25':'贷款公司','26':'金融资产管理公司','31':'证券公司','41':'保险公司','51':'小额贷款公司','52':'公积金管理中心','53':'融资担保公司','99':'其他机构',}
businessType_Mapping = {'11':'个人住房商业贷款','12':'个人商用房（含商住两用）贷款','13':'个人住房公积金贷款','21':'个人汽车消费贷款','31':'个人助学贷款','32':'国家助学贷款','33':'商业助学贷款','41':'个人经营性贷款','51':'农户贷款','52':'经营性农户贷款','53':'消费性农户贷款','91':'其他个人消费贷款','99':'其他贷款','71':'准贷记卡','81':'贷记卡','82':'大额专项分期卡','61':'约定购回式证券交易','62':'股票质押式回购交易','63':'融资融券业务','64':'其他证券类融资','92':'融资租赁业务','A1':'资产处置','B1':'代偿债务',}

repaymentMethod_Mapping = {'11':'分期等额本息','12':'分期等额本金','13':'到期还本分期结息','14':'等比累进分期还款','15':'等额累进分期还款','19':'其他类型分期还款','21':'到期一次还本付息','22':'预先付息到期还本','23':'随时还','29':'其他类型非分期还款','31':'按期结息，到期还本','32':'按期结息，自由还本','33':'按期计算还本付息','39':'循环贷款下其他还款方式','90':'不区分还款方式',}
repaymentPeriod_Mapping = {'01':'日','02':'周','03':'月','04':'季','05':'半年','06':'年','07':'一次性','08':'不定期','12':'旬','13':'双周','14':'双月','99':'其他',}
guarantorType_Mapping = {'1':'质押','2':'抵押','3':'保证','4':'信用/免担保','5':'组合(含保证)','6':'组合（不含保证）','7':'农户联保','9':'其他',}
coBorrowingFlag_Mapping = {'0':'无','1':'主借款人','2':'从借款人',}
# repaymentStateWhenTransferingClaim_Mapping = {'0':'债务人即将违约时自动垫款','1':'逾期1-30天','2':'逾期31-60天','3':'逾期61-90天','4':'逾期91-120天','5':'逾期121-150天','6':'逾期151-180天','7':'逾期180天以上','9':'未知',}

currency_Mapping = {'ADP':'安道尔比塞塔',
'AED':'UAE迪拉姆',
'AFA':'阿富汗尼',
'ALL':'列克',
'AMD':'亚美尼亚达姆',
'ANG':'荷属安的列斯盾',
'AOA':'宽扎',
'ARS':'阿根廷比索',
'ATS':'先令',
'AUD':'澳大利亚元',
'AWG':'阿鲁巴盾',
'AZM':'阿塞拜疆马纳特',
'BAM':'可自由兑换标记',
'BBD':'巴巴多斯元',
'BDT':'塔卡',
'BEF':'比利时法郎',
'BGL':'列弗',
'BGN':'保加利亚列弗',
'BHD':'巴林第纳尔',
'BIF':'布隆迪法郎',
'BMD':'百慕大元',
'BND':'文莱元',
'BOB':'玻利瓦尔',
'BOV':'Mvdol',
'BRL':'巴西瑞尔',
'BSD':'巴哈马元',
'BTN':'努尔特鲁姆',
'MMK':'缅元',
'BWP':'普拉',
'BYR':'白俄罗斯卢布',
'BZD':'伯利兹元',
'CAD':'加元',
'CDF':'刚果法郎',
'CFC':'记帐法国法郎（旧）',
'CHF':'瑞士法郎',
'CLF':'发展单位',
'CLP':'智利比索',
'CNY':'人民币元',
'COP':'哥伦比亚比索',
'CPS':'记帐英镑（旧）',
'CRC':'哥斯达黎加科朗',
'CUP':'古巴比索',
'CSF':'记帐瑞士法郎（旧）',
'CZK':'捷克克朗',
'CUR':'清算卢布（旧）',
'CUS':'记帐美元（旧）',
'CVE':'佛得角埃斯库多',
'CYP':'塞浦路斯镑',
'DEM':'德国马克',
'DJF':'即菩提法郎',
'DKK':'丹麦克朗',
'DOP':'多米尼加比索',
'DZD':'阿尔及利亚第纳尔',
'EEK':'克罗姆',
'EGP':'埃及镑',
'ERN':'纳克法',
'ESP':'西班牙比塞塔',
'ETB':'埃塞俄比亚比尔',
'EUR':'欧元',
'FIM':'马克',
'FJD':'斐济元',
'FKP':'福克兰群岛镑',
'FRF':'法国法郎',
'GBP':'英镑',
'GEL':'拉里',
'GHC':'赛地',
'GIP':'直布罗陀镑',
'GMD':'达拉西',
'GNF':'几内亚法郎',
'GRD':'德拉克马',
'GTQ':'格查尔',
'GWP':'几内亚比绍比索',
'GWD':'圭亚那元',
'HKD':'香港元',
'HNL':'伦皮拉',
'HRK':'克罗地亚库纳',
'HTG':'古德',
'HUF':'福林',
'IDR':'卢比',
'IEP':'爱尔兰镑',
'ILS':'新谢克尔',
'INR':'印度卢比',
'IQD':'伊拉克第纳尔',
'IRR':'伊朗里亚尔',
'ISK':'冰岛克朗',
'ITL':'意大利里拉',
'JMD':'牙买加元',
'JOD':'约旦第纳尔',
'JPY':'日元',
'KES':'肯尼亚先令',
'KGS':'索姆',
'KHR':'瑞尔',
'KMF':'科摩罗法郎',
'KPW':'北朝鲜圆',
'KRW':'圆',
'KWD':'科威特第纳尔',
'KYD':'开曼群岛元',
'KZT':'坚戈',
'LAK':'基普',
'LBP':'黎巴嫩镑',
'LKR':'斯里兰卡卢比',
'LRD':'利比里亚元',
'LSL':'罗提',
'LTL':'立陶宛',
'LUF':'卢森堡法郎',
'LVL':'拉脱维亚拉特',
'LYD':'利比亚第纳尔',
'MAD':'摩洛哥迪拉姆',
'MDL':'摩尔瓦多列伊',
'MGF':'马尔加什法郎',
'MKD':'第纳尔',
'MLF':'马里法郎（旧）',
'MNT':'图格里克',
'MOP':'澳门元',
'MRO':'乌吉亚',
'MTL':'马尔他里拉',
'MUR':'毛里求斯卢比',
'MVR':'卢菲亚',
'MWK':'克瓦查',
'MXP':'墨西哥比索（旧）',
'MXN':'墨西哥比索',
'MXV':'墨西哥发展单位',
'MYR':'马来西亚林吉特',
'MZM':'麦梯卡尔',
'NAD':'纳米比亚元',
'NGN':'奈拉',
'NIO':'金科多巴',
'NLG':'荷兰盾',
'NOK':'挪威克朗',
'NPR':'尼泊尔卢比',
'NZD':'新西兰元',
'OMR':'阿曼里亚尔',
'PAB':'巴波亚',
'PEN':'索尔',
'PGK':'基那',
'PHP':'菲律宾比索',
'PKR':'巴基斯坦卢比',
'PLZ':'波兰兹罗提（旧）',
'PLN':'兹罗提',
'PTE':'葡萄牙埃斯库多',
'PYG':'瓜拉尼',
'QAR':'卡塔尔里亚尔',
'ROL':'列伊',
'RUB':'俄罗斯卢布',
'RUR':'俄罗斯卢布',
'RWF':'卢旺达法郎',
'SAR':'沙特里亚尔',
'SBD':'所罗门群岛元',
'SCR':'塞舌尔卢比',
'SDD':'苏丹第纳尔',
'SDP':'苏丹镑（旧）',
'SEK':'瑞典克朗',
'SGD':'新加坡元',
'SHP':'圣赫勒拿镑',
'SIT':'托拉尔',
'SKK':'斯洛伐克克朗',
'SLL':'利昂',
'SOS':'索马里先令',
'SRG':'苏里南盾',
'STD':'多布拉',
'SVC':'萨尔瓦多科朗',
'SYP':'叙利亚镑',
'SZL':'里兰吉尼',
'THB':'铢',
'TJS':'索莫尼',
'TMM':'马纳特',
'TND':'突尼斯第纳尔',
'TOP':'邦加',
'TPE':'东帝汶埃斯库多',
'TRL':'土耳其里拉',
'TTD':'特立尼达和多巴哥元',
'TWD':'新台湾元',
'TZS':'坦桑尼亚先令',
'UAH':'格里夫纳',
'UDM':'蒙古美元（旧）',
'UGX':'乌干达先令',
'USD':'美元',
'UYU':'乌拉圭比索',
'UZS':'乌兹别克斯坦苏姆',
'VND':'盾',
'VUV':'瓦图',
'WST':'塔拉',
'XAF':'中非法郎',
'XAG':'银',
'XAU':'黄金',
'XBA':'欧洲货币合成单位',
'XBB':'欧洲货币单位(E.M.U.-6)',
'XBC':'欧洲账户9单位',
'XBD':'欧洲账户17单位',
'XCD':'东加勒比元',
'XDR':'特别提款权',
'XFO':'黄金法郎',
'XFU':'UIC法郎',
'XOF':'CFA法郎BCEAO',
'XPF':'CFP法郎',
'YER':'也门里亚尔',
'YUM':'南斯拉夫第纳尔',
'ZAR':'兰特',
'ZMK':'克瓦查',
'ZWD':'津巴布韦元',}

df_CreditTransaction['CreditType'] = df_CreditTransaction['CreditType'].astype(str).map(creditType_Mapping)
df_CreditTransaction['ManagementInstituion'] = df_CreditTransaction['ManagementInstituion'].astype(str).map(managementInstituion_Mapping) + '"' + df_CreditTransaction['ManageOrgCode']+ '"'
df_CreditTransaction['BusinessType'] = df_CreditTransaction['BusinessType'].astype(str).map(businessType_Mapping)
df_CreditTransaction['RepaymentMethod'] = df_CreditTransaction['RepaymentMethod'].map(repaymentMethod_Mapping)
df_CreditTransaction['RepaymentPeriod'] = df_CreditTransaction['RepaymentPeriod'].map(repaymentPeriod_Mapping)
df_CreditTransaction['GuarantorType'] = df_CreditTransaction['GuarantorType'].map(guarantorType_Mapping)
df_CreditTransaction['CoBorrowingFlag'] = df_CreditTransaction['CoBorrowingFlag'].map(coBorrowingFlag_Mapping)
# df_CreditTransaction['RepaymentStateWhenTransferingClaim'] = df_CreditTransaction['RepaymentStateWhenTransferingClaim'].map(repaymentStateWhenTransferingClaim_Mapping)
df_CreditTransaction['Currency'] = df_CreditTransaction['Currency'].map(currency_Mapping)
#yl===end===

#-------信贷账户交易信息扩展
df_CreditTransactionExtra = pd.read_csv('PCR2_CreditTransactionExtra.csv', low_memory=False,dtype={'AccountState':str,'FiveLoanGradesOfRecord1':str,'FiveLoanGradesOfRecord2':str})
# df_CreditTransactionExtra.AccountState.fillna(1,inplace=True)
# df_CreditTransactionExtra.Record1Description.fillna("missing",inplace=True)
df_CreditTransactionExtra.LastPaymentDate = pd.to_datetime(df_CreditTransactionExtra.LastPaymentDate)
df_CreditTransactionExtra.Record2RepaymentDate = pd.to_datetime(df_CreditTransactionExtra.Record2RepaymentDate)
df_CreditTransactionExtra.AccountClosingDate = pd.to_datetime(df_CreditTransactionExtra.AccountClosingDate)

#===yl start===
type_D1_1 = {'1':'正常','2':'逾期','3':'结清','4':'呆账','5':'转出','6':'担保物不足','7':'强制平仓','8':'司法追偿'}
type_R4_2 = {'1':'正常','2':'逾期','3':'结清','4':'呆账','6':'担保物不足','8':'司法追偿',}
type_R1_3 = {'1':'正常','2':'逾期','3':'结清','4':'呆账','5':'银行止付','6':'担保物不足','8':'司法追偿',}
type_R2_4_R3_5 = {'1':'正常','2':'冻结','3':'止付','31':'银行止付','4':'销户','5':'呆账','6':'未激活','8':'司法追偿',}
type_C1_6 = {'1':'催收','2':'结束',}
five_class = {'1':'正常','2':'关注','3':'次级','4':'可疑','5':'损失','9':'未分类',}
df_CreditTransactionExtra.loc[df_CreditTransactionExtra.CreditType=='D1','AccountState'] = df_CreditTransactionExtra.loc[df_CreditTransactionExtra.CreditType=='D1','AccountState'].map(type_D1_1)
df_CreditTransactionExtra.loc[df_CreditTransactionExtra.CreditType=='R4','AccountState'] = df_CreditTransactionExtra.loc[df_CreditTransactionExtra.CreditType=='R4','AccountState'].map(type_R4_2)
df_CreditTransactionExtra.loc[df_CreditTransactionExtra.CreditType=='R1','AccountState'] = df_CreditTransactionExtra.loc[df_CreditTransactionExtra.CreditType=='R1','AccountState'].map(type_D1_1)
df_CreditTransactionExtra.loc[df_CreditTransactionExtra.CreditType.isin(['R2','R3']),'AccountState'] = df_CreditTransactionExtra.loc[df_CreditTransactionExtra.CreditType.isin(['R2','R3']),'AccountState'].map(type_R2_4_R3_5)
df_CreditTransactionExtra.loc[df_CreditTransactionExtra.CreditType=='C1','AccountState'] = df_CreditTransactionExtra.loc[df_CreditTransactionExtra.CreditType=='C1','AccountState'].map(type_C1_6)
df_CreditTransactionExtra['FiveLoanGradesOfRecord1'] = df_CreditTransactionExtra['FiveLoanGradesOfRecord1'].map(five_class)
df_CreditTransactionExtra['FiveLoanGradesOfRecord2'] = df_CreditTransactionExtra['FiveLoanGradesOfRecord2'].map(five_class)
#===yl end===

#90+未还本金
df_CreditTransactionExtra['OverduePrincipal90Plus'] = \
    df_CreditTransactionExtra[['OverduePrincipal91To180Days','OverduePrincipalMoreThan180Days']].sum(axis=1,min_count=1)
#五级分类
df_CreditTransactionExtra['LoanGrade'] = df_CreditTransactionExtra.FiveLoanGradesOfRecord2 \
    .combine_first(df_CreditTransactionExtra.FiveLoanGradesOfRecord1)
#账户状态
df_CreditTransactionExtra['AcctStatus'] = df_CreditTransactionExtra['AccountState']
# df_CreditTransactionExtra.loc[df_CreditTransactionExtra.Record1Description.str.contains('未激活'),'AcctStatus'] = '未激活'

#余额
df_CreditTransactionExtra['Bal'] = df_CreditTransactionExtra.Record2Balance \
    .combine_first(df_CreditTransactionExtra.Record1Balance) \
    .combine_first(df_CreditTransactionExtra.UsedAmount)    
#最近一次还款时间
df_CreditTransactionExtra['LastPmtDate'] = df_CreditTransactionExtra.Record2RepaymentDate \
    .combine_first(df_CreditTransactionExtra.LastPaymentDate) \
    .combine_first(df_CreditTransactionExtra.AccountClosingDate)
df_CreditTransactionExtra['LastPmtDateCard'] = df_CreditTransactionExtra.Record2RepaymentDate \
    .combine_first(df_CreditTransactionExtra.LastPaymentDate) 

#-------
#拼表
df_CreditTransJoined = pd.merge(df_CreditTransaction,df_CreditTransactionExtra.drop(['PCRID','CreditType'],axis=1), how='left',on='SID')

df_CreditTransJoined  = pd.merge(df_CreditTransJoined,report_dates,how='left',on='PCRID')

del df_CreditTransaction
del df_CreditTransactionExtra

#当前额度使用率
ratio = df_CreditTransJoined.UsedAmount.fillna(0)/df_CreditTransJoined.CreditLine
df_CreditTransJoined['UsageRate'] = np.round(ratio.replace(np.inf, np.nan),3)
#近6个月平均额度使用率
ratio = df_CreditTransJoined.AverageUtilizationInLast6Month.fillna(0)/df_CreditTransJoined.CreditLine
df_CreditTransJoined['Avg6mUsageRate'] = np.round(ratio.replace(np.inf, np.nan),3)
#本月还款比例
ratio = df_CreditTransJoined.PaymentAmountOfThisMonth.fillna(0)/df_CreditTransJoined.PayableAmountOfThisMonth
df_CreditTransJoined['PaymentRatio'] = np.round(ratio.replace(np.inf, np.nan),3)
#余额占授信比例
ratio = df_CreditTransJoined.Bal.fillna(0)/df_CreditTransJoined.CreditAmt
df_CreditTransJoined['BalProp'] = np.round(ratio.replace(np.inf, np.nan),3)

#开立时间距今天数
df_CreditTransJoined['DaySinceOpen'] = \
    (df_CreditTransJoined.ReportDate - df_CreditTransJoined.LoanIssuingDate)/np.timedelta64(1,'D')
#开立时间距今月份数 
df_CreditTransJoined['MonSinceOpen'] = \
    (df_CreditTransJoined.ReportDate.dt.year - df_CreditTransJoined.LoanIssuingDate.dt.year)*12+ \
    (df_CreditTransJoined.ReportDate.dt.month - df_CreditTransJoined.LoanIssuingDate.dt.month)
      
    
#最近一次还款时间距今月份数
df_CreditTransJoined['MonSinceLastPmt'] = \
    (df_CreditTransJoined.ReportDate.dt.year - df_CreditTransJoined.LastPmtDate.dt.year)*12+ \
    (df_CreditTransJoined.ReportDate.dt.month - df_CreditTransJoined.LastPmtDate.dt.month)
df_CreditTransJoined['MonSinceLastPmtCard'] = \
    (df_CreditTransJoined.ReportDate.dt.year - df_CreditTransJoined.LastPmtDateCard.dt.year)*12+ \
    (df_CreditTransJoined.ReportDate.dt.month - df_CreditTransJoined.LastPmtDateCard.dt.month)
#在册时间止
df_CreditTransJoined['LoanEndDate'] = df_CreditTransJoined.AccountClosingDate \
    .combine_first(df_CreditTransJoined.ReportDate) 
df_CreditTransJoined.loc[(df_CreditTransJoined.AcctStatus=='转出'),'LoanEndDate'] = pd.NaT
#在册天数
df_CreditTransJoined['LoanLife'] = \
    (df_CreditTransJoined.LoanEndDate - df_CreditTransJoined.LoanIssuingDate)/np.timedelta64(1,'D')
df_CreditTransJoined['AccountNumber'] = df_CreditTransJoined['AccountNumber'].astype(str)

#各种子类
loan_and_credit_card_ids =  df_CreditTransJoined[df_CreditTransJoined.CreditType.isin([1,2,3,4,5])].SID
loan_ids = df_CreditTransJoined[df_CreditTransJoined.CreditType.isin([1,2,3])].SID
card_ids = df_CreditTransJoined[df_CreditTransJoined.CreditType==4].SID
semicard_ids = df_CreditTransJoined[df_CreditTransJoined.CreditType==5].SID

unsettled_loan_ids = df_CreditTransJoined[df_CreditTransJoined.CreditType.isin([1,2,3]) & ~df_CreditTransJoined.AccountState.isin(['结清'])].SID
unclosed_credit_card_ids = df_CreditTransJoined[df_CreditTransJoined.CreditType.isin([4,5]) & ~df_CreditTransJoined.AccountState.isin(['销户','未激活']) ].SID
unclosed_credit_card_accountnumbers = df_CreditTransJoined[df_CreditTransJoined.CreditType.isin([4,5]) & ~df_CreditTransJoined.AccountState.isin(['销户','未激活']) ].AccountNumber


nonrev_loan_ids = df_CreditTransJoined[df_CreditTransJoined.CreditType==1].SID
revsep_loan_ids = df_CreditTransJoined[df_CreditTransJoined.CreditType==2].SID
rev_loan_ids = df_CreditTransJoined[df_CreditTransJoined.CreditType==3].SID

bank_loan_ids = df_CreditTransJoined[df_CreditTransJoined.ManagementInstituion.astype(str).str.contains('银行') & df_CreditTransJoined.CreditType.isin([1,2,3])].SID
nonbank_loan_ids = df_CreditTransJoined[(~df_CreditTransJoined.ManagementInstituion.astype(str).str.contains('银行')) & df_CreditTransJoined.CreditType.isin([1,2,3])].SID
finlease_loan_ids = df_CreditTransJoined[df_CreditTransJoined.ManagementInstituion.astype(str).str.contains('融资租赁公司') & df_CreditTransJoined.CreditType.isin([1,2,3])].SID
autofin_loan_ids = df_CreditTransJoined[df_CreditTransJoined.ManagementInstituion.astype(str).str.contains('汽车金融') & df_CreditTransJoined.CreditType.isin([1,2,3])].SID
consumerfin_loan_ids = df_CreditTransJoined[df_CreditTransJoined.ManagementInstituion.astype(str).str.contains('消费金融公司') & df_CreditTransJoined.CreditType.isin([1,2,3])].SID
microfin_loan_ids = df_CreditTransJoined[df_CreditTransJoined.ManagementInstituion.astype(str).str.contains('小额贷款公司') & df_CreditTransJoined.CreditType.isin([1,2,3])].SID
finguar_loan_ids = df_CreditTransJoined[df_CreditTransJoined.ManagementInstituion.astype(str).str.contains('融资担保公司') & df_CreditTransJoined.CreditType.isin([1,2,3])].SID

house_loan_ids = df_CreditTransJoined[df_CreditTransJoined.BusinessType.isin(["个人住房商业贷款","个人商用房（含商住两用）贷款","个人住房公积金贷款"])].SID
car_loan_ids = df_CreditTransJoined[df_CreditTransJoined.BusinessType=="个人汽车消费贷款"].SID
student_loan_ids = df_CreditTransJoined[df_CreditTransJoined.BusinessType.isin(["个人助学贷款","国家助学贷款","商业助学贷款"])].SID
business_loan_ids = df_CreditTransJoined[df_CreditTransJoined.BusinessType=="个人经营性贷款"].SID
farmer_loan_ids =  df_CreditTransJoined[df_CreditTransJoined.BusinessType.isin( ["农户贷款","经营性农户贷款","消费性农户贷款"])].SID
consumer_loan_ids = df_CreditTransJoined[df_CreditTransJoined.BusinessType=="其他个人消费贷款"].SID

credit_loan_ids = df_CreditTransJoined[(df_CreditTransJoined.GuarantorType=="信用/免担保") & df_CreditTransJoined.CreditType.isin([1,2,3])].SID
coll_loan_ids = df_CreditTransJoined[(df_CreditTransJoined.GuarantorType.isin(["质押","抵押"])) & df_CreditTransJoined.CreditType.isin([1,2,3])].SID
guar_loan_ids = df_CreditTransJoined[(df_CreditTransJoined.GuarantorType=='保证') & df_CreditTransJoined.CreditType.isin([1,2,3])].SID
secured_loan_ids = df_CreditTransJoined[(df_CreditTransJoined.GuarantorType!="信用/免担保") & df_CreditTransJoined.CreditType.isin([1,2,3])].SID

#---还款记录---
my_header = ['SID', 'PSID', 'RepaymentYear', 'PaymentRecordType', 'Month1', 'Month2',
       'Month3', 'Month4', 'Month5', 'Month6', 'Month7', 'Month8', 'Month9',
       'Month10', 'Month11', 'Month12']
df_PmtRecordOriginal = pd.read_csv('PCR2_CreditPaymentRecord.csv', low_memory=False)
mapping_dict = {('Month'+str(i)):i for i in range(1,13)}

df_PmtRecord1 = pd.melt(df_PmtRecordOriginal[df_PmtRecordOriginal.PaymentRecordType==1] , id_vars =['PSID','RepaymentYear'],
                        value_vars=mapping_dict.keys(),var_name ='RepaymentMon',value_name='Status')
df_PmtRecord2 = pd.melt(df_PmtRecordOriginal[df_PmtRecordOriginal.PaymentRecordType==2] , id_vars =['PSID','RepaymentYear'],
                        value_vars=mapping_dict.keys(),var_name ='RepaymentMon',value_name='Amount')
df_PmtRecord = pd.merge(df_PmtRecord1,df_PmtRecord2, how='left',on=['PSID', 'RepaymentYear', 'RepaymentMon'])
df_PmtRecord = df_PmtRecord[df_PmtRecord.Status.notnull()] 

del df_PmtRecordOriginal
del df_PmtRecord1
del df_PmtRecord2

df_PmtRecord['RepaymentMon'] = df_PmtRecord['RepaymentMon'].map(mapping_dict)
df_PmtRecord['RepaymentYearMon'] = pd.to_datetime(df_PmtRecord.RepaymentYear*10000 +df_PmtRecord.RepaymentMon*100+1, format='%Y%m%d')
df_PmtRecord.sort_values(by=['PSID','RepaymentYearMon'], inplace=True)

df_PmtRecord.Amount.replace('--', np.nan, inplace=True)
# df_PmtRecord.Amount = df_PmtRecord.Amount.str.replace(',','').astype(float)
# 改进方案：分步处理 + 空值安全转换
df_PmtRecord['Amount'] = (df_PmtRecord['Amount'].astype(str).str.replace(',', '', regex=False).replace(['nan', ''], np.nan).apply(pd.to_numeric, errors='coerce'))

num2int_dict={'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7}
df_PmtRecord['StatusNew'] = df_PmtRecord.Status.replace(num2int_dict)

#准贷记卡调整
df_PmtRecord.loc[df_PmtRecord.PSID.isin(semicard_ids) & df_PmtRecord.StatusNew.isin([1,2,3,4,5,6,7]),'StatusNew'] -=2

status2num_dict = {'B':8,'D':9,'Z':10,'G':11}
df_PmtRecord['StatusNum'] = df_PmtRecord.StatusNew.replace(status2num_dict)
df_PmtRecord.loc[~df_PmtRecord.StatusNum.isin([1,2,3,4,5,6,7,8,9,10,11]),'StatusNum'] = 0
df_PmtRecord.StatusNum = df_PmtRecord.StatusNum.astype(int)

flag_dict = {'N':1,'B':2,'D':2,'Z':2,'G':2,'M':2,
             1:2,2:2,3:2,4:2,5:2,6:2,7:2}
df_PmtRecord['Flag'] = df_PmtRecord.StatusNew.map(flag_dict).fillna(0).astype(int)

df_PmtRecord['PSID'] = df_PmtRecord['PSID'].astype(str)
df_CreditTransJoined['SID'] = df_CreditTransJoined['SID'].astype(str)
df_PmtRecord = pd.merge(df_PmtRecord,df_CreditTransJoined[['SID','PCRID','CreditType']],how='left',left_on='PSID',right_on='SID')
df_PmtRecord = pd.merge(df_PmtRecord,report_dates,how='left',on='PCRID')
df_PmtRecord['MonSincePmt'] = \
    (df_PmtRecord.ReportDate.dt.year - df_PmtRecord.RepaymentYearMon.dt.year)*12+\
    (df_PmtRecord.ReportDate.dt.month - df_PmtRecord.RepaymentYearMon.dt.month)    

#连续逾期计算
df_PmtRecord['Ovd'] = (df_PmtRecord['StatusNum']>0)+0
df_PmtRecord['Ovd_shift'] = df_PmtRecord.Ovd.shift()
df_PmtRecord['PCRID_shift'] = df_PmtRecord.PCRID.shift()
df_PmtRecord['PSID_shift'] = df_PmtRecord.PSID.shift()
df_PmtRecord['group_start'] = (df_PmtRecord.Ovd!=df_PmtRecord.Ovd_shift) | \
    (df_PmtRecord.PCRID!=df_PmtRecord.PCRID_shift) | (df_PmtRecord.PSID!=df_PmtRecord.PSID_shift)
df_PmtRecord['group_id']  = df_PmtRecord.group_start.cumsum()

#曾经逾期账户
ever_ovd_ids = pd.unique(df_PmtRecord[(df_PmtRecord.Flag==2)].PSID)

#---特殊交易---
df_CreditSpecialTransaction = pd.read_csv('PCR2_CreditSpecialTransaction.csv', low_memory=False,dtype={'SpecialTransactionType':str})
df_CreditSpecialTransaction.TransactionDate = pd.to_datetime(df_CreditSpecialTransaction.TransactionDate)
specialTransactionType_Mapping = {'1':'展期','2':'担保人（第三方）代偿','3':'以资抵债','4':'提前还款','5':'提前结清','6':'强制平仓，未结清','7':'强制平仓，已结清','8':'司法追偿','9':'其他','11':'债务减免','14':'信用卡个性化分期','16':'银行主动延期','17':'强制平仓',}
df_CreditSpecialTransaction['SpecialTransactionType'] = df_CreditSpecialTransaction['SpecialTransactionType'].map(specialTransactionType_Mapping)

df_CreditSpecialTransaction['PSID'] = df_CreditSpecialTransaction['PSID'].astype(str)
df_CreditSpecialTransaction = pd.merge(df_CreditSpecialTransaction.drop("PCRID",axis=1),df_CreditTransJoined[['AccountNumber','SID','PCRID','CreditType']],how='left',left_on='PSID',right_on='AccountNumber')

df_CreditSpecialTransaction = pd.merge(df_CreditSpecialTransaction,report_dates,how='left',on='PCRID')
df_CreditSpecialTransaction['DaySinceTrans'] = \
    (df_CreditSpecialTransaction.ReportDate - df_CreditSpecialTransaction.TransactionDate)/np.timedelta64(1,'D')

#---大额专项分期---
df_LargeAmountSpecialInstalme = pd.read_csv('PCR2_LargeAmountSpecialInstalment.csv', low_memory=False)
df_LargeAmountSpecialInstalme['SID2'] = df_LargeAmountSpecialInstalme.groupby('PCRID')[['SpecialInstalmentBeginDate']].rank(ascending=False,method='first') #yl

df_LargeAmountSpecialInstalme['SID'] = df_LargeAmountSpecialInstalme['SID'].astype(str)
# df_LargeAmountSpecialInstalme = pd.merge(df_LargeAmountSpecialInstalme.drop('PCRID',axis=1),df_CreditTransJoined[df_CreditTransJoined.BusinessType=='82'][['AccountNumber','SID','PCRID','CreditType']],how='left',left_on='SID',right_on='AccountNumber')
df_LargeAmountSpecialInstalme.SpecialInstalmentEndDate = pd.to_datetime(df_LargeAmountSpecialInstalme.SpecialInstalmentEndDate)
df_LargeAmountSpecialInstalme.SpecialInstalmentBeginDate = pd.to_datetime(df_LargeAmountSpecialInstalme.SpecialInstalmentBeginDate)

#---相关还款责任明细---
df_CreditRelatedRepayment = pd.read_csv('PCR2_CreditRelatedRepayment.csv', low_memory=False,dtype={'PrimaryBorrowerFlag':str,'RelatedRepayDutyBusinessManageOrgType':str,'BusinessType':str,'CoBorrowingFlag':str,'SecuredLoanGrade':str})
df_CreditRelatedRepayment.SecuredLoanIssuingDate = pd.to_datetime(df_CreditRelatedRepayment.SecuredLoanIssuingDate)

#===yl start===
company_bus_Mapping = {'10':'企业债','11':'贷款','12':'贸易融资','13':'保理融资','14':'融资租赁','15':'证券类融资','16':'透支','21':'票据贴现','31':'黄金借贷','41':'垫款','51':'资产处置',}
coBorrowingFlag_Mapping = {'1':'共同借款人','2':'保证人','3':'票据承兑人','4':'应收账款债务人','5':'供应链中核心企业','9':'其他',}

df_CreditRelatedRepayment['RelatedRepayDutyBusinessManageOrgType'] = df_CreditRelatedRepayment['RelatedRepayDutyBusinessManageOrgType'].map(managementInstituion_Mapping)
df_CreditRelatedRepayment['SecuredLoanIssuer'] = df_CreditRelatedRepayment['RelatedRepayDutyBusinessManageOrgType'] + '&quot;' + df_CreditRelatedRepayment['SecuredLoanIssuer'] + '&quot;'
df_CreditRelatedRepayment.loc[df_CreditRelatedRepayment.PrimaryBorrowerFlag=='1','BusinessType'] = df_CreditRelatedRepayment.loc[df_CreditRelatedRepayment.PrimaryBorrowerFlag=='1','BusinessType'].map(businessType_Mapping)

df_CreditRelatedRepayment.loc[df_CreditRelatedRepayment.PrimaryBorrowerFlag=='2','BusinessType'] = df_CreditRelatedRepayment.loc[df_CreditRelatedRepayment.PrimaryBorrowerFlag=='2','BusinessType'].map(company_bus_Mapping)
df_CreditRelatedRepayment['CoBorrowingFlag'] = df_CreditRelatedRepayment['CoBorrowingFlag'].map(coBorrowingFlag_Mapping)
df_CreditRelatedRepayment['Currency'] = df_CreditRelatedRepayment['Currency'].map(currency_Mapping)
df_CreditRelatedRepayment['SecuredLoanGrade'] = df_CreditRelatedRepayment['SecuredLoanGrade'].map(five_class)
df_CreditRelatedRepayment['SID'] = df_CreditRelatedRepayment.groupby('PCRID')[['SecuredLoanIssuingDate']].rank(ascending=False,method='first')

df_CreditRelatedRepayment = pd.merge(df_CreditRelatedRepayment,report_dates,how='left',on='PCRID')
df_CreditRelatedRepayment['DaySinceOpen'] = \
    (df_CreditRelatedRepayment.ReportDate - df_CreditRelatedRepayment.SecuredLoanIssuingDate)/np.timedelta64(1,'D')
#===yl end===

#===非信贷信息明细===
df_NonCreditTransaction = pd.read_csv('PCR2_NonCreditTransaction.csv', low_memory=False,dtype={'BusinessType':str,'PaymentStatus':str})  
df_NonCreditTransaction.BusinessDate = pd.to_datetime(df_NonCreditTransaction.BusinessDate)
businessType_Mapping = {'1':'固定电话','2':'移动电话','3':'互联网接入','4':'数据专线及集群业务','5':'卫星业务','6':'组合业务','0':'其他业务',} #yl

df_NonCreditTransaction['BusinessType'] = df_NonCreditTransaction['BusinessType'].map(businessType_Mapping) #yl
df_NonCreditTransaction['SID'] = df_NonCreditTransaction.groupby('PCRID')[['BillingDate']].rank(ascending=False,method='first') #yl
paymentStatus_Mapping = {'0':'欠费','1':'正常',} #yl
df_NonCreditTransaction['PaymentStatus'] = df_NonCreditTransaction['PaymentStatus'].map(paymentStatus_Mapping) #yl
df_NonCreditTransaction = pd.merge(df_NonCreditTransaction,report_dates,how='left',on='PCRID')
df_NonCreditTransaction['DaySinceOpen'] = \
    (df_NonCreditTransaction.ReportDate - df_NonCreditTransaction.BusinessDate)/np.timedelta64(1,'D')

#===公共信息明细===
# #欠税
df_OwingTaxInformation = pd.read_csv('PCR2_OwingTaxInformation.csv', low_memory=False)
df_OwingTaxInformation.StatisticsDate = pd.to_datetime(df_OwingTaxInformation.StatisticsDate)
df_OwingTaxInformation['SID'] = df_OwingTaxInformation.groupby('PCRID')[['StatisticsDate']].rank(ascending=False,method='first') #yl

df_OwingTaxInformation = pd.merge(df_OwingTaxInformation,report_dates,how='left',on='PCRID')
df_OwingTaxInformation['DaySinceRecord'] = \
    (df_OwingTaxInformation.ReportDate - df_OwingTaxInformation.StatisticsDate)/np.timedelta64(1,'D')

#民事判决
df_CivilJudgmentRecords = pd.read_csv('PCR2_CivilJudgmentRecords.csv', low_memory=False,dtype={'ClosedMode':str})
df_CivilJudgmentRecords.RegisterDate = pd.to_datetime(df_CivilJudgmentRecords.RegisterDate)

df_CivilJudgmentRecords = pd.merge(df_CivilJudgmentRecords,report_dates,how='left',on='PCRID')
df_CivilJudgmentRecords['DaySinceRecord'] = \
    (df_CivilJudgmentRecords.ReportDate - df_CivilJudgmentRecords.RegisterDate)/np.timedelta64(1,'D')

closedMode_Mapping = {'1':'判决','2':'调解','3':'其他'}
df_CivilJudgmentRecords['ClosedMode'] = df_CivilJudgmentRecords['ClosedMode'].map(closedMode_Mapping)
df_CivilJudgmentRecords['SID'] = df_CivilJudgmentRecords.groupby('PCRID')[['RegisterDate']].rank(ascending=False,method='first') 

#强制执行
df_EnforcementRecords = pd.read_csv('PCR2_EnforcementRecords.csv', low_memory=False)
df_EnforcementRecords.RegisterDate = pd.to_datetime(df_EnforcementRecords.RegisterDate)

df_EnforcementRecords = pd.merge(df_EnforcementRecords,report_dates,how='left',on='PCRID')
df_EnforcementRecords['DaySinceRecord'] = \
    (df_EnforcementRecords.ReportDate - df_EnforcementRecords.RegisterDate)/np.timedelta64(1,'D')
df_EnforcementRecords['SID'] = df_EnforcementRecords.groupby('PCRID')[['RegisterDate']].rank(ascending=False,method='first') 


#行政处罚
df_PunishmentRecords = pd.read_csv('PCR2_PunishmentRecords.csv', low_memory=False)
df_PunishmentRecords.EffectiveDate = pd.to_datetime(df_PunishmentRecords.EffectiveDate)

df_PunishmentRecords['SID'] = df_PunishmentRecords.groupby('PCRID')[['EffectiveDate']].rank(ascending=False,method='first') 

df_PunishmentRecords = pd.merge(df_PunishmentRecords,report_dates,how='left',on='PCRID')
df_PunishmentRecords['DaySinceRecord'] = \
    (df_PunishmentRecords.ReportDate - df_PunishmentRecords.EffectiveDate)/np.timedelta64(1,'D')

#低保救助
df_LowReliefRecords =  pd.read_csv('PCR2_LowReliefRecords.csv', low_memory=False,dtype={'Category':str})
df_LowReliefRecords.ApplyDate = pd.to_datetime(df_LowReliefRecords.ApplyDate)
df_LowReliefRecords.ApproveDate = pd.to_datetime(df_LowReliefRecords.ApproveDate)

category_Mapping = {'1':'在职职工','2':'离岗','3':'失业','4':'离退休人员','5':'三无人员','6':'居民','7':'学生',}
df_LowReliefRecords['Category'] = df_LowReliefRecords['Category'].map(category_Mapping)
df_LowReliefRecords['SID'] = df_LowReliefRecords.groupby('PCRID')[['UpdateDate']].rank(ascending=False,method='first') 

df_LowReliefRecords = pd.merge(df_LowReliefRecords,report_dates,how='left',on='PCRID')
df_LowReliefRecords['DaySinceRecord'] = \
    (df_LowReliefRecords.ReportDate - df_LowReliefRecords.ApplyDate)/np.timedelta64(1,'D')

#执业资格
df_QualificationRecords = pd.read_csv('PCR2_QualificationRecords.csv', low_memory=False,dtype={'Grade':str})
df_QualificationRecords.GrantDate = pd.to_datetime(df_QualificationRecords.GrantDate)
grade_Mapping = {'1':'国家级机构或行业协会颁发的执业资格证书','2':'省市级机构或行业协会颁发的执业资格证书','3':'地市级机构或行业协会颁发的执业资格证书','4':'独立行业协会或制订行业标准的企业颁发的执业资格证书','5':'其他机构颁发的执业资格证书',}
df_QualificationRecords['Grade'] = df_QualificationRecords['Grade'].map(grade_Mapping)
df_QualificationRecords['SID'] = df_QualificationRecords.groupby('PCRID')[['GrantDate']].rank(ascending=False,method='first') 


df_QualificationRecords = pd.merge(df_QualificationRecords,report_dates,how='left',on='PCRID')
df_QualificationRecords['DaySinceRecord'] = \
    (df_QualificationRecords.ReportDate - df_QualificationRecords.GrantDate)/np.timedelta64(1,'D')

#行政奖励
df_AwardRecords = pd.read_csv('PCR2_AwardRecords.csv', low_memory=False)
df_AwardRecords.EffectiveDate = pd.to_datetime(df_AwardRecords.EffectiveDate, errors='coerce')
df_AwardRecords['SID'] = df_AwardRecords.groupby('PCRID')[['EffectiveDate']].rank(ascending=False,method='first') #yl

df_AwardRecords = pd.merge(df_AwardRecords,report_dates,how='left',on='PCRID')
df_AwardRecords['DaySinceRecord'] = \
    (df_AwardRecords.ReportDate - df_AwardRecords.EffectiveDate)/np.timedelta64(1,'D')


#公积金
df_HousingProvidentFundRecords = pd.read_csv('PCR2_HousingProvidentFundRecords.csv', low_memory=False,dtype={'IndividualRatio':str,'CompanyRatio':str,'PaymentStatus':str})
df_HousingProvidentFundRecords = pd.merge(df_HousingProvidentFundRecords,report_dates,how='left',on='PCRID')

df_HousingProvidentFundRecords.EndPaymentMonth = pd.to_datetime(df_HousingProvidentFundRecords.EndPaymentMonth, errors='coerce')
df_HousingProvidentFundRecords.PaymentDate = pd.to_datetime(df_HousingProvidentFundRecords.PaymentDate, errors='coerce')
df_HousingProvidentFundRecords.UpdateDate = pd.to_datetime(df_HousingProvidentFundRecords.UpdateDate, errors='coerce')

df_HousingProvidentFundRecords.loc[df_HousingProvidentFundRecords.EndPaymentMonth<dt.datetime(1920,1,1,0,0,0),'EndPaymentMonth'] = pd.NaT
df_HousingProvidentFundRecords.loc[df_HousingProvidentFundRecords.EndPaymentMonth>df_HousingProvidentFundRecords.ReportDate,'EndPaymentMonth'] = \
    df_HousingProvidentFundRecords.loc[df_HousingProvidentFundRecords.EndPaymentMonth>df_HousingProvidentFundRecords.ReportDate,'ReportDate']
df_HousingProvidentFundRecords.loc[df_HousingProvidentFundRecords.PaymentDate<dt.datetime(1920,1,1,0,0,0),'PaymentDate'] = pd.NaT

df_HousingProvidentFundRecords.IndividualRatio = df_HousingProvidentFundRecords.IndividualRatio.replace('--',np.nan)
df_HousingProvidentFundRecords.loc[df_HousingProvidentFundRecords.IndividualRatio.notnull(),'IndividualRatio'] = \
    df_HousingProvidentFundRecords.loc[df_HousingProvidentFundRecords.IndividualRatio.notnull(),'IndividualRatio'].astype(str).str.replace('%','').astype(int)/100

df_HousingProvidentFundRecords.CompanyRatio = df_HousingProvidentFundRecords.CompanyRatio.replace('--',np.nan)
df_HousingProvidentFundRecords.loc[df_HousingProvidentFundRecords.CompanyRatio.notnull(),'CompanyRatio'] = \
    df_HousingProvidentFundRecords.loc[df_HousingProvidentFundRecords.CompanyRatio.notnull(),'CompanyRatio'].astype(str).str.replace('%','').astype(int)/100

paymentStatus_Mapping = {'1':'缴交','2':'封存','3':'销户',}
df_HousingProvidentFundRecords['PaymentStatus'] = df_HousingProvidentFundRecords['PaymentStatus'].map(paymentStatus_Mapping)
df_HousingProvidentFundRecords['SerialNumer'] = df_HousingProvidentFundRecords.groupby('PCRID')[['PaymentDate']].rank(ascending=False,method='first') #yl

df_HousingProvidentFundRecords['EndMonthRank'] = df_HousingProvidentFundRecords \
    .groupby('PCRID').EndPaymentMonth.rank(method='min', ascending=False)    
df_HousingProvidentFundRecords['UpdateRank'] = df_HousingProvidentFundRecords \
    .groupby(['PCRID','EndMonthRank']).UpdateDate.rank(method='min', ascending=False)
df_HousingProvidentFundRecords['SerialRank'] = df_HousingProvidentFundRecords \
    .groupby(['PCRID','EndMonthRank','UpdateRank']).SerialNumer.rank(method='min', ascending=True)
    
df_HousingProvidentFundRecords['RatioSum'] = \
    df_HousingProvidentFundRecords.IndividualRatio.fillna(0) + df_HousingProvidentFundRecords.CompanyRatio.fillna(0)
income = df_HousingProvidentFundRecords.MonthPayAmount/df_HousingProvidentFundRecords.RatioSum
df_HousingProvidentFundRecords['Income'] = np.round(income.replace(np.inf,np.nan),2)
df_HousingProvidentFundRecords['Duration'] = \
    (df_HousingProvidentFundRecords.EndPaymentMonth.dt.year-df_HousingProvidentFundRecords.PaymentDate.dt.year)*12+ \
    (df_HousingProvidentFundRecords.EndPaymentMonth.dt.month-df_HousingProvidentFundRecords.PaymentDate.dt.month)  

df_HousingProvidentFundRecords.loc[df_HousingProvidentFundRecords.Duration<0,'Duration'] = np.nan

#===查询记录===
df_QueryRecord = pd.read_csv('PCR2_QueryRecord.csv', low_memory=False,dtype={'InquiryRecordInquiryOrgType':str,'QueryReason':str})
df_QueryRecord.QueryDate = pd.to_datetime(df_QueryRecord.QueryDate)

queryReason_Mapping = {'01':'贷后管理','02':'贷款审批','03':'信用卡审批','08':'担保资格审查','09':'司法调查','16':'公积金提取复核查询','18':'股指期货开户','19':'特约商户实名审查','20':'保前审查','21':'保后管理','22':'法人代表、负责人、高管等资信审查','23':'客户准入资格审查','24':'融资审批','25':'资信审查','26':'额度审批',}
df_QueryRecord['QueryInstitution'] = df_QueryRecord['InquiryRecordInquiryOrgType'].map(managementInstituion_Mapping) + '"'+ df_QueryRecord['QueryInstitution'] +'"'
df_QueryRecord['QueryReason'] = df_QueryRecord['QueryReason'].map(queryReason_Mapping)
df_QueryRecord['SID'] = df_QueryRecord.groupby('PCRID')[['QueryDate']].rank(ascending=False,method='first') 

df_QueryRecord  = pd.merge(df_QueryRecord,report_dates,how='left',on='PCRID')
df_QueryRecord['DaySinceQuery'] = \
    (df_QueryRecord.ReportDate - df_QueryRecord.QueryDate)/np.timedelta64(1,'D')
df_QueryRecord['QueryYearMon'] = df_QueryRecord.QueryDate.dt.year*100+ \
    df_QueryRecord.QueryDate.dt.month

def parse_report_header():
    result = df_ReportHeaderInformation[['PCRID','ReportTime']].set_index('PCRID')
    result.rename(columns={'ReportTime':'报告时间'}, inplace=True)

    result['报告时间距今天数'] = np.round (( dt.datetime.now() - result['报告时间']) / np.timedelta64(1, 'D'),3)

    antifraud_cnt = df_ReportheaderAntiFraudWarning.groupby('PCRID').SID.count()
    result['是否有防欺诈警示'] = np.sign(antifraud_cnt)
    return result

def parse_identity_info():
    mapping_dict = {
        'Age':'年龄',
        'Gender':'性别',
        'EducationLevel':'学历',
        'EducationDegree':'学位',
        'MaritalStatus':'婚姻状况',
        'EmploymentStatus':'就业状况',
        'Nationality':'是否为我国居民',        
        'QueryRecordId':'报告编号',        #20231007add
        'PCRID2':'身份证号'    #20231007add
    }
    
    result = df_IdentifiableInformation[['PCRID']+list(mapping_dict.keys())].set_index('PCRID')
    result.Nationality = result.Nationality.map({'中国':1})
    result.rename(columns=mapping_dict, inplace=True)
    return result

def parse_phone_info():
    result = pd.DataFrame(index=pd.unique(df_PhoneInformation.PCRID))  
    result['最近一次手机号码信息更新日期距今天数'] = df_PhoneInformation \
        .groupby('PCRID').DaySinceUpdate.min()
    result['最早一次手机号码信息更新日期距今天数'] = df_PhoneInformation \
        .groupby('PCRID').DaySinceUpdate.max()
    
    periods = [3,6,12,24]
    for period in periods:
        var = '近{}个月手机号码个数'.format(period)
        result[var] = df_PhoneInformation[df_PhoneInformation.DaySinceUpdate<=period*30] \
            .groupby('PCRID').PhoneNo.nunique()
            
        var = '近{}个月手机号码信息更新次数'.format(period)
        result[var] = df_PhoneInformation[df_PhoneInformation.DaySinceUpdate<=period*30] \
            .groupby('PCRID').PhoneNo.count()        
    return result

def parse_living_info():
    result = pd.DataFrame(index=pd.unique(df_LivingInformation.PCRID))  
    result['最新居住状况'] = df_LivingInformation.loc[(df_LivingInformation.UpdateRank==1) & (df_LivingInformation.SerialRank==1), ['PCRID','LivingSituation']] \
        .set_index('PCRID')
    result['最近一次居住信息更新日期距今天数'] = df_LivingInformation \
        .groupby('PCRID').DaySinceUpdate.min()
    result['最早一次居住信息更新日期距今天数'] = df_LivingInformation \
        .groupby('PCRID').DaySinceUpdate.max()
    
    periods = [3,6,12,24]
    for period in periods:
        var = '近{}个月居住地址个数'.format(period)
        result[var] = df_LivingInformation[df_LivingInformation.DaySinceUpdate<=period*30] \
            .groupby('PCRID').Address.nunique()
            
        var = '近{}个月居住地址信息更新次数'.format(period)
        result[var] = df_LivingInformation[df_LivingInformation.DaySinceUpdate<=period*30] \
            .groupby('PCRID').Address.count()        
    return result

def parse_career_info():
    result = pd.DataFrame(index=pd.unique(df_CareeInformation.PCRID))  
    result['最新职业'] = df_CareeInformation.loc[(df_CareeInformation.UpdateRank==1) & (df_CareeInformation.SerialRank==1), ['PCRID','Profession']] \
        .set_index('PCRID')
    result['最新行业'] = df_CareeInformation.loc[(df_CareeInformation.UpdateRank==1) & (df_CareeInformation.SerialRank==1), ['PCRID','Industry']] \
        .set_index('PCRID')
    result['最新职务'] = df_CareeInformation.loc[(df_CareeInformation.UpdateRank==1) & (df_CareeInformation.SerialRank==1), ['PCRID','Position']] \
        .set_index('PCRID')
    result['最新职称'] = df_CareeInformation.loc[(df_CareeInformation.UpdateRank==1) & (df_CareeInformation.SerialRank==1), ['PCRID','Title']] \
        .set_index('PCRID')
    result['最近一次职业信息更新日期距今天数'] = df_CareeInformation \
        .groupby('PCRID').DaySinceUpdate.min()
    result['最早一次职业信息更新日期距今天数'] = df_CareeInformation \
        .groupby('PCRID').DaySinceUpdate.max()
        
    periods = [3,6,12,24]
    for period in periods:
        var = '近{}个月工作单位个数'.format(period)
        result[var] = df_CareeInformation[df_CareeInformation.DaySinceUpdate<=period*30] \
            .groupby('PCRID').Employer.nunique()
        
        var = '近{}个月工作单位信息更新次数'.format(period)
        result[var] = df_CareeInformation[df_CareeInformation.DaySinceUpdate<=period*30] \
            .groupby('PCRID').Employer.count()
    return result

def parse_digital_score():
    mapping_dict = {
        'RelativePosition':'相对位置', 
        'DigitalInterpretation':'数字解读评分'}
    
    result = df_SummaryDigitalInterpretation[['PCRID']+list(mapping_dict.keys())].set_index('PCRID').sort_values(by='DigitalInterpretation', ascending=False).head(1)
    result.rename(columns=mapping_dict, inplace=True)
    return result

def parse_credit_tips():
    result = pd.DataFrame(index=pd.unique(df_SummaryCreditTips.PCRID))  
    
    tot_acct_cnt = df_SummaryCreditTips.groupby('PCRID').CountOfAccount.sum(min_count=1)
    
    businessSubType_Mapping = {11:'个人住房贷款',12:'个人商用房（包括商住两用房）贷款',19:'其他类贷款',21:'贷记卡',22:'准贷记卡',99:'其他'} #yl
    businessType_Mapping = {1:'贷款',2:'信用卡',9:'其他'} #yl
    df_SummaryCreditTips['BusinessSubType'] = df_SummaryCreditTips['BusinessSubType'].map(businessSubType_Mapping) #yl
    df_SummaryCreditTips['BusinessType'] = df_SummaryCreditTips['BusinessType'].map(businessType_Mapping) #yl
    
    accts = ['个人住房贷款','个人商用房贷款（包括商住两用房）','其他类贷款','贷记卡','准贷记卡']
    for acct in accts:
        if acct!='个人商用房贷款（包括商住两用房）':
            acct_label = acct
        else:
            acct_label = '个人商用房贷款'
            
        result['{}的首笔业务距今月份数'.format(acct_label)] = \
            df_SummaryCreditTips[df_SummaryCreditTips.BusinessSubType==acct] \
            .groupby('PCRID').MonSinceFirstTrans.max()
        result['{}账户数'.format(acct_label)] = \
            df_SummaryCreditTips[df_SummaryCreditTips.BusinessSubType==acct] \
            .groupby('PCRID').CountOfAccount.sum(min_count=1)
            
        ratio = result['{}账户数'.format(acct_label)].fillna(0)/tot_acct_cnt
        result['{}账户数占比'.format(acct_label)] = np.round(ratio.replace(np.inf, np.nan),3)

    #贷款
    result['贷款的首笔业务距今月份数'] = df_SummaryCreditTips[df_SummaryCreditTips.BusinessSubType.isin(["个人住房贷款","个人商用房贷款（包括商住两用房）","其他类贷款"])] \
        .groupby('PCRID').MonSinceFirstTrans.max()
    result['贷款账户数'] = df_SummaryCreditTips[df_SummaryCreditTips.BusinessSubType.isin(["个人住房贷款","个人商用房贷款（包括商住两用房）","其他类贷款"])] \
        .groupby('PCRID').CountOfAccount.sum(min_count=1) 
        
    ratio = result['贷款账户数'].fillna(0)/tot_acct_cnt
    result['贷款账户数占比'] = np.round(ratio.replace(np.inf, np.nan),3)
     
    #信用卡
    result['信用卡的首笔业务距今月份数'] = df_SummaryCreditTips[df_SummaryCreditTips.BusinessSubType.isin(["贷记卡","准贷记卡"])] \
        .groupby('PCRID').MonSinceFirstTrans.max()
    result['信用卡账户数'] = df_SummaryCreditTips[df_SummaryCreditTips.BusinessSubType.isin(["贷记卡","准贷记卡"])] \
        .groupby('PCRID').CountOfAccount.sum(min_count=1)   
        
    ratio = result['信用卡账户数'].fillna(0)/tot_acct_cnt
    result['信用卡账户数占比'] = np.round(ratio.replace(np.inf, np.nan),3) 
       
    #其他业务
    result['其他业务的首笔业务距今月份数'] = df_SummaryCreditTips[df_SummaryCreditTips.BusinessType=="其他"] \
        .groupby('PCRID').MonSinceFirstTrans.max()
    result['其他业务账户数'] = df_SummaryCreditTips[df_SummaryCreditTips.BusinessType=="其他"] \
        .groupby('PCRID').CountOfAccount.sum(min_count=1)  
    
    #房贷    
    result['房贷账户数'] = df_SummaryCreditTips[df_SummaryCreditTips.BusinessSubType.isin(["个人住房贷款","个人商用房贷款（包括商住两用房）"])] \
        .groupby('PCRID').CountOfAccount.sum(min_count=1)
        
    ratio = result['房贷账户数'].fillna(0)/tot_acct_cnt
    result['房贷账户数占比'] = np.round(ratio.replace(np.inf, np.nan),3)
        
    ratio = result['房贷账户数'].fillna(0)/result['贷款账户数']
    result['房贷账户数占贷款账户数比例'] = np.round(ratio.replace(np.inf, np.nan),3)
    
    #全部业务
    result['信贷交易中最早的首笔业务距今月份数'] = df_SummaryCreditTips \
        .groupby('PCRID').MonSinceFirstTrans.max()
    return result

def parse_dunning_summary():
    result = pd.DataFrame(index=pd.unique(df_SummaryDunningInformation.PCRID))  

    trans_list = ['资产处置','垫款']
    
    businessType_Mapping = {1.0:'资产处置',2.0:'垫款'} #yl
    df_SummaryDunningInformation['BusinessType'] = df_SummaryDunningInformation['BusinessType'].map(businessType_Mapping) #yl
    
    for trans in trans_list:
        result['{}账户数'.format(trans)] = \
            df_SummaryDunningInformation[df_SummaryDunningInformation.BusinessType=='{}业务'.format(trans)] \
            .groupby('PCRID').CountOfAccount.sum(min_count=1)
        result['{}余额'.format(trans)] = \
            df_SummaryDunningInformation[df_SummaryDunningInformation.BusinessType=='{}业务'.format(trans)] \
            .groupby('PCRID').Balance.sum(min_count=1)
            
    result['被追偿账户数'] = df_SummaryDunningInformation.groupby('PCRID').CountOfAccount.sum(min_count=1)
    result['被追偿余额'] = df_SummaryDunningInformation.groupby('PCRID').Balance.sum(min_count=1)
    return result

def parse_bad_debts_summary():
    mapping_dict = {
        'CountOfAccount':'呆账账户数',
        'Balance':'呆账余额'}
    
    result = df_SummaryBadDebts[['PCRID']+list(mapping_dict.keys())].set_index('PCRID').groupby(level=0).sum()
    result.rename(columns=mapping_dict, inplace=True)
    return result

def parse_ovd_summary():
    result = pd.DataFrame(index=pd.unique(df_SummaryOverdue.PCRID))  
    accountType_Mapping = {1.0:'非循环贷账户',2.0:'循环额度下分账户',3.0:'循环贷账户',4.0:'贷记卡账户',5.0:'准贷记卡账户'} #yl
    df_SummaryOverdue['AccountType'] = df_SummaryOverdue['AccountType'].map(accountType_Mapping) #yl
    accts = ['非循环贷账户','循环额度下分账户','循环贷账户','贷记卡账户']
    for acct in accts:
        var = '{}逾期账户数'.format(acct)
        result[var] = df_SummaryOverdue[df_SummaryOverdue.AccountType==acct] \
            .groupby('PCRID').CountOfAccount.sum(min_count=1)
            
        var = '{}逾期月份数'.format(acct)
        result[var] = df_SummaryOverdue[df_SummaryOverdue.AccountType==acct] \
            .groupby('PCRID').CountOfMonth.sum(min_count=1)
            
        var = '{}单月最高逾期总额'.format(acct)
        result[var] = df_SummaryOverdue[df_SummaryOverdue.AccountType==acct] \
            .groupby('PCRID').HighestOverdueAmountByMonth.max()
            
        var = '{}最长逾期月数'.format(acct)
        result[var] = df_SummaryOverdue[df_SummaryOverdue.AccountType==acct] \
            .groupby('PCRID').LongestOverdueMonth.max()

    result['准贷记卡账户透支账户数'] = df_SummaryOverdue[df_SummaryOverdue.AccountType=='准贷记卡账户'] \
            .groupby('PCRID').CountOfAccount.sum(min_count=1)
    result['准贷记卡账户透支月份数'] = df_SummaryOverdue[df_SummaryOverdue.AccountType=='准贷记卡账户'] \
            .groupby('PCRID').CountOfMonth.sum(min_count=1)
    result['准贷记卡账户单月最高透支总额'] = df_SummaryOverdue[df_SummaryOverdue.AccountType=='准贷记卡账户'] \
            .groupby('PCRID').HighestOverdueAmountByMonth.max()
    result['准贷记卡账户最长透支月数'] = df_SummaryOverdue[df_SummaryOverdue.AccountType=='准贷记卡账户'] \
            .groupby('PCRID').LongestOverdueMonth.max()
        
    result['贷款逾期账户数'] = df_SummaryOverdue[df_SummaryOverdue.AccountType.isin(["非循环贷账户","循环额度下分账户","循环贷账户"])] \
        .groupby('PCRID').CountOfAccount.sum(min_count=1)
    result['贷款最长逾期月数'] = df_SummaryOverdue[df_SummaryOverdue.AccountType.isin(["非循环贷账户","循环额度下分账户","循环贷账户"])] \
        .groupby('PCRID').LongestOverdueMonth.max()
        
    result['信用卡逾期(透支)账户数'] = df_SummaryOverdue[df_SummaryOverdue.AccountType.isin(["贷记卡账户","准贷记卡账户"])] \
        .groupby('PCRID').CountOfAccount.sum(min_count=1)   
    result['信用卡最长逾期(透支)月数'] = df_SummaryOverdue[df_SummaryOverdue.AccountType.isin(["贷记卡账户","准贷记卡账户"])] \
        .groupby('PCRID').LongestOverdueMonth.max()
    
    result['贷款及信用卡逾期(透支)账户数'] = df_SummaryOverdue \
        .groupby('PCRID').CountOfAccount.sum(min_count=1)
    result['贷款及信用卡最长逾期(透支)月数'] = df_SummaryOverdue\
        .groupby('PCRID').LongestOverdueMonth.max()
    return result

def parse_credit_info_summary():
    result = pd.DataFrame(index=pd.unique(df_SummaryCreditAcountInformation.PCRID)).rename_axis('PCRID')
    #未结清(未销户)贷款及信用卡
    result['未结清(未销户)贷款及信用卡账户数'] = df_SummaryCreditAcountInformation \
        .groupby('PCRID').CountOfAccount.sum(min_count=1)

    result['未结清(未销户)贷款及信用卡授信总额'] =  df_SummaryCreditAcountInformation \
        .groupby('PCRID').CreditTotalAmount.sum(min_count=1) 
        
    sum1 = df_SummaryCreditAcountInformation[(df_SummaryCreditAcountInformation.AccountType.isin([1,2,3]))] \
        .groupby('PCRID').AverageInstallmentOfRecent6Months.sum(min_count=1)
    sum2 = df_SummaryCreditAcountInformation[(df_SummaryCreditAcountInformation.AccountType.isin([4,5]))] \
        .groupby('PCRID').AverageOverdraftAmountInLast6Month.sum(min_count=1)
    total_sum = pd.DataFrame({'sum1':sum1,'sum2':sum2}).sum(axis=1, min_count=1)
    result['未结清(未销户)贷款及信用卡最近6个月平均应还'] = total_sum

    #未结清贷款
    result['未结清贷款账户数'] = \
        df_SummaryCreditAcountInformation[df_SummaryCreditAcountInformation.AccountType.isin([1,2,3])] \
        .groupby('PCRID').CountOfAccount.sum(min_count=1)  
        
    ratio = result['未结清贷款账户数'].fillna(0)/result['未结清(未销户)贷款及信用卡账户数']
    result['未结清贷款账户数占比'] = np.round(ratio.replace(np.inf, np.nan),3)
    
    result['未结清贷款授信总额'] = \
        df_SummaryCreditAcountInformation[df_SummaryCreditAcountInformation.AccountType.isin([1,2,3])] \
        .groupby('PCRID').CreditTotalAmount.sum(min_count=1) 
    
    avg = result['未结清贷款授信总额']/result['未结清贷款账户数']
    result['未结清贷款平均授信额度'] = np.round(avg.replace(np.inf, np.nan),2)
    
    ratio = result['未结清贷款授信总额'].fillna(0)/result['未结清(未销户)贷款及信用卡授信总额']
    result['未结清贷款授信总额占比'] = np.round(ratio.replace(np.inf, np.nan),3)
    
    result['未结清贷款余额'] = \
        df_SummaryCreditAcountInformation[df_SummaryCreditAcountInformation.AccountType.isin([1,2,3])] \
        .groupby('PCRID').OutstandingBalance.sum(min_count=1) 
    
    ratio = result['未结清贷款余额'].fillna(0)/result['未结清贷款授信总额']
    result['未结清贷款余额占授信总额比例'] = np.round(ratio.replace(np.inf, np.nan),3)
    
    avg = result['未结清贷款余额']/result['未结清贷款账户数']
    result['未结清贷款平均余额'] = np.round(avg.replace(np.inf, np.nan),2)
    
    result['未结清贷款最近6个月平均应还款'] =  \
        df_SummaryCreditAcountInformation[df_SummaryCreditAcountInformation.AccountType.isin([1,2,3])] \
        .groupby('PCRID').AverageInstallmentOfRecent6Months.sum(min_count=1) 
    
    #未销户信用卡
    result['未销户信用卡账户数'] = \
        df_SummaryCreditAcountInformation[df_SummaryCreditAcountInformation.AccountType.isin([4,5])] \
        .groupby('PCRID').CountOfAccount.sum(min_count=1)  
        
    ratio = result['未销户信用卡账户数'].fillna(0)/result['未结清(未销户)贷款及信用卡账户数']
    result['未销户信用卡账户数占比'] = np.round(ratio.replace(np.inf, np.nan),3)
        
    result['未销户信用卡授信总额'] = \
        df_SummaryCreditAcountInformation[df_SummaryCreditAcountInformation.AccountType.isin([4,5])] \
        .groupby('PCRID').CreditTotalAmount.sum(min_count=1) 
    
    avg = result['未销户信用卡授信总额']/result['未销户信用卡账户数']
    result['未销户信用卡平均授信额度'] = np.round(avg.replace(np.inf, np.nan),2)
    
    ratio = result['未销户信用卡授信总额'].fillna(0)/result['未结清(未销户)贷款及信用卡授信总额']
    result['未销户信用卡授信总额占比'] = np.round(ratio.replace(np.inf, np.nan),3)

    #未结清三类贷款
    accts = ['非循环贷账户','循环额度下分账户','循环贷账户']
    result_subloan_list =[]
    for i,acct in enumerate(accts):
        mapping_dict = {
            'CountOfAccount':'未结清{}数'.format(acct),
            'CountOfInstitutions':'未结清{}管理机构数'.format(acct),
            'CreditTotalAmount':'未结清{}授信总额'.format(acct),
            'OutstandingBalance':'未结清{}余额'.format(acct),
            'AverageInstallmentOfRecent6Months':'未结清{}最近6个月平均应还款'.format(acct)}
        
        result_subloan = df_SummaryCreditAcountInformation.loc[df_SummaryCreditAcountInformation.AccountType==(i+1),['PCRID']+list(mapping_dict.keys())].set_index('PCRID').groupby(level=0).sum()
        result_subloan.rename(columns=mapping_dict, inplace=True) 
        
        avg = result_subloan['未结清{}数'.format(acct)]/result_subloan['未结清{}管理机构数'.format(acct)]
        result_subloan['未结清{}的机构平均账户数'.format(acct)] = np.round(avg.replace(np.inf, np.nan),2)
        
        avg = result_subloan['未结清{}授信总额'.format(acct)]/result_subloan['未结清{}数'.format(acct)]
        result_subloan['未结清{}平均授信额度'.format(acct)] = np.round(avg.replace(np.inf, np.nan),2)
        
        avg = result_subloan['未结清{}授信总额'.format(acct)]/result_subloan['未结清{}管理机构数'.format(acct)]
        result_subloan['未结清{}的机构平均授信额度'.format(acct)] = np.round(avg.replace(np.inf, np.nan),2)
         
        ratio = result_subloan['未结清{}余额'.format(acct)].fillna(0)/result_subloan['未结清{}授信总额'.format(acct)]
        result_subloan['未结清{}余额占授信总额比例'.format(acct)] = np.round(ratio.replace(np.inf, np.nan),3)
        
        avg = result_subloan['未结清{}余额'.format(acct)]/result_subloan['未结清{}数'.format(acct)]
        result_subloan['未结清{}平均余额'.format(acct)] = np.round(avg.replace(np.inf, np.nan),2)
        
        avg = result_subloan['未结清{}余额'.format(acct)]/result_subloan['未结清{}管理机构数'.format(acct)]
        result_subloan['未结清{}的机构平均余额'.format(acct)] = np.round(avg.replace(np.inf, np.nan),2)
        
        result_subloan_list.append(result_subloan)

    #未销户贷记卡    
    mapping_dict = {
        'CountOfAccount':'未销户贷记卡账户数',
        'CountOfInstitutions':'未销户贷记卡发卡机构数',
        'CreditTotalAmount':'未销户贷记卡授信总额',
        'MaxCreditAmountOfSingleBank':'未销户贷记卡单家机构最高授信额',
        'MinCreditAmountOfSingleBank':'未销户贷记卡单家机构最低授信额',
        'OverdraftAmount':'未销户贷记卡已用额度',
        'AverageOverdraftAmountInLast6Month':'未销户贷记卡最近6个月平均使用额度'}
    
    result_card = df_SummaryCreditAcountInformation.loc[df_SummaryCreditAcountInformation.AccountType==4,['PCRID']+list(mapping_dict.keys())].set_index('PCRID').groupby(level=0).sum()
    result_card.rename(columns=mapping_dict, inplace=True)    
       
    avg = result_card['未销户贷记卡授信总额']/result_card['未销户贷记卡账户数']
    result_card['未销户贷记卡平均授信额度'] = np.round(avg.replace(np.inf, np.nan),2)
    
    avg = result_card['未销户贷记卡授信总额']/result_card['未销户贷记卡发卡机构数']
    result_card['未销户贷记卡的机构平均授信额度'] = np.round(avg.replace(np.inf, np.nan),2)
    
    ratio = result_card['未销户贷记卡已用额度'].fillna(0)/result_card['未销户贷记卡授信总额']
    result_card['未销户贷记卡当前额度使用率'] = np.round(ratio.replace(np.inf, np.nan),3)
    
    avg = result_card['未销户贷记卡已用额度'].fillna(0)/result_card['未销户贷记卡账户数']
    result_card['未销户贷记卡平均已用额度'] = np.round(avg.replace(np.inf, np.nan),2)
    
    avg = result_card['未销户贷记卡已用额度'].fillna(0)/result_card['未销户贷记卡发卡机构数']
    result_card['未销户贷记卡的机构平均已用额度'] = np.round(avg.replace(np.inf, np.nan),2)
    
    ratio = result_card['未销户贷记卡最近6个月平均使用额度'].fillna(0)/result_card['未销户贷记卡授信总额']
    result_card['未销户贷记卡最近6个月平均额度使用率'] = np.round(ratio.replace(np.inf, np.nan),3)       
    
    ratio = result_card['未销户贷记卡单家机构最高授信额'].fillna(0)/result_card['未销户贷记卡授信总额']
    result_card['未销户贷记卡单家机构最高授信额占授信总额比例'] = np.round(ratio.replace(np.inf, np.nan),3)

    #未销户准贷记卡
    mapping_dict = {
        'CountOfAccount':'未销户准贷记卡账户数',
        'CountOfInstitutions':'未销户准贷记卡发卡机构数',
        'CreditTotalAmount':'未销户准贷记卡授信总额',
        'MaxCreditAmountOfSingleBank':'未销户准贷记卡单家机构最高授信额',
        'MinCreditAmountOfSingleBank':'未销户准贷记卡单家机构最低授信额',
        'OverdraftAmount':'未销户准贷记卡透支余额',
        'AverageOverdraftAmountInLast6Month':'未销户准贷记卡最近6个月平均透支余额'}
    
    result_semicard = df_SummaryCreditAcountInformation.loc[df_SummaryCreditAcountInformation.AccountType==5,['PCRID']+list(mapping_dict.keys())].set_index('PCRID').groupby(level=0).sum()
    result_semicard.rename(columns=mapping_dict, inplace=True)  
    
    avg = result_semicard['未销户准贷记卡授信总额']/result_semicard['未销户准贷记卡账户数']
    result_semicard['未销户准贷记卡平均授信额度'] = np.round(avg.replace(np.inf, np.nan),2)
    
    avg = result_semicard['未销户准贷记卡授信总额']/result_semicard['未销户准贷记卡发卡机构数']
    result_semicard['未销户准贷记卡的机构平均授信额度'] = np.round(avg.replace(np.inf, np.nan),2)
    
    ratio = result_semicard['未销户准贷记卡透支余额'].fillna(0)/result_semicard['未销户准贷记卡授信总额']
    result_semicard['未销户准贷记卡透支余额占授信总额比例'] = np.round(ratio.replace(np.inf, np.nan),3)
    
    avg = result_semicard['未销户准贷记卡透支余额'].fillna(0)/result_semicard['未销户准贷记卡账户数']
    result_semicard['未销户准贷记卡平均透支余额'] = np.round(avg.replace(np.inf, np.nan),2)
    
    avg = result_semicard['未销户准贷记卡透支余额'].fillna(0)/result_semicard['未销户准贷记卡发卡机构数']
    result_semicard['未销户准贷记卡的机构平均透支余额'] = np.round(avg.replace(np.inf, np.nan),2)

    ratio = result_semicard['未销户准贷记卡最近6个月平均透支余额'].fillna(0)/result_semicard['未销户准贷记卡授信总额']
    result_semicard['未销户准贷记卡最近6个月平均透支余额占授信总额比例'] = np.round(ratio.replace(np.inf, np.nan),3)
    
    ratio = result_semicard['未销户准贷记卡单家机构最高授信额'].fillna(0)/result_semicard['未销户准贷记卡授信总额']
    result_semicard['未销户准贷记卡单家机构最高授信额占授信总额比例'] = np.round(ratio.replace(np.inf, np.nan),3)


    for result_subloan in result_subloan_list:
        result = pd.merge(result, result_subloan,how='left',on='PCRID')

    result = pd.merge(result, result_card, how='left',left_index=True, right_index=True)

    result = pd.merge(result, result_semicard, how='left',left_index=True, right_index=True)

    for acct in accts:
        ratio = result['未结清{}授信总额'.format(acct)]/result['未结清贷款授信总额']
        result['未结清{}授信总额占贷款账户授信总额比例'.format(acct)] = \
            np.round(ratio.replace(np.inf, np.nan),3)
    return result

def parse_related_pmt_summary():
    result = pd.DataFrame(index=pd.unique(df_SummaryReleatedRepayment.PCRID))    
       
    borrowerType_Mapping = {1.0:'为个人',2.0:'为企业'} #yl
    repaymentType_Mapping = {1.0:'担保责任',9.0:'其他相关还款责任'} #yl
    df_SummaryReleatedRepayment['BorrowerType'] = df_SummaryReleatedRepayment['BorrowerType'].map(borrowerType_Mapping) #yl
    df_SummaryReleatedRepayment['RepaymentType'] = df_SummaryReleatedRepayment['RepaymentType'].map(repaymentType_Mapping) #yl
    
    borrower_list = ['为个人','为企业']
    resp_list = ['担保责任','其他相关还款责任']
    
    for borrower in borrower_list:    
        for resp in resp_list:
            result['{}{}账户数'.format(borrower,resp)] = \
                df_SummaryReleatedRepayment[(df_SummaryReleatedRepayment.BorrowerType==borrower) & (df_SummaryReleatedRepayment.RepaymentType==resp)] \
                .groupby('PCRID').CountOfAccount.sum(min_count=1)  
            result['{}{}金额'.format(borrower,resp)] = \
                df_SummaryReleatedRepayment[(df_SummaryReleatedRepayment.BorrowerType==borrower) & (df_SummaryReleatedRepayment.RepaymentType==resp)] \
                .groupby('PCRID').AmountOfGuarantee.sum(min_count=1)  
            result['{}{}余额'.format(borrower,resp)] = \
                df_SummaryReleatedRepayment[(df_SummaryReleatedRepayment.BorrowerType==borrower) & (df_SummaryReleatedRepayment.RepaymentType==resp)] \
                .groupby('PCRID').OutstandingBalance.sum(min_count=1)
            
    for resp in resp_list:
        result['为个人及企业{}账户数'.format(resp)] = \
            df_SummaryReleatedRepayment[df_SummaryReleatedRepayment.RepaymentType==resp] \
            .groupby('PCRID').CountOfAccount.sum(min_count=1)  
        result['为个人及企业{}金额'.format(resp)] = \
            df_SummaryReleatedRepayment[df_SummaryReleatedRepayment.RepaymentType==resp] \
            .groupby('PCRID').AmountOfGuarantee.sum(min_count=1)  
        result['为个人及企业{}余额'.format(resp)] = \
            df_SummaryReleatedRepayment[df_SummaryReleatedRepayment.RepaymentType==resp] \
            .groupby('PCRID').OutstandingBalance.sum(min_count=1)
    
    for borrower in borrower_list:    
        result['{}相关还款责任账户数'.format(borrower)] = \
            df_SummaryReleatedRepayment[df_SummaryReleatedRepayment.BorrowerType==borrower] \
            .groupby('PCRID').CountOfAccount.sum(min_count=1)  
        result['{}相关还款责任金额'.format(borrower)] = \
            df_SummaryReleatedRepayment[df_SummaryReleatedRepayment.BorrowerType==borrower] \
            .groupby('PCRID').AmountOfGuarantee.sum(min_count=1)  
        result['{}相关还款责任余额'.format(borrower)] = \
            df_SummaryReleatedRepayment[df_SummaryReleatedRepayment.BorrowerType==borrower] \
            .groupby('PCRID').OutstandingBalance.sum(min_count=1)        
    
    result['相关还款责任合计帐户数'] = df_SummaryReleatedRepayment \
        .groupby('PCRID').CountOfAccount.sum(min_count=1)  
    result['相关还款责任合计金额'] = df_SummaryReleatedRepayment \
        .groupby('PCRID').AmountOfGuarantee.sum(min_count=1)  
    result['相关还款责任合计余额'] = df_SummaryReleatedRepayment \
        .groupby('PCRID').OutstandingBalance.sum(min_count=1)
    return result

def parse_noncredit_info_summary():
    result = pd.DataFrame(index=pd.unique(df_SummaryOverduePostpayFee.PCRID)) 
    result['非信贷交易欠费账户数'] = df_SummaryOverduePostpayFee. \
        groupby('PCRID').CountOfAccounts.sum(min_count=1)
    result['非信贷交易欠费金额'] = df_SummaryOverduePostpayFee. \
        groupby('PCRID').OverdueAmount.sum(min_count=1)
    return result

def parse_public_info_summary():
    result = pd.DataFrame(index=pd.unique(df_SummaryPublicInformation.PCRID))
    
    informationType_Mapping = {1.0:'欠税',2.0:'民事判决',3.0:'强制执行',4.0:'行政处罚'} #yl
    df_SummaryPublicInformation['InformationType'] = df_SummaryPublicInformation['InformationType'].map(informationType_Mapping) #yl
    
    trans_list = ['欠税','民事判决','强制执行','行政处罚']
    for trans in trans_list:
       result['{}记录数'.format(trans) ] = \
           df_SummaryPublicInformation[df_SummaryPublicInformation.InformationType=='{}信息'.format(trans)] \
           .groupby('PCRID').CountOfRecord.sum(min_count=1)
       result['{}涉及金额'.format(trans) ] = \
           df_SummaryPublicInformation[df_SummaryPublicInformation.InformationType=='{}信息'.format(trans)] \
           .groupby('PCRID').TotalAmount.sum(min_count=1)
               
    result['公共信息总记录数'] = df_SummaryPublicInformation \
        .groupby('PCRID').CountOfRecord.sum(min_count=1)
    result['公共信息涉及金额总和'] = df_SummaryPublicInformation \
        .groupby('PCRID').TotalAmount.sum(min_count=1)
    return result

def parse_query_summary():
    mapping_dict = {
        'CountOfCreditApprovalQueryInstitutionInLastMonth':'最近1个月贷款审批查询机构数',
        'CountOfCreditCardApprovalQueryInstitutionInLastMonth':'最近1个月信用卡审批查询机构数',
        'QueryTimesOfCreditApprovalInLastMonth':'最近1个月贷款审批查询次数',
        'QueryTimesOfCreditCardApprovalInLastMonth':'最近1个月信用卡审批查询次数',
        'SelfQueryTimesInLastMonth':'最近1个月本人查询次数',
        'QueryTimesOfPostloanManagementInLastTwoMonth':'最近2年贷后管理查询次数',
        'QueryTimesOfGuaranteeQualificationAssessment':'最近2年担保资格审查查询次数',
        'QueryTimesOfMerchantsRealnameReview':'最近2年特约商户实名审查查询次数'}
    
    result = df_SummaryQueryInformation[['PCRID']+list(mapping_dict.keys())].set_index('PCRID').groupby(level=0).sum()
    result.rename(columns=mapping_dict, inplace=True)
    return result

def parse_query_record(cond=None,label=None):        
    if cond is None:
        df_subset = df_QueryRecord
    else:
        df_subset = df_QueryRecord[cond]
    result = pd.DataFrame(index=pd.unique(df_subset.PCRID))
    
    if label is None:
        label=''  
    
    var = '最近一次{}查询距今天数'.format(label)
    result[var] = df_subset.groupby('PCRID').DaySinceQuery.min()


    periods = [3,6,12,24]
    for period in periods:               
        var = '最近{}个月{}查询次数'.format(period,label)
        result[var] = df_subset[df_subset.DaySinceQuery<=(period*30)] \
            .groupby('PCRID').SID.count()

        if period==24 and label=='':
            queryTimesOfPostloanManagement =  df_SummaryQueryInformation.groupby('PCRID').QueryTimesOfPostloanManagementInLastTwoMonth.sum(min_count=1).fillna(0)
            ratio = queryTimesOfPostloanManagement / (result['最近24个月查询次数'] + queryTimesOfPostloanManagement)
            result['最近2年贷后管理查询次数占比'] = np.round(ratio.replace(np.inf, np.nan), 3)
        
        var = '最近{}个月{}查询机构数'.format(period,label)
        result[var] = df_subset[df_subset.DaySinceQuery<=(period*30)] \
            .groupby('PCRID').QueryInstitution.nunique()
        
        var = '最近{}个月{}最大月查询次数'.format(period,label)
        monthly_summary = df_subset[df_subset.DaySinceQuery<=(period*30)] \
            .groupby(['PCRID','QueryYearMon']).SID.count().rename('QueryCnt')
        result[var] = monthly_summary.reset_index().groupby('PCRID').QueryCnt.max()
        
        var = '最近{}个月{}最大月查询机构数'.format(period,label)
        monthly_summary = df_subset[df_subset.DaySinceQuery<=(period*30)] \
            .groupby(['PCRID','QueryYearMon']).QueryInstitution.nunique().rename('QueryInstUniqueCnt')
        result[var] = monthly_summary.reset_index().groupby('PCRID').QueryInstUniqueCnt.max()

    periods = [3, 7, 15, 30]
    for period in periods:
        var = '最近{}天{}查询次数'.format(period, label)
        result[var] = df_subset[df_subset.DaySinceQuery <= period] \
            .groupby('PCRID').SID.count()

        var = '最近{}天{}查询机构数'.format(period, label)
        result[var] = df_subset[df_subset.DaySinceQuery <= period] \
            .groupby('PCRID').QueryInstitution.nunique()

    return result

def parse_query_approval(mode):
    if mode=='贷款':
        df_query_subset = df_QueryRecord[(df_QueryRecord.QueryReason=='贷款审批')]
        df_trans_subset = df_CreditTransJoined[df_CreditTransJoined.CreditType.isin([1,2,3])]
    else:        
        df_query_subset = df_QueryRecord[(df_QueryRecord.QueryReason=='信用卡审批')]
        df_trans_subset = df_CreditTransJoined[df_CreditTransJoined.CreditType.isin([4,5])]  
    
    result = pd.DataFrame(index=pd.unique(df_QueryRecord.PCRID))
    
    periods = [3,6,12,24]
    for period in periods:
        df_query_no_dup = df_query_subset.loc[df_query_subset.DaySinceQuery<=(period*30),['PCRID','QueryInstitution']].drop_duplicates()
        df_trans_no_dup = df_trans_subset.loc[df_trans_subset.DaySinceOpen<=(period*30),['PCRID','ManagementInstituion']].drop_duplicates()
        df_paired = pd.merge(df_query_no_dup,df_trans_no_dup,how='left',left_on=['PCRID','QueryInstitution'],right_on=['PCRID','ManagementInstituion'])
        
        query_cnt = df_paired.groupby('PCRID').QueryInstitution.count()
        pass_cnt = df_paired.groupby('PCRID').ManagementInstituion.count()
        
        var = '近{}个月{}审批机构通过率'.format(period,mode)
        ratio = pass_cnt/query_cnt
        result[var] = np.round(ratio.replace(np.inf, np.nan),3)   
        
        var = '近{}个月{}审批查询且未通过机构数'.format(period,mode)
        result[var] = query_cnt - pass_cnt
           
    return result

def parse_dunning_detail():
    df_subset = df_CreditTransJoined[df_CreditTransJoined.CreditType==6]
    result = pd.DataFrame(index=pd.unique(df_subset.PCRID)) 
    
    trans_list = ['资产处置','代偿债务']
    for trans in trans_list:
        var = '{}账户状态为催收的账户数'.format(trans)
        result[var] = df_subset[(df_subset.BusinessType==trans) & (df_subset.AcctStatus=='催收')] \
            .groupby('PCRID').SID.count()

        var = '{}账户状态为结束的账户数'.format(trans)
        result[var] = df_subset[(df_subset.BusinessType==trans) & (df_subset.AcctStatus=='结束')] \
            .groupby('PCRID').SID.count()
        var = '{}债权金额'.format(trans)
        result[var] = df_subset[(df_subset.BusinessType==trans) ] \
            .groupby('PCRID').LoanAmount.sum(min_count=1)
        var = '{}最近一次债权接收日期距今月份数'.format(trans)
        result[var] = df_subset[(df_subset.BusinessType==trans) ] \
            .groupby('PCRID').MonSinceOpen.min()
    
    result['被追偿账户状态为催收的账户数'] = df_subset[(df_subset.AcctStatus=='催收')].groupby('PCRID').SID.count()
    result['被追偿账户状态为结束的账户数'] = df_subset[(df_subset.AcctStatus=='结束')].groupby('PCRID').SID.count()
    result['被追偿债权金额'] = df_subset.groupby('PCRID').LoanAmount.sum(min_count=1)
    result['被追偿最近一次债权接收日期距今月份数'] = df_subset.groupby('PCRID').MonSinceOpen.min()
    return result

def parse_loan_detail(id_list=None,label=None):
    if id_list is None:
        df_subset = df_CreditTransJoined[df_CreditTransJoined.CreditType.isin([1,2,3])]
    else:
        df_subset = df_CreditTransJoined[df_CreditTransJoined.SID.isin(id_list)]
    result = pd.DataFrame(index=pd.unique(df_subset.PCRID))  
    
    if label is None:
        label='贷款'
    
    #===逾期===
    var = '{}当前逾期账户数'.format(label)
    result[var] = df_subset[df_subset.CurrentDelinquencyTerm>0] \
        .groupby('PCRID').SID.count()
    
    var = '{}当前逾期90+账户数'.format(label)
    result[var] = df_subset[df_subset.CurrentDelinquencyTerm>3] \
        .groupby('PCRID').SID.count()
    
    var = '{}当前逾期总额'.format(label)
    result[var] = df_subset.groupby('PCRID').CurrentArrearAmount.sum(min_count=1) 
    
    var = '{}当前最大逾期期数'.format(label)
    result[var] = df_subset.groupby('PCRID').CurrentDelinquencyTerm.max()
    
    var = '{}当前最大逾期金额'.format(label)
    result[var] = df_subset.groupby('PCRID').CurrentArrearAmount.max()
    
    var = '{}逾期90+未还本金'.format(label)
    result[var]=df_subset.groupby('PCRID').OverduePrincipal90Plus.sum(min_count=1)
            
    var = '{}五级分类正常账户数'.format(label)
    result[var] = df_subset[df_subset.LoanGrade=='正常'] \
        .groupby('PCRID').SID.count()
        
    var = '{}五级分类非正常账户数'.format(label)
    result[var] = df_subset[df_subset.LoanGrade.isin(['关注','次级','可疑','损失'])] \
        .groupby('PCRID').SID.count()
        
    var = '{}五级分类非正常账户余额'.format(label)
    result[var] = df_subset[df_subset.LoanGrade.isin(['关注','次级','可疑','损失'])] \
        .groupby('PCRID').Bal.sum(min_count=1)
        
    for loan_grade in['关注','次级','可疑','损失']:
         var = '{}五级分类为{}的账户数'.format(label,loan_grade)
         result[var] = df_subset[df_subset.LoanGrade==loan_grade] \
             .groupby('PCRID').SID.count()
        
    var = '{}账户状态正常的账户数'.format(label)
    result[var] = df_subset[df_subset.AcctStatus=='正常'] \
        .groupby('PCRID').SID.count()
    
    risky_status = ['逾期','呆账','银行止付','担保物不足','强制平仓','司法追偿']
    var = '{}账户状态不良的账户数'.format(label)
    result[var] = df_subset[df_subset.AcctStatus.isin(risky_status)] \
        .groupby('PCRID').SID.count()
        
    var = '{}账户状态不良的账户余额'.format(label)
    result[var] = df_subset[df_subset.AcctStatus.isin(risky_status)] \
        .groupby('PCRID').Bal.sum(min_count=1)
        
    for status in ['银行止付','担保物不足','强制平仓','司法追偿']:
         var = '{}账户状态为{}的账户数'.format(label,status)
         result[var] = df_subset[df_subset.AcctStatus==status] \
             .groupby('PCRID').SID.count()
    
    var = '{}最近一次还款距今月份数'.format(label) 
    result[var] = df_subset.groupby('PCRID').MonSinceLastPmt.min()
    
    #===全状态===
    var = '{}账户数'.format(label)    
    result[var] = df_subset.groupby('PCRID').SID.count()

    var = '{}额度小于1000账户数'.format(label)
    result[var] = df_subset[df_subset.CreditAmt<=1000].groupby('PCRID').SID.count()

    var = '{}管理机构数'.format(label)
    result[var] = df_subset.groupby('PCRID').ManagementInstituion.nunique()
    
    var = '{}授信总额'.format(label)    
    result[var] = df_subset.groupby('PCRID').CreditAmt.sum(min_count=1)
    
    var = '{}平均授信额度'.format(label)
    result[var] = np.round(df_subset.groupby('PCRID').CreditAmt.mean(),2)
    
    var = '{}授信额度中位数'.format(label)
    result[var] = np.round(df_subset.groupby('PCRID').CreditAmt.median(),2)
    
    var = '{}最高授信额度'.format(label)    
    result[var] = df_subset.groupby('PCRID').CreditAmt.max()
    
    var = '{}最低授信额度'.format(label)    
    result[var] = df_subset.groupby('PCRID').CreditAmt.min()
    
    var = '{}额度不超过5000元账户数'.format(label)    
    result[var] = df_subset[df_subset.CreditAmt<=5000].groupby('PCRID').SID.count()
    
    var = '{}首笔业务距今月份数'.format(label)    
    result[var] = df_subset.groupby('PCRID').MonSinceOpen.max()

    #===未结清===
    unclosed_cond = (~df_subset.AcctStatus.isin(['结清','转出']))
    
    var = '未结清{}账户数'.format(label)    
    result[var] = df_subset[unclosed_cond] \
        .groupby('PCRID').SID.count()
    
    var = '未结清{}管理机构数'.format(label)    
    result[var] = df_subset[unclosed_cond] \
        .groupby('PCRID').ManagementInstituion.nunique()
    
    var = '未结清{}授信总额'.format(label)    
    result[var] = df_subset[unclosed_cond] \
        .groupby('PCRID').CreditAmt.sum(min_count=1)
    
    var = '未结清{}最高授信额度'.format(label) 
    result[var] = df_subset[unclosed_cond] \
        .groupby('PCRID').CreditAmt.max()
        
    var = '未结清{}最低授信额度'.format(label) 
    result[var] = df_subset[unclosed_cond] \
        .groupby('PCRID').CreditAmt.min()
        
    var = '未结清{}本月应还'.format(label) 
    result[var] = df_subset[unclosed_cond] \
        .groupby('PCRID').PayableAmountOfThisMonth.sum(min_count=1)
        
    var = '未结清{}本月实还'.format(label) 
    result[var] = df_subset[unclosed_cond] \
        .groupby('PCRID').PaymentAmountOfThisMonth.sum(min_count=1)
    
    var = '未结清{}本月还款比例'.format(label)
    var1 = '未结清{}本月实还'.format(label) 
    var2 = '未结清{}本月应还'.format(label) 
    ratio = result[var1].fillna(0)/result[var2]
    result[var] = np.round(ratio.replace(np.inf, np.nan),3) 
    
    var = '未结清{}单账户最高还款比例'.format(label)
    result[var] = df_subset[unclosed_cond].groupby('PCRID').PaymentRatio.max()
    
    var = '未结清{}单账户最低还款比例'.format(label)
    result[var] = df_subset[unclosed_cond].groupby('PCRID').PaymentRatio.min()
    
    var = '未结清{}余额'.format(label)    
    result[var] = df_subset[unclosed_cond] \
        .groupby('PCRID').Bal.sum(min_count=1)
    
    var = '未结清{}已还金额'.format(label)    
    var1 = '未结清{}余额'.format(label)    
    var2 = '未结清{}授信总额'.format(label)  
    result[var] = result[var2] - result[var1]
    
    var = '未结清{}余额占授信总额比例'.format(label) 
    var1 = '未结清{}余额'.format(label)    
    var2 = '未结清{}授信总额'.format(label)  
    ratio = result[var1].fillna(0)/result[var2]
    result[var] = np.round(ratio.replace(np.inf, np.nan),3) 
    
    cutoffs = [50, 70, 90]
    for cutoff in cutoffs:
         var = '余额占授信额度比例大于{}%的{}账户数'.format(cutoff, label)
         result[var] = df_subset[unclosed_cond & (df_subset.BalProp>(cutoff/100))] \
             .groupby('PCRID').SID.count()
    
    #===已结清===
    closed_cond = (df_subset.AcctStatus=='结清')
        
    var = '已结清{}账户数'.format(label)    
    result[var] = df_subset[closed_cond] \
        .groupby('PCRID').SID.count()
    
    var = '已结清{}授信总额'.format(label)    
    result[var] = df_subset[closed_cond] \
        .groupby('PCRID').CreditAmt.sum(min_count=1)
    
    var = '{}账户结清比例'.format(label)
    var1 = '已结清{}账户数'.format(label)     
    var2 = '{}账户数'.format(label)    
    ratio = result[var1].fillna(0)/result[var2]
    result[var] = np.round(ratio.replace(np.inf, np.nan),3)   
    
    var = '{}授信额度结清比例'.format(label)   
    var1 = '已结清{}授信总额'.format(label)    
    var2 = '{}授信总额'.format(label)    
    ratio = result[var1].fillna(0)/result[var2]
    result[var] = np.round(ratio.replace(np.inf, np.nan),3)
    
    #===新开===
    periods = [3,6,12,24]
    for period in periods:
        var = '近{}个月新开{}账户数'.format(period,label)
        result[var] = df_subset[df_subset.DaySinceOpen<=(period*30)] \
            .groupby('PCRID').SID.count()
            
        var = '近{}个月新开{}账户数占比'.format(period,label)
        var1 = '近{}个月新开{}账户数'.format(period,label)
        var2 = '{}账户数'.format(label)    
        ratio = result[var1].fillna(0)/result[var2]
        result[var] = np.round(ratio.replace(np.inf, np.nan),3)
            
        var = '近{}个月新开{}管理机构数'.format(period,label)
        result[var] = df_subset[df_subset.DaySinceOpen<=(period*30)] \
            .groupby('PCRID').ManagementInstituion.nunique()
        
        var = '近{}个月新开{}授信总额'.format(period,label)
        result[var] = df_subset[df_subset.DaySinceOpen<=(period*30)] \
            .groupby('PCRID').CreditAmt.sum(min_count=1)
        
        var = '近{}个月新开{}授信总额占比'.format(period,label)
        var1 = '近{}个月新开{}授信总额'.format(period,label)
        var2 = '{}授信总额'.format(label)    
        ratio = result[var1].fillna(0)/result[var2]
        result[var] = np.round(ratio.replace(np.inf, np.nan),3)
        
        var = '近{}个月新开{}平均授信额度'.format(period,label)
        result[var] = np.round(df_subset[df_subset.DaySinceOpen<=(period*30)] \
            .groupby('PCRID').CreditAmt.mean(),2)
        
        var = '近{}个月新开{}最高授信额度'.format(period,label)
        result[var] = df_subset[df_subset.DaySinceOpen<=(period*30)] \
            .groupby('PCRID').CreditAmt.max()
        
        var = '近{}个月新开{}最低授信额度'.format(period,label)
        result[var] = df_subset[df_subset.DaySinceOpen<=(period*30)] \
            .groupby('PCRID').CreditAmt.min()
            
        var = '近{}个月新开{}额度不超过5000元账户数'.format(period,label)
        result[var] = df_subset[(df_subset.DaySinceOpen<=(period*30)) & (df_subset.CreditAmt<=5000)] \
            .groupby('PCRID').SID.count()
        
    var = '最近一笔{}的授信额度'.format(label) 
    open_rank = df_subset.groupby('PCRID').DaySinceOpen.rank(method='min')
    result[var] = df_subset[open_rank==1].groupby('PCRID').CreditAmt.max()
    
    
    var = '最近一笔{}的开立时间距今月份数'.format(label)
    result[var] = df_subset.groupby('PCRID').MonSinceOpen.min()
    
    #===在册===
    if label=='贷款':
        df_subset_never_ovd = df_subset[~df_subset.SID.isin(ever_ovd_ids)]
        periods = [3,6,12,24]
        for period in periods:
            var = '在册{}个月及以上{}从未逾期账户数'.format(period,label)
            result[var] = df_subset_never_ovd[df_subset_never_ovd.LoanLife>=(period*30)] \
                .groupby('PCRID').SID.count()
            
            var = '在册{}个月及以上{}从未逾期账户最大授信额度'.format(period,label)
            result[var] = df_subset_never_ovd[df_subset_never_ovd.LoanLife>=(period*30)] \
                .groupby('PCRID').CreditAmt.max()
                
    if label=='贷款':
        result.rename(columns={'贷款账户数':'贷款账户数(基于明细)'}, inplace=True)  
    if label!='贷款':
        result.rename(columns={'最近一笔{}的授信额度'.format(label):'最近一笔{}授信额度'.format(label) }, inplace=True)
        for period in periods:
            result.rename(columns={'近{}个月新开{}授信总额'.format(period,label):'近{}个月新开{}授信额度'.format(period,label)}, inplace=True)
    result.columns = result.columns.str.replace('账户账户','账户')
    return result

def parse_credit_card_detail(id_list=None,label=None):
    if id_list is None:
        df_subset = df_CreditTransJoined[df_CreditTransJoined.CreditType.isin([4,5])]
    else:
        df_subset = df_CreditTransJoined[df_CreditTransJoined.SID.isin(id_list)]
    result = {}
    
    if label is None:
        label='信用卡'
    
    #===逾期===
    if label=='贷记卡':
        var = '{}当前逾期账户数'.format(label)
        result[var] = df_subset[df_subset.CurrentDelinquencyTerm>0] \
            .groupby('PCRID').SID.count()
        
        var = '{}当前逾期90+账户数'.format(label)
        result[var] = df_subset[df_subset.CurrentDelinquencyTerm>3] \
            .groupby('PCRID').SID.count()
        
        var = '{}当前逾期总额'.format(label)
        result[var] = df_subset.groupby('PCRID').CurrentArrearAmount.sum(min_count=1) 
        
        var = '{}当前最大逾期期数'.format(label)
        result[var] = df_subset.groupby('PCRID').CurrentDelinquencyTerm.max()
        
        var = '{}当前最大逾期金额'.format(label)
        result[var] = df_subset.groupby('PCRID').CurrentArrearAmount.max()    
        
    var = '{}账户状态正常的账户数'.format(label)
    result[var] = df_subset[df_subset.AcctStatus=='正常'] \
        .groupby('PCRID').SID.count()
    
    risky_status = ['冻结','止付','银行止付','呆账','司法追偿']
    var = '{}账户状态不良的账户数'.format(label)
    result[var] = df_subset[df_subset.AcctStatus.isin(risky_status)] \
        .groupby('PCRID').SID.count()
        
    var = '{}账户状态不良的账户余额'.format(label)
    result[var] = df_subset[df_subset.AcctStatus.isin(risky_status)] \
        .groupby('PCRID').Bal.sum(min_count=1)
        
    for status in ['冻结','止付','银行止付','司法追偿']:
         var = '{}账户状态为{}的账户数'.format(label,status)
         result[var] = df_subset[df_subset.AcctStatus==status] \
             .groupby('PCRID').SID.count()
    
    var = '{}最近一次还款距今月份数'.format(label) 
    result[var] = df_subset.groupby('PCRID').MonSinceLastPmtCard.min()
    
    #===全状态===
    var = '{}账户数'.format(label)    
    result[var] = df_subset.groupby('PCRID').SID.count()
    
    var = '{}发卡机构数'.format(label)    
    result[var] = df_subset.groupby('PCRID').ManagementInstituion.nunique()
    
    var = '{}授信总额'.format(label)    
    result[var] = df_subset \
        .groupby(['PCRID','ManagementInstituion','LoanIssuingDate']).CreditLine.max() \
        .reset_index().groupby('PCRID').CreditLine.sum(min_count=1)      

    var = '{}平均授信额度'.format(label)
    result[var] = np.round(df_subset \
        .groupby(['PCRID','ManagementInstituion','LoanIssuingDate']).CreditLine.max() \
        .reset_index().groupby('PCRID').CreditLine.mean(),2)
    
    var = '{}授信额度中位数'.format(label)
    result[var] = np.round(df_subset \
        .groupby(['PCRID','ManagementInstituion','LoanIssuingDate']).CreditLine.max() \
        .reset_index().groupby('PCRID').CreditLine.median(),2)
    
    var = '{}最高授信额度'.format(label)    
    result[var] = df_subset.groupby('PCRID').CreditLine.max()
    
    var = '{}最低授信额度'.format(label)    
    result[var] = df_subset.groupby('PCRID').CreditLine.min()
    
    var = '{}额度不超过5000元账户数'.format(label)    
    result[var] = df_subset[df_subset.CreditLine<=5000].groupby('PCRID').SID.count()
    
    var = '{}首笔业务距今月份数'.format(label)    
    result[var] = df_subset.groupby('PCRID').MonSinceOpen.max()

    #===未销户===
    unclosed_cond = (df_subset.AcctStatus!='销户')
    
    var = '未销户{}账户数'.format(label)    
    result[var] = df_subset[unclosed_cond] \
        .groupby('PCRID').SID.count()
    
    var = '未销户{}发卡机构数'.format(label)    
    result[var] = df_subset[unclosed_cond] \
        .groupby('PCRID').ManagementInstituion.nunique()
    
    var = '未销户{}授信总额'.format(label)    
    result[var] = df_subset[unclosed_cond] \
        .groupby(['PCRID','ManagementInstituion','LoanIssuingDate']).CreditLine.max() \
        .reset_index().groupby('PCRID').CreditLine.sum(min_count=1)
    
    # var = '未销户{}最高授信额度'.format(label) 
    # result[var] = df_subset[unclosed_cond] \
    #     .groupby('PCRID').CreditLine.max()
    
    var = '未销户{}已用额度'.format(label) 
    result[var] = df_subset[unclosed_cond] \
        .groupby('PCRID').UsedAmount.sum(min_count=1)       
    
    var = '未销户{}最近6个月平均使用额度'.format(label)     
    result[var] = df_subset[unclosed_cond] \
        .groupby('PCRID').AverageUtilizationInLast6Month.sum(min_count=1)
    
    var = '未销户{}最大使用额度'.format(label)     
    result[var] = df_subset[unclosed_cond] \
        .groupby('PCRID').MaxUtilization.sum(min_count=1)              

    if label=='贷记卡':      
        result['未销户贷记卡本月应还'] = df_subset[unclosed_cond] \
            .groupby('PCRID').PayableAmountOfThisMonth.sum(min_count=1) 
        result['未销户贷记卡本月实还'] = df_subset[unclosed_cond] \
            .groupby('PCRID').PaymentAmountOfThisMonth.sum(min_count=1) 
            
        var = '未销户{}本月还款比例'.format(label)
        var1 = '未销户{}本月实还'.format(label) 
        var2 = '未销户{}本月应还'.format(label) 
        ratio = result[var1].fillna(0)/result[var2]
        result[var] = np.round(ratio.replace(np.inf, np.nan),3) 
        
        var = '未销户{}单账户最高还款比例'.format(label)
        result[var] = df_subset[unclosed_cond].groupby('PCRID').PaymentRatio.max()
        
        var = '未销户{}单账户最低还款比例'.format(label)
        result[var] = df_subset[unclosed_cond].groupby('PCRID').PaymentRatio.min()
        
    elif label=='准贷记卡':
        result['未销户准贷记卡透支180天以上未付余额'] = df_subset[unclosed_cond] \
            .groupby('PCRID').UnpaidAmountOfOverdueForMoreThan180days.sum(min_count=1) 
   
    #===未销户已激活=== 
    df_subset_activated = df_subset[~df_subset.AcctStatus.isin(['销户','未激活'])]
    df_subset_activated_no_bad_debt = df_subset[~df_subset.AcctStatus.isin(['销户','未激活','呆账'])]
    
    var = '未销户已激活{}账户数'.format(label)
    result[var] = df_subset_activated.groupby('PCRID').SID.count()
    
    var = '未销户已激活{}发卡机构数'.format(label)
    result[var] = df_subset_activated.groupby('PCRID').ManagementInstituion.nunique()
    
    var = '未销户已激活{}授信总额'.format(label)
    result[var] = df_subset_activated \
        .groupby(['PCRID','ManagementInstituion','LoanIssuingDate']).CreditLine.max() \
        .reset_index().groupby('PCRID').CreditLine.sum(min_count=1)
        
    var = '未销户已激活{}平均授信额度'.format(label)
    result[var] = np.round(df_subset_activated \
        .groupby(['PCRID','ManagementInstituion','LoanIssuingDate']).CreditLine.max() \
        .reset_index().groupby('PCRID').CreditLine.mean(), 2)   
        
    var = '未销户已激活{}最高授信额度'.format(label)   
    result[var] = df_subset_activated.groupby('PCRID').CreditLine.max()
    
    var = '未销户已激活{}最低授信额度'.format(label)   
    result[var] = df_subset_activated.groupby('PCRID').CreditLine.min()
    
    #额度使用率        
    activated_no_bad_debt_credit_amt = df_subset_activated_no_bad_debt\
        .groupby(['PCRID','ManagementInstituion','LoanIssuingDate']).CreditLine.max() \
        .reset_index().groupby('PCRID').CreditLine.sum(min_count=1)
    var = '未销户已激活{}当前额度使用率'.format(label)
    ratio = result['未销户{}已用额度'.format(label)].fillna(0)/activated_no_bad_debt_credit_amt
    result[var] = np.round(ratio.replace(np.inf, np.nan),3)
    
    var = '未销户已激活{}最近6个月平均额度使用率'.format(label)
    ratio = result['未销户{}最近6个月平均使用额度'.format(label)].fillna(0)/activated_no_bad_debt_credit_amt
    result[var] = np.round(ratio.replace(np.inf, np.nan),3)
    
    var = '{}单账户最高当前额度使用率'.format(label)
    result[var] = df_subset_activated_no_bad_debt.groupby('PCRID').UsageRate.max()
    var = '{}单账户最低当前额度使用率'.format(label)
    result[var] = df_subset_activated_no_bad_debt.groupby('PCRID').UsageRate.min()
    
    var = '{}单账户最高近6个月平均额度使用率'.format(label)
    result[var] = df_subset_activated_no_bad_debt.groupby('PCRID').Avg6mUsageRate.max()
    var = '{}单账户最低近6个月平均额度使用率'.format(label)
    result[var] = df_subset_activated_no_bad_debt.groupby('PCRID').Avg6mUsageRate.min()
        
    cutoffs = [50, 70, 90]
    for cutoff in cutoffs:
        var = '当前额度使用率大于{}%的{}账户数'.format(cutoff, label)
        result[var] =  df_subset_activated_no_bad_debt[df_subset_activated_no_bad_debt.UsageRate>(cutoff/100)] \
            .groupby('PCRID').SID.count()
    
    var = '当前额度使用率不足20%的{}账户数'.format(label)
    result[var] =  df_subset_activated_no_bad_debt[df_subset_activated_no_bad_debt.UsageRate<0.2] \
        .groupby('PCRID').SID.count()
        
    for cutoff in cutoffs:
        var = '近6个月平均额度使用率大于{}%的{}账户数'.format(cutoff, label)
        result[var] =  df_subset_activated_no_bad_debt[df_subset_activated_no_bad_debt.Avg6mUsageRate>(cutoff/100)] \
            .groupby('PCRID').SID.count()
    
    var = '近6个月平均额度使用率不足20%的{}账户数'.format(label)
    result[var] =  df_subset_activated_no_bad_debt[df_subset_activated_no_bad_debt.Avg6mUsageRate<0.2] \
        .groupby('PCRID').SID.count()

    #===活跃==
    if label=='贷记卡':
        df_subset_active = df_subset[df_subset.AverageUtilizationInLast6Month>=500]
            
        result['活跃贷记卡账户数'] = df_subset_active \
            .groupby('PCRID').SID.count()
        result['活跃贷记卡发卡机构数'] = df_subset_active \
            .groupby('PCRID').ManagementInstituion.nunique()
        result['活跃贷记卡授信总额'] = df_subset_active \
            .groupby(['PCRID','ManagementInstituion','LoanIssuingDate']).CreditLine.max() \
            .reset_index().groupby('PCRID').CreditLine.sum(min_count=1)
        result['活跃贷记卡平均授信额度'] = np.round(df_subset_active \
            .groupby(['PCRID','ManagementInstituion','LoanIssuingDate']).CreditLine.max() \
            .reset_index().groupby('PCRID').CreditLine.mean(), 2)
        result['活跃贷记卡最高授信额度'] = df_subset_active \
            .groupby('PCRID').CreditLine.max()
        result['活跃贷记卡最低授信额度'] = df_subset_active \
            .groupby('PCRID').CreditLine.min()
        result['活跃贷记卡已用额度'] = df_subset_active \
            .groupby('PCRID').UsedAmount.sum(min_count=1)
        result['活跃贷记卡最近6个月平均使用额度'] = df_subset_active \
            .groupby('PCRID').AverageUtilizationInLast6Month.sum(min_count=1)
        
        ratio = result['活跃贷记卡已用额度'].fillna(0)/result['活跃贷记卡授信总额']
        result['活跃贷记卡当前额度使用率'] = np.round(ratio.replace(np.inf, np.nan),3)
        
        ratio = result['活跃贷记卡最近6个月平均使用额度'].fillna(0)/result['活跃贷记卡授信总额']
        result['活跃贷记卡最近6个月平均额度使用率'] = np.round(ratio.replace(np.inf, np.nan),3)
    
    #===未激活===        
    var = '未激活{}账户数'.format(label) 
    result[var] = df_subset[df_subset.AcctStatus=='未激活'] \
        .groupby('PCRID').SID.count()
        
    var = '未激活{}授信总额'.format(label) 
    result[var] = df_subset[df_subset.AcctStatus=='未激活'] \
        .groupby(['PCRID','ManagementInstituion','LoanIssuingDate']).CreditLine.max() \
        .reset_index().groupby('PCRID').CreditLine.sum(min_count=1)
    
    var = '未激活{}最高授信额度'.format(label) 
    result[var] = df_subset[df_subset.AcctStatus=='未激活'] \
        .groupby('PCRID').CreditLine.max()
    
    #===已销户===
    var = '已销户{}账户数'.format(label) 
    result[var] = df_subset[df_subset.AcctStatus=='销户'] \
        .groupby('PCRID').SID.count()  
    
    #===新开===
    periods = [3,6,12,24]
    for period in periods:
        var = '近{}个月新开{}账户数'.format(period,label)
        result[var] = df_subset[df_subset.DaySinceOpen<=(period*30)] \
            .groupby('PCRID').SID.count()
            
        var = '近{}个月新开{}发卡机构数'.format(period,label)
        result[var] = df_subset[df_subset.DaySinceOpen<=(period*30)] \
            .groupby('PCRID').ManagementInstituion.nunique()
        
        var = '近{}个月新开{}授信总额'.format(period,label)
        result[var] = df_subset[df_subset.DaySinceOpen<=(period*30)] \
            .groupby(['PCRID','ManagementInstituion','LoanIssuingDate']).CreditLine.max() \
            .reset_index().groupby('PCRID').CreditLine.sum(min_count=1)
        
        var = '近{}个月新开{}授信总额占比'.format(period,label)
        var1 = '近{}个月新开{}授信总额'.format(period,label)
        var2 = '{}授信总额'.format(label)    
        ratio = result[var1].fillna(0)/result[var2]
        result[var] = np.round(ratio.replace(np.inf, np.nan),3)
        
        var = '近{}个月新开{}平均授信额度'.format(period,label)
        result[var] = np.round(df_subset[df_subset.DaySinceOpen<=(period*30)] \
            .groupby(['PCRID','ManagementInstituion','LoanIssuingDate']).CreditLine.max() \
            .reset_index().groupby('PCRID').CreditLine.mean(),2)
        
        var = '近{}个月新开{}最高授信额度'.format(period,label)
        result[var] = df_subset[df_subset.DaySinceOpen<=(period*30)] \
            .groupby('PCRID').CreditLine.max()
            
        var = '近{}个月新开{}最低授信额度'.format(period,label)
        result[var] = df_subset[df_subset.DaySinceOpen<=(period*30)] \
            .groupby('PCRID').CreditLine.min()
            
        var = '近{}个月新开{}额度不超过5000元账户数'.format(period,label)
        result[var] = df_subset[(df_subset.DaySinceOpen<=(period*30)) & (df_subset.CreditLine<=5000)] \
            .groupby('PCRID').SID.count()
            
        if label=='贷记卡':
            var = '近{}个月新开{}激活比例'.format(period,label)
            var1 = '近{}个月新开{}已激活账户数'.format(period,label)
            var2 = '近{}个月新开{}账户数'.format(period,label)
            result[var1] = df_subset[(df_subset.DaySinceOpen<=(period*30)) & (df_subset.AcctStatus!='未激活')] \
                .groupby('PCRID').SID.count()
            ratio = result[var1].fillna(0)/result[var2]
            result[var] = np.round(ratio.replace(np.inf, np.nan),3)
            
    var = '最近一张{}的授信额度'.format(label)       
    open_rank = df_subset.groupby('PCRID').DaySinceOpen.rank(method='min')
    result[var] = df_subset[open_rank==1].groupby('PCRID').CreditLine.max()
    
    var = '最近一张{}的开立时间距今月份数'.format(label)
    result[var] = df_subset.groupby('PCRID').MonSinceOpen.min()
    
    #===在册===
    df_subset_never_ovd = df_subset[~df_subset.SID.isin(ever_ovd_ids)]
    periods = [3,6,12,24]
    for period in periods:
        var = '在册{}个月及以上{}从未逾期账户数'.format(period,label)
        result[var] = df_subset_never_ovd[df_subset_never_ovd.LoanLife>=(period*30)] \
            .groupby('PCRID').SID.count()
        
        var = '在册{}个月及以上{}从未逾期账户最大授信额度'.format(period,label)
        result[var] = df_subset_never_ovd[df_subset_never_ovd.LoanLife>=(period*30)] \
            .groupby('PCRID').CreditLine.max()

    rtn_result = pd.DataFrame(result, index=pd.unique(df_subset.PCRID))
    if label=='准贷记卡':
        rtn_result.columns = rtn_result.columns.str.replace('已用额度','透支余额')
        rtn_result.columns = rtn_result.columns.str.replace('最近6个月平均使用额度','最近6个月平均透支余额')
        rtn_result.columns = rtn_result.columns.str.replace('当前额度使用率','透支余额占授信总额比例')
        rtn_result.columns = rtn_result.columns.str.replace('近6个月平均额度使用率','近6个月平均透支余额占授信总额比例')
        rtn_result.columns = rtn_result.columns.str.replace('最大使用额度','最大透支余额')

    return rtn_result

def parse_loan_and_credit_card_detail():
    df_subset = df_CreditTransJoined[df_CreditTransJoined.CreditType.isin([1,2,3,4,5])]
    df_subset_no_semi = df_CreditTransJoined[df_CreditTransJoined.CreditType.isin([1,2,3,4])]
    result = pd.DataFrame(index=pd.unique(df_subset.PCRID))  
    
    label = '贷款及信用卡'
    label_no_semi = '贷款及贷记卡'
    
    #===逾期===
    var = '{}当前逾期账户数'.format(label_no_semi)
    result[var] = df_subset_no_semi[df_subset_no_semi.CurrentDelinquencyTerm>0] \
        .groupby('PCRID').SID.count()
    
    var = '{}当前逾期90+账户数'.format(label_no_semi)
    result[var] = df_subset_no_semi[df_subset_no_semi.CurrentDelinquencyTerm>3] \
        .groupby('PCRID').SID.count()
    
    var = '{}当前逾期总额'.format(label_no_semi)
    result[var] = df_subset_no_semi.groupby('PCRID').CurrentArrearAmount.sum(min_count=1) 
    
    var = '{}当前最大逾期期数'.format(label_no_semi)
    result[var] = df_subset_no_semi.groupby('PCRID').CurrentDelinquencyTerm.max()
    
    var = '{}当前最大逾期金额'.format(label_no_semi)
    result[var] = df_subset_no_semi.groupby('PCRID').CurrentArrearAmount.max()
    
        
    var = '{}账户状态正常的账户数'.format(label)
    result[var] = df_subset[df_subset.AcctStatus=='正常'] \
        .groupby('PCRID').SID.count()
    
    risky_status = ['逾期','呆账','银行止付','担保物不足','强制平仓','司法追偿','冻结','止付']
    var = '{}账户状态不良的账户数'.format(label)
    result[var] = df_subset[df_subset.AcctStatus.isin(risky_status)] \
        .groupby('PCRID').SID.count()
    
    var = '{}账户状态不良的账户余额'.format(label)
    result[var] = df_subset[df_subset.AcctStatus.isin(risky_status)] \
        .groupby('PCRID').Bal.sum(min_count=1)
        
    highly_risky_status =  ['呆账','银行止付','强制平仓','司法追偿','冻结']
    var = '{}账户状态高风险的账户数'.format(label)
    result[var] = df_subset[df_subset.AcctStatus.isin(highly_risky_status)] \
        .groupby('PCRID').SID.count()
        
    
    #===全状态===
    var = '{}账户数'.format(label)    
    result[var] = df_subset.groupby('PCRID').SID.count()  
    
    var = '{}管理机构数'.format(label)    
    result[var] = df_subset.groupby('PCRID').ManagementInstituion.nunique()
    
    var = '{}授信总额'.format(label)    
    df_loan_amt = df_subset.loc[df_subset.CreditType.isin([1,2,3]),['PCRID','CreditAmt']]
    df_credit_card_amt = df_subset[df_subset.CreditType.isin([4,5])] \
        .groupby(['PCRID','CreditType','ManagementInstituion','LoanIssuingDate']).CreditAmt.max() \
        .reset_index()[['PCRID','CreditAmt']]
    df_tot_amt = pd.concat([df_loan_amt,df_credit_card_amt])
    result[var] = df_tot_amt.groupby('PCRID').CreditAmt.sum(min_count=1)
    
    var = '{}最高授信额度'.format(label)    
    result[var] = df_subset.groupby('PCRID').CreditAmt.max()
    
    var = '{}最低授信额度'.format(label)    
    result[var] = df_subset.groupby('PCRID').CreditAmt.min()
    
    var = '信用类{}账户数'.format(label)    
    result[var] = df_subset[df_subset.GuarantorType=='信用/免担保'] \
        .groupby('PCRID').SID.count()  
    
    var = '信用类{}管理机构数'.format(label)    
    result[var] = df_subset[df_subset.GuarantorType=='信用/免担保'] \
        .groupby('PCRID').ManagementInstituion.nunique()
    
    var = '信用类{}授信总额'.format(label)    
    df_loan_amt = df_subset.loc[(df_subset.GuarantorType=='信用/免担保') & df_subset.CreditType.isin([1,2,3]),['PCRID','CreditAmt']]
    df_credit_card_amt = df_subset[(df_subset.GuarantorType=='信用/免担保') & df_subset.CreditType.isin([4,5])] \
        .groupby(['PCRID','CreditType','ManagementInstituion','LoanIssuingDate']).CreditAmt.max() \
        .reset_index()[['PCRID','CreditAmt']]
    df_tot_amt = pd.concat([df_loan_amt,df_credit_card_amt])
    result[var] = df_tot_amt.groupby('PCRID').CreditAmt.sum(min_count=1)
    
    var = '信用类{}最高授信额度'.format(label)    
    result[var] = df_subset[df_subset.GuarantorType=='信用/免担保'] \
        .groupby('PCRID').CreditAmt.max()
    
    var = '{}额度不超过5000元账户数'.format(label_no_semi)    
    result[var] = df_subset_no_semi[df_subset_no_semi.CreditAmt<=5000].groupby('PCRID').SID.count()
    
    #===负债===
    sum1 = df_subset[df_subset.CreditType.isin([1,2,3])] \
        .groupby('PCRID').Bal.sum(min_count=1)
    sum2 = df_subset[df_subset.CreditType.isin([4,5])] \
        .groupby('PCRID').UsedAmount.sum(min_count=1)
    total_sum = pd.DataFrame({'sum1':sum1,'sum2':sum2}).sum(axis=1, min_count=1)
    result['总负债'] = total_sum
    
    sum1 = df_subset[(df_subset.CreditType.isin([1,2,3])) & (df_subset.GuarantorType=="信用/免担保")] \
        .groupby('PCRID').Bal.sum(min_count=1)
    sum2 = df_subset[(df_subset.CreditType.isin([4,5])) & (df_subset.GuarantorType=="信用/免担保")] \
        .groupby('PCRID').UsedAmount.sum(min_count=1)
    total_sum = pd.DataFrame({'sum1':sum1,'sum2':sum2}).sum(axis=1, min_count=1)
    result['信用类总负债'] = total_sum    
  
    sum1 = df_subset[(df_subset.CreditType.isin([1,2,3]))] \
        .groupby('PCRID').PayableAmountOfThisMonth.sum(min_count=1)
    sum2 = df_subset[(df_subset.CreditType.isin([4,5]))] \
        .groupby('PCRID').AverageUtilizationInLast6Month.sum(min_count=1)
    total_sum = pd.DataFrame({'sum1':sum1,'sum2':sum2}).sum(axis=1, min_count=1)
    result['月负债'] = total_sum
    
    sum1 = df_subset[(df_subset.CreditType.isin([1,2,3])) & (df_subset.GuarantorType=="信用/免担保")] \
        .groupby('PCRID').PayableAmountOfThisMonth.sum(min_count=1)
    sum2 = df_subset[(df_subset.CreditType.isin([4,5])) & (df_subset.GuarantorType=="信用/免担保")] \
        .groupby('PCRID').AverageUtilizationInLast6Month.sum(min_count=1)
    total_sum = pd.DataFrame({'sum1':sum1,'sum2':sum2}).sum(axis=1, min_count=1)
    result['信用类月负债'] = total_sum
    
    #===未结清(未销户)===
    unclosed_cond = (~df_subset.AcctStatus.isin(['结清','转出','销户']))
    
    var = '未结清(未销户){}账户数'.format(label)    
    result[var] = df_subset[unclosed_cond] \
        .groupby('PCRID').SID.count()
    
    var = '未结清(未销户){}管理机构数'.format(label)    
    result[var] = df_subset[unclosed_cond] \
        .groupby('PCRID').ManagementInstituion.nunique()
    
    var = '未结清(未销户){}授信总额'.format(label)    
    df_loan_amt = df_subset.loc[df_subset.CreditType.isin([1,2,3]) & unclosed_cond,['PCRID','CreditAmt']]
    df_credit_card_amt = df_subset[df_subset.CreditType.isin([4,5]) & unclosed_cond] \
        .groupby(['PCRID','CreditType','ManagementInstituion','LoanIssuingDate']).CreditAmt.max() \
        .reset_index()[['PCRID','CreditAmt']]
    df_tot_amt = pd.concat([df_loan_amt,df_credit_card_amt])
    result[var] = df_tot_amt.groupby('PCRID').CreditAmt.sum(min_count=1)
    
    var = '未结清(未销户){}最高授信额度'.format(label) 
    result[var] = df_subset[unclosed_cond] \
        .groupby('PCRID').CreditAmt.max()
        
    var = '未结清(未销户){}最低授信额度'.format(label) 
    result[var] = df_subset[unclosed_cond] \
        .groupby('PCRID').CreditAmt.min()
        
    var = '未结清(未销户){}本月实还'.format(label) 
    result[var] = df_subset[unclosed_cond] \
        .groupby('PCRID').PaymentAmountOfThisMonth.sum(min_count=1)
        
    var = '未结清(未销户)信用类{}账户数'.format(label)    
    result[var] = df_subset[unclosed_cond & (df_subset.GuarantorType=='信用/免担保')] \
        .groupby('PCRID').SID.count()
    
    var = '未结清(未销户)信用类{}管理机构数'.format(label)    
    result[var] = df_subset[unclosed_cond & (df_subset.GuarantorType=='信用/免担保')] \
        .groupby('PCRID').ManagementInstituion.nunique()
    
    var = '未结清(未销户)信用类{}授信总额'.format(label)    
    df_loan_amt = df_subset.loc[df_subset.CreditType.isin([1,2,3]) & unclosed_cond & (df_subset.GuarantorType=='信用/免担保'),['PCRID','CreditAmt']]
    df_credit_card_amt = df_subset[df_subset.CreditType.isin([4,5]) & unclosed_cond & (df_subset.GuarantorType=='信用/免担保')] \
        .groupby(['PCRID','CreditType','ManagementInstituion','LoanIssuingDate']).CreditAmt.max() \
        .reset_index()[['PCRID','CreditAmt']]
    df_tot_amt = pd.concat([df_loan_amt,df_credit_card_amt])
    result[var] = df_tot_amt.groupby('PCRID').CreditAmt.sum(min_count=1)
    
    var = '未结清(未销户)信用类{}最高授信额度'.format(label) 
    result[var] = df_subset[unclosed_cond & (df_subset.GuarantorType=='信用/免担保')] \
        .groupby('PCRID').CreditAmt.max()
    
    #===新开===
    periods = [3,6,12,24]
    for period in periods:
        var = '近{}个月新开{}账户数'.format(period,label)
        result[var] = df_subset[df_subset.DaySinceOpen<=(period*30)] \
            .groupby('PCRID').SID.count()
            
        var = '近{}个月新开{}管理机构数'.format(period,label)
        result[var] = df_subset[df_subset.DaySinceOpen<=(period*30)] \
            .groupby('PCRID').ManagementInstituion.nunique()
        
        var = '近{}个月新开{}授信总额'.format(period,label)
        df_loan_amt = df_subset.loc[(df_subset.DaySinceOpen<=(period*30)) & df_subset.CreditType.isin([1,2,3]),['PCRID','CreditAmt']]
        df_credit_card_amt = df_subset[(df_subset.DaySinceOpen<=(period*30)) & df_subset.CreditType.isin([4,5])] \
            .groupby(['PCRID','CreditType','ManagementInstituion','LoanIssuingDate']).CreditAmt.max() \
            .reset_index()[['PCRID','CreditAmt']]
        df_tot_amt = pd.concat([df_loan_amt,df_credit_card_amt])        
        result[var] = df_tot_amt.groupby('PCRID').CreditAmt.sum(min_count=1)
        
        var = '近{}个月新开{}授信总额占比'.format(period,label)
        var1 = '近{}个月新开{}授信总额'.format(period,label)
        var2 = '{}授信总额'.format(label)    
        ratio = result[var1].fillna(0)/result[var2]
        result[var] = np.round(ratio.replace(np.inf, np.nan),3)        
        
        var = '近{}个月新开{}最高授信额度'.format(period,label)
        result[var] = df_subset[df_subset.DaySinceOpen<=(period*30)] \
            .groupby('PCRID').CreditAmt.max()
        
        var = '近{}个月新开{}最低授信额度'.format(period,label)
        result[var] = df_subset[df_subset.DaySinceOpen<=(period*30)] \
            .groupby('PCRID').CreditAmt.min()
            
        var = '近{}个月新开{}额度不超过5000元账户数'.format(period,label_no_semi)
        result[var] = df_subset_no_semi[(df_subset_no_semi.DaySinceOpen<=(period*30)) & (df_subset_no_semi.CreditAmt<=5000)] \
            .groupby('PCRID').SID.count()
        
    #===在册===
    df_subset_never_ovd = df_subset[~df_subset.SID.isin(ever_ovd_ids)]
    periods = [3,6,12,24]
    for period in periods:
        var = '在册{}个月及以上{}从未逾期账户数'.format(period,label)
        result[var] = df_subset_never_ovd[df_subset_never_ovd.LoanLife>=(period*30)] \
            .groupby('PCRID').SID.count()
        
        var = '在册{}个月及以上{}从未逾期账户最大授信额度'.format(period,label)
        result[var] = df_subset_never_ovd[df_subset_never_ovd.LoanLife>=(period*30)] \
            .groupby('PCRID').CreditAmt.max()
        
    result['从未逾期贷款及信用卡账户距今最大账龄'] = df_subset_never_ovd \
        .groupby('PCRID').LoanLife.max()
    return result

def parse_pmt_record(id_list=None,label=None):
    if id_list is None:
        df_subset = df_PmtRecord
    else:
        df_subset = df_PmtRecord[df_PmtRecord.PSID.isin(id_list)]
    result = {}
    pcr_index = pd.unique(df_subset.PCRID)

    if label is None:
        label = ''

    var = '{}最近一次逾期距今月份数'.format(label)
    result[var] = df_subset[(df_subset.StatusNum > 0)] \
        .groupby('PCRID').MonSincePmt.min()

    var = '{}单月最大逾期总额'.format(label)
    ovd_amt_summary = df_subset \
        .groupby(['PCRID', 'RepaymentYearMon']).Amount.sum().rename('MonthlyAmount')
    result[var] = ovd_amt_summary.reset_index().groupby('PCRID').MonthlyAmount.max()

    periods = [3, 6, 12, 24, 36, 60]
    for period in periods:
        var = '近{}个月{}最大逾期期数'.format(period, label)
        result[var] = df_subset[(df_subset.MonSincePmt < period) & (df_subset.StatusNum <= 7)] \
            .groupby('PCRID').StatusNum.max()

        var = '近{}个月{}逾期次数'.format(period, label)
        result[var] = df_subset[(df_subset.MonSincePmt < period) & (df_subset.StatusNum > 0)] \
            .groupby('PCRID').PSID.count()

        if label in ['贷款', '贷记卡', '准贷记卡', '贷款及信用卡']:
            var = '近{}个月{}单账户最大累计逾期次数'.format(period, label)
            filtered_data = df_subset[
                (df_subset.MonSincePmt < period) & (df_subset.StatusNum <= 7) & (df_subset.StatusNum > 0)]
            group_counts = filtered_data.groupby('PSID').size()
            max_count = group_counts.max() if not group_counts.empty else 0
            result[var] = max_count

            var = '近{}个月{}逾期账户数'.format(period, label)
            result[var] = df_subset[(df_subset.MonSincePmt < period) & (df_subset.StatusNum > 0)] \
                .groupby('PCRID').PSID.nunique()

            var = '近{}个月{}逾期1期次数'.format(period, label)
            result[var] = df_subset[(df_subset.MonSincePmt < period) & (df_subset.StatusNum == 1)] \
                .groupby('PCRID').PSID.count()

            var = '近{}个月{}逾期2期及以上次数'.format(period, label)
            result[var] = df_subset[(df_subset.MonSincePmt < period) & (df_subset.StatusNum >= 2)] \
                .groupby('PCRID').PSID.count()

            var = '近{}个月{}逾期3期及以上次数'.format(period, label)
            result[var] = df_subset[(df_subset.MonSincePmt < period) & (df_subset.StatusNum >= 3)] \
                .groupby('PCRID').PSID.count()

            var = '近{}个月{}逾期4期及以上次数'.format(period, label)
            result[var] = df_subset[(df_subset.MonSincePmt < period) & (df_subset.StatusNum >= 4)] \
                .groupby('PCRID').PSID.count()

            var = '近{}个月{}逾期5期及以上次数'.format(period, label)
            result[var] = df_subset[(df_subset.MonSincePmt < period) & (df_subset.StatusNum >= 5)] \
                .groupby('PCRID').PSID.count()

            var = '近{}个月{}逾期6期及以上次数'.format(period, label)
            result[var] = df_subset[(df_subset.MonSincePmt < period) & (df_subset.StatusNum >= 6)] \
                .groupby('PCRID').PSID.count()

            var = '近{}个月{}还款状态为B的次数'.format(period, label)
            result[var] = df_subset[(df_subset.MonSincePmt < period) & (df_subset.StatusNum == 8)] \
                .groupby('PCRID').PSID.count()

            var = '近{}个月{}还款状态为D的次数'.format(period, label)
            result[var] = df_subset[(df_subset.MonSincePmt < period) & (df_subset.StatusNum == 9)] \
                .groupby('PCRID').PSID.count()

            var = '近{}个月{}还款状态为Z的次数'.format(period, label)
            result[var] = df_subset[(df_subset.MonSincePmt < period) & (df_subset.StatusNum == 10)] \
                .groupby('PCRID').PSID.count()

            var = '近{}个月{}还款状态为G的次数'.format(period, label)
            result[var] = df_subset[(df_subset.MonSincePmt < period) & (df_subset.StatusNum == 11)] \
                .groupby('PCRID').PSID.count()

            var = '近{}个月{}逾期金额超过500元逾期次数'.format(period, label)
            result[var] = df_subset[
                (df_subset.MonSincePmt < period) & (df_subset.Amount > 500) & (df_subset.StatusNum > 0)] \
                .groupby('PCRID').PSID.count()

            var = '近{}个月{}逾期金额超过500元最大逾期期数'.format(period, label)
            result[var] = df_subset[
                (df_subset.MonSincePmt < period) & (df_subset.Amount > 500) & (df_subset.StatusNum <= 7)] \
                .groupby('PCRID').StatusNum.max()

            var = '近{}个月{}单月最大逾期总额'.format(period, label)
            ovd_amt_summary = df_subset[(df_subset.MonSincePmt < period)] \
                .groupby(['PCRID', 'RepaymentYearMon']).Amount.sum().rename('MonthlyAmount')
            result[var] = ovd_amt_summary.reset_index().groupby('PCRID').MonthlyAmount.max()

            var = '近{}个月{}最大连续逾期次数'.format(period, label)
            max_ovd_summary = df_subset[(df_subset.MonSincePmt < period)] \
                .groupby(['PCRID', 'group_id']).Ovd.sum(min_count=1).rename('ConsecutiveOvdCnt')
            result[var] = max_ovd_summary.reset_index().groupby('PCRID').ConsecutiveOvdCnt.max()

            var = '近{}个月{}正常还款的月份数'.format(period, label)
            max_flag_summary = df_subset[(df_subset.MonSincePmt < period)] \
                .groupby(['PCRID', 'RepaymentYearMon']).Flag.max()
            result[var] = max_flag_summary[max_flag_summary == 1].reset_index() \
                .groupby('PCRID').Flag.count()

            var = '近{}个月{}逾期1期且逾期金额不超过1000元逾期次数'.format(period, label)
            result[var] = df_subset[
                (df_subset.MonSincePmt < 6) & (df_subset.Amount <= 1000) & (df_subset.StatusNum == 1)] \
                .groupby('PCRID').PSID.count()

    # 一次性创建DataFrame
    rtn_result = pd.DataFrame(result, index=pcr_index)

    return rtn_result

def parse_pmt_un_record(id_list=None,label=None):
    if id_list is None:
        df_subset = df_PmtRecord
    else:
        df_subset = df_PmtRecord[df_PmtRecord.PSID.isin(id_list)]
    result = pd.DataFrame(index=pd.unique(df_subset.PCRID))

    if label is None:
        label=''

    var = '未结清(未销户){}最近一次逾期距今月份数'.format(label)
    result[var] = df_subset[(df_subset.StatusNum>0)] \
        .groupby('PCRID').MonSincePmt.min()

    periods = [3,6,12,24,36,60]
    for period in periods:
        var = '近{}个月未结清(未销户){}单账户最大累计逾期次数'.format(period, label)
        filtered_data = df_subset[
            (df_subset.MonSincePmt < period) & (df_subset.StatusNum <= 7) & (df_subset.StatusNum > 0)]
        group_counts = filtered_data.groupby('PSID').size()
        max_count = group_counts.max() if not group_counts.empty else 0
        result[var] = max_count

        var = '近{}个月未结清(未销户){}最大逾期期数'.format(period,label)
        result[var] = df_subset[(df_subset.MonSincePmt<period)  & (df_subset.StatusNum<=7)] \
            .groupby('PCRID').StatusNum.max()

        var = '近{}个月未结清(未销户){}逾期次数'.format(period,label)
        result[var] = df_subset[(df_subset.MonSincePmt<period) & (df_subset.StatusNum>0)] \
            .groupby('PCRID').PSID.count()

        if label in ['贷款','信用卡']:
            var = '近{}个月未结清(未销户){}单月最大逾期总额'.format(period,label)
            ovd_amt_summary = df_subset \
                .groupby(['PCRID', 'RepaymentYearMon']).Amount.sum().rename('MonthlyAmount')
            result[var] = ovd_amt_summary.reset_index().groupby('PCRID').MonthlyAmount.max()

            var = '近{}个月未结清(未销户){}逾期账户数'.format(period,label)
            result[var] = df_subset[(df_subset.MonSincePmt<period) & (df_subset.StatusNum>0)] \
                .groupby('PCRID').PSID.nunique()

            var = '近{}个月未结清(未销户){}逾期1期次数'.format(period, label)
            result[var] = df_subset[(df_subset.MonSincePmt < period) & (df_subset.StatusNum == 1)] \
                .groupby('PCRID').PSID.count()

            var = '近{}个月未结清(未销户){}逾期2期及以上次数'.format(period,label)
            result[var] = df_subset[(df_subset.MonSincePmt<period) & (df_subset.StatusNum>=2)] \
                .groupby('PCRID').PSID.count()

            var = '近{}个月未结清(未销户){}逾期3期及以上次数'.format(period,label)
            result[var] = df_subset[(df_subset.MonSincePmt<period) & (df_subset.StatusNum>=3)] \
                .groupby('PCRID').PSID.count()

            var = '近{}个月未结清(未销户){}逾期4期及以上次数'.format(period,label)
            result[var] = df_subset[(df_subset.MonSincePmt<period) & (df_subset.StatusNum>=4)] \
                .groupby('PCRID').PSID.count()

            var = '近{}个月未结清(未销户){}逾期金额超过500元逾期次数'.format(period,label)
            result[var] = df_subset[(df_subset.MonSincePmt<period) & (df_subset.Amount>500) & (df_subset.StatusNum>0)] \
                .groupby('PCRID').PSID.count()

            var = '近{}个月未结清(未销户){}逾期金额超过500元最大逾期期数'.format(period,label)
            result[var] = df_subset[(df_subset.MonSincePmt<period) & (df_subset.Amount>500)  & (df_subset.StatusNum<=7)] \
                .groupby('PCRID').StatusNum.max()

            var = '近{}个月未结清(未销户){}单月最大逾期总额'.format(period,label)
            ovd_amt_summary = df_subset[(df_subset.MonSincePmt<period)] \
                .groupby(['PCRID','RepaymentYearMon']).Amount.sum().rename('MonthlyAmount')
            result[var] = ovd_amt_summary.reset_index().groupby('PCRID').MonthlyAmount.max()

            var = '近{}个月未结清(未销户){}最大连续逾期次数'.format(period,label)
            max_ovd_summary =  df_subset[(df_subset.MonSincePmt<period)] \
                .groupby(['PCRID','group_id']).Ovd.sum(min_count=1).rename('ConsecutiveOvdCnt')
            result[var] = max_ovd_summary.reset_index().groupby('PCRID').ConsecutiveOvdCnt.max()

            var = '近{}个月未结清(未销户){}正常还款的月份数'.format(period,label)
            max_flag_summary = df_subset[(df_subset.MonSincePmt<period)] \
                .groupby(['PCRID','RepaymentYearMon']).Flag.max()
            result[var] = max_flag_summary[max_flag_summary==1].reset_index() \
                .groupby('PCRID').Flag.count()

            var = '近{}个月未结清(未销户){}逾期1期且逾期金额不超过1000元逾期次数'.format(period, label)
            result[var] = df_subset[(df_subset.MonSincePmt < period) & (df_subset.Amount <= 1000) & (df_subset.StatusNum == 1)] \
                .groupby('PCRID').PSID.count()

    return result

def parse_special_trans():
    result = pd.DataFrame(index=pd.unique(df_CreditSpecialTransaction.PCRID))
    periods = [6,12,24,60] 
    trans_list = ['展期','提前还款','提前结清','信用卡个性化分期']
    for period in periods:
        for trans in trans_list:
            var = '近{}个月{}账户数'.format(period, trans)
            result[var] = df_CreditSpecialTransaction[(df_CreditSpecialTransaction.SpecialTransactionType==trans) \
                & (df_CreditSpecialTransaction.DaySinceTrans<=(period*30))].groupby('PCRID') \
                .PSID.nunique()
        
        risky_trans = ["展期","担保人（第三方）代偿","以资抵债","强制平仓，未结清",
                       "强制平仓，已结清","司法追偿","资产剥离","资产转让","强制平仓"]
        var = '近{}个月有不良特殊交易的账户数'.format(period)
        result[var] = df_CreditSpecialTransaction[(df_CreditSpecialTransaction.SpecialTransactionType.isin(risky_trans)) \
                & (df_CreditSpecialTransaction.DaySinceTrans<=(period*30))].groupby('PCRID') \
                .PSID.nunique()   
    return result

def parse_large_amt_installment():
    df_subset = df_LargeAmountSpecialInstalme[df_LargeAmountSpecialInstalme.PCRID.notna()]
    result = pd.DataFrame(index=pd.unique(df_subset.PCRID))
    result['大额专项分期账户数'] = df_LargeAmountSpecialInstalme \
        .groupby('PCRID').SID2.count()
    result['大额专项分期额度'] = df_LargeAmountSpecialInstalme \
        .groupby('PCRID').SpecialInstalmentCreditLine.sum(min_count=1)
    result['大额专项分期已用金额'] = df_LargeAmountSpecialInstalme \
        .groupby('PCRID').SpecialInstalmentUsedAmount.sum(min_count=1)
    
    ratio = result['大额专项分期已用金额'].fillna(0)/result['大额专项分期额度']
    result['大额专项分期额度使用率'] = np.round(ratio.replace(np.inf, np.nan),3)

    #未销户大额专项分期
    filtered_df2 = df_LargeAmountSpecialInstalme[df_LargeAmountSpecialInstalme['SID'].isin(unclosed_credit_card_accountnumbers)]
    if not filtered_df2.empty :
        result['未销户大额专项分期账户数'] = filtered_df2.groupby('PCRID').SID2.count()
        result['未销户大额专项分期额度'] =filtered_df2.groupby('PCRID').SpecialInstalmentCreditLine.sum(min_count=1)
        result['未销户大额专项分期已用金额'] = filtered_df2.groupby('PCRID').SpecialInstalmentUsedAmount.sum(min_count=1)
        result['近6个月新开户大额专项分期账户数'] = filtered_df2[filtered_df2['SpecialInstalmentBeginDate'] >= report_dates['ReportDate'].iloc[0] - pd.DateOffset(months=6)].groupby('PCRID').SID2.count()
    else:
        result['未销户大额专项分期账户数'] = np.nan
        result['未销户大额专项分期额度'] = np.nan
        result['未销户大额专项分期已用金额'] = np.nan
        result['近6个月新开户大额专项分期账户数'] = np.nan
    return result

def parse_related_payment(cond=None, label=None):
    if cond is None:
        df_subset = df_CreditRelatedRepayment
    else:
        df_subset = df_CreditRelatedRepayment[cond]
    result = pd.DataFrame(index=pd.unique(df_subset.PCRID)) 
    
    var = '{}五级分类非正常账户数'.format(label)
    result[var] = df_subset[df_subset.SecuredLoanGrade.isin(['关注','次级','可疑','损失'])] \
        .groupby('PCRID').SID.count()
		
    
    var = '{}五级分类非正常账户余额'.format(label)
    result[var] = df_subset[df_subset.SecuredLoanGrade.isin(['关注','次级','可疑','损失'])] \
        .groupby('PCRID').BadDebtAmount.sum(min_count=1)
            
    periods = [3,6,12] 
    for period in periods:
        var = '近{}个月新增{}账户数'.format(period, label)
        result[var] = df_subset[df_subset.DaySinceOpen<=(period*30)] \
            .groupby('PCRID').SID.count()
            
        var = '近{}个月新增{}金额(不含外币)'.format(period, label)
        result[var] = df_subset[(df_subset.DaySinceOpen<=(period*30)) & (df_subset.Currency=='人民币元')] \
            .groupby('PCRID').SecuredAmount.sum(min_count=1)
    return result

def parse_noncredit():
    result = pd.DataFrame(index=pd.unique(df_NonCreditTransaction.PCRID))
    internet_cnt = df_NonCreditTransaction[df_NonCreditTransaction.BusinessType=='互联网接入'] \
        .groupby('PCRID').SID.count()
		
    result['后付费业务类型是否包含互联网接入'] = np.sign(internet_cnt)
    
    trans_list = ['固定电话','移动电话','互联网接入','数据专线及集群业务',
                  '卫星业务','组合业务','其他业务']
    for trans in trans_list:
        var = '{}当前欠费账户数'.format(trans)
        result[var] = df_NonCreditTransaction[(df_NonCreditTransaction.BusinessType==trans) & (df_NonCreditTransaction.PaymentStatus=="欠费")] \
            .groupby('PCRID').SID.count()
			
        
        var = '{}当前欠费金额'.format(trans)
        result[var] = df_NonCreditTransaction[(df_NonCreditTransaction.BusinessType==trans)] \
            .groupby('PCRID').ArrearAmount.sum(min_count=1)
            
        var = '{}最早开通日期距今天数'.format(trans)
        result[var] = df_NonCreditTransaction[(df_NonCreditTransaction.BusinessType==trans)] \
            .groupby('PCRID').DaySinceOpen.max()
    return result

def parse_tax_owe():
    result = pd.DataFrame(index=pd.unique(df_OwingTaxInformation.PCRID))
    result['最近一次欠税统计日期距今天数'] = df_OwingTaxInformation \
        .groupby('PCRID').DaySinceRecord.min()
    
    periods = [12,24]
    for period in periods:
        var = '最近{}个月欠税总额'.format(period)
        result[var] = df_OwingTaxInformation[df_OwingTaxInformation.DaySinceRecord<=(period*30)] \
            .groupby('PCRID').TotalTaxArrears.sum(min_count=1)
        var = '最近{}个月欠税记录数'.format(period)
        result[var] = df_OwingTaxInformation[df_OwingTaxInformation.DaySinceRecord<=(period*30)] \
            .groupby('PCRID').SID.count()
			
    return result

def parse_civil_case():        
    result = pd.DataFrame(index=pd.unique(df_CivilJudgmentRecords.PCRID))
    result['最近一次民事判决立案日期距今天数'] = df_CivilJudgmentRecords \
        .groupby('PCRID').DaySinceRecord.min()
        
    result['借贷纠纷记录数'] = \
        df_CivilJudgmentRecords[df_CivilJudgmentRecords.Cause.astype(str).str.contains('借贷纠纷') | \
        df_CivilJudgmentRecords.Cause.astype(str).str.contains('借款合同纠纷') | df_CivilJudgmentRecords.Cause.astype(str).str.contains('信用卡纠纷')] \
        .groupby('PCRID').SID.count()
		
            
    periods = [12,24]
    for period in periods:
        var = '最近{}个月民事判决记录数'.format(period)
        result[var] = df_CivilJudgmentRecords[df_CivilJudgmentRecords.DaySinceRecord<=(period*30)] \
            .groupby('PCRID').SID.count()
			
    return result

def parse_enforcement():       
    result = pd.DataFrame(index=pd.unique(df_EnforcementRecords.PCRID))
    result['最近一次强制执行立案日期距今天数'] = df_EnforcementRecords \
        .groupby('PCRID').DaySinceRecord.min()
    
    result['强制执行申请执行标的总价值'] = df_EnforcementRecords \
        .groupby('PCRID').ApplicationExecutionAmount.sum(min_count=1)
        
    result['失信被执行人记录数'] = \
        df_EnforcementRecords[df_EnforcementRecords.CaseStatus.astype(str).str.contains('失信被执行')] \
        .groupby('PCRID').SID.count()
		
    
    result['失信被执行人最近立案日期距今天数'] = \
        df_EnforcementRecords[df_EnforcementRecords.CaseStatus.astype(str).str.contains('失信被执行')] \
        .groupby('PCRID').DaySinceRecord.min()
    
    periods = [12,24]
    for period in periods:
        var = '最近{}个月强制执行记录数'.format(period)
        result[var] = df_EnforcementRecords[df_EnforcementRecords.DaySinceRecord<=(period*30)] \
            .groupby('PCRID').SID.count()
			
    return result

def parse_admin_punish(): 
    result = pd.DataFrame(index=pd.unique(df_PunishmentRecords.PCRID))
    result['最近一次行政处罚生效日期距今天数'] = df_PunishmentRecords \
        .groupby('PCRID').DaySinceRecord.min()
    
    result['恶意逃废债记录数'] = df_PunishmentRecords[df_PunishmentRecords.PunishingMatter.astype(str).str.contains('恶意逃废债')] \
        .groupby('PCRID').SID.count()
		
        
    result['行政处罚最大处罚金额'] = df_PunishmentRecords.groupby('PCRID').PunishmentAmount.max()
    
    periods = [12,24]
    for period in periods:
        var = '最近{}个月行政处罚记录数'.format(period)
        result[var] = df_PunishmentRecords[df_PunishmentRecords.DaySinceRecord<=(period*30)] \
            .groupby('PCRID').SID.count()   
			
    return result

def parse_housing_fund():
    result = pd.DataFrame(index=pd.unique(df_HousingProvidentFundRecords.PCRID))  
    latest_record = df_HousingProvidentFundRecords[(df_HousingProvidentFundRecords.EndMonthRank==1) & \
            (df_HousingProvidentFundRecords.UpdateRank==1) & (df_HousingProvidentFundRecords.SerialRank==1)].set_index('PCRID')
    
    result['最近一次公积金缴费状态'] = latest_record.PaymentStatus
    result['最近一次公积金月缴存额'] = latest_record.MonthPayAmount
    result['最近一次公积金个人缴存比例'] = latest_record.IndividualRatio
    result['最近一次公积金单位缴存比例'] = latest_record.CompanyRatio
    result['最近一次公积金月缴存额倒推月收入'] = latest_record.Income
    result['最近一次公积金参缴地'] = latest_record.PaymentPlace
    result['最近一家公司的公积金累计缴存月数'] = latest_record.Duration
    
    result['公积金月缴存最大金额'] = df_HousingProvidentFundRecords \
        .groupby('PCRID').MonthPayAmount.max()
    result['公积金总缴存月数'] = df_HousingProvidentFundRecords \
        .groupby('PCRID').Duration.sum(min_count=1)
    return result

def parse_subsidy():
    result = pd.DataFrame(index=pd.unique(df_LowReliefRecords.PCRID))
    record_cnt = df_LowReliefRecords[df_LowReliefRecords.ApproveDate.notnull()] \
        .groupby('PCRID').SID.count()
		
    result['是否有低保救助记录'] = np.sign(record_cnt)
    result['最近一次低保救助申请日期距今天数'] = df_LowReliefRecords \
        .groupby('PCRID').DaySinceRecord.min()    
    return result

def parse_qualification():
    result = pd.DataFrame(index=pd.unique(df_QualificationRecords.PCRID))
    result['执业资格记录数'] = df_QualificationRecords.groupby('PCRID').SID.count()
    revocation_cnt = df_QualificationRecords[df_QualificationRecords.RevocationDate.notnull()] \
        .groupby('PCRID').SID.count()
		
    result['执业资格是否有吊销记录'] = np.sign(revocation_cnt)
    result['最近一次执业资格获得日期距今天数'] = df_QualificationRecords \
        .groupby('PCRID').DaySinceRecord.min()    
    result['最早一次执业资格获得日期距今天数'] = df_QualificationRecords \
        .groupby('PCRID').DaySinceRecord.max()    
    return result

def parse_award():
    result = pd.DataFrame(index=pd.unique(df_AwardRecords.PCRID))
    result['行政奖励记录数'] = df_AwardRecords.groupby('PCRID').SID.count()
    result['最近一次行政奖励生效日期距今天数'] = df_AwardRecords \
        .groupby('PCRID').DaySinceRecord.min()    
    result['最早一次行政奖励生效日期距今天数'] = df_AwardRecords \
        .groupby('PCRID').DaySinceRecord.max()    
    return result