import pandas as pd
import matplotlib.pyplot as plt




df=pd.read_csv("./data/processed/clean_data_1.csv")

df.tail()

#18,213 total shows

df["hours_viewed"].sum()/10000000000

# 9.345 billions hours watched

top_10_df = df.sort_values(by='hours_viewed', ascending=False).head(11)

top_10_df = top_10_df.sort_values(by='hours_viewed', ascending=True)

plt.barh(top_10_df['title'], top_10_df['hours_viewed'])


df["hours_viewed"].describe()

df["hours_viewed"]=df["hours_viewed"]/1000000





top_10_df = df.sort_values(by='hours_viewed', ascending=False).head(11)

top_10_df = top_10_df.sort_values(by='hours_viewed', ascending=True)

plt.barh(top_10_df['title'], top_10_df['hours_viewed'])



df['cumulative_sum'] = df['hours_viewed'].cumsum()
total_sum = df['hours_viewed'].sum()

df['cumulative_percentage'] = (df['cumulative_sum'] / total_sum) * 100

top_10_df

plt.plot(df['cumulative_percentage'], marker='o') 


grouped_total = df.groupby('language').sum()


table_language = grouped_total.sort_values("hours_viewed", ascending=False).head(10)

table_language= table_language[["hours_viewed"]]

#fix pl = as Polish?

table_language.dtypes

table_language.columns

total_hours_viewed = df['hours_viewed'].sum()


df['percent_of_total'] = (df['hours_viewed'] / total_hours_viewed) * 100

