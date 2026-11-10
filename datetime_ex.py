from datetime import datetime, timedelta

date_string = input().split()

base_date = datetime.strptime(date_string[0], "%Y-%m-%d")

for date_string in date_string[1:]:
    current_date = datetime.strptime(date_string, "%Y-%m-%d")

    difference = current_date - base_date

    print(difference.days)


from datetime import datetime, timedelta

date_string = input()
days = int(input())

date = datetime.strptime(date_string, "%Y-%m-%d")
new_date = date + timedelta(days = days)

print(new_date.strftime("%Y-%m-%d"))





from datetime import datetime, timedelta

date1s = datetime.strptime(input(), "%Y-%m-%d %H:%M")
date2s = datetime.strptime(input(), "%Y-%m-%d %H:%M")


difference = date2s - date1s

minutes = difference.total_seconds() / 60

print(int(minutes))