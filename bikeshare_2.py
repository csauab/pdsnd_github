import time
import pandas as pd

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please enter the name of the city, (chicago, new york city, washington) to analyze").lower()
    while city not in ('chicago', 'new york city', 'washington'):
        city = input("The name of the city is invalid, please re-enter (chicago, new york city, washington)").lower()
    
    if city == 'new york city':
        city = city.replace(' ', '_')
        
    # get user input for month (all, january, february, ... , june)
    valid_month_input = (
        'january', 'february', 'march', 'april', 'may', 'june', 'all'
    )
    month = input("Please enter the month to analyze, ('january' to 'june', or 'all') to analyze").lower()
    while month not in valid_month_input:
        month = input("The month is invalid, please re-enter. ('january' to 'june', or 'all') ").lower()
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_day_input = (
        'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'
    )
    day = input("Please enter the day to analyze, ('monday' to 'sunday', or 'all') to analyze").lower()
    while day not in valid_day_input:
        day = input("The day is invalid, please re-enter. ('monday' to 'sunday', or 'all')").lower()

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

    df = pd.read_csv(f'{city}.csv', index_col=0)
    df[['Start Time', 'End Time']] = df[['Start Time', 'End Time']].apply(pd.to_datetime)
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Start Time'].dt.month == month]
    
    if day != 'all':
        df = df[df['Start Time'].dt.day_name() == day.title()]
        
    df = df.reset_index(drop = True)
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print(f"The most common month is {months[df['Start Time'].dt.month.mode()[0] - 1].title()}")

    # display the most common day of week
    print(f"The most common day of week is {df['Start Time'].dt.day_name().mode()[0]}")

    # display the most common start hour
    print(f"The most common start hour is {df['Start Time'].dt.hour.mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f"The most commonly used start station is {df['Start Station'].mode()[0]}")

    # display most commonly used end station
    print(f"The most commonly used end station is {df['End Station'].mode()[0]}")

    # display most frequent combination of start station and end station trip
    start_to_end = df['Start Station'] + ' to ' + df['End Station']
    print(f"The most frequent combination of start station and end station trip is {start_to_end.mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print(f"Total travel time in seconds is {df['Trip Duration'].sum()} s")

    # display mean travel time
    print(f"Mean travel time in seconds is {df['Trip Duration'].mean():.2f} s")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCount for user types\n')
    print(df['User Type'].value_counts())
    try:
        # Display counts of gender
        print('\nCount for Gender\n')
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        print(f"\nEaliest birth year is {int(df['Birth Year'].min())}")
        print(f"Most recent birth year is {int(df['Birth Year'].max())}")
        print(f"Most common birth year is {int(df['Birth Year'].mode()[0])}")
    except:
        print('There is no Gender / Birth year data in the dataframe')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw(df):
    """Display the raw df upon user request"""
    start_row = 0
    while True and start_row < len(df):
        user_input = input('Do you want to see next 5 lines of raw data? (yes/no)').lower()
        if user_input != 'yes':
            return
        else:
            print('\n 5 rows of raw dataframe \n')
            print(df[start_row: start_row+5])
            start_row += 5
    print('There is no more raw data to dislplay')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
