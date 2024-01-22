import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from mizani.formatters import custom_format


# Plotting
from plotnine import (
    ggplot, aes, geom_col, geom_line, 
    geom_smooth, facet_wrap, scale_y_continuous,
    scale_x_datetime,labs,
    theme, theme_minimal, theme_matplotlib,
    theme_538,theme_dark,
    expand_limits, ggsave,
    element_text, geom_bar,coord_flip
)



df=pd.read_csv("./data/processed/clean_data_1.csv")


# Highlevel Stats
total_hours_viewed_b=df["hours_viewed"].sum()/1000000000
n_titles = len(df)


f"This report covers {total_hours_viewed_b:.2f} billion hours across {n_titles:,} titles."


# Top Titles

top_10_df = df.sort_values(by='hours_viewed', ascending=False)\
              .head(10)\
              .sort_values(by='hours_viewed', ascending=True)




top_10_df['title'] = pd.Categorical(top_10_df['title'], 
                                    categories=top_10_df['title'], 
                                    ordered=True)



top_10_df["hours_viewed"]=top_10_df["hours_viewed"]/1000000


million_formatter = custom_format('{:,.0f}M')

top_10_fig = ggplot(top_10_df, aes(x='title', y='hours_viewed')) \
                + geom_bar(stat='identity',fill="blue") \
                + coord_flip() \
                + labs(
                    title='Top 10 Titles by Hours Viewed',
                    x='',
                    y='Hours Viewed'
                ) \
                + theme_minimal() \
                + scale_y_continuous(labels=million_formatter, 
                                     expand=(0.1, 0)) \
                + expand_limits(y=0)
 
 


top_10_fig.save('figures/top_ten_fig.png', 
                width=10, height=5, 
                units='in', dpi=300)


#Top IPs
top_10_series_df= df[["series","hours_viewed"]]\
                    .groupby("series") \
                    .agg(func={"hours_viewed":np.sum})\
                    .sort_values("hours_viewed",ascending=False)\
                    .head(20) \
                    .reset_index() \
                    .sort_values(by='hours_viewed', ascending=True)


top_10_series_df['series'] = pd.Categorical(top_10_series_df['series'], 
                                    categories=top_10_series_df['series'], 
                                    ordered=False)


top_10_series_df["hours_viewed"]=top_10_series_df["hours_viewed"]/1000000


top_10_series_fig = ggplot(top_10_series_df, aes(x='series', y='hours_viewed')) \
                        + geom_bar(stat='identity',fill="blue") \
                        + coord_flip() \
                        + labs(
                            title='Top 10 Titles by Hours Viewed',
                            x='',
                            y='Hours Viewed'
                        ) \
                        + theme_minimal() \
                        + scale_y_continuous(labels=million_formatter, expand=(0.1, 0)) \
                        + expand_limits(y=0)
                
top_10_series_fig

top_10_series_fig.save('figures/top_ten_series_fig.png', 
                        width=10, height=5, 
                        units='in', dpi=300)




# Top Languages and Percent

# top_10_df["hours_viewed"]=top_10_df["hours_viewed"]/1000000



top_lang_df=df[["language","hours_viewed"]] \
    .groupby("language") \
    .agg(func={"hours_viewed":np.sum})\
    .sort_values("hours_viewed",ascending=False) \
    .reset_index()
    
    
   
top_languages = top_lang_df.head(10)
other_languages = top_lang_df.tail(len(top_lang_df)-10)
 

other_sum = pd.DataFrame(data={"language":["Other"],"hours_viewed":[other_languages["hours_viewed"].sum()]})
   

final_df = pd.concat([top_languages,other_sum])
    
final_df.reset_index(drop=True, inplace=True)

final_df

final_df["hours_viewed"]=final_df["hours_viewed"]/1000000

final_df["hours_viewed"].sum()

total_hours_viewed_lang = final_df["hours_viewed"].sum()

final_df["per_of_total_views"]=(final_df["hours_viewed"]/total_hours_viewed_lang) * 100


final_df.columns






# Correct DataFrame name and column references for the plot
final_df['label'] = final_df['language'] + ' (' + final_df['per_of_total_views'].map(lambda x: '{:.2f}%'.format(x)) + ')'

# Create figure and axis for the donut chart
fig, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(aspect="equal"))

# The pie chart parameters
wedges, texts, autotexts = ax.pie(final_df['hours_viewed'],
                                   startangle=140,
                                   labels=final_df['label'],
                                   autopct='%1.1f%%',
                                   textprops=dict(color="black"),
                                   colors=plt.cm.tab20.colors)

# Draw a white circle in the middle to create the donut hole
centre_circle = plt.Circle((0, 0), 0.70, color='white')
fig.gca().add_artist(centre_circle)

# Equal aspect ratio ensures that pie is drawn as a circle
ax.axis('equal')

# Title for the donut chart
plt.title('Top Languages by Hours Viewed (%)')

# Adjust layout to make room for the legend
plt.tight_layout()

# Display the plot with labels
plt.show()


# NOTE to SELF: Need a better chart than donut