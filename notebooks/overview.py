import pandas as pd
import matplotlib.pyplot as plt



df=pd.read_csv("./data/processed/clean_data_1.csv")


# Highlevel Stats
total_hours_viewed_b=df["hours_viewed"].sum()/1000000000
n_titles = len(df)


f"This report covers {total_hours_viewed_b:.2f} billion hours across {n_titles:,} titles."


# Top Titles
top_10_df = df.sort_values(by='hours_viewed', ascending=False).head(11)

top_10_df = top_10_df.sort_values(by='hours_viewed', ascending=True)

plt.barh(top_10_df['title'], top_10_df['hours_viewed'])

top_10_df[["title","hours_viewed"]]\
    .sort_values(by='hours_viewed',
                 ascending=False) \
    .reset_index(drop=True)
