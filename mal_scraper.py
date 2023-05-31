from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

# Scrape the page
url = "https://myanimelist.net/topmanga.php"

# Make the request
response = requests.get(url)

# Parse the response
soup = BeautifulSoup(response.text, "html.parser")

# Save the results under an html to view
with open ("manga_ratings.html", "w") as file:
     file.write(str(soup.prettify()))

# Parse the html to a dataframe
dfs = pd.read_html("manga_ratings.html")
df = pd.concat(dfs)

# # extract columns using regular expressions
# extracted_columns = df.iloc[:, 1].str.extract(r'^(.*?)\s+(Manga|Novel)?\s*(?:\((?:(\d+|\?)\s*vols|\?)\)\s*)?(?:(\w{3}\s\d{4})\s*-\s*(\w{3}\s\d{4}|\w+)|Ongoing)(?:\s+([\d,]+(?:\.\d+)?\s*members))?')
# extracted_columns.columns = ['Title', 'Type', 'Volumes', 'Start Date', 'End Date', 'Members']

# # check if the 'End Date' column has a valid date
# valid_dates = pd.to_datetime(extracted_columns['End Date'], errors='coerce').notnull()

# # replace the missing 'Members' with the value in the 'End Date' column
# extracted_columns.loc[extracted_columns['Members'].isna(), 'Members'] = extracted_columns.loc[extracted_columns['Members'].isna(), 'End Date']


# Isolate the rank list of the manga in order
rank_list = df.iloc[:,0].tolist()
df_rank = pd.DataFrame(rank_list)
df_rank_title = df_rank.iloc[0]
df_rank_sorted = df_rank[1:].reset_index(drop=True)
df_rank_sorted.columns = df_rank_title

# Isolate the scores of the manga in order
score_list = df.iloc[:,2].tolist()
df_score = pd.DataFrame(score_list)
df_score_title = df_score.iloc[0]
df_score_sorted = df_score[1:].reset_index(drop=True)
df_score_sorted.columns = df_score_title

# Access the String Containing the Data of the Manga
data = df.iloc[:,1].tolist()

# The Regex pattern that allows the Data to be cleaned
pattern = r'^(.*?)\s+(Manga|Light Novel|Novel)\s+\((\d+|\?)\s+vols\)\s+([A-Za-z]{3}\s+\d{4})\s+(?:-\s*([A-Za-z]{3}\s+\d{4}))?.*?(\d+,\d+)\s+members$'

# Create a list of dictionaries to store the data
df_data = []

# Iterate through the data
for item in data:
    # Extract the titles
    match = re.match(pattern, item)
    # If a match is found group the matches by specific parameters
    if match:
        title = match.group(1)
        type = match.group(2)
        volumes = match.group(3)
        start_date = match.group(4)
        end_date = match.group(5).strip() if match.group(5) else 'Ongoing'
        members = match.group(6).replace(',', '')
        # Append the titles to the Data
        df_data.append({
            'Title': title,
            'Type': type,
            'Volumes': volumes,
            'Start Date': start_date,
            'End Date': end_date,
            'Members': members
        })

# Make the Extracted Columns into a DataFrame
extracted_columns = pd.DataFrame(df_data)

# Concatenate the Ranking, the Data, and the Rating
final = pd.concat([df_rank_sorted,extracted_columns,df_score_sorted],axis=1)

#print(final)

# extracted_columns.to_excel("manga_ratings_split.xlsx", index=False)

# Export Data into an Excel Sheet
final.to_excel("sorted_manga_ratings.xlsx", index=False)
