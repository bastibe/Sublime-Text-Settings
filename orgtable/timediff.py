def Execute(row):
	import sublime
	import datetime
	times = [cell_to_minutes(cell) for cell in row]
	try:
		start, stop, pause = times
	except:
		sublime.status_message("invalid row '{}'".format(row))
		return
		
	minutes_diff = stop - start - pause
	hours = minutes_diff // 60	
	minutes = minutes_diff % 60
	return "{:02d}:{:02d}".format(int(hours), int(minutes))


def cell_to_minutes(cell):
	if ':' in str(cell):
		hours, minutes = str(cell).strip().split(':')
		hours, minutes = int(hours), int(minutes)
		if hours < 0:
			minutes = -minutes
	else:
		hours, minutes = 0, 0

	return hours * 60 + minutes
