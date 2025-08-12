# Watiqa Administrative Geography Scraper

This project allows you to scrape the Moroccan administrative divisions (regions, prefectures, communes) from [watiqa.ma](https://www.watiqa.ma/) in both French and Arabic, and export the data to JSON, CSV, and Excel formats.

> **Note:** Ready-to-use data files (JSON, CSV, Excel) for both French and Arabic are already available in the `data` folder. All generated files will also be created in this folde

## Features

- Scrape regions, prefectures, and communes from the official Moroccan administrative document request portal.
- Supports both French and Arabic interfaces.
- Export data to JSON, CSV, and Excel files (all in the `data` folder).

## Requirements

- Python 3.7+
- See `requirements.txt` for dependencies:
  - requests
  - beautifulsoup4
  - lxml
  - pandas
  - openpyxl

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

### Scraping Data

Use the unified script to scrape either French or Arabic data:

```bash
python scrap_watiqa_multi.py fr
# or for Arabic
python scrap_watiqa_multi.py ar
```

- Output files (in `data/`):
  - French: `regions_prefectures_communes.json`
  - Arabic: `regions_prefectures_communes_ar.json`

### Export to CSV and Excel

Convert the JSON data to CSV and Excel:

```bash
python json_to_csv_excel.py
# or for Arabic
python json_to_csv_excel.py ar
```

- Output files (in `data/`):
  - French: `regions_prefectures_communes.csv`, `regions_prefectures_communes.xlsx`
  - Arabic: `regions_prefectures_communes_ar.csv`, `regions_prefectures_communes_ar.xlsx`

## File Overview

- `scrap_watiqa_multi.py`: Main scraper, supports both languages.
- `json_to_csv_excel.py`: Converts JSON output to CSV and Excel.
- `requirements.txt`: Python dependencies.
- `README.md`: This documentation.

## Notes

- Scraping is rate-limited (`time.sleep(0.5)`) to avoid being blocked.
- The scripts simulate form navigation as a real user would.
- Data is extracted directly from the official portal, so structure may change if the website is updated.

## License

The data in this project is made available under the [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](http://creativecommons.org/licenses/by-nc/4.0/) license.

!

#### You are permitted to:
* **Share** — copy and redistribute the material in any medium or format.
* **Adapt** — remix, transform, and build upon the material.

#### Under the following terms:
* **Attribution (BY)** — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
* **NonCommercial (NC)** — You may not use the material for commercial purposes.

For any commercial licensing requests, please contact me via **[LinkedIn]**.

---

Feel free to fork, contribute, or open issues!
