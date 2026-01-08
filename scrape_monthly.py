from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True

from bs4 import BeautifulSoup
import requests
from pathlib import Path
from datetime import datetime
import time

base_url="https://ifcb.caloos.org"
start_url = "https://ifcb.caloos.org/bin?dataset=scripps-pier-ifcb-183&bin=D20250101T185049_IFCB183"
end_url = "https://ifcb.caloos.org/timeline?dataset=scripps-pier-ifcb-183&bin=D20260101T002031_IFCB183"
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

while url != end_url:  # download files until 2026 (real run)
    
    while new_month == month:
        time.sleep(2)  # wait for Js to load content
        # wait up to 15 seconds, poll every 1 seconds
        wait = WebDriverWait(driver, 15, poll_frequency=1)

        def href_not_hash(driver):
            el1 = driver.find_element(By.ID, "download-hdr")
            href1 = el1.get_attribute("href")
            return "hdr" in href1
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
        
        # physically click the "Next Bin" button
        # there is some js shenanigans that prevents just getting the href
        next_button = driver.find_element(By.ID, "next-bin")
        driver.execute_script("arguments[0].click();", next_button)

        # wait for URL to change
        WebDriverWait(driver, 10).until(lambda d: d.current_url != url)
        new_date = driver.current_url.split("bin=")[1].split("_")[0][1:9]
        new_month= driver.current_url.split("bin=")[1].split("_")[0][5:7]
        if new_date != date: 
            print(f"Downloaded day: {date} in {(datetime.now()- s).total_seconds()}s")
            date = new_date
        url = driver.current_url

    print(f"== Downloaded all data of month {month} in {(datetime.now()- s).total_seconds()}s")
    month=new_month
    out_dir = Path(f"./ifcb_downloads/2025{month}")
    out_dir.mkdir(parents=True, exist_ok=True)

driver.quit()
print(f"Finished downloading ALL DATA in {(datetime.now()- s).total_seconds()}s")