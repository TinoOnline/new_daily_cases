from request_data import request_data
from forcast import forecast
import json

def main():
    """
    Forcasts the new covid cases

    Outputs:
        forecase.png: which is an image showcasing the predicted results
        new_cases.csv: which is a list of the forcaseted cases
    """
    
    dates, data = request_data()
    forecast(json.loads(dates), json.loads(data))

if __name__ == '__main__':
    main()

