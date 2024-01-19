import pandas as pd
import matplotlib.pyplot as plt


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
                + scale_y_continuous(labels=million_formatter, expand=(0.1, 0)) \
                + expand_limits(y=0)
 
 
 
ggsave(plot="top_10_fig", filename="./figures/top_ten_fig.png")




top_10_fig.save('figures/top_ten_fig.png', width=10, height=5, units='in', dpi=300)
