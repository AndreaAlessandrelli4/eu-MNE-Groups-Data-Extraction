import pandas as pd
from googlesearch import search
import warnings
warnings.filterwarnings("ignore")
from tqdm import tqdm
from urllib.parse import urlparse
import PyPDF2
import io
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
from pdfminer.pdfdocument import PDFSyntaxError
import re
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai import async_configs
from pydantic import BaseModel, Field
import os, json
from crawl4ai import LLMConfig
from typing import List, Dict, Optional
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.processors.pdf import PDFCrawlerStrategy, PDFContentScrapingStrategy
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.processors.pdf import PDFCrawlerStrategy, PDFContentScrapingStrategy
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import logging
logging.getLogger("crawl4ai").setLevel(logging.ERROR)

df = pd.read_csv("/extraction.csv", sep=";", encoding="utf-8")
ent_list_ID =  df["NAME"].unique()
ent_list_ID_tuple = list(zip(df["ID"].unique(), df["NAME"].unique()))
field_key = df['VARIABLE'].unique()
del df



## Google Search: for search the information on google


def search_google(company, year, field, n_pdf=3, n_nopdf=3):
    results_dict = {}
    results_dict['ACTIVITY'] = []
    results_pdf= search(f"{company} financial annual report {year} consolidated filetype:pdf", num_results=n_pdf, lang="en",  ssl_verify=False, advanced=True)
    results_nopdf = search(f"{company} financial annual report {year} consolidated -filetype:pdf", num_results=n_nopdf, lang="en",  ssl_verify=False, advanced=True)
    for result in results_pdf:
        url = result.url
        if 'http' not in url:
                continue
        title = result.title
        description = result.description
        results_dict['ACTIVITY'].append({"company_name":company, "year":year, "url":url, "title":title, "text_snippet":description})

    for result in results_nopdf:
        url = result.url
        if 'http' not in url:
                continue
        title = result.title
        description = result.description
        results_dict['ACTIVITY'].append({"company_name":company, "year":year, "url":url, "title":title, "text_snippet":description})
    
    for f in field:
        if f == 'ACTIVITY':
            continue
        results_dict[f] = []
        if f == 'WEBSITE':
            query = f"{company} {field[f]}"
        elif f == 'COUNTRY':
            query = f"{company} {field[f]}"
        else:
            query = f"{company} {field[f]} {year}"
        results_generic= search(query, num_results=n_nopdf, lang="en",  ssl_verify=False, advanced=True)
        for result in results_generic:
            url = result.url
            if 'http' not in url:
                continue
            title = result.title
            description = result.description
            results_dict[f].append({"company_name":company, "year":year, "url":url, "title":title, "text_snippet":description})
    return results_dict



## Splitting long Markdown: for spliting long text
def split_markdown(markdown: str, max_tokens: int = 10000) -> list[str]:
    """
    Splits a long markdown into GPT-manageable chunks.
    Estimate: 1 token ≈ 4 English characters (depends on language).
    """
    approx_max_len = max_tokens * 4  

    if len(markdown) <= approx_max_len:
        return [markdown]

    blocks = []
    lines = markdown.splitlines()
    current_block = []

    current_len = 0
    for line in lines:
        line_len = len(line) + 1  # include newline
        if current_len + line_len > approx_max_len:
            blocks.append("\n".join(current_block))
            current_block = [line]
            current_len = line_len
        else:
            current_block.append(line)
            current_len += line_len

    if current_block:
        blocks.append("\n".join(current_block))

    return blocks


## Crawl4ai function using [crawl4ai](https://github.com/unclecode/crawl4ai) to SCRAPE and READ in Markdown


async def clean_content(url):
    if 'http' not in url:
        return ''
    else:
        if '.pdf' not in url:
            async with AsyncWebCrawler(verbose=False) as crawler:
                config = CrawlerRunConfig(
                    excluded_tags=['nav', 'footer', 'aside'],
                    remove_overlay_elements=True,
                    verbose=False,
                    markdown_generator=DefaultMarkdownGenerator(
                        content_filter=PruningContentFilter(threshold=0.48, threshold_type="fixed", min_word_threshold=0),
                        options={
                            "ignore_links": True
                        }
                    ),
                )
                result = await crawler.arun(
                    url=url,
                    config=config,
                )
        else:
            async with AsyncWebCrawler(crawler_strategy=PDFCrawlerStrategy(), verbose=False) as crawler:
                result = await crawler.arun(
                    url=url,
                    config=CrawlerRunConfig(
                        scraping_strategy=PDFContentScrapingStrategy(),
                        verbose=False,
                        excluded_tags=['nav', 'footer', 'aside'],
                        remove_overlay_elements=True,
                        markdown_generator=DefaultMarkdownGenerator(
                            content_filter=PruningContentFilter(threshold=0.48, threshold_type="fixed", min_word_threshold=0),
                            options={
                                "ignore_links": True
                            }
                        ),
                        )
                )
        return result