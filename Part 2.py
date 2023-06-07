import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Read the data files
data_df = pd.read_csv('data.csv')
data2_df = pd.read_csv('data-2.csv')
data3_df = pd.read_csv('data-3.csv')


# Query 1: New Cases Worldwide (2020 vs. 2021):
def compare_new_cases_worldwide_2020_2021():
    worldwide_2020_data = data_df[data_df['year_week'].str.startswith('2020')]
    worldwide_2021_data = data_df[data_df['year_week'].str.startswith('2021')]
    weekly_cases_2020 = worldwide_2020_data.groupby('year_week')['new_cases'].sum().reset_index()
    weekly_cases_2021 = worldwide_2021_data.groupby('year_week')['new_cases'].sum().reset_index()
    week_numbers_2020 = weekly_cases_2020['year_week'].str[-2:].astype(int)
    week_numbers_2021 = weekly_cases_2021['year_week'].str[-2:].astype(int)
    plt.plot(week_numbers_2020, weekly_cases_2020['new_cases'], marker='o', label='2020')
    plt.plot(week_numbers_2021, weekly_cases_2021['new_cases'], marker='o', label='2021')
    plt.xlabel('Week')
    plt.ylabel('Total New Cases (Millions)')
    plt.title('New Cases Worldwide (2020 vs. 2021)')
    plt.legend()
    plt.xticks(range(1, 53))
    plt.grid(True)
    plt.show()


compare_new_cases_worldwide_2020_2021()


# Query 2: Positive Test Percentages in Countries with Lowest Death Cases:
def compare_positive_test_percentage_lowest_death_cases():
    data = data2_df.groupby('countriesAndTerritories')['deaths'].sum().nsmallest(5).reset_index()
    positive_test_percentages = data_df[data_df['country'].isin(data['countriesAndTerritories'])].groupby('country')['positivity_rate'].mean()
    population_counts = data2_df[data2_df['countriesAndTerritories'].isin(data['countriesAndTerritories'])].groupby('countriesAndTerritories')['popData2020'].max()
    labels = [f"{country}\n({population_counts[country]:,} pop.)" for country in positive_test_percentages.index]
    plt.pie(positive_test_percentages, labels=labels, autopct='%1.1f%%')
    plt.title('Positive Test Percentages in Countries with Lowest Death Cases')
    plt.show()


compare_positive_test_percentage_lowest_death_cases()


# Query 3: Positivity rates between Sweden and Spain in 2021:
def compare_positivity_rates_sweden_spain_2021():
    sweden_data = data_df[(data_df['country'] == 'Sweden') & (data_df['year_week'].str.startswith('2021'))]
    spain_data = data_df[(data_df['country'] == 'Spain') & (data_df['year_week'].str.startswith('2021'))]
    sweden_weeks = sweden_data['year_week'].str.split('-', expand=True)[1]
    spain_weeks = spain_data['year_week'].str.split('-', expand=True)[1]
    plt.plot(sweden_weeks, sweden_data['positivity_rate'], label='Sweden')
    plt.plot(spain_weeks, spain_data['positivity_rate'], label='Spain')
    plt.xlabel('Week')
    plt.ylabel('Positivity Rate')
    plt.title('Positivity rates between Sweden and Spain in 2021')
    plt.legend()
    plt.xticks(rotation=90)
    plt.xticks(range(1, 53))
    plt.show()


compare_positivity_rates_sweden_spain_2021()


# Query 4: Number of deaths between Italy and Spain in the first quarter of 2020.
def compare_deaths_Italy_spain_q1_2020():
    Italy_data = data2_df[(data2_df['countriesAndTerritories'] == 'Italy') & (data2_df['year'] == 2020) & (
        data2_df['month'].between(1, 3))]
    spain_data = data2_df[(data2_df['countriesAndTerritories'] == 'Spain') & (data2_df['year'] == 2020) & (
        data2_df['month'].between(1, 3))]
    Italy_total_deaths = Italy_data['deaths'].sum()
    spain_total_deaths = spain_data['deaths'].sum()
    countries = ['Italy', 'Spain']
    deaths = [Italy_total_deaths, spain_total_deaths]
    plt.bar(countries, deaths, color='lightgreen')
    plt.xlabel('Country')
    plt.ylabel('Total Deaths')
    plt.title('Deaths in Italy and Spain (Q1 2020)')
    for i, value in enumerate(deaths):
        plt.text(i, value, "{:,}".format(value), ha='center', va='bottom')
    plt.show()


compare_deaths_Italy_spain_q1_2020()


# Query 5: Average Tests Done Across Countries with Highest Death Cases:
data = data2_df.groupby('countriesAndTerritories')['deaths'].sum().nlargest(8).reset_index()
d = data_df[data_df['country'].isin(data['countriesAndTerritories'])].groupby('country')['tests_done'].mean().reset_index()
d = d.sort_values('tests_done', ascending=False)
sns.set(style="whitegrid")
ax = sns.barplot(x='country', y='tests_done', data=d, palette='Pastel2')
plt.xlabel('Country')
plt.ylabel('Average Tests Done (Millions)')
plt.title('Average Tests Done Across Countries with Highest Death Cases')
for i, v in enumerate(d['tests_done']):
    ax.text(i, v + 0.5, "{:,.2f}".format(v), ha='center', va='bottom')
plt.show()


