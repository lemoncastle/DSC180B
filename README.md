## CapstoneB

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
- To improve code, there should be exception handling and retries implemented. 
