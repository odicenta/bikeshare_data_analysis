import time
import pandas as pd
import numpy as np
import datetime
from pprint import pprint

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

list_of_cities = ['chicago', 'new york city', 'washington' ]
list_of_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

list_of_days = ['all', 'monday', 'tuesday', 'wednesday', 
                'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')


    city, month, day = False, False, False

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city == False:
        city = str.lower(input("What city would you like to study? (Chicago, New York City or Washington: "))
        if city not in list_of_cities:
            print('Please, check your input and try again (valid options: [Chicago, New York City, Washington]')
            city = False

    # get user input for month (all, january, february, ... , june)
    while month == False:
        month = str.lower(input("What month do you want to study (January to June, use full name): "))
        if month not in list_of_months: 
            print('Please, check your input and try again, make sure you use [all] or the full month name')
            print('Notice that dagta is only available for months January to June')
            month = False

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day == False:
        day = str.lower(input('What day do you want to study (all, or name of the day): '))
        if day not in list_of_days:
            print('Please, check your input and try again, make sure you input [all] or the full name of the day')
            day = False

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print(" ".join(['Filters applied: ',city, month, day]))
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Before starting to filter, fill the NaN of the Gender and Year of Birth with data
    # to avoid losing both columns
    if 'Gender' in df.columns:
        df['Gender'].fillna('Not specified')
    # Notice that by ffilling the Birth year, we will not lose the youngest or oldes, but it may
    # affect the most frequent value obtained, removing these users would affect other maybe 
    #more important stats
    if 'Birth Year' in df.columns:
        df['Birth Year'].fillna(method='ffill', axis=0)

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = list_of_months.index(month) 
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # Create a column for the trip (from - to)
    df['Trip'] = df[['Start Station', 'End Station']].apply(' - '.join, axis=1) 

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Calculate most frequent times of travel
    common_month = df['month'].mode()[0]
    common_day = df['day_of_week'].mode()[0]
    common_hour = df['Start Time'].dt.hour.mode()[0]

    # display the most common month
    print(f'The most common month of travel is: {common_month}.')

    # display the most common day of week
    print(f'The most common day of travel of the week is: {common_day}.')

    # display the most common start hour
    print(f'The most common start hour of travel is: {common_hour}h.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Calcualte most popular stations and trip
    popular_start_station = df['Start Station'].mode()[0]
    popular_end_station = df['End Station'].mode()[0]
    popular_combination = df['Trip'].mode()[0]

    # display most commonly used start station
    print(f'The most common start station is: {popular_start_station}.')

    # display most commonly used end station
    print(f'The most common end station is: {popular_end_station}.')

    # display most frequent combination of start station and end station trip
    print(f'The most common trip (start to end station combination) is: {popular_combination}.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    # Format it for a more friendly version 
    # (https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds)
    total_travel_time = str(datetime.timedelta(seconds=round(int(total_travel_time))))
    print('\nTotal travel time for the selected range of dates is: {}.'.format(total_travel_time))

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    avg_travel_time = str(datetime.timedelta(seconds=round(int(avg_travel_time))))
    print('\nAverage travel time for the selected range of dates is: {}.'.format(avg_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # Preformat the count of user types and number
    users_dict = dict(df['User Type'].value_counts())
    print('\nThe following user types have used the bikesharing program in the selected range: ')
    for key, value in users_dict.items():
        print(': '.join([key, str(value)]))

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_dict = dict(df['Gender'].value_counts())
        print('\nClassified as gender type: ')
        for key, value in gender_dict.items():
            print(': '.join([key, str(value)]))
    else:
        print('There is no data available regarding the gender distribution.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        youngest_user = int(df['Birth Year'].min())
        oldest_user = int(df['Birth Year'].max())
        common_user = int(df['Birth Year'].mode())
        print('Breakdown by year of birth: Youngest: {} - Oldest: {} - Most Frequent: {}'.format(youngest_user,
                                                                                             oldest_user,
                                                                                             common_user))
    else:
        print('There is no data avalable regarding the Birth Year of the users.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Addition to allow the user to see some of the data:
        see_data = input('\nWould you like to see some of the data? Enter yes or no.\n')
        counter = 0
        while see_data.lower() == 'yes':
            pprint(df[counter:counter+5])
            counter += 5
            see_data = input('\nDo you want to see more data? Enter yes or no.\n')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
