## CapstoneB

### Repo Directory
- ```/collect-process``` Scripts for scraping/processing
- ```/data``` Processed data
- ```/docs``` Project website
- ```/imgs```
- ```/models```
- ```/other``` Writeup/poster and etc..

Links to raw data (UCSD personal OneDrive):
- [IFCB_2023](https://ucsdcloud-my.sharepoint.com/:u:/g/personal/ady005_ucsd_edu/IQDU5ICaVgteR6p-yTmGK5ZyAV6XU1SX7uJmfHw1TL4uduM?e=NNUJUo) 3.4GB zipped / 10.8GB raw
- [IFCB_2024](https://ucsdcloud-my.sharepoint.com/:u:/g/personal/ady005_ucsd_edu/IQDocyNz6CAwTIjfQ7Km2OMKAUuFbsN1E14rkuqEvRW0irA?e=LexqwY) 17.6GB zipped / 56.2GB raw
- [IFCB_2025](https://ucsdcloud-my.sharepoint.com/:u:/g/personal/ady005_ucsd_edu/IQBVWe3tqkhSR6woE53VSHQIAU3e1OL_qt1NLX22Xg_CuYc?e=3Vj1pC) 14.5GB zipped / 46GB raw
- [Enviromental_data](https://ucsdcloud-my.sharepoint.com/:u:/g/personal/ady005_ucsd_edu/IQAI0c6g1BGVR4mSs5817iNPAdLmKkZRhRyK1Gqtv3AbpTk?e=N9DJht) 66MB zipped / 620MB raw

### Data Collection
Data was collected from [Scripps Pier IFCB 183](https://ifcb.caloos.org/timeline?dataset=scripps-pier-ifcb-183)
- Data spans March 2023 - January 2026, scraping took place Jan 5-26th
- Used laptop running Windows 11 LTSC
    - Ungoogled chromium Version 137.0.7151.119 (Official Build, ungoogled-chromium) (64-bit)
        - Any modern browser works ([documentation](https://pypi.org/project/webdriver-manager/))

Python 3.11.9
```
selenium==4.39.0
webdriver-manager==4.0.2
beautifulsoup4==4.14.2
requests==2.32.5
```

### Other Data Collected
[California Ocean Observing Systems Data Portal](https://data.caloos.org/#metadata/120738/station/data) at Scripps Pier
- CTD and with SeapHOx

```
Temperature
Salinity 
Chlorophyll
Conductivity
Sea Water Density 
Sea Water Pressure 
pH
Oxygen
```
From [Tides and Currents](https://tidesandcurrents.noaa.gov/stationhome.html?id=9410230) at Scripps Pier

We collected various meteorlogical data sampled by hour:
```
Wind Speed (m/s)
Wind Dir (deg)
Wind Gust (m/s)
Air Temp (°C)
Baro (mb)Humidity (%)
Visibility (km)
Water Levels (m)
```
[CALHABMAP](https://data.caloos.org/#module-metadata/5c35689e-2b3a-4bc9-9f5d-e526a9c19620/85653d75-c0b7-48e9-b1b1-f1c4071b10d3) also provides more data at Scripps Pier however we have not acquired it yet :)