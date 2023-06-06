import pandas as pd
import matplotlib.pyplot as plt

# Read the data files
data_df = pd.read_csv('data.csv')
data2_df = pd.read_csv('data-2.csv')
data3_df = pd.read_csv('data-3.csv')

# Define the queries
queries = {
    1: {
        'description': 'Total deaths by country',
        'data': data2_df.groupby('countriesAndTerritories')['deaths'].sum().reset_index()
    },
    2: {
        'description': 'Total deaths per population by country',
        'data': data2_df.groupby('countriesAndTerritories').apply(
            lambda x: (x['deaths'].sum() / x['popData2020'].max())).reset_index(name='deaths_per_population')
    },
    3: {
        # need to change to months
        'description': 'Positivity rate in Italy per month (2020)',
        'data': data_df[(data_df['country'] == 'Italy') & (data_df['year_week'].str.startswith('2020'))].groupby(
            'year_week')['positivity_rate'].mean().reset_index()
    },
    4: {
        # need to change
        'description': 'Daily new cases worldwide',
        'data': data2_df.groupby('dateRep')['cases'].sum().reset_index()
    },
    5: {
        'description': 'Total tests done by top 5 countries in 2021',
        'data': data_df[data_df['year_week'].str.contains('2021')].groupby('country')['tests_done'].sum().nlargest(
            5).reset_index()
    },
    6: {
        'description': 'Top 5 countries with the highest number of new cases in 2020',
        'data': data_df[data_df['year_week'].str.contains('2020')].groupby('country')['new_cases'].sum().nlargest(
            5).reset_index()
    },
    7: {

        # 'description': 'Total cases vs. total deaths in Greece (2021)',
        # 'data': pd.DataFrame({
        #     'Total Cases': [data2_df[(data2_df['countriesAndTerritories'] == 'Greece') & (data2_df['year'] == 2021)][
        #                         'cases'].sum()],
        #     'Total Deaths': [data2_df[(data2_df['countriesAndTerritories'] == 'Greece') & (data2_df['year'] == 2021)][
        #                          'deaths'].sum()]
        # })

        # dosent work
        'description': 'Total cases vs. total deaths in Greece (2021)',
        'data': pd.DataFrame({
            'Total Cases': [data2_df[(data2_df['countriesAndTerritories'] == 'Greece') & (data2_df['year'] == 2021)][
                                'cases'].sum()],
            'Total Deaths': [data2_df[(data2_df['countriesAndTerritories'] == 'Greece') & (data2_df['year'] == 2021)][
                                 'deaths'].sum()]
        }, index=[0])

    },
    8: {
        'description': 'Min 5 countries Testing rate for 2022',
        'data': data_df[data_df['year_week'].str.contains('2022')].groupby('country')['testing_rate'].mean().nsmallest(5).reset_index()

    },
    9: {
        # need to change graph
        'description': 'Positive and negative tests by top 5 countries with max population',
        'data': pd.merge(
            data_df.groupby('country')['new_cases'].sum().reset_index(),
            data_df.groupby('country')['tests_done'].sum().reset_index(),
            on='country'
        ).merge(
            data_df.groupby('country')['population'].max().nlargest(5).reset_index(),
            on='country'
        )
    },
    10:{
        'description': 'Top 5 countries with the lowest death cases for 2021',
        'data': data2_df[data2_df['year'] == 2021].groupby('countriesAndTerritories')['deaths'].sum().nsmallest(
            5).reset_index()
    },
    11:  {
        'description': 'Value trends for a specific indicator',
        'data': None  # Placeholder for dynamic input
    }
}

# Display the menu
while True:
    print("Choose a query to display:")
    for key, value in queries.items():
        # Swap options for Query 1 and Query 2
        print(f"{key}. {value['description']}")
    print("0. Exit")

    # Get user input
    choice = input("Enter your choice: ")

    if choice == '0':
        print("Goodbye!")
        break

    try:
        choice = int(choice)
        if choice in queries:
            if choice == 7:
                # Plot the graph for Query 7
                data = queries[7]['data']
                if isinstance(data, pd.DataFrame):
                    if len(data) > 0:
                        plt.plot(data.index, data['Total Cases'], label='Total Cases')
                        plt.plot(data.index, data['Total Deaths'], label='Total Deaths')
                        plt.xlabel('Date')
                        plt.ylabel('Count')
                        plt.title(queries[7]['description'])
                        plt.legend()
                        plt.show()
                    else:
                        print("No data available for Greece in 2021.")
                else:
                    print("Invalid data format for the selected query.")
            elif choice == 11:
                # Get indicator name from the user
                indicator_name = input("Enter the indicator name: ")
                queries[choice]['data'] = data3_df[data3_df['indicator'].str.lower() == indicator_name.lower()]
            else:
                # Plot the graph for other queries
                data = queries[choice]['data']
                if isinstance(data, pd.DataFrame):
                    if len(data) > 0:
                        if choice == 4:
                            data['dateRep'] = pd.to_datetime(data['dateRep'])
                            data = data.set_index('dateRep')
                            data.plot(figsize=(10, 6))
                        else:
                            data.plot(x=data.columns[0], y=data.columns[1], kind='bar', figsize=(10, 6))
                        plt.xlabel(data.columns[0])
                        plt.ylabel(data.columns[1])
                        plt.title(queries[choice]['description'])
                        plt.show()
                    else:
                        print("No data available for the selected query.")
                else:
                    print("Invalid data format for the selected query.")
        else:
            print("Invalid choice. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")