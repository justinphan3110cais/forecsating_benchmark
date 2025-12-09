import re
import html
from urllib.parse import urljoin
from collections import OrderedDict
from aiohttp import ClientTimeout
import aiohttp
from playwright.async_api import async_playwright
from typing import List, Dict
import time
from urllib.parse import urlparse
from chat_forecasting.parse_date import DATE_FORMAT, UNKNOWN_TIME, extract_date
from chat_forecasting.news_domains import is_news_domains
import newspaper
from datetime import datetime

BLACKLIST_DOMAINS = ["crunchbase", "dealroom", "bloomberg", "washingtonpost"]
BROWSWER_DOMAINS = [""]

async def block_resources(route, request):
    if request.resource_type in ["image", "stylesheet", "font", "media"]:
        await route.abort()
    else:
        await route.continue_()

async def fetch_article_playwright(url: str, timeout: int = 5) -> str:
    async with async_playwright() as p:
        t0 = time.time()
        context = await p.chromium.launch_persistent_context(user_data_dir='.', headless=True, args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'])
        t1 = time.time()
        try:
            await context.route('**/*', lambda route: route.abort() 
                if route.request.resource_type in ['image', 'stylesheet', 'font', 'media']
                else route.continue_()
            )
            page = await context.new_page()
            await page.goto(url, timeout=timeout * 1000, wait_until="domcontentloaded")
            await page.wait_for_selector('body', timeout=timeout * 1000)

            content = await page.content()
            
            t2 = time.time()
            return content
        except Exception as e:
            print(f"Error fetching {url} with Playwright:", str(e))
            return ""
        finally:
            await context.close()


async def fetch_article(url: str, timeout: int=5) -> str:
    timeout = ClientTimeout(total=timeout)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as response:
            content = await response.read()
            return content.decode('utf-8', errors='replace')

async def fetch_article_newspaper(url: str, timeout: int=5) -> str:
    article = newspaper.article(url)
    favicon_url = extract_favicon(article.html, url)
    date = article.publish_date
    date = date.strftime(DATE_FORMAT) if date else UNKNOWN_TIME
    text = article.text
    return dict(favicon_url=favicon_url, date=date, content=text)

def extract_favicon(html: str, base_url: str):
    # Extract favicon
    favicon_url = ""
    favicon_match = re.search(r'<link[^>]*rel=["\'](icon|shortcut icon)["\'][^>]*href=["\'](.*?)["\']', html, re.IGNORECASE)
    if favicon_match:
        favicon_path = favicon_match.group(2)
        favicon_url = urljoin(base_url, favicon_path)
    else:
        # Look for the first image if favicon is not found
        img_match = re.search(r'<img[^>]*src=["\'](.*?)["\']', html)
        if img_match:
            img_path = img_match.group(1)
            favicon_url = urljoin(base_url, img_path)
    return favicon_url

def html_to_markdown(html: str, base_url: str, max_length: int = 2048):
    favicon_url = extract_favicon(html, base_url)
    date = extract_date(html)
    
    # Original markdown conversion logic
    html = re.sub(r'<(script|style|footer).*?</\1>', '', html, flags=re.DOTALL)
    html = re.sub(r'<(h[1-6]|p)\s+[^>]*>', r'<\1>', html)
    pattern = r'<(h[1-6]|p)>(.*?)</\1>'
    extracted = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
    
    processed = []
    for tag, content in extracted:
        # Remove HTML comments
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        
        # Remove all remaining HTML tags
        content = re.sub(r'<.*?>', '', content)
        
        # Clean up whitespace
        content = re.sub(r'\s+', ' ', content).strip()
        
        if content:
            content = decode_html_entities(content)
            if tag.startswith('h'):
                level = tag[1]
                processed.append(f"{'#' * int(level)} {content}")
            else:
                processed.append(content)
    
    markdown = '\n\n'.join(processed)

    # Split, truncate, and rejoin
    words = markdown.split()
    truncated_words = words[:max_length]
    markdown = ' '.join(truncated_words)

    return dict(favicon_url=favicon_url, date=date, content=markdown)

def decode_html_entities(text: str) -> str:
    return html.unescape(text)

def deduplicate_search_links(search_results: List[List[Dict]]) -> List[List[Dict]]:
    seen_domains = OrderedDict()
    deduplicated_results = []

    for result_list in search_results:
        deduped_list = []
        for result in result_list:
            url = result['link']
            domain = urlparse(url).netloc.lower()

            if any(blacklisted_domain in domain for blacklisted_domain in BLACKLIST_DOMAINS):
                continue

            if domain not in seen_domains:
                seen_domains[domain] = result
                deduped_list.append(result)
        if deduped_list:
            deduplicated_results.append(deduped_list)
        
    return deduplicated_results

def validate_html_content(html_content: str):
    blocked_terms = ["cloudflare", "page not found", "enable js", "error 404", "access denied", "doesn't seem to exist"]
    
    html_content_lower = html_content.lower()
    for term in blocked_terms:
        if term.lower() in html_content_lower:
            return False
    return True

def validate_markdown_content(markdown_content: str):
    if not markdown_content.strip():
        return False
    return True

def validate_time(before_timestamp, source_date_str):
    if before_timestamp == None:
        return True
    if before_timestamp == UNKNOWN_TIME:
        return False
    
    source_date = datetime.strptime(source_date_str, DATE_FORMAT)
    before_date = datetime.fromtimestamp(before_timestamp)
    return source_date < before_date

async def fetch_content(query, 
                        search_results, 
                        search_type="search", 
                        before_timestamp=None,
                        max_trials=3, 
                        browser=False, 
                        max_length: int = 2048):
    for i in range(min(max_trials, len(search_results))):
        try:
            url = search_results[i]['link']
            if browser:
                html_content = await fetch_article_playwright(url)
            elif search_type == "news" or is_news_domains(url):
                content = await fetch_article_newspaper(url)
            else:
                html_content = await fetch_article(url)
            
                # check for captcha block
                if not validate_html_content(html_content):
                    print(f"Invalidate {url}")
                    continue

                content = html_to_markdown(html_content, url, max_length)
                if not validate_markdown_content(content['content']):
                    continue
            
            if not validate_time(before_timestamp, content['date']):
                continue

            return {
                "query": query,
                **search_results[i],
                **content
            }
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            if i == max_trials - 1:
                print(f"Failed to fetch any article for query: {query}")
            continue
    return None