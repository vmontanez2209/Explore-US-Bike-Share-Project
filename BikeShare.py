import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday',
            'friday', 'saturday', 'sunday']

strlen = 90

print_line = lambda char: print(char[0] * strlen)


def filter_month():
    """
    Asks user to specify a month to filter on, or choose all.
    Returns:
        (str) month - name of the month to filter by, or 'all' for no filter
    """
    while True:
        try:
            month = input('    Enter the month with January=1, June=6 or "a" for all:  ')
        except:
            print('        ---->>  Valid input:  1 - 6, a')
            continue
        if month == 'a':
            month = 'all'
            break
        elif month in {'1', '2', '3', '4', '5', '6'}:
            month = MONTHS[int(month) - 1]
            break
        else:
            continue
    return month


def filter_day():
    """
    Asks user to specify a day to filter on, or choose all.
    Returns:
        (str) day - day of the week to filter by, or 'all' for no filter
    """
    while True:
        try:
            day = input('    Enter the day with Monday=1, Sunday=7 or "a" for all:  ')
        except:
            print('---->>  Valid input:  1 - 7, a')
            continue
        if day == 'a':
            day = 'all'
            break
        elif day in {'1', '2', '3', '4', '5', '6', '7'}:
            day = WEEKDAYS[int(day) - 1]
            break
        else:
            continue

    return day


def filter_city():
    """
    Asks user to specify a city.
    Returns:
        (str) city - name of the city to analyze
    """
    cities_list = []
    num_cities = 0

    for a_city in CITY_DATA:
        cities_list.append(a_city)
        num_cities += 1
        print('{0:20}. {1}'.format(num_cities, a_city.title()))

    while True:
        try:
            city_option = int(input('\n    Enter a number for the city (1 - {}):  '.format(len(cities_list))))
        except:
            continue
        if city_option in range(1, len(cities_list)+1):
            break
    city = cities_list[city_option - 1]
    return city


