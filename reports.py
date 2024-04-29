import pandas as pd

hcris_alpha = pd.read_csv('HOSP10_2023_ALPHA.CSV',
                          names=['RPT_REC_NUM','WKSHT_CD','LINE_NUM','CLMN_NUM','ITM_VAL_NUM']
                          )
hcris_nmrc = pd.read_csv('HOSP10_2023_NMRC.CSV',
                         names=['RPT_REC_NUM','WKSHT_CD','LINE_NUM','CLMN_NUM','ITM_VAL_NUM']
                         )
hcris_report = pd.read_csv('HOSP10_2023_RPT.CSV',
                           names=['RPT_REC_NUM','PRVDR_CTRL_TYPE_CD','PRVDR_NUM','NPI',
                                    'RPT_STUS_CD','FY_BGN_DT','FY_END_DT','PROC_DT',
                                    'INITL_RPT_SW','LAST_RPT_SW','TRNSMTL_NUM','FI_NUM',
                                    'ADR_VNDR_CD','FI_CREAT_DT','UTIL_CD','NPR_DT',
                                    'SPEC_IND','FI_RCPT_DT'
                                ]
                            )

# Variable locations
hcris_vars = pd.DataFrame(columns=["variable", "WKSHT_CD", "LINE_NUM", "CLMN_NUM", "source"])

# Populate variable locations dataframe
variables = [
    ['beds', 'S300001', 1400, '00200', 'numeric'],
    ['tot_charges', 'G300000',100,'00100', 'numeric'],
    ['street','S200001',100,100,'alpha']
]

for var in variables:
    hcris_vars = hcris_vars._append(pd.Series(var, index=hcris_vars.columns), ignore_index=True)
# print(hcris_vars)
final_hcris = pd.DataFrame()

final_reports = hcris_report[['RPT_REC_NUM', 'PRVDR_NUM', 'NPI', 'FY_BGN_DT', 'FY_END_DT', 'PROC_DT', 'FI_CREAT_DT', 'RPT_STUS_CD']].assign(year=2023)

for _, row in hcris_vars.iterrows():
    print(row)
    hcris_data = hcris_alpha if row['source'] == 'alpha' else hcris_nmrc
    
    filtered_data = hcris_data[
        (hcris_data['WKSHT_CD'] == row['WKSHT_CD']) & 
        (hcris_data['LINE_NUM'] == row['LINE_NUM']) & 
        (hcris_data['CLMN_NUM'] == row['CLMN_NUM'])]\
    [['RPT_REC_NUM', 'ITM_VAL_NUM']].rename(columns={'ITM_VAL_NUM': row['variable']})
    # print(filtered_data)
    final_reports = pd.merge(final_reports, filtered_data, on='RPT_REC_NUM', how='left')
    # print(final_reports)
    # break

final_hcris = pd.concat([final_hcris, final_reports])
final_hcris.to_csv('report.csv',index=False)
# print(final_hcris)