# Query 6:Average Weekly Hospital Occupancy between Countries
def Average_weekly_hospital_occupancy_between_countries():
    hospital_occupancy_data = data3_df[data3_df['indicator'] == 'Daily hospital occupancy']
    average_occupancy_by_country = hospital_occupancy_data.groupby('country')['value'].mean().sort_values(
        ascending=False)
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    colors = sns.color_palette("Pastel1")
    ax = sns.barplot(x=average_occupancy_by_country.index, y=average_occupancy_by_country, palette=colors)
    for i, v in enumerate(average_occupancy_by_country):
        ax.text(i, v + 0.5, "{:,.2f}".format(v), ha='center', va='bottom')
    plt.xlabel('Country')
    plt.ylabel('Average Hospital Occupancy')
    plt.title('Average Hospital Occupancy between Countries')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()


Average_weekly_hospital_occupancy_between_countries()


# Query 7:Maximum COVID-19 Cases (2020 vs. 2021) - Cyprus, Luxembourg, Greece'
countries = ['Cyprus', 'Luxembourg', 'Greece']
years = [2020, 2021]
filtered_data = data2_df[data2_df['countriesAndTerritories'].isin(countries) & data2_df['year'].isin(years)]
max_cases_by_country_year = filtered_data.groupby(['countriesAndTerritories', 'year'])['cases'].max().unstack()
ax = max_cases_by_country_year.plot(kind='bar', color=['lightblue', 'lightgreen'])
plt.xlabel('Country')
plt.ylabel('Maximum Number of Cases')
plt.title('Maximum COVID-19 Cases (2020 vs. 2021) - Cyprus, Luxembourg, Greece')
for p in ax.patches:
    ax.annotate(f"{p.get_height():,}", (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')
plt.legend(title='Year')
plt.grid(True)
plt.xticks(rotation=0)  # Set rotation to 0 degrees
plt.show()


# Query 8: Percentage of Deaths out of All Patients in Germany per Month (2020 vs. 2021)
def compare_percentage_deaths_germany_2020_2021():
    germany_data_2020 = data2_df[(data2_df['countriesAndTerritories'] == 'Germany') & (data2_df['year'] == 2020)]
    germany_data_2021 = data2_df[(data2_df['countriesAndTerritories'] == 'Germany') & (data2_df['year'] == 2021)]
    monthly_cases_2020 = germany_data_2020.groupby('month')['cases'].sum()
    monthly_deaths_2020 = germany_data_2020.groupby('month')['deaths'].sum()
    percentage_deaths_2020 = (monthly_deaths_2020 / monthly_cases_2020) * 100
    monthly_cases_2021 = germany_data_2021.groupby('month')['cases'].sum()
    monthly_deaths_2021 = germany_data_2021.groupby('month')['deaths'].sum()
    percentage_deaths_2021 = (monthly_deaths_2021 / monthly_cases_2021) * 100
    months_2020 = monthly_cases_2020.index
    months_2021 = monthly_cases_2021.index
    plt.plot(months_2020, percentage_deaths_2020, marker='o', label='2020', color='green')
    plt.plot(months_2021, percentage_deaths_2021, marker='o', label='2021', color='purple')
    plt.xlabel('Month')
    plt.ylabel('Percentage of Deaths')
    plt.title('Percentage of Deaths out of All Patients in Germany per Month (2020 vs. 2021)')
    plt.legend()
    plt.xticks(ticks=months_2020, labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.grid(True)
    plt.show()


compare_percentage_deaths_germany_2020_2021()


# Query 9: Percentage of Deaths in Countries with Highest Hospital Occupancy
def compare_death_percentage_highest_hospital_occupancy():
    total_deaths_by_country = data2_df.groupby('countriesAndTerritories')['deaths'].sum()
    highest_hospital_occupancy_countries = \
    data3_df[data3_df['indicator'] == 'Daily hospital occupancy'].groupby('country')['value'].mean().nlargest(6).index
    filtered_deaths_by_country = total_deaths_by_country.loc[highest_hospital_occupancy_countries]
    total_deaths = filtered_deaths_by_country.sum()
    death_percentages = (filtered_deaths_by_country / total_deaths) * 100
    pastel_colors = ['#FFB3E6', '#FFD9B3', '#B3E6FF', '#B3FFC9', '#FFE6B3', '#E6B3FF']
    plt.figure(figsize=(8, 8))
    patches, texts, _ = plt.pie(death_percentages, labels=death_percentages.index, autopct='%1.1f%%',
                                colors=pastel_colors)
    plt.title('Percentage of Deaths in Countries with Highest Hospital Occupancy')
    for i, text in enumerate(texts):
        country = death_percentages.index[i]
        hospital_occupancy = \
        data3_df[(data3_df['country'] == country) & (data3_df['indicator'] == 'Daily hospital occupancy')][
            'value'].mean()
        text.set_text(f'{country}\n(Hospital Occupancy: {hospital_occupancy:,.2f})')
    plt.show()


compare_death_percentage_highest_hospital_occupancy()


# Query 10: Number of Positive Tests for the Top 3 Countries with Largest Population in 2020
data_df['year'] = data_df['year_week'].str.slice(0, 4)
data_df['week'] = data_df['year_week'].str.slice(6)
data_2020 = data_df[data_df['year'] == '2021']
top_3_countries = data_2020.groupby('country')['population'].max().nlargest(3).index
data_top_3_countries = data2_df[data2_df['countriesAndTerritories'].isin(top_3_countries)]
cases_data = {}
for country in top_3_countries:
    country_cases = data_top_3_countries[data_top_3_countries['countriesAndTerritories'] == country]['cases']
    cases_data[country] = country_cases
cases_data_list = [cases_data[country] for country in top_3_countries]
plt.figure(figsize=(10, 6))
plt.boxplot(cases_data_list, showfliers=False)
plt.xlabel('Country')
plt.ylabel('Number of Positive Tests')
plt.title('Number of Positive Tests for the Top 3 Countries with Largest Population in 2020')
plt.xticks(range(1, len(top_3_countries) + 1), top_3_countries)
plt.grid(True)
plt.show()



