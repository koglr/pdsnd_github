import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'Chicago': 'chicago.csv',
    'New York City': 'new_york_city.csv',
    'Washington': 'washington.csv'
}

CITY_OPTIONS = {
    0: 'Chicago',
    1: 'New York City',
    2: 'Washington'
}

MONTH_OPTIONS = {
    0: 'All',
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'Oktober',
    11: 'November',
    12: 'December'
}

DAY_OPTIONS = {
    0: 'All',
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday',
    7: 'Sunday'
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = get_user_input_for_options('City', CITY_OPTIONS)
    month = get_user_input_for_options('Month', MONTH_OPTIONS)
    day = get_user_input_for_options('Day', DAY_OPTIONS)

    print('Filters are set to: \n\t City = {} \n\t Month = {} \n\t Day = {}'.format(CITY_OPTIONS[city],
                                                                                     MONTH_OPTIONS[month],
                                                                                     DAY_OPTIONS[day]))

    print('-' * 40)
    return city, month, day


def get_user_input_for_options(name, option_set):
    """
    Generic helper function to get a selection from the user for a given set of options from the command line.

    Args:
        (str) name - name of the option which shall be displayed to the user
        (str) option_set - a dictionary in the form of {option_value as int: option_name as string}
    Returns:
        chosen_option - the option_value chosen as int
    """

    error_message = 'You entered an invalid option!'
    chosen_option = -1

    while True:
        try:
            print('Please choose a valid value for {}. Valid options are:'.format(name))
            for option_name, option_value in option_set.items():
                print('\t{} => {}'.format(option_name, option_value))

            chosen_option = int(input())
        except ValueError:
            print(error_message)
            continue

        if chosen_option < 0 or chosen_option >= len(option_set):
            print(error_message)
        else:
            break

    return chosen_option


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

    df = pd.read_csv(CITY_DATA[CITY_OPTIONS[city]])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # Filter by month if applicable
    if month != 0:
        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 0:
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == (day - 1)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    most_common_month_msg = 'The most common month is: \n{}\n\n'.format(most_common_month)
    print(most_common_month_msg)

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    most_common_day_of_week_msg = 'The most common day of week is: \n{}\n\n'.format(most_common_day_of_week)
    print(most_common_day_of_week_msg)

    # display the most common start hour
    most_common_start_hour = df['Start Time'].dt.hour.mode()[0]
    most_common_start_hour_msg = 'The most common start hour is: \n{}\n\n'.format(most_common_start_hour)
    print(most_common_start_hour_msg)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    most_common_start_station_msg = 'The most commonly used start station is: \n{}\n\n'.format(
        most_common_start_station)
    print(most_common_start_station_msg)

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    most_common_end_station_msg = 'The most commonly used end station is: \n{}\n\n'.format(most_common_end_station)
    print(most_common_end_station_msg)

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    most_common_start_end_station_msg = \
        'The most frequent combination of start and end station is: \n{}\n\n'.format(most_common_start_end_station)
    print(most_common_start_end_station_msg)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_msg = 'The total travel time is: \n{}\n\n'.format(total_travel_time)
    print(total_travel_time_msg)

    # display mean travel time
    average_travel_time = round(df['Trip Duration'].mean())
    average_travel_time_msg = 'The average travel time is: \n{}\n\n'.format(average_travel_time)
    print(average_travel_time_msg)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    user_type_count_msg = 'The counts of user types is: \n{}\n\n'.format(user_type_count)
    print(user_type_count_msg)

    # Display counts of gender
    gender_count = df['Gender'].value_counts()
    gender_count_msg = 'The counts of genders is: \n{}\n\n'.format(gender_count)
    print(gender_count_msg)

    # Display earliest, most recent, and most common year of birth
    earliest_year_of_birth = int(df['Birth Year'].min())
    earliest_year_of_birth_msg = 'The earliest year of birth is: \n{}\n\n'.format(earliest_year_of_birth)
    print(earliest_year_of_birth_msg)

    most_recent_year_of_birth = int(df['Birth Year'].max())
    most_recent_year_of_birth_msg = 'The most recent year of birth is: \n{}\n\n'.format(most_recent_year_of_birth)
    print(most_recent_year_of_birth_msg)

    most_common_year_of_birth_msg = int(df['Birth Year'].mode()[0])
    most_common_year_of_birth_msg = 'The most common year of birth is: \n{}\n\n'.format(most_common_year_of_birth_msg)
    print(most_common_year_of_birth_msg)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


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
