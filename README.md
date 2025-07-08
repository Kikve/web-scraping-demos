# Web-Scraping Demos 
*Python · Selenium · BeautifulSoup · pandas Web-Scraping-Demos

[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)


Need to learn how to extract data from modern websites?
This repo shows **three self-contained examples**—static HTML, infinite scroll,
and pagination with filters—each exporting clean CSV/JSON.
*Code is for educational purposes; always follow site Terms before scraping.*


## Table of Contents
- [Quickstart](#quickstart)
- [Demo Line-up](#available-scrapers)
- [AliExpress Scrapper](#aliexpress-scrapper)
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



## Demo Line-up
| Demo | Target | Techniques | Key Output |
|------|--------|------------|------------|
| [AliExpress Scrapper](#aliexpress-scrapper) | Infinite-scroll product list | Selenium + dynamic waits | 4 columns (name, price, URL, seller) |

---


##  AliExpress Scrapper
**Scrapes AliExpress search results for product and seller data**

### What it does
1. Launches Selenium ChromeDriver with configurable headless mode, user-agent, window size.
2. Loads search results (e.g., "laptops"), scrolls to fetch all product cards.
3. Extracts `product_name`, `price`, and `url` from each card.
4. Resolves captchas manually. 
4. Visits each product page; hovers seller-info popup to scrape seller's info
5. Outputs a structured CSV.

### Analysis & Results
- **CSV:** `results/aliexpress.csv` with columns: `product_name`, `price`, `url`, `seller_info`.
- **Notebook:** `notebooks/aliexpress_analysis.ipynb`:
  - Buckets prices into ranges (0–50, 51–100, 101–200, 200+).
  - Computes count.
  - Plots distribution chart.

<div align="center">
  <img src="media/aliexpress_console.png" width="280">
  <img src="media/aliexpress_excel.png"  width="280">
</div>

## Links & Contact
- **CSV Outputs:** [Results folder](https://github.com/Kikve/web-scraping-demos/tree/main/documents)
- **Notebooks:**
  - [AliExpress Analysis](https://github.com/Kikve/web-scraping-demos/tree/main/notebooks)
- **Repo:** https://github.com/Kikve/web-scraping-demos
- **Contact:** enriquevh.dev@gmail.com 
