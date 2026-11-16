import pandas as pd
import sqlite3

df = pd.read_csv('data/raw_hrrp_fy2026.csv')
print(df.shape)
print(df.isnull().sum())

df.columns = df.columns.str.lower().str.replace(' ', '_')

condition_names = {
    'READM-30-AMI-HRRP': 'Heart Attack',
    'READM-30-HF-HRRP': 'Heart Failure',
    'READM-30-PN-HRRP': 'Pneumonia',
    'READM-30-COPD-HRRP': 'COPD',
    'READM-30-CABG-HRRP': 'Bypass Surgery',
    'READM-30-HIP-KNEE-HRRP': 'Hip/Knee Replacement'
}
df['condition'] = df['measure_name'].replace(condition_names)

# CMS puts "Too Few to Report" instead of a number when the count is small
df['number_of_readmissions'] = pd.to_numeric(df['number_of_readmissions'], errors='coerce')

# no ratio means CMS didn't score it
df = df.dropna(subset=['excess_readmission_ratio'])
print('rows left:', len(df))

df['worse_than_expected'] = (df['excess_readmission_ratio'] > 1).astype(int)

# rough count of extra readmissions = (predicted rate - expected rate) x discharges
df['excess_readmissions'] = (df['predicted_readmission_rate'] - df['expected_readmission_rate']) / 100 * df['number_of_discharges']

df = df.drop(columns=['measure_name', 'footnote', 'start_date', 'end_date'])
df.to_csv('data/hrrp_clean.csv', index=False)

conn = sqlite3.connect('data/hrrp.db')
df.to_sql('readmissions', conn, if_exists='replace', index=False)
conn.close()
