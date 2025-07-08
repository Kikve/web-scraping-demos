# Web-Scraping-Demos

[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)


Web-Scraping-Demos is a collection of Python scripts and notebooks that demonstrate how to extract, parse and process data from modern websites. Whether you’re dealing with static HTML, JavaScript‐rendered pages or large-scale crawls, you’ll find working examples that you can adapt to your own projects.


## Table of Contents
- [Quickstart](#quickstart)
- [Available Scrapers](#available-scrapers)
- [Links & Contact](#links--contact)

---

## Quickstart
Clone the repository and install all dependencies:

```bash
git clone https://github.com/you/web-scraping-demos.git
cd web-scraping-demos
pip install -r requirements.txt
```

run the AliExpress scraper:
```bash
python python -m aliexpress
```

---



## Available Scrapers
- [AliExpress Scrapper](#aliexpress-scrapper)
  - Scrapes product name, price, URL, seller specs.

---


## Detailed Scraper Sections

###  AliExpress Scrapper
**Scrapes AliExpress search results for product and seller data**

#### What it does
1. Launches Selenium ChromeDriver with configurable headless mode, user-agent, window size.
2. Loads search results (e.g., "laptops"), scrolls to fetch all product cards.
3. Extracts `product_name`, `price`, and `url` from each card.
4. Resolves captchas manually. 
4. Visits each product page; hovers seller-info popup to scrape seller's info
5. Outputs a structured CSV.

#### Analysis & Results
- **CSV:** `results/aliexpress.csv` with columns: `product_name`, `price`, `url`, `seller_info`.
- **Notebook:** `notebooks/aliexpress_analysis.ipynb`:
  - Buckets prices into ranges (0–50, 51–100, 101–200, 200+).
  - Computes count.
  - Plots distribution chart.

<img src="media/aliexpress_excel.png" width="350">
<img src="media/aliexpress_console.png" width="350">
<img src="media/range_prices_plot.png" width="350">

## Links & Contact
- **CSV Outputs:** [Results folder](https://github.com/Kikve/web-scraping-demos/tree/main/documents)
- **Notebooks:**
  - [AliExpress Analysis](https://github.com/Kikve/web-scraping-demos/tree/main/notebooks)
- **Repo:** https://github.com/Kikve/web-scraping-demos
- **Contact:** enriquevh.dev@gmail.com 
