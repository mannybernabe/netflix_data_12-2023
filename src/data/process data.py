# Load Libraries ----

import pandas as pd
import numpy as np



from langdetect import detect

# Load and Clean Datat ----
df=pd.read_excel("./data/raw/What_We_Watched_A_Netflix_Engagement_Report_2023Jan-Jun.xlsx",
              skiprows=5,
              usecols="B:E")



df.columns = ["title", "avail_global", "date_release", "hours_viewed"]


# Create variable for Language ----

# Dictionary mapping ISO 639-1 language codes to full language names
language_codes = {
    "en": "English",
    "es": "Spanish",
    "ko": "Korean",
    "ja": "Japanese",
    "cs": "Czech",
    "tr": "Turkish",
    "th": "Thai",
    "pt": "Portuguese",
    "hi": "Hindi",
    "fr": "French",
    "id": "Indonesian",
    "ca": "Catalan",
    "sv": "Swedish",
    "mr": "Marathi",
    "sl": "Slovenian",
    "de": "German",
    "it": "Italian",
    "pl": "Polish"
}



# Function to detect language with improved handling of Spanish titles
def detect_language_full_name_or_code(title):
    if " //" in title:
        # Split the title into two parts
        parts = title.split(" // ")
        # Check for specific Spanish keywords in each part
        spanish_keywords = ['temporada', 'perfil', 'el', 'la', 'del']
        for part in parts:
            if any(keyword in part.lower() for keyword in spanish_keywords):
                return "Spanish"
        try:
            # Detect the language code of the part after ' // '
            language_code = detect(parts[1])
            # Return the full language name using the dictionary if available, else return the language code
            return language_codes.get(language_code, language_code)
        except:
            # In case of an error during detection, return 'Unknown'
            return 'Unknown-Error'
    else:
        # If ' // ' is not in the title, assume the language is English
        return "English"



# create new variable
df['language'] = df['title'].apply(detect_language_full_name_or_code)




#clean up variabls
df['title'] = df['title'].apply(lambda x: x.split(" // ")[0])

# Create "year" variable
df=df.sort_values(by='hours_viewed', ascending=False)



#replace blank strings w/ NaN in "data_release"
df["date_release"] = df["date_release"].replace(" ",np.nan)



df["year"]=pd.to_datetime(df['date_release'], 
                          errors='coerce')\
            .dt.year


df["year"] = np.where(df["date_release"].isna(), np.nan, df["year"])


df["year"] = np.where(df["date_release"].isna(),
                      pd.NA,
                      df["year"])\
                    .astype('Int64')







# Convert 'date_release' to datetime
df['date_release'] = pd.to_datetime(df['date_release'], errors='coerce')

# Define the target date (June 30, 2023)
report_date = pd.to_datetime('2023-06-30')



# Calculate the difference in days, divide by 30 to get months, and round
df['months_out'] = ((report_date - df['date_release']).dt.days / 30).round()
# RENAME THIS ^^^
# This has errors -- there are NAN in "data_releases" that go to "0", have listed as NA

# Fill NaN values with a placeholder (e.g., 0) and convert to integer
df['months_out'] = df['months_out'].fillna(0).astype(int)
# This has errors 


df["hours_viewed"]=df["hours_viewed"]/1000000

df["views_per_month"]=df["hours_viewed"]/df['months_out']


# save output to disk




def extract_series(title):
    if ": Season" in title:
        return title.split(": Season")[0]
    elif ": Part" in title:
        return title.split(": Part")[0]
    else:
        return title
    
    
df["series"]=df["title"].apply(extract_series)











df.to_csv("./data/processed/clean_data_1.csv",index=False)
df.to_csv("./data/processed/clean_data_1.pkl")
