import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

list_of_cities = ['chicago', 'new york city', 'washington' ]
list_of_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june',
                  'july', 'august', 'september', 'october', 'november', 'december']
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
        month = str.lower(input("What month do you want to study (use full name): "))
        if month not in list_of_months: 
            print('Please, check your input and try again, make sure you use [all] or the full month name')
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
    print(" ".join([city, month, day]))
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    print(df)
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = list_of_months.index(month) 
        print(month) 
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    print(df)
    # TODO: notice that there are some months that do not have data, as starting in july for chicago
    # need to add some logic to cover this issue or will provide a Key error as the dataframe is empty
    # Maybe after the filtering, a recount of how much data is available for this particular
    # month and day can provide insight and help with the logic.

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    print(df)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month of travel is: {}'.format(df['month'].mode()[0]))

    # display the most common day of week
    print('The most common day of travel of the week is: {}'.format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print('The most common start hour of travel is: {}'.format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nThe most common start station is: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('\nThe most common end station is: {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time


    # display mean travel time


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types


    # Display counts of gender


    # Display earliest, most recent, and most common year of birth


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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
