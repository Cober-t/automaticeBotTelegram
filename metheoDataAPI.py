
from datetime import datetime
from meteostat import Point, Daily
from definitions import LOCATION_POINT

def getDate():
    return datetime.today().date()

# Set time period
today = datetime.today()
today = datetime(today.year, today.month, today.day)
# end = datetime(today.year, today.month, today.day)

# Create Point for Madird, Spain
location = Point(LOCATION_POINT["lat"], LOCATION_POINT["long"], LOCATION_POINT["alt"])

# Get daily data
data = Daily(location, start=today, end=today)
data = data.fetch()
