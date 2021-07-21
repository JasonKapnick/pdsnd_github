import time
import pandas as pd
import numpy as np

months = ['january', 'february', 'march', 'april', 'may',
          'june', 'all']
days_of_week = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday',
                'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    ##create lists for valid selections
    valid_months = ['january', 'february', 'march', 'april', 'may',
                    'june', 'all']
    valid_cities = ['chicago', 'new york', 'washington']
    valid_days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday',
                  'friday', 'saturday', 'sunday', 'all']

    print('Hi, welcome to my project! Let\'s explore some US bikeshare data!')
    valid_selection = False
    while valid_selection is False:
        city = input("Enter city: ").lower()
        if city in valid_cities:
            valid_selection = True
        else:
            print("Invalid selection, please retry. Valid selections:")
            print (valid_cities)

    # get user input for month (all, january, february, ... , june)
    valid_selection = False
    while valid_selection is False:
            month = input("Enter a month January thru June, or 'all':").lower()
            if month in valid_months:
                valid_selection = True
            else:
                print("Invalid selection, please retry. Valid selections:")
                print (valid_months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_selection = False
    while valid_selection is False:
        day = input("Enter day, or choose 'all':").lower()
        if day in valid_days:
            valid_selection = True
        else:
            print("Invalid selection, please retry. Valid selections:")
            print (valid_days)

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
        df - pandas DataFrame containing city data filtered by month and day
    """
    CITY_DATA = {'chicago': 'chicago.csv',
                 'new york': 'new_york_city.csv',
                 'washington': 'washington.csv'}
    city_file = CITY_DATA.get(city)
    print("The city file is: " + city_file)

    # load data file into a dataframe
    df = pd.read_csv(city_file)
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    df['day_of_week'] = pd.DatetimeIndex(df['Start Time']).weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        days_of_week = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday',
                        'friday', 'saturday', 'sunday']
        day = days_of_week.index(day)+1
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = int(df.mode()['month'][0])
    common_month = months[common_month - 1].title()
    print("{} is the most common month.".format(common_month))

    # display the most common day of week
    common_day = int(df.mode()['day_of_week'][0])
    common_day = days_of_week[common_day - 1].title()
    print("{} is the most common day.".format(common_day))

    # display the most common start hour
    df['Start Hour'] = pd.DatetimeIndex(df['Start Time']).hour
    common_start = int(df.mode()['Start Hour'][0] * 100)
    print("{} is the most common starting hour (24hr format)"
          .format(common_start))

    print("\nThis took {:.5f} seconds.".format(time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("{} is the most common start station."
          .format(df.mode()['Start Station'][0]))

    # display most commonly used end station
    print("{} is the most common end station."
          .format(df.mode()['End Station'][0]))

    # display most frequent combination of start station and end station trip
    df['Start Stop Combo'] = df['Start Station'] + " to " + df['End Station']
    # create new column by concatenating start & stop stations
    print("{} is the most common start start stop combo."
          .format(df.mode()['Start Stop Combo'][0]))

    print("\nThis took {:.5f} seconds.".format(time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration_seconds = int(df['Trip Duration'].sum())

    """
    The following variables and calulations convert the total trip duration
    provided in seconds, to a more readable 'days, hours, minutes, seconds'
    format
    """

    total_duration_days = total_duration_seconds // 86400
    remainder_hours = (total_duration_seconds
                        - total_duration_days * 86400) // 3600
    remainder_minutes = (total_duration_seconds
                        - total_duration_days * 86400
                        - remainder_hours * 3600) // 60
    remainder_seconds = (total_duration_seconds
                        - total_duration_days * 86400
                        - remainder_hours * 3600) % 60

    print("Total duration is {} days, {} hours, {} minutes, and {} seconds".
          format(total_duration_days, remainder_hours,
                 remainder_minutes,remainder_seconds))

    # display mean travel time
    mean_duration_seconds = int(df['Trip Duration'].mean())
    mean_duration_days = mean_duration_seconds // 86400
    remainder_hours = (mean_duration_seconds
                        - mean_duration_days * 86400) // 3600
    remainder_minutes = (mean_duration_seconds
                          - mean_duration_days * 86400
                          - remainder_hours * 3600) // 60
    remainder_seconds = (mean_duration_seconds
                          - mean_duration_days * 86400
                          - remainder_hours * 3600) % 60
    print("Mean duration is {} minutes, and {} seconds".
          format(remainder_minutes, remainder_seconds))
    print("\nThis took {:.5f} seconds.".format(time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        print(df['User Type'].value_counts())
    except:
        print("User Type data not available for your selection.")
    print('\n \n')

"""
Gender and birth year data is not provided in all of the data sets.
The program will attempt to provide these statistics, but if unable,
it will print an error message indicating that this data is not available
for the current selection.
"""
    # Display counts of gender
    try:
         print(df['Gender'].value_counts())
    except:
        print("Gender data not available for your selection.")
    print('\n \n')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth = df['Birth Year'].min()
        latest_birth =  df['Birth Year'].max()
        most_common_birth = df['Birth Year'].mode()[0]

        print("The earliest birth year is {:.0f}. \n ".format(earliest_birth))
        print("The most recent birth year is {:.0f}.\n ".format(latest_birth))
        print("The most common birth year is {:.0f}.\n ".format(most_common_birth))
    except:
        print("Birth year data is not available for your selection.")

    print("\nThis took {:.5f} seconds.".format(time.time() - start_time))
    print('-'*40)


def show_data(df):
    """"Displays raw data """
    i = 0
    see_more = 'y'
    while see_more == 'y':
        print(df.iloc[i:i+5])
        i += 5
        see_more = input("Would you like to see the next 5 rows? y/n: ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        see_data = input('\nWould you like to see raw data? y/n \n').lower()
        if see_data == 'y':
                show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
