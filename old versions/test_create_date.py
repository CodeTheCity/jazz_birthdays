import datetime

def create_date(d,m,y):

	date1 = datetime.date(y,m,d)
	return date1

date2 = create_date (4, 5, 1966)

print date2

