# Job Scraper Project

Automated tool for scraping contract job opportunities from LinkedIn, Monster, and Dice platforms.

---

## 📖 Overview

This project is an automated job scraping tool that extracts contract job opportunities from LinkedIn, Monster, and Dice. It classifies jobs across technology verticals and provides state-wise analysis of contractual roles. The system is designed to run on a schedule, ensuring up-to-date data collection with minimal manual intervention.

---

## 🚀 Features

- **Multi-Platform Scraping:** Extracts job data from LinkedIn, Monster, and Dice.
- **Automated Scheduling:**  
  - **Monday:** 72-hour window (captures weekend postings)  
  - **Tuesday-Friday:** 24-hour window (daily captures)
- **Vertical Classification:** Categorizes jobs into ERP, Infrastructure & BT, DevOps & BI, and QA/QE.
- **Contract Job Filtering:** Focuses specifically on contract/freelance opportunities.
- **State-wise Analysis:** Maps job opportunities across US states.
- **Excel Output:** Generates comprehensive reports with timestamped filenames.
- **Anti-Bot Protection:** Implements headless browsing, delays, and error handling to manage platform restrictions.

---

## 🧰 Tools & Methods

- **Python 3.8+**: Core programming language.
- **Selenium (headless Chrome):** For dynamic content scraping on Monster and Dice.
- **Requests & BeautifulSoup:** For efficient HTML parsing of LinkedIn job postings.
- **Pandas:** For data cleaning, transformation, and Excel export.
- **Schedule Library:** For automated, time-based execution of scraping jobs.
- **ChromeDriver:** Headless browser automation for platforms requiring JavaScript rendering.

### Approach & Innovation

- **Hybrid Scraping:** Combined lightweight HTTP scraping (for LinkedIn) with browser automation (for Monster/Dice) to handle both static and dynamic content efficiently.
- **Dynamic Scheduling:** Automatically adjusts the scraping window based on the day, ensuring comprehensive coverage of both weekday and weekend postings.
- **Robust Error Handling:** Used try/except blocks and Selenium waits to gracefully handle timeouts, page structure changes, and anti-bot measures.
- **State Extraction Logic:** Developed a parsing method to accurately extract US state information from job locations.
- **No Mock Data:** All data is scraped live from the platforms; no artificial or mock data is generated at any stage.

**Challenges Overcome:**
- Navigated anti-bot and dynamic content restrictions on Monster and Dice by leveraging headless Selenium and explicit waits.
- Ensured reliable and repeatable job collection with a persistent scheduler and timestamped output.
- Unified data from heterogeneous sources into a single, analyzable format.

---

## 📋 Prerequisites

- Python 3.8 or higher
- Google Chrome browser (for Selenium WebDriver)
- ChromeDriver installed and in PATH
- (Recommended) Virtual environment

---

## 🛠️ Installation

### Clone the repository
`git clone https://github.com/your-username/web-scraper-project.git`
`cd web-scraper-project`

### Create and activate virtual environment
`python -m venv venv`

### Windows
`venv\Scripts\activate`

### Mac/Linux
`source venv/bin/activate`

### Install dependencies
`pip install -r requirements.txt`


## ⚙️ Configuration

**Search Terms by Vertical (customizable in code):**
- **ERP:** SAP, Oracle
- **Infrastructure & BT:** Infrastructure Engineer, Business Technology
- **DevOps & BI:** DevOps, Business Intelligence
- **QA/QE:** Quality Assurance, Quality Engineering

**Scheduling:**
- **Monday 9:00 AM:** 72-hour window scraping (Fri-Sun)
- **Tuesday-Friday 9:00 AM:** 24-hour window scraping

---

## 🚀 Usage

**Manual Scraping (edit code to run once):**
`python job_scraper.py`


**Scheduled Scraping (default):**
- The scraper runs automatically at 9:00 AM Monday through Friday as per the schedule.
- Output files are saved as `Job_Postings_YYYYMMDD_HHMMSS.xlsx` in the project directory.

---

## 📊 Output Format

**Main Data Sheet:**
| Role                   | Vertical/Industry | State | Platform   | Job Posting Date | Contract Duration | Capture Date |
|------------------------|-------------------|-------|------------|------------------|------------------|--------------|
| SAP Consultant         | ERP               | NY    | LinkedIn   | 2025-06-24       | Contract         | 2025-06-25   |
| DevOps Engineer        | DevOps & BI       | CA    | Dice       | 2025-06-23       | Contract         | 2025-06-25   |

**Analysis Sheets (optional, can be generated in pandas/Excel):**
- **Vertical Analysis:** Job distribution by technology vertical.
- **State Analysis:** Geographic distribution of opportunities.
- **Platform Analysis:** Comparison across job platforms.

---

## ⚠️ Limitations

- **Platform Structure Changes:** Scraper may break if job sites update their HTML structure.
- **Geographic Focus:** State extraction logic is US-centric.
- **Pagination:** Only the first page of results is scraped for each role/platform.
- **Authentication:** Cannot access job postings requiring login.
- **Anti-Bot Measures:** Some job boards may block scraping attempts despite headless browsing.

---



---


