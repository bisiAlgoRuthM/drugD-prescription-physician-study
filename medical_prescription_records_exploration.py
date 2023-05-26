import numpy as np
import pandas as pd

#Loading the dataset Q1
sddm = pd.read_csv('sddm.csv')
sddm.reset_index(drop=True)
sddm.drop(sddm.columns[0], axis=1)


#Number of rows in the dataframe Q1-1
len(sddm)


#Sorted physicians by total quantity of drug D in descending order Q2
phy = sddm.groupby('phid')['quantity'].sum().sort_values(ascending=False)
df= pd.DataFrame(phy) #converting the the sorted phid to a dataframe
df.reset_index(inplace=True)

#rank the dataframe by total quantity of drug D 
df['rank'] = df['quantity'].rank(ascending=False, method='min')
df = df.rename(columns={'quantity': 'total_rx'})
df.head(10)

print(df.iloc[25])  #indexing begins at zero Q2-1
print(df[df['rank'] == 9])  #Q2-2

ave_age_region = sddm.groupby('region')['age'].mean()  #Q3

#printing the region-age table sorted and rounded to 2 decimals
sorted_gp = ave_age_region.sort_values().round(2)
sorted_gp = pd.DataFrame(sorted_gp)
sorted_gp.reset_index(inplace=True)
print(sorted_gp)

#converting the date format using datetime python module Q4
sddm['rxdate']=pd.to_datetime(sddm['rxdate'])
sddm_df = sddm[(sddm['rxdate'] >= '2017-01-01') & (sddm['rxdate'] <= '2017-05-31')]

#average daily cost per physician  Q4-1
average_daily_cost = sddm_df.groupby('phid')['cost'].mean()
result = average_daily_cost[average_daily_cost > 6000]
result.reset_index()
print(len(result))

#Q4-2
sorted_average_cost = average_daily_cost.sort_values(ascending=False)
second_highest = sorted_average_cost.iloc[1]
phid = sorted_average_cost.index[1]
print("Second highest average daily cost:", phid, "and the average daily cost is", second_highest)

#use .shift()to check if the difference between the date and the previous date is one day
is_consecutive = (sddm['rxdate'] - sddm['rxdate'].shift(1)).dt.days == 1


# Filter the physicians who are prescribed on two consecutive days
consecutive_ids = sddm[is_consecutive]['phid'].unique()
print(consecutive_ids)
print(len(consecutive_ids))

#how many physician who prescribed on two consecutive days more than once Q5-2
sddm.sort_values('rxdate', inplace=True)
sddm_group = sddm.groupby(['phid', 'rxdate']).size().reset_index(name= 'rxcount')

#select the physicians with more than one rx count a 1 day difference between any two prescription dates
target_physicians = sddm_group[
    (sddm_group['rxcount'] > 1) &
    sddm_group['phid'].duplicated(keep=False) &
    sddm_group['rxdate'].diff().dt.days.eq(1)] 

consecutive_count = target_physicians['phid'].nunique()
consecutive_count

#select time period Q6-1

period_df = sddm[
    (sddm['rxdate'] > '2017-04-01') & (sddm['rxdate'] < '2017-12-31')]

pre_period = sddm[
    (sddm['rxdate'] >= '2017-01-01') & (sddm['rxdate'] <= '2017-03-31')
]

#count the number of prescriptions for each phid
physicians_prescription_count = period_df.groupby('phid').size().reset_index(name='count')

#select phids who have prescriptions > 2 for the period 2017-04-01 and 2017-12-31
physicians_two_per_month = physicians_prescription_count[physicians_prescription_count['count'] >= 2 * 9]

#select physicians with no prescription in first 3 months
no_prescriptions_pre_period = set(sddm['phid']) - set(pre_period['phid'])

#select physicians who have no presciptions for the first 3 months and have an average of at least 2 prescriptions per month
filtered_result = physicians_two_per_month[physicians_two_per_month['phid'].isin(no_prescriptions_pre_period)]
filtered_result


#inner join the final reult of q6 to the dataframe Q6-2
physicians_selected = pd.merge(filtered_result, sddm, on='phid', how='inner')


ave_cost_physician = physicians_selected.groupby('phid')['cost'].mean()


#prescriptions exceeding average
prescriptions_above_avg = physicians_selected[physicians_selected['cost'] > physicians_selected['phid'].map(ave_cost_physician)]
prescriptions_above_avg_count = prescriptions_above_avg.groupby('phid').size().reset_index(name='above_avg_count')
prescriptions_above_avg_count


