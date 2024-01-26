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
    element_text, geom_bar,coord_flip, geom_point
)



df=pd.read_csv("./data/processed/clean_data_1.csv")


# Highlevel Stats
total_hours_viewed_b=df["hours_viewed"].sum()/1000
n_titles = len(df)


f"This report covers {total_hours_viewed_b:.2f} billion hours across {n_titles:,} titles."


# Top Titles

top_10_df = df.sort_values(by='hours_viewed', ascending=False)\
              .head(10)\
              .sort_values(by='hours_viewed', ascending=True)




top_10_df['title'] = pd.Categorical(top_10_df['title'], 
                                    categories=top_10_df['title'], 
                                    ordered=True)



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
 
 
top_10_fig

top_10_fig.save('figures/top_ten_fig.png', 
                width=10, height=5, 
                units='in', dpi=300)


#Top IPs
top_10_series_df= df[["series","hours_viewed"]]\
                    .groupby("series") \
                    .agg(func={"hours_viewed":np.sum})\
                    .sort_values("hours_viewed",ascending=False)\
                    .head(15) \
                    .reset_index() \
                    .sort_values(by='hours_viewed', ascending=True)


top_10_series_df['series'] = pd.Categorical(top_10_series_df['series'], 
                                    categories=top_10_series_df['series'], 
                                    ordered=False)



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


total_hours_viewed_lang = final_df["hours_viewed"].sum()

final_df["per_of_total_views"]=(final_df["hours_viewed"]/total_hours_viewed_lang) * 100




# Correct DataFrame name and column references for the plot
final_df['label'] = final_df['language'] + ' (' + final_df['per_of_total_views'].map(lambda x: '{:.2f}%'.format(x)) + ')'


df.columns

df_top100 = df.head(100)

# Using seaborn to create a scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_top100, x='months_out', y='hours_viewed')
plt.title('Scatter Plot of Hours Viewed vs Months Out')
plt.xlabel('Months Out')
plt.ylabel('Hours Viewed')
plt.show()



ggplot(data=df_top100, mapping=p9.aes(x='months_out', y='hours_viewed'))
    + p9.geom_point()
    
    
    
    
    
    
    



ggplot(df_top100, aes(x='months_out', 
                      y='hours_viewed')) \
                        + geom_point()
                        
                        
df.sort_values("views_per_month",ascending=False).head(10).replace([np.inf, -np.inf], np.nan)
#fix this ^^^