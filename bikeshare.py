import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = ''
    cities = ['chicago', 'new york city', 'washington']
    month = ''
    months = ['all', 'january', 'february','march','april','may','june']
    day = ''
    days = ['all', 'monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    
    city = ''
    
    while (city not in cities):
        if city == '':
            city = input('For which city would you like to see data? (Chicago, New York City, Washington):').lower()
        else:
            city = input('Sorry! The city you typed in is not a valid city. Try again. (Chicago, New York City, Washington):').lower()

    
    while (month not in months):
        if month == '':
            month = input('For which month would you like to view data? Please write the full name of the month (January to June). Write "all" if you would like to view the data of all available months:').lower()
        else:
            month = input('Sorry! We do not have data available for the month you typed in. Try again. :').lower()

    
    while(day not in days):
        if day == '':
            day = input('For which day would you like to view data? Please write the full name of the day of the week (Monday to Sunday). Write "all" if you would like to view the data of all days:').lower()
        else:
            day = input('Sorry! There is an error trying to fetch the data. Type the day of the week or "all" for which you would like the data:').lower()

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
    df = pd.read_csv(CITY_DATA[city])
    
    ## convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    ## extract month, day of week, and hour from the Start Time column to create a month, day of week, and hour column
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    ## find the most common month
    common_month = df['month'].mode()[0]
    print('Most Common Month:', common_month)


    ## find the most common month
    common_day_of_week = df['day_of_week'].mode()[0]
    print('Most Common Day of the Week:', common_day_of_week)

    ## find the most common start hour
    common_hour = df['hour'].mode()[0]   
    print('Most Common Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    ## find the most common start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:', common_start_station)

    common_end_station = df['End Station'].mode()[0]
    print('Most Common End Station:', common_end_station)

    # Combine the two columns into a single DataFrame
    combined = df.groupby(['Start Station', 'End Station']).size().reset_index(name='count')
    
    # Find the mode (most frequent combination)
    frequent_combination = combined.loc[combined['count'].idxmax()]
    print('Most Frequent Combination of Start and End Station:', frequent_combination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)

    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.
    
    The Gender and Birth Year columns are not present in one of the files. Therefore, we verify if
    this data exists in the table.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('The counts of user types:')
    print(df['User Type'].value_counts())

    if 'Gender' in df:
        print('The counts of gender:')
        print(df['Gender'].value_counts())

    if 'Birth Year' in df:
        earliest_year = df['Birth Year'].min()
        print('Earliest Birth Year:', earliest_year)

        most_recent_year = df['Birth Year'].max()
        print('Most Recent Birth Year:', most_recent_year)

        common_year = df['Birth Year'].mode()[0]
        print('Most Common Birth Year:', common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """
    This method asks the user if they want to display lines of raw data from the chosen city.
    """
    rows = 5
    check = input('Would you like to see the first 5 lines of raw data? (yes/no):').lower()
    if(check != 'yes'):
        print("Raw data will not be displayed.")
    else:
        while(check == 'yes' and rows <= len(df.index)):
            print(df.head(rows))
            rows += 5
            if rows <= len(df.index):
                check = input('Would you like to see the next 5 lines of raw data? (yes/no):').lower()
            else:
                print("There is no more data to display.")
                check = 'no'

def main():
    """
    Once the script is running, after displaying the information that was requested, it will ask the user
    if they want to display different kind of information.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
