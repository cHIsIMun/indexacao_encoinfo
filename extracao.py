import requests
import re
import pandas as pd
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor

urls = pd.DataFrame(columns=["url", "content"])

def clean_html(raw_html):
    cleaned_html = re.sub(r'<(script|style).*?>.*?</\1>', '', raw_html, flags=re.DOTALL)
    cleaned_html = re.sub(r'<!--.*?-->', '', cleaned_html, flags=re.DOTALL)
    cleaned_html = re.sub(r'<[^>]+>', '', cleaned_html)
    cleaned_html = re.sub(r'&[a-zA-Z0-9]+;', ' ', cleaned_html)
    cleaned_html = re.sub(r'\s+', ' ', cleaned_html)
    return cleaned_html.strip()

def fetch_and_clean(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        if response.status_code == 200:
            return clean_html(response.text)
    except requests.RequestException as e:
        print(f"Erro ao acessar {url}: {str(e)}")
    return None

def get_links(url,domain):
    response = requests.get(url)
    if response.status_code == 200:
        links = re.findall(r'href=["\']?([^"\'>]+)', response.text)
        links = [urljoin(url, link) for link in links] 
        links = [link for link in links if link.startswith(domain)]
        return list(set(links))
    return []

def crawl(url, domain, visited=set()):
    if url not in visited:
        print(f"Visitando: {url}")
        visited.add(url)
        content = fetch_and_clean(url)
        if content:
            urls.loc[len(urls)] = [url, content]
            sub_links = get_links(url, domain)
            for link in sub_links:
                if link not in visited:
                    crawl(link, domain, visited)

base_url = "https://ulbra-to.br/encoinfo/"
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.submit(crawl, base_url, base_url)

urls.to_csv("pages.csv", index=False)

