from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from requests.exceptions import ConnectionError, Timeout
import pandas as pd

from bs4 import BeautifulSoup
from pathlib import Path
import requests
from datetime import datetime
import time

options = webdriver.ChromeOptions()
# run in headless mode (doesn't open visible browser window)
options.add_argument('--headless=new') 

base_url="https://ifcb.caloos.org"

# scrape 2023 - 2024 data
start_url = "https://ifcb.caloos.org/bin?dataset=scripps-pier-ifcb-183&bin=D20230302T200944_IFCB183"
end_url = "https://ifcb.caloos.org/bin?dataset=scripps-pier-ifcb-183&bin=D20240118T161914_IFCB183"

# scrape 2024 - 2025 data
# start_url = "https://ifcb.caloos.org/bin?dataset=scripps-pier-ifcb-183&bin=D20240118T161914_IFCB183"
# end_url = "https://ifcb.caloos.org/bin?dataset=scripps-pier-ifcb-183&bin=D20250101T185049_IFCB183"

# scrape 2025 - 2026 data
# start_url = "https://ifcb.caloos.org/bin?dataset=scripps-pier-ifcb-183&bin=D20250101T185049_IFCB183"
# end_url = "https://ifcb.caloos.org/bin?dataset=scripps-pier-ifcb-183&bin=D20260101T002031_IFCB183"

url = start_url

date = url.split("bin=")[1].split("_")[0][1:9]
month = url.split("bin=")[1].split("_")[0][5:7]
new_month = month
s = datetime.now()
session = requests.Session()
# create output directory for month (MUST DEFINE YEAR, minor bug sry) 
out_dir = Path(f"./ifcb_downloads/2023{month}")
out_dir.mkdir(parents=True, exist_ok=True)

driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)
driver.get(url)

ml_data = []

# wait up to 15 seconds, poll every 1 seconds
wait = WebDriverWait(driver, timeout=15, poll_frequency=1)
def href_not_hash(driver): # wait until the href of download links are updated (not '#')
            el = driver.find_element(By.ID, "download-hdr")
            href = el.get_attribute("href")
            return "hdr" in href

# wait with retry function for selenium timeouts (loading javascript)
def wait_with_retry(wait1, driver, retry_delay=120):
    try:
        wait1()
        return True

    except TimeoutException:
        print("Page timed out. Refreshing page and retrying...")
        time.sleep(retry_delay)
        try:
            driver.refresh()
            wait1()
            return True
        except TimeoutException:
            print("Timed out after retrying, exiting...")
            return False

# for download requests
def download_with_retry(session, url, out_path, retries=1, delay=120):
    for attempt in range(retries + 1):
        try:
            with session.get(url, stream=True, timeout=30) as r:
                r.raise_for_status()
                with open(out_path, "wb") as f:
                    for chunk in r.iter_content(8192):
                        f.write(chunk)
            return True

        except (ConnectionError, Timeout) as e:
            if attempt < retries:
                print(f"Download failed ({e}). Retrying in {delay}s...")
                time.sleep(delay)
            else:
                return False 

try:
    while url != end_url:
        while new_month == month:
            time.sleep(4)  # global wait for Js to load content and update hrefs
            burger = wait_with_retry(lambda: wait.until(href_not_hash), driver)
            if not burger:
                print("Failed to load javascript content.")
                print(url)
                driver.quit()
                raise SystemExit

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            tag = soup.find("span", id="stat-ml-analyzed")
            ml_value = float(tag.get_text(strip=True).split()[0]) if tag else None
            ml_data.append({"date": date, "ml_analyzed": ml_value})
            
            for file_id in ["download-hdr","download-features","download-class-scores"]:
                tag = soup.find("a", id=file_id)
                file_url = base_url + tag["href"]

                filename = file_url.split("/")[-1]
                out_path = out_dir / filename
                if out_path.exists(): continue
                
                success = download_with_retry(session, file_url, out_path, retries=2, delay=120)
                if not success:
                    print(f"Failed to download {file_url} after retries. Exiting.")
                    driver.quit()
                    raise SystemExit
            
            # "physically" click the "next-bin" button
            #  js shenanigans prevents getting just the next bin href
            # wait for URL to change
            next_button = driver.find_element(By.ID, "next-bin")
            driver.execute_script("arguments[0].click();", next_button)        
            
            burger = wait_with_retry(lambda: wait.until(lambda d: d.current_url != url), driver)
            if not burger:
                print(url)
                driver.quit()
                raise SystemExit

            # update date, month, and url
            new_date = driver.current_url.split("bin=")[1].split("_")[0][1:9]
            new_month= driver.current_url.split("bin=")[1].split("_")[0][5:7]
            if new_date != date: 
                print(f"Downloaded day: {date} in {(datetime.now()- s).total_seconds()}s")
                date = new_date
            url = driver.current_url
        
        # end of month loop - save ml analyzed data and go next
        df = pd.DataFrame(ml_data)
        df.to_csv(out_dir / f"ml_{month}.csv", index=False)
        ml_data.clear()
        
        print(f"== Downloaded all data of month {month} in {(datetime.now()- s).total_seconds()}s")
        month=new_month
        # update for new month (MUST DEFINE YEAR, minor bug sry)
        out_dir = Path(f"./ifcb_downloads/2023{month}")
        out_dir.mkdir(parents=True, exist_ok=True)

finally: # the interwebs says try/finally is good incase cat errors
    driver.quit()
    print(url)
    print(f"Finished downloading ALL DATA in {(datetime.now()- s).total_seconds()}s")