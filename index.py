from request_data import request_data
from forcast import forecast
import json

dates, data = request_data()
print(forecast(json.loads(dates), json.loads(data)))

