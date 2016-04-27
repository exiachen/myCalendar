#!/usr/bin/python

import copy, time, sys

month = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
weekDays = ['Sun.', 'Mon.', 'Tues.', 'Wed.', 'Thurs.', 'Fri.', 'Sat.']

def getLocalTime():
	localtime = time.localtime()
	return (localtime.tm_year, localtime.tm_mon, localtime.tm_mday)

def colored(text, color = None):
    fmt_str = '\x1B[;%dm%s\x1B[0m'

    if color is not None:
        text = fmt_str % (color, text)

    return text

def isLeapYear(year):
	if ((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0):
		return True
	else:
		return False

def countLeapYear(dateStart, dateEnd):
	count = 0
	for year in range(dateStart[0] + 1, dateEnd[0]):
		if isLeapYear(year):
			count += 1
	return count

def countOrderDays(dateStart, dateEnd):
	passDays = {dateStart : 0, dateEnd : 0}
	remainDays = copy.copy(passDays)
	
	for item in (dateStart, dateEnd):
		for m in range(item[1] - 1):
			passDays[item] += month[m]
		passDays[item] += item[2]

		if isLeapYear(item[0]) and item[1] > 2:
			passDays[item] += 1
		remainDays[item] = [365, 366][int(isLeapYear(item[0]))] - passDays[item]

	if dateStart[0] == dateEnd[0]:
		count = passDays[dateEnd] - passDays[dateStart]
	else:	
		count = passDays[dateEnd] + remainDays[dateStart] + (dateEnd[0] - dateStart[0] - 1) * 365 + countLeapYear(dateStart, dateEnd)
	return count	


def countDays(date1, date2):
	if date1 < date2:
		return countOrderDays(date1, date2)
	else:
		return countOrderDays(date2, date1)

def countWeekDay(date):
	baseSunday = (2013, 12, 15)
	
	count = countDays(date, baseSunday)
	count %= 7

	if date >= baseSunday:
		return weekDays[count]
	else:
		return weekDays[-count]	

def genCalendar(year, mon, day = None):
	monthDays = month[mon - 1]

	if isLeapYear(year) and mon == 2:
		monthDays += 1
	
	print 'Year: %d  Mon: %d'%(year, mon)

	for item in weekDays:
		print '%-5s'%item,
	print '\n'
	
	weekDayIndex = weekDays.index(countWeekDay((year, mon, 1)))

	for i in range(weekDayIndex):
		print '%-5s' % ' ',
	
	for num in range(monthDays):
		if day is not None and day == (num + 1):
			print colored('%-5d' % (num + 1), 37),
		else:
			print '%-5d' % (num + 1),
		
		weekDayIndex += 1
		if (weekDayIndex % 7 == 0):
			print '\n'

def useage():
	print 'calendar.py [year] [month]'

if __name__ == '__main__':
	if len(sys.argv) == 1:
		y, m, d = getLocalTime()
		genCalendar(y, m, d)
	elif len(sys.argv) == 3:
		y = int(sys.argv[1])
		m = int(sys.argv[2])
		if y <= 2099 and y >= 1980 and m <= 12 and m >= 1:
			genCalendar(y, m)
		else:
			useage()
	else:
		useage() 

