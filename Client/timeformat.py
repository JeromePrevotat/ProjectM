#TIMESTAMP FORMAT FILE
from datetime import datetime
import resources as res

def get_time_format(ui):
	return (datetime.now().strftime(ui.res.timeFormat))
