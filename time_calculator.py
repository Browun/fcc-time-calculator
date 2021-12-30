def add_time(start: str, duration: str, day = None):
    '''
    Return the resulting time, including day of the week (if provided) and how many days afterward.

    '''

    # Convert input time to hours and minutes
    start_hours, start_minutes = convert_12_to_24_hour(start)
    input_hours, input_minutes = [int(x) for x in duration.split(':')]

    # Convert hours and minutes to days, hours, minutes
    days, hours, minutes = calculate_days(start_hours, start_minutes, input_hours, input_minutes)

    # If day is provided, calculate the day of the week
    if day:
        day_of_week = day_of_the_week(day, days)
        return output_format(days, hours, minutes, day_of_week)

    return output_format(days, hours, minutes)


def convert_12_to_24_hour(input_time: str):
    '''
    Converts a 12 hour input string (hh:mm a) to 24 hour (HH:mm) integers, hour and minutes.
    '''

    # Separate values from input
    time_value, time_period = input_time.split(' ')
    hour_string, minute_string = time_value.split(':')

    # Calculate base time based on AM or PM values
    base_time: int = 0 if time_period == 'AM' else 12

    # Convert strings to int
    hours: int = int(hour_string) + base_time
    minutes: int = int(minute_string)

    return hours, minutes


def output_format(days: int, hours: int, minutes: int, day_of_week = None):
    '''
    Converts a the days, hours, minutes and optinal day of the week to the required output string of format:
    {{hours}}:{{minutes}} {{AM/PM}}, {{day of week}}, ({{days}} days later)
    '''
    # 12:04 AM, Friday (2 days later)

    # Convert 24 hour hours to 12 hour representation
    hours, time_period = convert_24_to_12_hour(hours)

    # Initial output
    output = f"{hours}:{minutes:02d} {time_period}"

    if day_of_week:
        output += f', {day_of_week.capitalize()}'

    if days > 0:
        if days == 1:
            output += f' (next day)'
        else:
            output += f' ({days} days later)'

    return output


def convert_24_to_12_hour(hours: int):
    '''
    Converts a provided 24 hour formatted integer to its 12 hour representation, and provides the relevant time period AM/PM.
    '''
    # Set the base time period
    time_period: str = 'AM'

    # From 12:00 onwards 12 hours need to be deducted and PM set
    if hours > 11:
        hours -= 12
        time_period = 'PM'
    # 0 is equivalent to 12 when converting
    if hours == 0:
        hours += 12
    
    return hours, time_period


def calculate_days(start_hours: int, start_minutes: int, input_hours: int, input_minutes: int):
    '''
    Calculates the number of days from the start time, returning this as an integer.
    '''
    
    # Calculate total minutes
    minutes_added: int = start_minutes + input_minutes

    # Calculate hours and adjusted minutes
    hours, minutes = calculate_hours(start_hours, input_hours, minutes_added)

    # Calulate the number of days based on hours, and remove this number from hours
    if hours > 23:
        days: int = hours // 24
        hours -= days * 24
    else:
        days: int = 0

    return days, hours, minutes


def calculate_hours(start_hours: int, hours: int, minutes: int):
    '''
    Calculates the new time based on the start_hours and start_minutes, adding the hours input. Returns hours and minutes as integers.
    '''

    # Add beginning hours to current hours
    hours: int = start_hours + hours

    # Deal with minutes that need to be converted to hours
    if minutes > 59:
        hours_to_add = int(str(minutes / 60).split('.')[0]) # Done to avoid library import
        hours += hours_to_add
        minutes -= hours_to_add * 60

    return hours, minutes


def day_of_the_week(start_day: str, number_of_days: int):
    '''
    Finds the next day given the start day and number of days, returning the answer as a string.
    '''

    # Variable for week
    week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    # Strip and lowercase the inputted day
    starting_index = week.index(start_day.lower().strip())
    # Calculate the movement
    movement = (starting_index + number_of_days) % 7

    return week[int(movement % 7)]