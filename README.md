## CapstoneB

### repo directory
- ```/docs``` project website
- ```/data``` data collection and processing, includes data from caloos
- ```/models``` TBD but where models and other things are done
- ```/imgs``` where imgs for various things are stored

link to scraped data: sorry onedrive deleted the file lol


### Data Collection
Data was collected spanning January 5-10
- I used windows laptop running Windows 11 IoT Enterprise LTSC 2024
    - ungoogled chromium Version 137.0.7151.119 (Official Build, ungoogled-chromium) (64-bit)
        - https://github.com/ungoogled-software/ungoogled-chromium/releases/tag/137.0.7151.119-1 (June 20, 2025 build)

Python 3.11.9
```
selenium==4.39.0
webdriver-manager==4.0.2
beautifulsoup4==4.14.2
requests==2.32.5
```
During scraping of data the program timed out 4 times. I resumed from the last downloaded day.
- Improvements: exception handling and retries and longer waiting to be implemented. 


### Other Data Collected
All were collected from
- https://data.caloos.org/#metadata/120738/station/data
time span from
- 01/01/2024 00:00 - 01/01/2026 00:00

turbidity & FDOM: Fluorescent Dissolved Organic Matter were done at the earliest time online to January 1, 2026
- 12/03/2024 17:25 - 01/01/2026 01:00

From this website we get data binned by day for consistency
```
Temperature
Salinity 
Chlorophyll
Conductivity
Sea Water Density 
Sea Water Pressure 
pH (Newport Pier and Scripps Pier)
Oxygen (Newport Pier and Scripps Pier)
```
Add data from
- https://tidesandcurrents.noaa.gov/stationhome.html?id=9410230
which includes Collected hourly
```
Wind Speed (m/s)
Wind Dir (deg)
Wind Gust (m/s)
Air Temp (°C)
Baro (mb)Humidity (%)
Visibility (km)
Water Levels (m)
```

### other other data that has NOT been collected
https://data.caloos.org/#layer-data/59cb173d-9fab-44d0-9a13-5e1c35a10f1b/location_name:Scripps%20Pier
- just more data that can be downloaded omg there is legit so much data
