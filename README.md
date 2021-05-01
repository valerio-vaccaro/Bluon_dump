# Bluon_dump
Dump all data connected to a Bluon GPS Lora localizer.

## Install requirements
This script is totally based on python3, all libraries needed are available online via pip.

I suggest to install this tool in a virtualenv with the following commands.

```
virtualenv -p python3 venv3
. venv3/bin/activate
pip install -r requirements.text
```

## Usage
Just call the script directly or via python, you will need to specify a key for authentication (use the one present in the link in the email sent to you when you enter or exit a specific zone or the parameter `s` passed to `load_coords.php` page).

```
python bluon_dump.py --help

'||''|.   '||                            _      '||
 ||   ||   ||  ... ...    ...   .. ...        .. ||  ... ...  .. .. ..   ... ...
 ||'''|.   ||   ||  ||  .|  '|.  ||  ||     .'  '||   ||  ||   || || ||   ||'  ||
 ||    ||  ||   ||  ||  ||   ||  ||  ||     |.   ||   ||  ||   || || ||   ||    |
.||...|'  .||.  '|..'|.  '|..|' .||. ||.    '|..'||.  '|..'|. .|| || ||.  ||...'
        Dump all data connected to a Bluon GPS Lora localizer.           ||
                                                                        ''''
Usage: bluon_dump.py [OPTIONS]

  Dump all data connected to a Bluon GPS Lora localizer.

Options:
  --days INTEGER  (Numeric - Default:10) Days to go back in the history - if
                  you set 0 I will stop at first empty day
  --csv TEXT      (Boolean - Default:True) Save all data in a CSV file
  --key TEXT      (String) The bluon key like in the link present in some
                  email (url parameter s)
  --quiet TEXT    (Boolean - Default:False)  Be quiet
  --image TEXT    (Boolean - Default:False)  Create images
  --help          Show this message and exit.
```

### CSV
The script automatically save the fetched data points in a CSV with the following structure.

`,id,tracker_dev_id,lat,lon,date,speed,altitude,gps_num,hdop,emergency,charging,battery,seqno,sf,timestamp`

### Images
The script can generate some images using a `ggplot-like` library.
