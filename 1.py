import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar

# Read the data files
data_df = pd.read_csv('data.csv')
data2_df = pd.read_csv('data-2.csv')
data3_df = pd.read_csv('data-3.csv')

# #Query 1: Total deaths by country
description = 'Total deaths by country'
data = data2_df.groupby('countriesAndTerritories')['deaths'].sum().reset_index()
data_sorted = data.sort_values('deaths', ascending=False)
top_countries = data_sorted.head(5)['countriesAndTerritories']
color_palette = sns.color_palette("Set2", 5)
country_color_dict = {country: color for country, color in zip(top_countries, color_palette)}
bar_colors = [country_color_dict.get(country, 'gray') for country in data['countriesAndTerritories']]
plt.bar(data['countriesAndTerritories'], data['deaths'], color=bar_colors)
plt.xlabel('Country')
plt.ylabel('Total Deaths')
plt.title(description)
plt.xticks(rotation=90)
for i, value in enumerate(data['deaths']):
    label = '{:,.0f}'.format(value)  # Format label with comma
    plt.text(i, value, label, ha='center', va='bottom')
plt.show()

#Query 2: Total deaths per population by country, Top 5
description = 'Total deaths per population by country, Top 5'
data = data2_df.groupby('countriesAndTerritories').apply(lambda x: x['deaths'].sum() / x['popData2020'].max()).reset_index(name='deaths_per_population')
data_sorted = data.sort_values('deaths_per_population', ascending=False)
num_countries = 5
top_countries = data_sorted.head(num_countries)['countriesAndTerritories']
top_deaths_per_population = data_sorted.head(num_countries)['deaths_per_population']
percentages = (top_deaths_per_population / top_deaths_per_population.sum()) * 100
colors = sns.color_palette('Pastel1', num_countries)
plt.pie(percentages, labels=top_countries, colors=colors, autopct='%.1f%%')
plt.title(description)
plt.axis('equal')
plt.show()

#Query 3: Worldwide Total Cases by Month for 2020
d = data2_df[data2_df['year'] == 2020].groupby('month')['cases'].sum().reset_index()
d['month'] = d['month'].apply(lambda x: calendar.month_name[int(x)])
sns.set(style="whitegrid")
sns.barplot(data=d, x='month', y='cases', palette='Blues')
plt.xlabel('Month')
plt.ylabel('Total Cases (Ten Million)')
plt.title('Worldwide Total Cases by Month for 2020')
for i, value in enumerate(d['cases']):
    plt.text(i, value, "{:,}".format(int(value)), ha='center', va='bottom')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.show()

#Query 4: Total Number of New Cases Worldwide per Year
d = data_df.groupby(data_df['year_week'].str[:4])['new_cases'].sum().reset_index()
sns.set(style="whitegrid")
sns.barplot(x='year_week', y='new_cases', data=d, palette='Pastel2')
plt.xlabel('Year')
plt.ylabel('Number of New Cases (Hundred Millions)')
plt.title('Total Number of New Cases Worldwide per Year')

# Add labels on each bar
for i, value in enumerate(d['new_cases']):
    label = '{:,.0f}'.format(value)  # Format label with comma and without decimal
    plt.text(i, value, label, ha='center', va='bottom')

plt.show()

#Query 5: Total tests done and Positivity Rate in Germany per week in 2021
description = 'Total tests done and Positivity Rate in Germany per week in 2021'
data = data_df[(data_df['country'] == 'Germany') & data_df['year_week'].str.contains('2021')].reset_index()
fig, ax1 = plt.subplots()
ax1.bar(data['year_week'], data['tests_done'], color='lightgreen')  # Change bar color to light green
ax1.set_xlabel('Week')
ax1.set_ylabel('Total Tests Done', color='green')
ax1.tick_params(axis='y', labelcolor='green')
ax1.set_title(description)
ax2 = ax1.twinx()
ax2.plot(data['year_week'], data['positivity_rate'], color='salmon')  # Change line color to salmon
ax2.set_ylabel('Positivity Rate', color='red')
ax2.tick_params(axis='y', labelcolor='red')
ax1.set_xticklabels([week.split('-W')[1] for week in data['year_week']])
plt.tight_layout()
plt.xticks(rotation=90)
plt.show()

#Query 6: Weekly Hospital Occupancy in Austria (2020)
austria_data = data3_df[(data3_df['country'] == 'Austria') & (data3_df['date'].str[:4] == '2020')]
austria_data['date'] = pd.to_datetime(austria_data['date'])
weekly_data = austria_data.groupby('year_week')['value'].sum().reset_index()
weekly_data = weekly_data.sort_values('year_week')
plt.plot(weekly_data['year_week'], weekly_data['value'],color='coral')
plt.xlabel('Week')
plt.ylabel('Weekly Hospital Occupancy')
plt.title('Weekly Hospital Occupancy in Austria (2020)')
plt.xticks(rotation=90)
plt.show()

#Query 7: Total cases vs. total deaths in Greece (2021)
italy_2022_data = data2_df[(data2_df['countriesAndTerritories'] == 'Italy') & (data2_df['year'] == 2022)]
monthly_data = italy_2022_data.groupby('month').sum()
total_deaths = monthly_data['deaths']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
available_months = months[:len(total_deaths)]
plt.plot(available_months, total_deaths, label='Total Deaths')
plt.xlabel('Month')
plt.ylabel('Count')
plt.title('Total Deaths in Italy (2022)')
plt.legend()
plt.show()

# Query 8: Min 5 countries Testing rate for 2022
description = 'Min 5 countries tests done for 2021 (mean)'
data = data_df[data_df['year_week'].str.contains('2021')].groupby('country')['tests_done'].mean().nsmallest(5).reset_index()
plt.bar(data['country'], data['tests_done'], color='green')
plt.xlabel('Country')
plt.ylabel('Tests done')
plt.title(description)
plt.xticks(rotation=90)
for i, value in enumerate(data['tests_done']):
    label = '{:,.0f}'.format(value)  # Format label with comma
    plt.text(i, value, label, ha='center', va='bottom')
plt.show()


#Query 9: Top 5 countries with the lowest death cases for 2021
description = 'Top 5 countries with the lowest death cases for 2021'
data = data2_df[data2_df['year'] == 2022].groupby('countriesAndTerritories')['deaths'].sum().nsmallest(5).reset_index()
plt.bar(data['countriesAndTerritories'], data['deaths'], color='coral')
plt.xlabel('Country')
plt.ylabel('Total Deaths')
plt.title(description)
for i, value in enumerate(data['deaths']):
    label = '{:,.0f}'.format(value)  # Format label with comma
    plt.text(i, value, label, ha='center', va='bottom')

plt.show()


#Query 10: Positivity Rate Trend in Cyprus, years 2021-2022
d = data_df[(data_df['country'] == 'Cyprus') & ((data_df['year_week'].str[:4] == '2022') | (data_df['year_week'].str[:4] == '2021'))]
sns.lineplot(data=d, x="year_week", y="positivity_rate", color='green')
plt.grid(axis = 'y')
plt.xlabel('Year Week')
plt.xlim('2021-W01', '2022-W52')
plt.ylabel('Positivity Rate')
plt.title('Positivity Rate Trend in Cyprus, years 2021-2022')
plt.xticks(rotation=90)
plt.show()