def print_time(start_time):
    time_str = '[... %s seconds]' % round((time.time() - start_time), 3)
    print(time_str.rjust(strlen))
    print_line('-')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or 'all' to apply no month filter
        (str) day - name of the day of week to filter by, or 'all' to apply no day filter
    """
    print_line('=')
    print('\n  Hello! Let\'s explore some US bikeshare data!\n')

    city = filter_city()

    month = filter_month()

    day = filter_day()

    return city, month, day


def summary_filter(city, month, day, init_total_rides, df):
    """
    Displays selected city, filters chosen, and simple stats on dataset.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or 'all' to apply no month filter
        (str) day - name of the day of week to filter by, or 'all' to apply no day filter
        (int) init_total_rides - total number of rides in selected city before filter
        (dataframe) df - filtered dataset
    """
    start_time = time.time()

    filtered_rides = len(df)
    num_stations_start = len(df['Start Station'].unique())
    num_stations_end = len(df['End Station'].unique())

    print('  Gathering statistics for:      ', city)
    print('    Filters (month, day):        ', month, ', ', day)
    print('    Total rides in dataset:      ', init_total_rides)
    print('    Rides in filtered set:       ', filtered_rides)
    print('    Number of start stations:    ', num_stations_start)
    print('    Number of end stations:      ', num_stations_end)

    print_time(start_time)


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or 'all' to apply no month filter
        (str) day - name of the day of week to filter by, or 'all' to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    start_time = time.time()
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    init_total_rides = len(df)
    filtered_rides = init_total_rides

    if month != 'all':
        month_i = MONTHS.index(month) + 1
        df = df[df.month == month_i]
        month = month.title()

    if day != 'all':
        day_i = WEEKDAYS.index(day)
        df = df[df.day_of_week == day_i]
        day = day.title()

    print_time(start_time)

    summary_filter(city.title(), month, day, init_total_rides, df)

    return df


def hour_12_str(hour):
    """
    Converts an int hour time to string format with PM or AM.
    Args:
        (int) hour - int representing an hour
    Returns:
        (str) str_hour - string with time in 12 hour format
    """

    if hour == 0:
        str_hour = '12 AM'
    elif hour == 12:
        str_hour = '12 PM'
    else:
        str_hour = '{} AM'.format(hour) if hour < 12 else '{} PM'.format(hour - 12)
    return str_hour


def time_stat(df):
    """Displays statistics on the most frequent times of travel."""

    print('  Most Frequent Times of Travel...')
    start_time = time.time()

    month = MONTHS[df['month'].mode()[0] - 1].title()
    print('    Month:               ', month)

    common_day = df['day_of_week'].mode()[0]
    common_day = WEEKDAYS[common_day].title()
    print('    Day of the week:     ', common_day)

    hour = hour_12_str(df['hour'].mode()[0])
    print('    Start hour:          ', hour)
    print_time(start_time)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('  Most Popular Stations and Trip...')
    start_time = time.time()

    filtered_rides = len(df)
    start_station = df['Start Station'].mode()[0]
    start_station_trips = df['Start Station'].value_counts()[start_station]

    print('    Start station:       ', start_station)
    print('{0:30}{1}/{2} trips'.format(' ', start_station_trips, filtered_rides))

    end_station = df['End Station'].mode()[0]
    end_station_trips = df['End Station'].value_counts()[end_station]

    print('    End station:         ', end_station)
    print('{0:30}{1}/{2} trips'.format(' ', end_station_trips, filtered_rides))

    df_start_end_combination_gd = df.groupby(['Start Station', 'End Station'])
    most_freq_trip_count = df_start_end_combination_gd['Trip Duration'].count().max()
    most_freq_trip = df_start_end_combination_gd['Trip Duration'].count().idxmax()

    print('    Frequent trip:        {}, {}'.format(most_freq_trip[0], most_freq_trip[1]))
    print('{0:30}{1} trips'.format(' ', most_freq_trip_count))

    print_time(start_time)


def seconds_str(total_seconds):
    """
    Converts number of seconds to human readable string format.
    Args:
        (int) total_seconds - number of seconds to convert
    Returns:
        (str) day_hour_str - number of weeks, days, hours, minutes, and seconds
    """

    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)

    day_hour_str = ''
    if weeks > 0:
        day_hour_str += '{} weeks, '.format(weeks)
    if days > 0:
        day_hour_str += '{} days, '.format(days)
    if hours > 0:
        day_hour_str += '{} hours, '.format(hours)
    if minutes > 0:
        day_hour_str += '{} minutes, '.format(minutes)
    if total_seconds > 59:
        day_hour_str += '{} seconds'.format(seconds)

    return day_hour_str


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('  Trip Duration...')
    start_time = time.time()

    total_travel_time = int(df['Trip Duration'].sum())
    print('    Total travel time:   ', total_travel_time, 'seconds')
    print('                             ', seconds_str(total_travel_time))

    mean_travel_time = int(df['Trip Duration'].mean())
    print('    Mean travel time:    ', mean_travel_time, 'seconds')
    print('                             ', seconds_str(mean_travel_time))

    print_time(start_time)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('  User Stats...')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    for idx in range(len(user_types)):
        val = user_types[idx]
        user_type = user_types.index[idx]
        print('    {0:21}'.format((user_type + ':')), val)
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        for idx in range(len(genders)):
            val = genders[idx]
            gender = genders.index[idx]
            print('    {0:21}'.format((gender + ':')), val)
    if 'Birth Year' in df.columns:
        print('    Year of Birth...')
        print('        Earliest:        ', int(df['Birth Year'].min()))
        print('        Most recent:     ', int(df['Birth Year'].max()))
        print('        Most common:     ', int(df['Birth Year'].mode()))

    print_time(start_time)


def actual_data(df):
    """
    Asks if the user would like to see some lines of data from the filtered dataset.
    Displays 5 (show_rows) lines, then asks if they would like to see 5 more.
    Continues asking until they say stop.
    """
    show_rows = 5
    rows_start = 0
    rows_end = show_rows - 1

    print('\n    Would you like to see the raw data from the current dataset?')
    while True:
        raw_data = input('      (yes or no):  ')
        if raw_data.lower() == 'yes':
            print('\n    Displaying rows {} to {}:'.format(rows_start + 1, rows_end + 1))
            print('\n', df.iloc[rows_start: rows_end + 1])
            rows_start += show_rows
            rows_end += show_rows
            print_line('.')
            print('\n    Display the next {} rows?'.format(show_rows))
            continue
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stat(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        actual_data(df)
        restart = input('\n    Would you like to restart? (yes or no):  ')
        if restart.lower() != 'yes':
            break


if __name__ == '__main__':
    main()
