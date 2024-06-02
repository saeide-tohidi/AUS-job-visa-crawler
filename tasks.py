import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from celery_app import app


@app.task
def run_crawler(url):
    processed_data = {}

    def extract_data_from_page(soup):
        rows = soup.find_all("tr", tabindex="-1")
        print(f"Found {len(rows)} rows")

        for row in rows:
            title_tag = row.find("td")
            if title_tag:
                job_title = title_tag.get_text(strip=True)
                skills = [li.get_text(strip=True) for li in row.find_all("li")]
                print(job_title)
                print(skills)
                for skill in skills:
                    try:
                        visa_id, visa_title = skill.split(" - ", 1)
                        if skill in processed_data:
                            job_list = processed_data[skill]["Jobs"]
                            job_list.append(job_title)
                        else:
                            processed_data[skill] = {
                                "Jobs": [job_title],
                            }
                    except ValueError as e:
                        print(e)
                print("*" * 100)
            else:
                print("No <td> found in this row")

        return processed_data

    def crawl(url):
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install())
        )

        try:
            url = url
            driver.get(url)
            time.sleep(5)

            while True:
                soup = BeautifulSoup(driver.page_source, "html.parser")
                extract_data_from_page(soup)

                try:
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.LINK_TEXT, "Next"))
                    )
                    next_button.click()
                    time.sleep(5)
                except:
                    print("No more pages to load.")
                    break

            print(processed_data)
        finally:
            driver.quit()

        output_dir = "job_visa_files"
        os.makedirs(output_dir, exist_ok=True)

        for visa_id, data in processed_data.items():
            filename = os.path.join(output_dir, f"{visa_id[:90]}.txt")
            with open(filename, "w") as file:
                file.write(f"Visa Type: {visa_id}\n")
                file.write("Jobs:\n")
                for job in data["Jobs"]:
                    file.write(f"- {job}\n")

        print("Data has been written")

    crawl(url)
