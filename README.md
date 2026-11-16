# Hospital Readmissions Analysis

Ever wonder what happens when a patient gets sent home from the hospital and ends up right back there a couple weeks later? It's bad for the patient, and it also costs the hospital money, because Medicare cuts payments to hospitals that have more readmissions than they should. So I wanted to find out which conditions, states, and hospitals have the biggest readmission problem.

## Power BI Dashboard

I also built an interactive dashboard in Power BI where you can filter by condition and state.

![Dashboard](images/HR%20Dashboard.png)


## The data

I used the newest Hospital Readmissions Reduction Program file from CMS (FY 2026), which you can download [here](https://data.cms.gov/provider-data/dataset/9n3s-kdb3). It covers July 2021 to June 2024 and has 18,330 rows across 3,055 hospitals. Each row is one hospital and one condition: heart attack, heart failure, pneumonia, COPD, bypass surgery, or hip/knee replacement.

The main number I worked with is the **Excess Readmission Ratio**. CMS takes the hospital's patients into account and figures out how many readmissions it should have, then compares that to what actually happened. Anything over 1.0 means the hospital had more readmissions than expected.

## What I did

- **Cleaning (Python):** renamed the columns so they were easier to use in SQL, swapped the CMS measure codes for real condition names, turned the "Too Few to Report" values into blanks, and dropped the 6,610 rows CMS didn't give a score to. Then I loaded everything into a SQLite database.
- **Analysis (SQL):** wrote 5 queries looking at conditions, states, hospitals that are worse on multiple conditions, and New York hospitals specifically, since that's where I'm from.
- **Excess readmissions:** the ratio by itself is hard to picture, so I estimated the actual number of extra readmissions using (predicted rate - expected rate) x discharges.
- **Charts (matplotlib):** made the charts in this README from the query results.

## What I found

**Heart failure and pneumonia are the biggest problem by far.** Across all the hospitals doing worse than expected, there were about 12,245 extra readmissions, and roughly 77% of them (9,381) came from just these two conditions. Heart failure also had the highest average readmission rate at 19.4%.

**New Jersey and Massachusetts had the worst scores.** 65.4% of NJ's scores and 62.5% of MA's were worse than expected. New York was 10th out of 49 states at 52.7%.

![Top 15 states](images/states_top15.png)

**When a hospital is bad at one thing, it's usually bad at a few.** Out of 2,833 hospitals, 470 (about 17%) were worse than expected on 4 or more conditions, and 143 were worse on every single condition they were scored on.

![Conditions per hospital](images/conditions_per_hospital.png)

**In New York,** 53 hospitals were worse than expected on 3 or more conditions. Maimonides Medical Center, St. Joseph's Hospital Health Center, and Rochester General Hospital were each worse on 5 of their 6.

## What I'd recommend

I would say if a hospital system or insurance company wanted to bring readmissions down, heart failure and pneumonia patients are where I'd start, since that's where most of the extra readmissions are coming from. Things like a follow-up call a few days after discharge, double checking their medications, and making sure they have a doctor's appointment booked before they leave could make a real difference. For the hospitals that are worse on 4+ conditions, I think it's more of a hospital-wide problem with how they discharge patients and coordinate care, not something one department is going to fix on its own.

## Things to keep in mind

- Around half of all scores are going to be over 1.0 no matter what, because of how CMS sets up the ratio. So being over 1.0 once isn't a big deal. What matters is where those scores pile up.
- The 12,245 is probably on the low side. CMS doesn't show discharge counts for smaller programs, so I couldn't include them in the estimate.
- This is hospital-level data, so it shows where the problems are but not which patients are most at risk.

## How to run it

```
pip install -r requirements.txt
python src/clean_data.py
python src/analysis.py
```

The cleaned file (`data/hrrp_clean.csv`) can also be loaded right into Power BI or Tableau.

**Tools:** Python (pandas, matplotlib), SQL (SQLite)
