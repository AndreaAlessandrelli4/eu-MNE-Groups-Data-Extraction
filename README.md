# 📊 Eurostat Web-Crawling & Information Extraction Tool

This repository provides a modular tool for:

-   **Automated web crawling** on Eurostat or other structured sources\
-   **Information extraction** driven by customizable prompts\
-   **Parsing, cleaning, and structured data storage**\
-   **Reusable pipeline** via notebook or Python scripts

## 🚀 Key Features

### 🔍 1. Automated Extraction

-   Fetch web pages or indexed datasets\
-   Extract contents using rules and patterns\
-   Save results in CSV or JSON

### 📄 2. Customizable Prompts

-   Centralized in `data/prompt.json`\
-   Multiple template support\
-   Easily adaptable to different data domains

### 🧠 3. Modular Utilities

  File                    Purpose
  ----------------------- -------------------------------------
  `extraction_utils.py`   Parsing and information extraction
  `navigator_utils.py`    Navigation, HTTP requests, crawling
  `save_utils.py`         Structured saving logic
  `main.ipynb`            Demonstration pipeline

### 💾 4. Structured Storage

The `data/` folder contains prompt definitions and automatically saved
output files.

## 📁 Project Structure

    repo/
    ├── data/
    │   ├── prompt.json
    │   └── save_data/
    ├── extraction.csv
    ├── extraction_utils.py
    ├── navigator_utils.py
    ├── save_utils.py
    ├── main.ipynb
    ├── README.md
    └── requirements.txt

## 🧩 Requirements

    pip install -r requirements.txt



# Authors

* [Andrea Alessandrelli](mailto:andrea.alessandrelli@phd.unipi.it)
* [Pasquale Maritato](mailto:p.maritato@studenti.unipi.it)
* [Fabrizio Tomasso](mailto:f.tomasso@studenti.unipi.it)

## ▶️ How to Use

1.  Edit `data/prompt.json` to customize extraction rules\
2.  Run `main.ipynb` to launch the workflow\
3.  Extracted results will appear in `data/save_data/`
