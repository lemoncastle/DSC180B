from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
from pathlib import Path
import requests
from datetime import datetime
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')

base_url="https://ifcb.caloos.org"
start_url = "https://ifcb.caloos.org/bin?dataset=scripps-pier-ifcb-183&bin=D20250101T185049_IFCB183"
end_url = "https://ifcb.caloos.org/bin?dataset=scripps-pier-ifcb-183&bin=D20260101T002031_IFCB183"
url = start_url

date = url.split("bin=")[1].split("_")[0][1:9]
month = url.split("bin=")[1].split("_")[0][5:7]
new_month = month
s = datetime.now()
session = requests.Session()

out_dir = Path(f"./ifcb_downloads/2025{month}")
out_dir.mkdir(parents=True, exist_ok=True)

driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)
driver.get(url)

# wait up to 15 seconds, poll every 1 seconds
wait = WebDriverWait(driver, timeout=15, poll_frequency=1)
def href_not_hash(driver): # wait until the href of download links are updated (not '#')
            el = driver.find_element(By.ID, "download-hdr")
            href = el.get_attribute("href")
            return "hdr" in href

while url != end_url:
    while new_month == month:
        time.sleep(3)  # wait for Js to load content and update hrefs
        wait.until(href_not_hash)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        for file_id in ["download-hdr","download-features","download-class-scores"]:
            tag = soup.find("a", id=file_id)
            file_url = base_url + tag["href"]

            filename = file_url.split("/")[-1]
            out_path = out_dir / filename
            if out_path.exists(): continue
            
            with session.get(file_url, stream=True) as r:
                r.raise_for_status()
                with open(out_path, "wb") as f:
                    for chunk in r.iter_content(8192):
                        f.write(chunk)
        
        # "physically" click the "next-bin" button
        #  js shenanigans prevents getting just the next bin href
        # wait for URL to change
        next_button = driver.find_element(By.ID, "next-bin")
        driver.execute_script("arguments[0].click();", next_button)        
        wait.until(lambda d: d.current_url != url)

        # update date month, and url
        new_date = driver.current_url.split("bin=")[1].split("_")[0][1:9]
        new_month= driver.current_url.split("bin=")[1].split("_")[0][5:7]
        if new_date != date: 
            print(f"Downloaded day: {date} in {(datetime.now()- s).total_seconds()}s")
            date = new_date
        url = driver.current_url
    
    # end of month loop
    print(f"== Downloaded all data of month {month} in {(datetime.now()- s).total_seconds()}s")
    month=new_month
    out_dir = Path(f"./ifcb_downloads/2025{month}")
    out_dir.mkdir(parents=True, exist_ok=True)

driver.quit()
print(f"Finished downloading ALL DATA in {(datetime.now()- s).total_seconds()}s")