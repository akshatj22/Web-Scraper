import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Configuration
PLATFORMS = {
    "LinkedIn": "https://www.linkedin.com/jobs/search/?keywords={role}&location=United%20States&f_TPR={time_window}&f_JT=C",
    "Monster": "https://www.monster.com/jobs/search/?q={role}&where=USA&tm={time_window}&stype=Contract",
    "Dice": "https://www.dice.com/jobs?q={role}&location=USA&employmenttype=Contract&postedDate={time_window}"
}

VERTICALS = {
    "ERP": ["SAP", "Oracle"],
    "Infra & BT": ["Infrastructure Engineer", "Business Technology"],
    "DevOps & BI": ["DevOps", "Business Intelligence"],
    "QA/QE": ["Quality Assurance", "Quality Engineering"]
}

# Initialize Selenium browser
def init_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    return webdriver.Chrome(options=chrome_options)

def get_time_window():
    today = datetime.now()
    if today.weekday() == 0:  # Monday
        return "r259200"  # 72 hours (Fri-Sun)
    return "r86400"  # 24 hours (Tue-Fri)

def scrape_linkedin(role, time_window):
    url = PLATFORMS["LinkedIn"].format(role=role, time_window=time_window)
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = []
        for job in soup.select(".base-card"):
            title = job.select_one(".base-search-card__title").text.strip() if job.select_one(".base-search-card__title") else "N/A"
            company = job.select_one(".base-search-card__subtitle").text.strip() if job.select_one(".base-search-card__subtitle") else "N/A"
            location = job.select_one(".job-search-card__location").text.strip() if job.select_one(".job-search-card__location") else "N/A"
            date = job.select_one("time")["datetime"] if job.select_one("time") else "N/A"
            jobs.append([title, company, location, date])
        return jobs
    except Exception as e:
        print(f"LinkedIn error: {str(e)}")
        return []

def scrape_monster(role, time_window, driver):
    url = PLATFORMS["Monster"].format(role=role.replace(' ', '+'), time_window=time_window)
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article[data-testid='svx_jobCard']"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        jobs = []
        for job in soup.select("article[data-testid='svx_jobCard']"):
            title = job.select_one("[data-testid='jobTitle']").text.strip() if job.select_one("[data-testid='jobTitle']") else "N/A"
            company = job.select_one("[data-testid='company']").text.strip() if job.select_one("[data-testid='company']") else "N/A"
            location = job.select_one("[data-testid='jobDetailLocation']").text.strip() if job.select_one("[data-testid='jobDetailLocation']") else "N/A"
            date = job.select_one("time").text.strip() if job.select_one("time") else "N/A"
            jobs.append([title, company, location, date])
        return jobs
    except TimeoutException:
        print("Monster: Timeout waiting for job cards")
        return []
    except Exception as e:
        print(f"Monster error: {str(e)}")
        return []

def scrape_dice(role, time_window, driver):
    url = PLATFORMS["Dice"].format(role=role.replace(' ', '+'), time_window=time_window)
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".card-header"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        jobs = []
        for job in soup.select(".card-header"):
            title = job.select_one(".card-title-link").text.strip() if job.select_one(".card-title-link") else "N/A"
            company = job.select_one(".card-company a").text.strip() if job.select_one(".card-company a") else "N/A"
            location = job.select_one(".search-result-location").text.strip() if job.select_one(".search-result-location") else "N/A"
            date = job.select_one(".posted-date").text.strip() if job.select_one(".posted-date") else "N/A"
            jobs.append([title, company, location, date])
        return jobs
    except TimeoutException:
        print("Dice: Timeout waiting for job cards")
        return []
    except Exception as e:
        print(f"Dice error: {str(e)}")
        return []

def run_scraping_job():
    all_data = []
    current_date = datetime.now().strftime("%Y-%m-%d")
    time_window = get_time_window()
    browser = init_browser()
    
    print(f"\n{'='*50}")
    print(f"Starting scraping job at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Time window: {'72 hours (Fri-Sun)' if time_window == 'r259200' else '24 hours'}")
    print(f"{'='*50}\n")
    
    for vertical, roles in VERTICALS.items():
        for role in roles:
            # LinkedIn
            print(f"Scraping {role} in {vertical} from LinkedIn...")
            linkedin_jobs = scrape_linkedin(role, time_window)
            for job in linkedin_jobs:
                title, company, location, date = job
                state = location.split(",")[-1].strip() if "," in location else location
                all_data.append([title, vertical, state, "LinkedIn", date, "Contract", current_date])
            
            # Monster
            print(f"Scraping {role} in {vertical} from Monster...")
            monster_jobs = scrape_monster(role, time_window, browser)
            for job in monster_jobs:
                title, company, location, date = job
                state = location.split(",")[-1].strip() if "," in location else location
                all_data.append([title, vertical, state, "Monster", date, "Contract", current_date])
            
            # Dice
            print(f"Scraping {role} in {vertical} from Dice...")
            dice_jobs = scrape_dice(role, time_window, browser)
            for job in dice_jobs:
                title, company, location, date = job
                state = location.split(",")[-1].strip() if "," in location else location
                all_data.append([title, vertical, state, "Dice", date, "Contract", current_date])
            
            time.sleep(5)  # Respectful delay between requests
    
    browser.quit()  # Close browser after each job
    
    # Create DataFrame
    df = pd.DataFrame(all_data, columns=[
        "Role", 
        "Vertical/Industry", 
        "State", 
        "Platform", 
        "Job Posting Date", 
        "Contract Duration",
        "Capture Date"
    ])
    
    # Save to Excel with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Job_Postings_{timestamp}.xlsx"
    df.to_excel(filename, index=False)
    print(f"\n{'='*50}")
    print(f"Saved {len(df)} jobs to {filename}")
    print(f"Scraping completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

def schedule_jobs():
    # Schedule Monday job (72-hour window)
    schedule.every().monday.at("09:00").do(run_scraping_job)
    
    # Schedule Tuesday-Friday jobs (24-hour window)
    schedule.every().tuesday.at("09:00").do(run_scraping_job)
    schedule.every().wednesday.at("09:00").do(run_scraping_job)
    schedule.every().thursday.at("09:00").do(run_scraping_job)
    schedule.every().friday.at("09:00").do(run_scraping_job)
    
    print("Scheduler initialized. Next runs scheduled for:")
    for job in schedule.get_jobs():
        print(f"- {job.next_run.strftime('%A, %Y-%m-%d %H:%M:%S')}")
    
    # Continuous scheduler loop
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    # Run immediately for testing (optional)
    # run_scraping_job()
    
    # Start the scheduler
    schedule_jobs()
