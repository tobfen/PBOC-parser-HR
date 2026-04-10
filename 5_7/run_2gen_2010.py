# -*- coding: utf-8 -*-
"""
"""
import os
import traceback

import numpy as np
import pandas as pd

import parse_2gen_2010_0103 as par

try:
    vars_report_header = par.parse_report_header().add_prefix('RHD_')

    # ===个人基本信息===
    vars_identity_info = par.parse_identity_info().add_prefix('PBI_')
    vars_phone_info = par.parse_phone_info().add_prefix('PBI_')
    vars_living_info = par.parse_living_info().add_prefix('PBI_')
    vars_career_info = par.parse_career_info().add_prefix('PBI_')

    # ===信息概要===
    vars_digital_score = par.parse_digital_score().add_prefix('INS_')
    vars_credit_tips = par.parse_credit_tips().add_prefix('INS_')
    vars_dunning_summary = par.parse_dunning_summary().add_prefix('INS_')
    vars_bad_debts_summary = par.parse_bad_debts_summary().add_prefix('INS_')
    vars_ovd_summary = par.parse_ovd_summary().add_prefix('INS_')
    vars_credit_info_summary = par.parse_credit_info_summary().add_prefix('INS_')
    vars_related_pmt_summary = par.parse_related_pmt_summary().add_prefix('INS_')
    vars_noncredit_info_summary = par.parse_noncredit_info_summary().add_prefix('INS_')
    vars_public_info_summary = par.parse_public_info_summary().add_prefix('INS_')
    vars_query_summary = par.parse_query_summary().add_prefix('INS_')

    # ===信贷交易明细===
    # ---被追偿明细---
    vars_dunning_detail = par.parse_dunning_detail().add_prefix('CTD_')

    # ---五类账户明细---
    vars_loan_and_credit_card_detail = par.parse_loan_and_credit_card_detail().add_prefix('CTD_')
    vars_loan_detail = par.parse_loan_detail().add_prefix('CTD_')
    vars_card_detail = par.parse_credit_card_detail(id_list=par.card_ids, label='贷记卡').add_prefix('CTD_')
    vars_semicard_detail = par.parse_credit_card_detail(id_list=par.semicard_ids, label='准贷记卡').add_prefix('CTD_')

    vars_nonrev_loan_detail = par.parse_loan_detail(id_list=par.nonrev_loan_ids, label='非循环贷账户').add_prefix('CTD_')
    vars_revsep_loan_detail = par.parse_loan_detail(id_list=par.revsep_loan_ids, label='循环额度下分账户').add_prefix(
        'CTD_')
    vars_rev_loan_detail = par.parse_loan_detail(id_list=par.rev_loan_ids, label='循环贷账户').add_prefix('CTD_')

    vars_bank_loan_detail = par.parse_loan_detail(id_list=par.bank_loan_ids, label='银行发放贷款').add_prefix('CTD_')
    vars_nonbank_loan_detail = par.parse_loan_detail(id_list=par.nonbank_loan_ids, label='非银行发放贷款').add_prefix(
        'CTD_')
    vars_finlease_loan_detail = par.parse_loan_detail(id_list=par.finlease_loan_ids,
                                                      label='融资租赁公司发放贷款').add_prefix('CTD_')
    vars_autofin_loan_detail = par.parse_loan_detail(id_list=par.autofin_loan_ids, label='汽车金融公司发放贷款').add_prefix(
        'CTD_')
    vars_consumerfin_loan_detail = par.parse_loan_detail(id_list=par.consumerfin_loan_ids,
                                                         label='消费金融公司发放贷款').add_prefix('CTD_')
    vars_microfin_loan_detail = par.parse_loan_detail(id_list=par.microfin_loan_ids,
                                                      label='小额贷款公司发放贷款').add_prefix('CTD_')
    vars_finguar_loan_detail = par.parse_loan_detail(id_list=par.finguar_loan_ids, label='融资担保公司发放贷款').add_prefix(
        'CTD_')

    vars_house_loan_detail = par.parse_loan_detail(id_list=par.house_loan_ids, label='房贷(含公积金)').add_prefix('CTD_')
    vars_car_loan_detail = par.parse_loan_detail(id_list=par.car_loan_ids, label='车贷').add_prefix('CTD_')
    vars_student_loan_detail = par.parse_loan_detail(id_list=par.student_loan_ids, label='助学贷').add_prefix('CTD_')
    vars_business_loan_detail = par.parse_loan_detail(id_list=par.business_loan_ids, label='经营贷').add_prefix('CTD_')
    vars_farmer_loan_detail = par.parse_loan_detail(id_list=par.farmer_loan_ids, label='农户贷').add_prefix('CTD_')
    vars_consumer_loan_detail = par.parse_loan_detail(id_list=par.consumer_loan_ids, label='消费贷').add_prefix('CTD_')

    vars_credit_loan_detail = par.parse_loan_detail(id_list=par.credit_loan_ids, label='信用类贷款').add_prefix('CTD_')
    vars_coll_loan_detail = par.parse_loan_detail(id_list=par.coll_loan_ids, label='抵质押贷款').add_prefix('CTD_')
    vars_guar_loan_detail = par.parse_loan_detail(id_list=par.guar_loan_ids, label='保证贷款').add_prefix('CTD_')
    vars_secured_loan_detail = par.parse_loan_detail(id_list=par.secured_loan_ids, label='担保类贷款').add_prefix('CTD_')

    # ---逾期及还款---
    vars_loan_and_credit_card_ovd = par.parse_pmt_record(id_list=par.loan_and_credit_card_ids,
                                                         label='贷款及信用卡').add_prefix('CTD_')
    vars_loan_ovd = par.parse_pmt_record(id_list=par.loan_ids, label='贷款').add_prefix('CTD_')
    vars_card_ovd = par.parse_pmt_record(id_list=par.card_ids, label='贷记卡').add_prefix('CTD_')
    vars_semicard_ovd = par.parse_pmt_record(id_list=par.semicard_ids, label='准贷记卡').add_prefix('CTD_')

    vars_unsettled_loan_ovd = par.parse_pmt_un_record(id_list=par.unsettled_loan_ids, label='贷款').add_prefix('CTD_')
    vars_unclosed_card_ovd = par.parse_pmt_un_record(id_list=par.unclosed_credit_card_ids, label='信用卡').add_prefix('CTD_')

    vars_nonrev_loan_ovd = par.parse_pmt_record(id_list=par.nonrev_loan_ids, label='非循环贷账户').add_prefix('CTD_')
    vars_revsep_loan_ovd = par.parse_pmt_record(id_list=par.revsep_loan_ids, label='循环额度下分账户').add_prefix('CTD_')
    vars_rev_loan_ovd = par.parse_pmt_record(id_list=par.rev_loan_ids, label='循环贷账户').add_prefix('CTD_')

    vars_bank_loan_ovd = par.parse_pmt_record(id_list=par.bank_loan_ids, label='银行发放贷款').add_prefix('CTD_')
    vars_nonbank_loan_ovd = par.parse_pmt_record(id_list=par.nonbank_loan_ids, label='非银行发放贷款').add_prefix('CTD_')
    vars_finlease_loan_ovd = par.parse_pmt_record(id_list=par.finlease_loan_ids, label='融资租赁公司发放贷款').add_prefix(
        'CTD_')
    vars_autofin_loan_ovd = par.parse_pmt_record(id_list=par.autofin_loan_ids, label='汽车金融公司发放贷款').add_prefix(
        'CTD_')
    vars_consumerfin_loan_ovd = par.parse_pmt_record(id_list=par.consumerfin_loan_ids,
                                                     label='消费金融公司发放贷款').add_prefix('CTD_')
    vars_microfin_loan_ovd = par.parse_pmt_record(id_list=par.microfin_loan_ids, label='小额贷款公司发放贷款').add_prefix(
        'CTD_')
    vars_finguar_loan_ovd = par.parse_pmt_record(id_list=par.finguar_loan_ids, label='融资担保公司发放贷款').add_prefix(
        'CTD_')

    vars_house_loan_ovd = par.parse_pmt_record(id_list=par.house_loan_ids, label='房贷(含公积金)').add_prefix('CTD_')
    vars_car_loan_ovd = par.parse_pmt_record(id_list=par.car_loan_ids, label='车贷').add_prefix('CTD_')
    vars_student_loan_ovd = par.parse_pmt_record(id_list=par.student_loan_ids, label='助学贷').add_prefix('CTD_')
    vars_business_loan_ovd = par.parse_pmt_record(id_list=par.business_loan_ids, label='经营贷').add_prefix('CTD_')
    vars_farmer_loan_ovd = par.parse_pmt_record(id_list=par.farmer_loan_ids, label='农户贷').add_prefix('CTD_')
    vars_consumer_loan_ovd = par.parse_pmt_record(id_list=par.consumer_loan_ids, label='消费贷').add_prefix('CTD_')

    vars_credit_loan_ovd = par.parse_pmt_record(id_list=par.credit_loan_ids, label='信用类贷款').add_prefix('CTD_')
    vars_coll_loan_ovd = par.parse_pmt_record(id_list=par.coll_loan_ids, label='抵质押贷款').add_prefix('CTD_')
    vars_guar_loan_ovd = par.parse_pmt_record(id_list=par.guar_loan_ids, label='保证贷款').add_prefix('CTD_')
    vars_secured_loan_ovd = par.parse_pmt_record(id_list=par.secured_loan_ids, label='担保类贷款').add_prefix('CTD_')

    # ---审批通过率---
    vars_query_approval_loan = par.parse_query_approval(mode='贷款').add_prefix('CTD_')
    vars_query_approval_card = par.parse_query_approval(mode='信用卡').add_prefix('CTD_')

    # ---特殊交易---
    vars_special_trans = par.parse_special_trans().add_prefix('CTD_')

    # ---大额专项分期---
    vars_large_amt_installment = par.parse_large_amt_installment().add_prefix('CTD_')

    # ---相关还款责任明细---
    vars_guar_related_pmt = par.parse_related_payment((par.df_CreditRelatedRepayment.CoBorrowingFlag == "保证人"),
                                                      label='担保责任').add_prefix('CTD_')
    vars_all_related_pmt = par.parse_related_payment(None, label='相关还款责任').add_prefix('CTD_')

    # ===非信贷交易明细===
    vars_noncredit = par.parse_noncredit().add_prefix('NCD_')

    # ===公共信息明细===
    vars_tax_owe = par.parse_tax_owe().add_prefix('PBD_')
    vars_civil_case = par.parse_civil_case().add_prefix('PBD_')
    vars_enforcement = par.parse_enforcement().add_prefix('PBD_')
    vars_admin_punish = par.parse_admin_punish().add_prefix('PBD_')
    vars_housing_fund = par.parse_housing_fund().add_prefix('PBD_')
    vars_subsidy = par.parse_subsidy().add_prefix('PBD_')
    vars_qualification = par.parse_qualification().add_prefix('PBD_')
    vars_award = par.parse_award().add_prefix('PBD_')

    # ===查询记录===
    vars_query_overall = par.parse_query_record().add_prefix('QRD_')
    vars_query_loan = par.parse_query_record(cond=(par.df_QueryRecord.QueryReason == '贷款审批'),
                                             label='贷款审批').add_prefix('QRD_')
    vars_query_credit_card = par.parse_query_record(cond=(par.df_QueryRecord.QueryReason == '信用卡审批'),
                                                    label='信用卡审批').add_prefix('QRD_')
    vars_query_loan_and_credit_card = par.parse_query_record(
        cond=(par.df_QueryRecord.QueryReason.isin(['贷款审批', '信用卡审批'])), label='贷款及信用卡审批').add_prefix('QRD_')
    vars_query_guarantee_qualif = par.parse_query_record(cond=(par.df_QueryRecord.QueryReason == '担保资格审查'),
                                                         label='担保资格审查').add_prefix('QRD_')

    vars_query_bank = par.parse_query_record(cond=(par.df_QueryRecord.QueryInstitution.str.contains('银行', na=False)),
                                             label='银行').add_prefix('QRD_')
    vars_query_nonbank = par.parse_query_record(cond=(~par.df_QueryRecord.QueryInstitution.str.contains('银行', na=False)),
                                                label='非银').add_prefix('QRD_')
    vars_query_finlease = par.parse_query_record(
        cond=(par.df_QueryRecord.QueryInstitution.str.contains('融资租赁公司', na=False)), label='融资租赁公司').add_prefix(
        'QRD_')
    vars_query_autofin = par.parse_query_record(
        cond=(par.df_QueryRecord.QueryInstitution.str.contains('汽车金融', na=False)), label='汽车金融公司').add_prefix(
        'QRD_')
    vars_query_consumerfin = par.parse_query_record(
        cond=(par.df_QueryRecord.QueryInstitution.str.contains('消费金融公司', na=False)), label='消费金融公司').add_prefix(
        'QRD_')
    vars_query_microfin = par.parse_query_record(
        cond=(par.df_QueryRecord.QueryInstitution.str.contains('小额贷款公司', na=False)), label='小额贷款公司').add_prefix(
        'QRD_')
    vars_query_finguar = par.parse_query_record(
        cond=(par.df_QueryRecord.QueryInstitution.str.contains('融资担保公司', na=False)), label='融资担保公司').add_prefix(
        'QRD_')

    # ===拼表===
    vars_list_full = [
        vars_report_header, \
        # 个人基本信息
        vars_identity_info, vars_phone_info, vars_living_info, vars_career_info, \
        # 信息概要
        vars_digital_score, vars_credit_tips, vars_dunning_summary, \
        vars_bad_debts_summary, vars_ovd_summary, vars_credit_info_summary, \
        vars_related_pmt_summary, vars_noncredit_info_summary, vars_public_info_summary, \
        vars_query_summary, \
        # 信贷交易明细
        vars_dunning_detail, \
        vars_loan_and_credit_card_detail, vars_loan_detail, vars_card_detail, vars_semicard_detail, \
        vars_nonrev_loan_detail, vars_revsep_loan_detail, vars_rev_loan_detail, \
        vars_bank_loan_detail, vars_nonbank_loan_detail, vars_finlease_loan_detail, \
        vars_autofin_loan_detail, vars_consumerfin_loan_detail, \
        vars_microfin_loan_detail, vars_finguar_loan_detail, \
        vars_house_loan_detail, vars_car_loan_detail, vars_student_loan_detail, \
        vars_business_loan_detail, vars_farmer_loan_detail, vars_consumer_loan_detail, \
        vars_credit_loan_detail, vars_coll_loan_detail, vars_guar_loan_detail, vars_secured_loan_detail,
        # 逾期及还款
        vars_loan_and_credit_card_ovd, vars_loan_ovd, vars_card_ovd, vars_semicard_ovd, \
        vars_nonrev_loan_ovd, vars_revsep_loan_ovd, vars_rev_loan_ovd, \
        vars_bank_loan_ovd, vars_nonbank_loan_ovd, vars_finlease_loan_ovd, \
        vars_autofin_loan_ovd, vars_consumerfin_loan_ovd, \
        vars_microfin_loan_ovd, vars_finguar_loan_ovd, \
        vars_house_loan_ovd, vars_car_loan_ovd, vars_student_loan_ovd, \
        vars_business_loan_ovd, vars_farmer_loan_ovd, vars_consumer_loan_ovd, \
        vars_credit_loan_ovd, vars_coll_loan_ovd, vars_guar_loan_ovd, vars_secured_loan_ovd, \
        # 审批通过率
        vars_query_approval_loan, vars_query_approval_card, \
        # 特殊交易, 大额专项分期
        vars_special_trans, vars_large_amt_installment, \
        # 相关还款责任明细
        vars_guar_related_pmt, vars_all_related_pmt, \
        # 非信贷信息明细
        vars_noncredit, \
        # 公共信息明细
        vars_tax_owe, vars_civil_case, vars_enforcement, \
        vars_admin_punish, vars_housing_fund, vars_subsidy, \
        vars_qualification, vars_award, \
        # 查询记录
        vars_query_overall, vars_query_loan, vars_query_credit_card, \
        vars_query_loan_and_credit_card, vars_query_guarantee_qualif, \
        vars_query_bank, vars_query_nonbank, vars_query_finlease, \
        vars_query_autofin, vars_query_consumerfin, vars_query_microfin, \
        vars_query_finguar, vars_unsettled_loan_ovd, vars_unclosed_card_ovd]

    vars_full = pd.merge(vars_list_full[0], vars_list_full[1], how='left', left_index=True, right_index=True)
    for vars_list in vars_list_full[2:]:
        vars_full = pd.merge(vars_full, vars_list, how='left', left_index=True, right_index=True)

    
    full_list = pd.Series(list(vars_full))

    vars_template = pd.read_excel(r'../2010.xlsx', sheet_name=0)
    vars_template['var_name'] = vars_template['class'] + '_' + vars_template['特征名称']
    vars_template['var_name'] = vars_template['var_name'].str.strip()
    vars_template['done'] = np.nan

    # #限定第一批540
    vars_template.loc[vars_template.var_name.isin(vars_full.columns) & (vars_template.batch == 1), 'done'] = 1
    var_names_540 = vars_template.loc[vars_template.done == 1, 'var_name']

    fill_zero_var_names = vars_template.loc[(vars_template.done == 1) & (vars_template.fill_value == 0), 'var_name']
    fill_na_var_names = vars_template.loc[(vars_template.done == 1) & (vars_template.fill_value == -999), 'var_name']
    vars_important = vars_full[var_names_540].copy()
    vars_important[fill_zero_var_names] = vars_important[fill_zero_var_names].fillna(0)
    vars_important[fill_na_var_names] = vars_important[fill_na_var_names].fillna(-999)

    renaming_dict = {var_name: var_name[4:] for var_name in var_names_540}
    vars_important.rename(columns=renaming_dict, inplace=True)

    renaming_dict2 = vars_template.set_index('特征名称')['英文名称'].to_dict()
    vars_important.rename(columns=renaming_dict2, inplace=True)

    vars_important.drop('pcrid', axis=1).to_csv(r'./result_540.csv', index=True)

    # #全部2010
    vars_template = pd.read_excel(r'../2010.xlsx', sheet_name=0)
    vars_template['var_name'] = vars_template['class'] + '_' + vars_template['特征名称']
    vars_template['var_name'] = vars_template['var_name'].str.strip()

    var_names_2010 = vars_template.loc[:, 'var_name']

    fill_zero_var_names = vars_template.loc[(vars_template.fill_value == 0), 'var_name']
    fill_na_var_names = vars_template.loc[(vars_template.fill_value == -999), 'var_name']

    vars_2010 = vars_full[var_names_2010].copy()

    vars_2010[fill_zero_var_names] = vars_2010[fill_zero_var_names].fillna(0)
    vars_2010[fill_na_var_names] = vars_2010[fill_na_var_names].fillna(-999)

    renaming_dict = {var_name: var_name[4:] for var_name in var_names_2010}
    vars_2010.rename(columns=renaming_dict, inplace=True)

    renaming_dict2 = vars_template.set_index('特征名称')['英文名称'].to_dict()
    vars_2010.rename(columns=renaming_dict2, inplace=True)

    # vars_2010.drop('pcrid',axis=1).to_csv(r'./result_2010.csv',index=True)


    vars_2010.drop('pcrid', axis=1).to_json(r'./result_2010.json', orient='index')
except Exception as e:
    print("异常：", str(e))
    traceback.print_exc()
finally:
    os._exit(1)