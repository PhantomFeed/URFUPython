import pandas as pd
from datetime import datetime

pd.set_option('expand_frame_repr', False)
file = 'vacancies_by_year.csv'
df = pd.read_csv(file)
df['years'] = df['published_at'].apply(lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%S%z").year)
years = df['years'].unique()

for year in years:
    data = df[df['years'] == year]
    data.iloc[:, :6].to_csv(f"csv_files\\part_{year}.csv", index=False)
    # data[['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at']].to_csv(rf"csv_files\part_{year}.csv", index=False)