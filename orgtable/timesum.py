def Execute(column):
	import sublime
	import datetime
	minutes_sum = 0
	for cell in column:
		hours, minutes = str(cell).strip().split(':')
		minutes_sum += int(hours) * 60 + int(minutes)
	hours = minutes_sum // 60	
	minutes = minutes_sum % 60
	return "{:02d}:{:02d}".format(int(hours), int(minutes))