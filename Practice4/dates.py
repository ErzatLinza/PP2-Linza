from datetime import datetime, timedelta


# 1. Subtract five days from the current date

current_date = datetime.now()
five_days_ago = current_date - timedelta(days=5)

print("1. Current date:", current_date.date())
print("Five days ago:", five_days_ago.date())


# 2. Print yesterday, today, and tomorrow

today = datetime.now().date()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("\n2. Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)


# 3. Remove microseconds

current_time = datetime.now()
without_microseconds = current_time.replace(microsecond=0)

print("\n3. Original:", current_time)
print("Without microseconds:", without_microseconds)


# 4. Calculate the difference between two dates in seconds

date1 = datetime(2026, 9, 20, 10, 0, 0)
date2 = datetime(2026, 9, 21, 12, 30, 0)

difference = date2 - date1

print("\n4. Difference in seconds:", difference.total_seconds())