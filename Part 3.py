import pandas as pd
import locale
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


locale.setlocale(locale.LC_ALL, '')

# Read the data files
data_df = pd.read_csv('data.csv')
data2_df = pd.read_csv('data-2.csv')
data3_df = pd.read_csv('data-3.csv')

# User input
country = input("Country: ")
week = input("Week: ")
year = input("Year: ")

# Format the week and year to the correct format
formatted_week = f"{year}-W{week.zfill(2)}"

population = data_df[data_df['country'] == country]['population'].iloc[0]
d1 = data_df[(data_df['country'] == country) & (data_df['year_week'] == formatted_week)][['country', 'year_week', 'new_cases', 'tests_done', 'positivity_rate']]
d2 = data2_df[(data2_df['countriesAndTerritories'] == country) & (data2_df['year'] == int(year))][['dateRep', 'month', 'cases', 'deaths', 'countriesAndTerritories']]
d2['dateRep'] = pd.to_datetime(d2['dateRep'], format='%d/%m/%Y')
d3 = data3_df[(data3_df['country'] == country) & (data3_df['year_week'] == formatted_week)][['country', 'indicator', 'year_week', 'date', 'value']]

new_cases = d1['new_cases'].sum()
deaths = d2[d2['dateRep'].dt.strftime('%Y-W%U') == formatted_week]['deaths'].sum()
tests_done = d1['tests_done'].sum()
positivity_rate = d1['positivity_rate'].mean()

weekly_hospital_occupancy = data3_df[(data3_df['country'] == country) & (data3_df['indicator'] == 'Weekly new hospital admissions per 100k') & (data3_df['year_week'] == formatted_week)]
weekly_icu_occupancy = data3_df[(data3_df['country'] == country) & (data3_df['indicator'] == 'Weekly new ICU admissions per 100k') & (data3_df['year_week'] == formatted_week)]

if len(weekly_hospital_occupancy) > 0:
    weekly_hospital_occupancy_value = weekly_hospital_occupancy['value'].sum()
else:
    weekly_hospital_occupancy_value = 0

if len(weekly_icu_occupancy) > 0:
    weekly_icu_occupancy_value = weekly_icu_occupancy['value'].sum()
else:
    weekly_icu_occupancy_value = 0

# Replace NaN values with 0
new_cases = np.nan_to_num(new_cases, nan=0)
deaths = np.nan_to_num(deaths, nan=0)
tests_done = np.nan_to_num(tests_done, nan=0)
positivity_rate = np.nan_to_num(positivity_rate, nan=0)
weekly_hospital_occupancy_value = np.nan_to_num(weekly_hospital_occupancy_value, nan=0)
weekly_icu_occupancy_value = np.nan_to_num(weekly_icu_occupancy_value, nan=0)



# Define the figure size and padding
fig = plt.figure(figsize=(12, 8))
fig.tight_layout(pad=4)
kpi_style = {'fontweight': 'bold', 'fontsize': 16, 'color': 'blue'}

# Define the outer rectangle dimensions
rect_x = 0.05
rect_y = 0.05
rect_width = 0.9
rect_height = 0.9

# Plot 1: New Cases
ax1 = fig.add_subplot(2, 3, 1)
ax1.text(0.5, 0.5, f"{locale.format_string('%d', new_cases, grouping=True)}", ha='center', va='center', **kpi_style)
ax1.add_patch(patches.Rectangle((0.1, 0.1), 0.8, 0.8, linewidth=2, edgecolor='black', facecolor='none'))
ax1.axis('off')
ax1.set_title('New Cases', fontweight='bold', fontsize=10, pad=20)

# Plot 2: Deaths
ax2 = fig.add_subplot(2, 3, 2)
ax2.text(0.5, 0.5, f"{locale.format_string('%d', deaths, grouping=True)}", ha='center', va='center', **kpi_style)
ax2.add_patch(patches.Rectangle((0.1, 0.1), 0.8, 0.8, linewidth=2, edgecolor='black', facecolor='none'))
ax2.axis('off')
ax2.set_title('Deaths', fontweight='bold', fontsize=10, pad=20)

# Plot 3: Tests Done
ax3 = fig.add_subplot(2, 3, 3)
ax3.text(0.5, 0.5, f"{locale.format_string('%d', tests_done, grouping=True)}", ha='center', va='center', **kpi_style)
ax3.add_patch(patches.Rectangle((0.1, 0.1), 0.8, 0.8, linewidth=2, edgecolor='black', facecolor='none'))
ax3.axis('off')
ax3.set_title('Tests Done', fontweight='bold', fontsize=10, pad=20)

# Plot 4: Positivity Rate
ax4 = fig.add_subplot(2, 3, 4)
labels = ['Positive', 'Negative']
sizes = [positivity_rate, 100 - positivity_rate]
colors = ['blue', 'lightgray']
explode = (0.1, 0)
ax4.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax4.axis('equal')
ax4.set_title('Positivity Rate', fontweight='bold', fontsize=10, pad=30)

# Plot 5: Weekly Hospital Occupancy
ax5 = fig.add_subplot(2, 3, 5)
sizes = [weekly_hospital_occupancy_value, 100 - weekly_hospital_occupancy_value]
colors = ['red', 'lightgray']
explode = (0.1, 0.0)
ax5.pie(sizes, explode=explode, colors=colors, autopct='%1.1f%%', startangle=90)
ax5.axis('equal')
ax5.set_title('Weekly new hospital admissions \n(per 100k)', fontweight='bold', fontsize=10, pad=20)

# Plot 6: Weekly ICU Occupancy
ax6 = fig.add_subplot(2, 3, 6)
sizes = [weekly_icu_occupancy_value, 100 - weekly_icu_occupancy_value]
colors = ['red', 'lightgray']
explode = (0.1, 0.0)
ax6.pie(sizes, explode=explode, colors=colors, autopct='%1.1f%%', startangle=90)
ax6.axis('equal')
ax6.set_title('Weekly new ICU admissions \n(per 100k)', fontweight='bold', fontsize=10, pad=20)


# Add rectangle around the layout
rect = patches.Rectangle((rect_x, rect_y), rect_width, rect_height, linewidth=2, edgecolor='black', facecolor='none')
fig.patches.append(rect)

# Add title above the dashboard with population
fig.suptitle(f"COVID-19 Dashboard - {country}, {formatted_week}\nPopulation: {locale.format_string('%d', population, grouping=True)}", fontsize=18, fontweight='bold', y=0.95)

# Adjust the spacing between subplots
fig.tight_layout(rect=(rect_x, rect_y, rect_width, rect_height))

# Show the dashboard
plt.show()
