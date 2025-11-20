import os, json
import pandas as pd


def convert_for_saving(diz, df):
    tot = 0
    idx_missing = []
    TOT = []
    for k,v in diz.items():
        for k1, v1 in v.items():
            source = v1[1]
            value = v1[2]
            if '--' in value:
                vett = [x.strip() for x in value.split('--')]
                if len(vett)==3:
                    if k1 == 'ASSETS' or k1 =='TURNOVER':
                        diz1 = {'ID':int(k),'NAME':df[df['ID']== int(k)]['NAME'].unique()[0], 'VARIABLE':k1, 'SRC':source, 'VALUE':int(vett[1]), 'CURRENCY':vett[2], 'REFYEAR':vett[0]}
                        print(diz1)
                    else: 
                        diz1 = {'ID':int(k),'NAME':df[df['ID']== int(k)]['NAME'].unique()[0], 'VARIABLE':k1, 'SRC':source, 'VALUE':vett[1], 'CURRENCY':vett[2], 'REFYEAR':vett[0]}
                        print(diz1)
                else:
                    if k1 == 'ASSETS' or k1 =='TURNOVER':
                        diz1={'ID':int(k),'NAME':df[df['ID']== int(k)]['NAME'].unique()[0], 'VARIABLE':k1, 'SRC':source, 'VALUE':int(vett[1]), 'CURRENCY':df['VALUE'].unique()[0], 'REFYEAR':vett[0]}
                        print(diz1)
                    else: 
                        diz1 = {'ID':int(k),'NAME':df[df['ID']== int(k)]['NAME'].unique()[0], 'VARIABLE':k1, 'SRC':source, 'VALUE':vett[1], 'CURRENCY':'N/A', 'REFYEAR':vett[0]}
                        print(diz1)
            else:
                if k1 == 'WEBSITE':
                    diz1 = {'ID':int(k),'NAME':df[df['ID']== int(k)]['NAME'].unique()[0], 'VARIABLE':k1, 'SRC':source, 'VALUE':source, 'CURRENCY':'N/A', 'REFYEAR':2024}
                    print(diz1)
                else:
                    diz1 = {'ID':int(k),'NAME':df[df['ID']== int(k)]['NAME'].unique()[0], 'VARIABLE':k1, 'SRC':source, 'VALUE':value, 'CURRENCY':'N/A', 'REFYEAR':2024}
                    print(diz1)
            TOT.append(diz1)
        if len(v) != 6:
            tot += 1
            idx_missing.append(k)
            diz1 = {'ID':int(k),'NAME':df[df['ID']== int(k)]['NAME'].unique()[0], 'VARIABLE':'ASSETS', 'SRC':None, 'VALUE':None, 'CURRENCY':None, 'REFYEAR':None}
            print(diz1)
            TOT.append(diz1)
    return TOT



def save_json(SAVING_PATH, TOT, df):
    # Convert to DataFrame
    df_nuovi = pd.DataFrame(TOT)

    # Merge on the triplet ID, NAME, VARIABLE
    df_completo = df.merge(df_nuovi, on=['ID', 'NAME', 'VARIABLE'], how='left', suffixes=('', '_new'))

    # Only fills the missing values ​​from the new ones
    for col in ['SRC', 'VALUE', 'CURRENCY', 'REFYEAR']:
        df_completo[col] = df_completo[col].combine_first(df_completo[f'{col}_new'])

    # Remove temporary columns
    df_completo.drop(columns=[f'{col}_new' for col in ['SRC', 'VALUE', 'CURRENCY', 'REFYEAR']], inplace=True)

    df_completo.to_csv(SAVING_PATH, sep=";", encoding="utf-8", index=False)
    print(f"Data saved to {SAVING_PATH}")