import time
import pandas as pd

city_data = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

yes_no_data = ["yes",
               "no"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nHello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Which city do you want to explore (Chicago, New York City, or Washington)?\n')
            if city_data.get(city.strip().lower()) is None:
                print('City {} is not an option.  Please select a city from the 3 choices.\n'.format(city))
            else:
                city = city.strip().lower()
                break
        except (KeyboardInterrupt, ValueError, EOFError):
            print('Invalid input entered.  Please try again.\n')

    # get user input for which data filter to use (month, day, or none)
    print()
    filter_report_header = ""
    filter_choice = {"month":1,
                      "day":2,
                      "none":0}
    while True:
        try:
            time_filter_selected = input('Would you like to filter the data by month, day or not at all? Type \'none\' for no time filter.\n')
            if filter_choice.get(time_filter_selected.strip().lower()) is None:
                print('{} is not a valid time filter option.  Please select a filter from the 3 choices.\n'.format(time_filter_selected))
            else:
                time_filter_selected = time_filter_selected.strip().lower()
                break
        except (KeyboardInterrupt, ValueError, EOFError):
            print('Invalid input entered.  Please try again.\n')

    # get user input for month (all, january, february, ... , june)
    month_data = {"January":1,
                  "February":2,
                  "March":3,
                  "April":4,
                  "May":5,
                  "June":6,
                  "All":99}
    if filter_choice[time_filter_selected]==1:
        while True:
            try:
                month = input('\nFor which month (January, February, March, April, May, June or All)?\n')
                if month_data.get(month.strip().title()) is None:
                    print('{} is not a valid month option.  Please select a valid month.\n'.format(month))
                else:
                    filter_report_header = month.strip().title()
                    month = month_data[month.strip().title()]
                    break
            except (KeyboardInterrupt, ValueError, EOFError):
                print('Invalid input entered.  Please try again.\n')
    else:
        month = month_data['All']

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_data = {"Mon":0,
                "Tue":1,
                "Wed":2,
                "Thu":3,
                "Fri":4,
                "Sat":5,
                "Sun":6,
                "All":99}
    if filter_choice[time_filter_selected]==2:
        while True:
            try:
                day = input('\nFor which day (Mon, Tue, Wed, Thu, Fri, Sat, Sun, or All)?\n')
                if day_data.get(day.strip().title()) is None:
                    print('{} is not a valid day option.  Please select a valid day.\n'.format(day))
                else:
                    filter_report_header = day.strip().title()
                    day = day_data[day.strip().title()]
                    break
            except (KeyboardInterrupt, ValueError, EOFError):
                print('Invalid input entered.  Please try again.\n')
    else:
        day = day_data['All']

    print('-'*74)
    print(' '*10 + 'Statistics for city: ', city.title())
    print(' '*10 + 'Time Filter Used   : ', time_filter_selected, ' -{}'.format(filter_report_header))
    print('-'*74)

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

    # value of 99 for month or day means 'All'
    if month < 99:
        #filter by desired month
        df_temp = pd.read_csv(city_data[city])
        df_temp['Month'] = pd.to_datetime(df_temp['Start Time']).dt.month
        df = df_temp[df_temp.Month.eq(month)]
        #print('filtered by month')
        #print(df)
    elif day < 99:
        #filter by desired day
        df_temp = pd.read_csv(city_data[city])
        df_temp['Weekday'] = pd.to_datetime(df_temp['Start Time']).dt.weekday
        df = df_temp[df_temp.Weekday.eq(day)]
        #print('filtered by day')
        #print(df)
    else:
        # no filters
        df = pd.read_csv(city_data[city])

    print()

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # add Month name
    df['Month Name'] = pd.to_datetime(df['Start Time']).dt.month_name(locale = 'English')
    #groupby month name and then count the data per month name
    start_month_name_cnt = df.groupby(['Month Name'])['Month Name'].count()
    print('The most common month      : ',start_month_name_cnt.idxmax(), ' with ',start_month_name_cnt.max(), 'counts')

    # display the most common day of week
    # add weekday name
    df['Weekday Name'] = pd.to_datetime(df['Start Time']).dt.day_name()
    #groupby day name and then count the data per day name
    start_day_name_cnt = df.groupby(['Weekday Name'])['Weekday Name'].count()
    print('The most common day of week: ',start_day_name_cnt.idxmax(), ' with ',start_day_name_cnt.max(), 'counts')

    # display the most common start hour
    #add hour, groupby hour and then count the data per hour
    df['Hour'] = pd.to_datetime(df['Start Time']).dt.hour
    start_hour_cnt = df.groupby(['Hour'])['Hour'].count()
    print('The most common start hour : ',start_hour_cnt.idxmax(), ' with ',start_hour_cnt.max(), 'counts')

    print("\nThis took %s seconds." % (time.time() - start_time),"\n"+"-"*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_cnt = df.groupby(['Start Station'])['Start Station'].count()
    print('Most commonly used start station: ',start_station_cnt.idxmax(),' with ',start_station_cnt.max(),' counts')

    # display most commonly used end station
    end_station_cnt = df.groupby(['End Station'])['End Station'].count()
    print('Most commonly used end station  : ',end_station_cnt.idxmax(),' with ',end_station_cnt.max(),' counts')

    # display most frequent combination of start station and end station trip
    start_end_station_cnt = df.groupby(['Start Station','End Station'])['Start Station'].count()
    print('\nMost frequent combination of start station and end station trip:\n')
    print('-----Start Station-------------End Station----------------\n',start_end_station_cnt.idxmax()," with ",start_end_station_cnt.max()," counts")

    print("\nThis took %s seconds." % (time.time() - start_time),"\n"+"-"*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Time    : ', df['Trip Duration'].sum())

    # display mean travel time
    print('Average Trip Duration: ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time),"\n"+"-"*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df.groupby(['User Type'])['User Type'].count())

    print()
    # Display counts of gender
    #check if Gender column exists
    if 'Gender' in list(df.columns):
        print(df.groupby(['Gender'])['Gender'].count())
    else:
        print('No Gender data available.')

    # Display earliest, most recent, and most common year of birth
    #check if Birth Year column exists
    if 'Birth Year' in list(df.columns):
        # earliest
        print('\nEarliest year of birth   : ',int(df['Birth Year'].min()))
        # most recent
        print('Most recent year of birth: ',int(df['Birth Year'].max()))
        # most common year of birth
        birth_year_cnt = df.groupby(['Birth Year'])['Birth Year'].count()
        print('Most common year of birth: ',int(birth_year_cnt.idxmax())," with ",birth_year_cnt.max()," counts\n")
    else:
        print('No Birth Year data available.')

    print("\nThis took %s seconds." % (time.time() - start_time),"\n"+"-"*40)


def display_raw_data(df):
    """Displays raw data rows"""

    no_of_rows = 5

    while True:
        try:
            yes_no = input('\nDo you want to view 5 lines of raw data? Enter yes or no.\n')
            if yes_no.strip().lower() in yes_no_data:
                if yes_no.strip().lower() == yes_no_data[0]:
                    print(df.head(no_of_rows))
                    while True:
                        try:
                            yes_no = input('\nView 5 more lines of raw data? Enter yes or no.\n')
                            if yes_no.strip().lower() == yes_no_data[0]:
                                no_of_rows += 5
                                print(df.head(no_of_rows))
                            elif yes_no.strip().lower() == yes_no_data[1]:
                                break
                            else:
                                print('{} is not a valid option.  Please type yes or no.'.format(yes_no))
                        except (KeyboardInterrupt, ValueError, EOFError):
                            print('Invalid input entered.  Please try again.\n')
                break
            else:
                print('{} is not a valid option.  Please type yes or no'.format(yes_no))
        except (KeyboardInterrupt, ValueError, EOFError):
            print('Invalid input entered.  Please try again.\n')

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        while True:
            try:
                restart = input('\nWould you like to restart? Enter yes or no.\n')
                if restart.strip().lower() in yes_no_data:
                    break
                else:
                    print('{} is not a valid option.  Please type yes or no'.format(restart))
            except (KeyboardInterrupt, ValueError, EOFError):
                print('Invalid input entered.  Please try again.\n')

        if restart.strip().lower() != yes_no_data[0]:
            break

if __name__ == "__main__":
	main()
