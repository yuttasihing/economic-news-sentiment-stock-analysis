# Indonesian Economic Sentiment & Market Index Analysis (Q1 2026)

This repository contains a complete end-to-end Python pipeline for analyzing the relationship between financial news sentiment and the Indonesian Stock Market Index (IHSG) during the first quarter of 2026.

## 📌 Project Overview
This project demonstrates the integration of Web Scraping, Natural Language Processing (NLP), and Financial Data Extraction. The goal is to quantify media narratives from major Indonesian economic outlets and align them with market volatility.

**Data Source:**
- **News:** Kontan (Investasi), CNBC Indonesia (Market), and Bisnis.com (Bursa & Saham).
- **Market Index:** IHSG (Jakarta Composite Index) via Yahoo Finance.

## 📂 Repository Structure
The project is organized into three main modules:

- **`scrapers/`**: Scripts for automated link discovery and article content extraction using `BeautifulSoup`.
- **`analysis/`**: Sentiment classification using the **IndoBERT** model, unigram frequency extraction, and dataset merging.
- **`finance/`**: Extraction of historical OHLCV market data using the `yfinance` library.

## 🛠️ Tech Stack & Requirements
This project is built with Python 3.x and requires the following libraries:
- `pandas` & `numpy`: Data manipulation and structuring.
- `requests` & `beautifulsoup4`: Web scraping and HTML parsing.
- `transformers` & `torch`: Implementation of the IndoBERT sentiment model.
- `yfinance`: Financial data retrieval.
- `tqdm`: Visual progress tracking for long-running scripts.
- `nltk` & `re`: Text cleaning and unigram processing.

To install the requirements, run:
```bash
pip install -r requirements.txt
