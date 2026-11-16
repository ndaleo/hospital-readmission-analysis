import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os

os.makedirs('outputs', exist_ok=True)
os.makedirs('images', exist_ok=True)

conn = sqlite3.connect('data/hrrp.db')


def run_query(file_name):
    query = open('sql/' + file_name).read()
    return pd.read_sql(query, conn)


conditions = run_query('1_conditions.sql')
states = run_query('2_states.sql')
per_hospital = run_query('3_conditions_per_hospital.sql')
worst = run_query('4_worst_hospitals.sql')
ny = run_query('5_ny_hospitals.sql')
conn.close()

conditions.to_csv('outputs/conditions.csv', index=False)
states.to_csv('outputs/states.csv', index=False)
per_hospital.to_csv('outputs/conditions_per_hospital.csv', index=False)
worst.to_csv('outputs/worst_hospitals.csv', index=False)
ny.to_csv('outputs/ny_hospitals.csv', index=False)

print(conditions)
total = conditions['excess_readmissions'].sum()
hf_pn = conditions[conditions['condition'].isin(['Heart Failure', 'Pneumonia'])]['excess_readmissions'].sum()
print('total excess readmissions:', total)
print('heart failure + pneumonia share:', round(hf_pn / total * 100, 1), '%')

print(states.head(15))
print('NY rank:', states[states['state'] == 'NY'].index[0] + 1, 'out of', len(states))

print(per_hospital)
four_plus = per_hospital[per_hospital['conditions_worse'] >= 4]['hospitals'].sum()
print('worse on 4+ conditions:', four_plus, 'out of', per_hospital['hospitals'].sum())

print('worse on every condition:', len(worst))
print(ny.head(10))


# chart 1 - excess readmissions by condition
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(conditions['condition'], conditions['excess_readmissions'], color='#2a78d6')
ax.bar_label(bars, fmt='{:,.0f}', padding=3)
ax.set_xlim(0, 5500)
ax.invert_yaxis()
ax.set_title('Estimated Excess Readmissions by Condition (Jul 2021 - Jun 2024)')
ax.set_xlabel('Excess readmissions')
plt.tight_layout()
plt.savefig('images/excess_by_condition.png', dpi=150)

# chart 2 - top 15 states, NY in a darker color
top15 = states.head(15)
colors = ['#104281' if s == 'NY' else '#2a78d6' for s in top15['state']]
fig, ax = plt.subplots(figsize=(9, 6))
bars = ax.barh(top15['state'], top15['pct_worse'], color=colors)
ax.bar_label(bars, fmt='%.1f%%', padding=3)
ax.invert_yaxis()
ax.axvline(50, color='gray', linestyle='--')
ax.set_title('Top 15 States: % of Scores Worse Than Expected')
ax.set_xlabel('% worse than expected')
plt.tight_layout()
plt.savefig('images/states_top15.png', dpi=150)

# chart 3 - how many conditions hospitals are worse on
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(per_hospital['conditions_worse'].astype(str), per_hospital['hospitals'], color='#2a78d6')
ax.bar_label(bars, padding=3)
ax.set_ylim(0, 800)
ax.set_title('Hospitals by Number of Conditions Worse Than Expected')
ax.set_xlabel('Conditions worse than expected')
ax.set_ylabel('Hospitals')
plt.tight_layout()
plt.savefig('images/conditions_per_hospital.png', dpi=150)
