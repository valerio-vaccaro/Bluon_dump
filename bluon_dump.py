#!/usr/bin/python
####################################################################################
# '||''|.   '||                            _      '||
#  ||   ||   ||  ... ...    ...   .. ...        .. ||  ... ...  .. .. ..   ... ...
#  ||'''|.   ||   ||  ||  .|  '|.  ||  ||     .'  '||   ||  ||   || || ||   ||'  ||
#  ||    ||  ||   ||  ||  ||   ||  ||  ||     |.   ||   ||  ||   || || ||   ||    |
# .||...|'  .||.  '|..'|.  '|..|' .||. ||.    '|..'||.  '|..'|. .|| || ||.  ||...'
#                                                                           ||
#                                                                          ''''
####################################################################################
import requests
import json
import pandas as pd
from plotnine import *
import click

banner = """
'||''|.   '||                            _      '||
 ||   ||   ||  ... ...    ...   .. ...        .. ||  ... ...  .. .. ..   ... ...
 ||'''|.   ||   ||  ||  .|  '|.  ||  ||     .'  '||   ||  ||   || || ||   ||'  ||
 ||    ||  ||   ||  ||  ||   ||  ||  ||     |.   ||   ||  ||   || || ||   ||    |
.||...|'  .||.  '|..'|.  '|..|' .||. ||.    '|..'||.  '|..'|. .|| || ||.  ||...'
         Dump all data connected to a Bluon GPS Lora localizer.           ||
                                                                         ''''     """
print(banner)

@click.command()
@click.option('--days', default=10, help='(Numeric - Default:10) Days to go back in the history - if you set 0 I will stop at first empty day')
@click.option('--csv', default=True, help='(Boolean - Default:True) Save all data in a CSV file')
@click.option('--key', prompt='Your key', help='(String) The bluon key like in the link present in some email (url parameter s)')
@click.option('--quiet', default=False, help='(Boolean - Default:False)  Be quiet')
@click.option('--image', default=False, help='(Boolean - Default:False)  Create images')
def main(days, csv, key, quiet, image):
    """Dump all data connected to a Bluon GPS Lora localizer."""
    set = {}
    set['id'] = []
    set['tracker_dev_id'] = []
    set['lat'] = []
    set['lon'] = []
    set['date'] = []
    set['speed'] = []
    set['altitude'] = []
    set['gps_num'] = []
    set['hdop'] = []
    set['emergency'] = []
    set['charging'] = []
    set['battery'] = []
    set['seqno'] = []
    set['sf'] = []
    set['timestamp'] = []

    if (days==0):
        stop = 1000000
    else:
        stop = days

    for i in range (0, stop):
        payload = {'s': key, 'offset': str(i)}
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        r = requests.post('https://bluon.me/utilities/active/load_coords.php', data=payload, headers=headers)
        dataset = r.json()[0]['last_coord']

        if (days==0):
            if len(dataset) == 0:
                break

        for row in dataset:
            if not quiet:
                print(row)
            set['id'].append(row['id'])
            set['tracker_dev_id'].append(row['tracker_dev_id'])
            set['lat'].append(row['lat'])
            set['lon'].append(row['lon'])
            set['date'].append(row['date'])
            set['speed'].append(row['speed'])
            set['altitude'].append(row['altitude'])
            set['gps_num'].append(row['gps_num'])
            set['hdop'].append(row['hdop'])
            set['emergency'].append(row['emergency'])
            set['charging'].append(row['charging'])
            set['battery'].append(row['battery'])
            set['seqno'].append(row['seqno'])
            set['sf'].append(row['sf'])
            set['timestamp'].append(row['timestamp'])

    df = pd.DataFrame(set)
    df['id'] = pd.to_numeric(df.id)
    df['lat'] = pd.to_numeric(df.lat)
    df['lon'] = pd.to_numeric(df.lon)
    df['speed'] = pd.to_numeric(df.speed)
    df['altitude'] = pd.to_numeric(df.altitude)
    df['gps_num'] = pd.to_numeric(df.gps_num)
    df['hdop'] = pd.to_numeric(df.hdop)
    df['emergency'] = pd.to_numeric(df.emergency)
    df['charging'] = pd.to_numeric(df.charging)
    df['battery'] = pd.to_numeric(df.battery)
    df['seqno'] = pd.to_numeric(df.seqno)
    df['sf'] = pd.to_numeric(df.sf)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', origin='unix')
    if csv:
        df.to_csv('dataset.csv')
    if image:
        img = ggplot(df, aes('lat', 'lon')) + geom_point()
        img.save(filename="lat-lon.png")
        img = ggplot(df, aes('timestamp', 'altitude')) + geom_point()
        img.save(filename="altitude.png")
        img = ggplot(df, aes('timestamp', 'speed')) + geom_point()
        img.save(filename="speed.png")
        img = ggplot(df, aes('timestamp', 'battery')) + geom_point()
        img.save(filename="battery.png")

if __name__ == '__main__':
    main()
